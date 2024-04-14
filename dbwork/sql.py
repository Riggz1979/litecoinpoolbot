from sqlalchemy import (Column, String, create_engine,
                        MetaData, Table, insert,
                        update, select, BigInteger,
                        ForeignKey, Boolean, Float)


class DBWork:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.engine.connect()
        self.metadata = MetaData()
        self.user = Table('users', self.metadata,
                          Column('user_id', BigInteger, primary_key=True),
                          Column('tg_id', BigInteger, unique=True),
                          Column('api_key', String(255), unique=True),
                          Column('hash_wd', BigInteger, default=0)
                          )
        self.alert = Table('alerts', self.metadata,
                           Column('alert_id', BigInteger, primary_key=True),
                           Column('user_id', BigInteger, ForeignKey('users.tg_id')),
                           Column('crypto', String(255)),
                           Column('value', Float, default=0),
                           Column('go_up', Boolean, default=False),

                           )

        self.metadata.create_all(self.engine)
        self.conn = self.engine.connect()

    def add_user(self, tg_id, api_key):
        user_to_add = insert(self.user).values(
            tg_id=tg_id,
            api_key=api_key,
        )
        self.conn.execute(user_to_add)
        self.conn.commit()

    def get_all_users(self):
        users = self.user.select()
        r = self.conn.execute(users)
        return r.fetchall()

    def check_user_exist(self, tg_id_to_check):
        u = self.user.select().where(self.user.c.tg_id == tg_id_to_check)
        r = self.conn.execute(u)
        if r.fetchall():
            return True
        return False

    def hash_watchdog(self, tg_id, *args):
        if args:
            u = (update(self.user)
                 .where(self.user.c.tg_id == tg_id)
                 .values(hash_wd=args[0]))
            self.conn.execute(u)
            self.conn.commit()
            return args[0]
        else:
            u = (select(self.user.c['hash_wd'])
                 .where(self.user.c.tg_id == tg_id))
            r = self.conn.execute(u)
            return r.fetchone()[0]

    def get_user(self, tg_id_to_check):
        u = self.user.select().where(self.user.c.tg_id == tg_id_to_check)
        r = self.conn.execute(u)
        return r.fetchone()

    def check_api_key_exist(self, api_key):
        u = self.user.select().where(self.user.c.api_key == api_key)
        r = self.conn.execute(u)
        if r.fetchall():
            return True
        return False

    def set_alert(self, user_id, crypto, value, go_up):
        alert_to_add = (insert(self.alert).
                        values(user_id=user_id,
                               crypto=crypto,
                               value=value,
                               go_up=go_up))
        self.conn.execute(alert_to_add)
        self.conn.commit()

    def alerts_list(self, for_user):
        u = self.alert.select().where(self.alert.c.user_id == for_user)
        r = self.conn.execute(u)
        return r.fetchall()


