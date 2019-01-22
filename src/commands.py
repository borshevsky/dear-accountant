from party import Party, AlreadyMember, MemberWastedMoneyAlready, PartyIsTooBoring, IncorrectMoney, _to_money


class PartyAlreadyStarted(Exception):
    pass


def party(bot, update, args, chat_data):
    try:
        party_name, members = args[0], args[1:]
        if 'party' in chat_data:
            raise PartyAlreadyStarted()
        chat_data['party'] = Party(party_name, members)

        update.message.reply_text('🍾 💃 🕺 Вечерина {} начинается!'.format(party_name), quote=False)
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /party <name> <members> ⛔️', quote=False)
    except PartyAlreadyStarted:
        update.message.reply_text(
            '🤦 ‍Для начала нужно закончить предыдущую вечерину: /finish {}'.format(
                chat_data['party'].name), quote=False)


def add(bot, update, args, chat_data):
    try:
        new_member = args[0]
        party = chat_data['party']
        party.add(new_member)
        update.message.reply_text('➕ Понял принял, {} теперь в теме'.format(new_member))
    except KeyError:
        update.message.reply_text('🌞 🌞 Вечерина еще не началась :(', quote=False)
    except IndexError:
        update.message.reply_text('Usage: /add <member> ⛔️', quote=False)
    except AlreadyMember:
        update.message.reply_text('🥳 🥳 {} уже на вечерине!'.format(args[0]), quote=False)


def remove(bot, update, args, chat_data):
    try:
        removed_member = args[0]
        party = chat_data['party']
        party.remove(removed_member)
        update.message.reply_text('➖ {} уходит в закат'.format(removed_member))
    except IndexError:
        update.message.reply_text('Usage: /remove <member> ⛔️')
    except KeyError:
        update.message.reply_text('🌞 🌞 Вечерина еще не началась :(', quote=False)
    except NotAMember:
        update.message.reply_text('😞 😞 {} еще не на вечерине :('.format(args[0]), quote=False)
    except MemberWastedMoneyAlready:
        update.message.reply_text('😡 😡 {} уже потратился, как-то некрасиво выгонять'.format(args[0]), quote=False)


def members(bot, update, chat_data):
    try:
        party = chat_data['party']
        members = party.members_list()
        if not members:
            update.message.reply_text('Вечерина пустует...')
            return
        update.message.reply_text('В вечерине учавствуют:\n{}'.format('\n'.join(members)))
    except KeyError:
        update.message.reply_text('🌞 🌞 Вечерина еще не началась :(', quote=False)


def money(bot, update, chat_data):
    try:
        party = chat_data['party']
        money = party.money()
        if not money:
            update.message.reply_text('Вечерина пустует...')
            return

        messages = ['{} потратил {}'.format(member, money) for member, money in money.items()]
        update.message.reply_text('Текущие траты:\n{}'.format('\n'.join(messages)))
    except KeyError:
        update.message.reply_text('🌞 🌞 Вечерина еще не началась :(', quote=False)


def waste(bot, update, args, chat_data):
    try:
        sponsor, amount = args[0], _to_money(args[1])
        party = chat_data['party']
        party.waste(sponsor, amount)

        update.message.reply_text('💰 💵 💴 Понял, сенкью, {} потратил {} рублей'.format(sponsor, amount), quote=False)
    except IndexError:
        update.message.reply_text('Usage: /waste <who> <amount> ⛔️', quote=False)
    except KeyError:
        update.message.reply_text('😭 😭 Вечерина еще не началась :(', quote=False)
    except IncorrectMoney:
        update.message.reply_text('Что за дичь? {}'.format(args[1]), quote=False)


def payoff(bot, update, chat_data):
    try:
        party = chat_data['party']
        transactions = party.payoff()

        message = '\n'.join(['{} => {}: {}'.format(f, t, a) for f, t, a in transactions])
        update.message.reply_text(message)

    except KeyError:
        update.message.reply_text('😭 😭 Вечерина еще не началась :(', quote=False)

    except PartyIsTooBoring:
        update.message.reply_text('Рассчитывать тут особо нечего...', quote=False)


def finish(bot, update, chat_data):
    try:
        party_name = chat_data['party'].name
        del chat_data['party']
        update.message.reply_text('Вечерина {} закончилась! 🔥🔥🔥'.format(party_name), quote=False)
    except KeyError:
        update.message.reply_text('Вечерины не было :( 😢 😢', quote=False)
