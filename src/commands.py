from party import (
    Party, AlreadyMember, MemberWastedMoneyAlready,
    PartyIsTooBoring, IncorrectMoney, NotAMember,
    _to_money)


class PartyAlreadyStarted(Exception):
    pass


def _send_message(update, message):
    update.message.reply_text(message, quote=False)


def party(bot, update, args, chat_data):
    try:
        party_name, members = args[0], args[1:]
        if 'party' in chat_data:
            raise PartyAlreadyStarted()
        chat_data['party'] = Party(party_name, members)

        _send_message(update, '🍾 💃 🕺 Вечерина {} начинается!'.format(party_name), quote=False)
    except (IndexError, ValueError):
        _send_message(update, 'Usage: /party <name> <members> ⛔️', quote=False)
    except PartyAlreadyStarted:
        _send_message(update,
                      '🤦 ‍Для начала нужно закончить предыдущую вечерину: /finish {}'.format(
                          chat_data['party'].name), quote=False)


def add(bot, update, args, chat_data):
    try:
        new_member = args[0]
        party = chat_data['party']
        party.add(new_member)
        _send_message(update, '➕ Понял принял, {} теперь в теме'.format(new_member))
    except KeyError:
        _send_message(update, '🌞 🌞 Вечерина еще не началась :(', quote=False)
    except IndexError:
        _send_message(update, 'Usage: /add <member> ⛔️', quote=False)
    except AlreadyMember:
        _send_message(update, '🥳 🥳 {} уже на вечерине!'.format(args[0]), quote=False)


def remove(bot, update, args, chat_data):
    try:
        removed_member = args[0]
        party = chat_data['party']
        party.remove(removed_member)
        _send_message(update, '➖ {} уходит в закат'.format(removed_member))
    except IndexError:
        _send_message(update, 'Usage: /remove <member> ⛔️')
    except KeyError:
        _send_message(update, '🌞 🌞 Вечерина еще не началась :(', quote=False)
    except NotAMember:
        _send_message(update, '😞 😞 {} еще не на вечерине :('.format(args[0]), quote=False)
    except MemberWastedMoneyAlready:
        _send_message(update, '😡 😡 {} уже потратился, как-то некрасиво выгонять'.format(args[0]), quote=False)

def reset(bot, update, args, chat_data):
    try:
        reset_member = args[0]
        party = chat_data['party']
        party.reset(reset_member)
    except IndexError:
        _send_message(update, 'Usage: /reset <member> ⛔️')
    except KeyError:
        _send_message(update, '🌞 🌞 Вечерина еще не началась :(', quote=False)
    except NotAMember:
        _send_message(update, '😞 😞 {} еще не на вечерине :('.format(args[0]), quote=False)



def members(bot, update, chat_data):
    try:
        party = chat_data['party']
        members = party.members_list()
        if not members:
            _send_message(update, 'Вечерина пустует...')
            return
        _send_message(update, 'В вечерине учавствуют:\n{}'.format('\n'.join(members)))
    except KeyError:
        _send_message(update, '🌞 🌞 Вечерина еще не началась :(', quote=False)


def money(bot, update, chat_data):
    try:
        party = chat_data['party']
        money = party.money()
        if not money:
            _send_message(update, 'Вечерина пустует...')
            return

        messages = ['{} потратил {}'.format(member, money) for member, money in money.items()]
        _send_message(update, 'Текущие траты:\n{}'.format('\n'.join(messages)))
    except KeyError:
        _send_message(update, '🌞 🌞 Вечерина еще не началась :(', quote=False)


def waste(bot, update, args, chat_data):
    try:
        sponsor, amount = args[0], _to_money(args[1])
        party = chat_data['party']
        party.waste(sponsor, amount)

        _send_message(update, '💰 💵 💴 Понял, сенкью, {} потратил {} рублей'.format(sponsor, amount), quote=False)
    except IndexError:
        _send_message(update, 'Usage: /waste <who> <amount> ⛔️', quote=False)
    except KeyError:
        _send_message(update, '😭 😭 Вечерина еще не началась :(', quote=False)
    except IncorrectMoney:
        _send_message(update, 'Что за дичь? {}'.format(args[1]), quote=False)


def payoff(bot, update, chat_data):
    try:
        party = chat_data['party']
        transactions = party.payoff()

        message = '\n'.join(['{} => {}: {}'.format(f, t, a) for f, t, a in transactions])
        _send_message(update, message)

    except KeyError:
        _send_message(update, '😭 😭 Вечерина еще не началась :(', quote=False)

    except PartyIsTooBoring:
        _send_message(update, 'Рассчитывать тут особо нечего...', quote=False)


def finish(bot, update, chat_data):
    try:
        party_name = chat_data['party'].name
        del chat_data['party']
        _send_message(update, 'Вечерина {} закончилась! 🔥🔥🔥'.format(party_name), quote=False)
    except KeyError:
        _send_message(update, 'Вечерины не было :( 😢 😢', quote=False)
