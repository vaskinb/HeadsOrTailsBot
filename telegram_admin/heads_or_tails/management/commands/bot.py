import random
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request
from heads_or_tails.models import Profile


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message: str = f'Произошла ошибка: {e}'
            print(error_message)
            raise e

    return inner


@log_errors
def do_start(update: Update,  context: CallbackContext):
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': username,
            'balance': 1000,
        }
    )
    balance = p.balance
    reply_text = f'Приветсвую, {username}\nНа вашем счету {balance} монет\n' \
                 f'/play_heads - ставка 100 на орла\n' \
                 f'/play_tails - ставка 100 на решку\n' \
                 f'/leaderboard - таблица лидеров'
    update.message.reply_text(
        text=reply_text,
    )


@log_errors
def do_play_heads(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': username,
            'balance': 1000,
        }
    )
    reply_text = f'Вы поставили 100 монет на орла'
    update.message.reply_text(
        text=reply_text,
    )

    result = random.choice(["выиграли", "проиграли"])
    if result == "выиграли":
        p.balance += 100
    elif result == "проиграли":
        p.balance -= 100

    update.message.reply_text(
        text=f'Вы {result}\nНа вашем счету {p.balance} монет'
    )
    p.save(update_fields=['balance'])


@log_errors
def do_play_tails(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': username,
            'balance': 1000,
        }
    )
    reply_text = 'Вы поставили 100 монет на решку'
    update.message.reply_text(
        text=reply_text,
    )

    result = random.choice(["выиграли", "проиграли"])
    if result == "выиграли":
        p.balance += 100
    elif result == "проиграли":
        p.balance -= 100

    update.message.reply_text(
        text=f'Вы {result}\nНа вашем счету {p.balance} монет'
    )
    p.save(update_fields=['balance'])


@log_errors
def display_leaderboard(update: Update, context: CallbackContext):
    leaderboard = Profile.objects.order_by('-balance')[0:10]
    reply_text = "Таблица лидеров:\n"
    for item in leaderboard:
        reply_text += str(item) + '\n'
    update.message.reply_text(text=reply_text)


class Command(BaseCommand):
    help = 'Телеграм-бот "Орел или решка"'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
        )
        print(bot.get_me())

        updater = Updater(
            bot=bot,
            use_context=True,
        )

        start_handler = CommandHandler('start', do_start)
        updater.dispatcher.add_handler(start_handler)

        play_heads_handler = CommandHandler("play_heads", do_play_heads)
        updater.dispatcher.add_handler(play_heads_handler)

        play_tails_handler = CommandHandler("play_tails", do_play_tails)
        updater.dispatcher.add_handler(play_tails_handler)

        leaderboard_handler = CommandHandler("leaderboard", display_leaderboard)
        updater.dispatcher.add_handler(leaderboard_handler)

        updater.start_polling()
        updater.idle()
