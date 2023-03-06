# Anki Memory Bot
This telegram single-user bot helps you to memorize words using Anki.

## Installation
1. git clone git@github.com:andreygaag/anki_memory.git
2. cp env_example .env
3. replace the values in .env with your own
   1. Configure the database environment variables.
   2. [Create Telegram bot](https://core.telegram.org/bots#how-do-i-create-a-bot) and get the token.
   3. Set TELEGRAM_ADMIN_ID to your Telegram ID, run without it environment variable if you don't know it.
4. docker-compose up
   (use tmux or up -d to run in background)
