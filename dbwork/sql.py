from sqlalchemy import Column, Integer, String, create_engine, MetaData, Table, insert


class DBWork:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.engine.connect()
        self.metadata = MetaData()
        self.user = Table('users', self.metadata,
                          Column('user_id', Integer, primary_key=True),
                          Column('tg_id', Integer, unique=True),
                          Column('api_key', String(255), unique=True)
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
