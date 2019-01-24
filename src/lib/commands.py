from enum import Enum

from party import (
    Party, AlreadyMember, MemberWastedMoneyAlready,
    PartyIsTooBoring, IncorrectMoney, NotAMember, UnknownParticipant)
from song import TEXT as song_text

from functools import wraps, partial
from inspect import signature, Parameter
import random


class Service:
    def __call__(self, *args, **kwargs):
        raise RuntimeError('Service variable should not be called')

    def __getattr__(self, item):
        raise RuntimeError('Service variable should not be called')


class InParty(Enum):
    yes = 'yes'
    no = 'no'
    doesnt_matter = 'doesnt_matter'


def make_arguments(params, cmd_args):
    arguments = {p.name: value for p, value in zip(params, cmd_args)}

    # Put all tail arguments to the last parameter if it is list
    if len(cmd_args) > len(params) and params[-1].annotation == list:
        last_param_name = params[-1].name
        tail = [arguments.pop(last_param_name)]
        tail.extend(cmd_args[len(params):])
        arguments[last_param_name] = tail

    return arguments

def command(in_party=InParty.yes):
    def decorator(f):
        params = [p for p in signature(f).parameters.values()
                  if p.kind == Parameter.POSITIONAL_OR_KEYWORD
                  and not isinstance(p.default, Service)]

        @wraps(f)
        def wrapper(*args, **kwargs):
            chat_data = kwargs.get('chat_data', {})
            cmd_args = kwargs.get('args', [])
            update = args[1]

            sink = partial(_send_message, update=update)

            if in_party == InParty.yes and 'party' not in chat_data:
                sink('🌞 🌞 Вечерина еще не началась :(')
                return

            if in_party == InParty.no and 'party' in chat_data:
                sink('🌞 🌞 Вечерина уже началась :(')
                return

            if len(cmd_args) < len(params):
                params_strings = [('<{}>', '[{}]')[p.default != Parameter.empty].format(p.name) for p in params]
                usage = '⛔️ Usage: {} {}'.format(f.__name__, ' '.join(params_strings))
                sink(usage)
                return

            arguments = make_arguments(params, cmd_args)

            kwargs['sink'] = sink
            if in_party == InParty.yes:
                kwargs['party'] = chat_data['party']
            f(**kwargs, **arguments)

        return wrapper
    return decorator


class PartyAlreadyStarted(Exception):
    def __init__(self, name):
        self.name = name


def _send_message(message, update, md=False):
    if md:
        update.message.reply_markdown(message, quote=False)
        return

    update.message.reply_text(message, quote=False)


@command(in_party=InParty.no)
def party(name, members: list, sink=Service(), **kwargs):
    kwargs['chat_data']['party'] = Party(name, members)
    sink('🍾 💃 🕺 Вечерина {} начинается!'.format(name))


@command()
def add(member, sink=Service(), party=Service(), **kwargs):
    try:
        party.add(member)
        sink('➕ Понял принял, {} теперь в теме'.format(member))
    except AlreadyMember:
        sink('👎 👎 {} еще не учавствует в вечерине'.format(member))


@command()
def remove(member, sink=Service(), party=Service(), **kwargs):
    try:
        party.remove(member)
        sink('➖ {} уходит в закат'.format(member))
    except NotAMember:
        sink('😞 😞 {} еще не на вечерине :('.format(member))
    except MemberWastedMoneyAlready:
        sink('😡 😡 {} уже потратился, как-то некрасиво выгонять'.format(member))


@command()
def reset(member, sink=Service(), party=Service(), **kwargs):
    try:
        party.reset(member)
    except NotAMember:
        sink('😞 😞 {} еще не на вечерине :('.format(member))


@command()
def members(sink=Service(), party=Service(), **kwargs):
    m = party.members
    if not m:
        sink('🍆 Вечерина пустует...')
        return

    sink('🕴🏼 💃🏼 🕺🏼 🚶🏼‍♀️ 🚶🏼 🏃🏼‍♀️ 🏃🏼 Участники вечерины {}:\n{}'.format(
        party.name, '\n'.join(m)))


@command()
def money(sink=Service(), party=Service(), **kwargs):
    money = party.money()
    if not money:
        sink('🍆 Вечерина пустует...')
        return

    messages = ['{} потратил {}'.format(member, money) for member, m in money.items()]
    sink('Текущие траты:\n{}'.format('\n'.join(messages)))


@command()
def waste(member, amount, sink=Service(), party=Service(), **kwargs):
    try:
        party.waste(member, amount)
        sink('💰 💵 💴 Понял, сенкью, {} потратил {} рублей'.format(member, amount))
    except IncorrectMoney:
        sink('🙈 🙉 💩 🙊 Что за дичь? {}'.format(amount))
    except UnknownParticipant:
        sink('{} не учавствует в вечерине'.format(member))


@command()
def payoff(party=Service(), sink=Service(), **kwargs):
    try:
        transactions = party.payoff()
        message = '\n'.join(['{} => {}: {}'.format(f, t, a) for f, t, a in transactions])
        sink(message)
    except PartyIsTooBoring:
        sink('🐒 Рассчитывать тут особо нечего...')


@command()
def finish(party=Service(), sink=Service(), **kwargs):
    party_name = party.name
    del kwargs['chat_data']['party']
    sink('Вечерина {} закончилась! 🔥🔥🔥'.format(party_name))


@command(in_party=InParty.doesnt_matter)
def help(sink=Service(), **kwargs):
    text = """ ***Команды***
          */party* <название> <люди>: Начать вечерину. ex: /party тусуем пельш луч жанна
          */add* <имя>: Добавить кого-нибудь на вечерину. ex: /add владос
          */remove* <имя>: Кто позвал его на вечерину? ex: /remove пельш
          */waste* <имя> <сколько>: Отметить трату. ex: /waste луч 1к
          */members*: Список участников.
          */money*: Текущие затраты.
          */payoff*: Рассчет.
          */finish*: Конец вечерины.
          
          */song*: Спой плиз.
    """
    sink(text, md=True)


@command(in_party=InParty.doesnt_matter)
def song(sink=Service(), **kwargs):
    lines_count = len(song_text)
    first_line = random.randint(0, int(lines_count / 2) - 1)
    line = first_line * 2

    message = '{}...'.format('\n'.join(song_text[line:line+2]))
    sink(message)
