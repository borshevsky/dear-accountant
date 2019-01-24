from telegram.ext import Updater, CommandHandler
from commands import party, waste, payoff, finish, add, remove, members, money, help
from song import song

import logging
import random
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error_handler(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    token = os.environ['TLGRM_TOKEN']

    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('party', party, pass_args=True, pass_chat_data=True))
    dispatcher.add_handler(CommandHandler('add', add, pass_args=True, pass_chat_data=True))
    dispatcher.add_handler(CommandHandler('remove', remove, pass_args=True, pass_chat_data=True))
    dispatcher.add_handler(CommandHandler('waste', waste, pass_args=True, pass_chat_data=True))
    dispatcher.add_handler(CommandHandler('payoff', payoff, pass_chat_data=True))
    dispatcher.add_handler(CommandHandler('finish', finish, pass_chat_data=True))
    dispatcher.add_handler(CommandHandler('members', members, pass_chat_data=True))
    dispatcher.add_handler(CommandHandler('money', money, pass_chat_data=True))

    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('song', song))

    dispatcher.add_error_handler(error_handler)

    logger.info('Start polling')
    updater.start_polling()

    logger.info('Idle')
    updater.idle()


if __name__ == '__main__':
    random.seed()
    main()
