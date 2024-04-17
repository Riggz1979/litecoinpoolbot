COMMANDS = (f'Commands list:\n'
            f'/start - Greetings\n'
            f'/prices - Popular crypto prices\n'
            f'/api - API key registration for pool monitoring\n'
            f'/stats - Mining statistics\n'
            f'/watchdog - Watchdog set or check\n'
            f'/set_alert <crypto> <comp> <price> - Set alert for crypto price\n'
            f'/alerts - Get your alerts list\n'
            f'/del_alert <id> - Delete alert\n')

ADMIN_COMMANDS = (f'\nAdmin commands:\n'
                  f'/admin - Check admin status\n'
                  f'/restart - Restart bot\n'
                  f'Send OTA.zip to OTA update\n')

HELP = ('Hello. This bot is designed to monitor mining on the litecoinpool.org server.Bot commands:\n\n'
        '/start – sends a greeting message\n\n'
        '/commands – displays a brief list of bot commands\n\n'
        '/prices – returns current prices of popular cryptocurrencies.Currently supported cryptocurrencies include:\n'
        '• Litecoin\n'
        '• Dogecoin\n'
        '• Bitcoin\n'
        '• Ethereum\n\n'
        '/api <key> - registers an API key for monitoring mining, setting watchdogs, and price alerts.\n'
        'Example command:\n'
        '/api abcdef765431wwfgsdgs\n\n'
        'The following commands require a registered API key:\n\n'
        '/stats – returns mining statistics:\n'
        '• Current hash rate\n'
        '• LTC balance\n'
        '• Doge balance\n'
        '• Average number of LTC mined per day\n'
        '• Average number of Doge mined per day\n'
        '• Approximate income in USD\n\n'
        '/watchdog <number> - sets a watchdog value for your hash rate in MH/s. '
        'If the hash rate falls below the set level, the bot will periodically send notifications.\n'
        'Example command:\n'
        '/watchdog 500\n'
        'A command without arguments will return the current set value.\n\n'
        '/set_alert <crypto> <sign> <price> - sets a price alert. '
        'When the price reaches the set level, the bot will send notifications.\n'
        'The sign can be \'>\' or \'<\'.\n'
        'Example command:\n'
        '/set_alert bitcoin > 100000\n\n'
        '/alerts – returns a list of set alerts.\n\n'
        '/del_alert <id> - deletes an alert with the specified id. '
        'Id can be found through the /alerts command or in the alert notification.\n'
        'Example command:\n'
        '/del_alert 5\n\n')

ADMIN_HELP = ('Commands for admin only:\n'
              '/admin – checks administrative rights\n'
              '/restart – restarts the bot\n'
              '/shutdown – stops the bot\n\n'
              'For "over-the-air" updates, send the bot an OTA.zip file containing the code as a regular message.')
