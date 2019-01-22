from typing import List


class UnknownParticipant(Exception):
    pass


class AlreadyMember(Exception):
    pass


class NotAMember(Exception):
    pass


class MemberWastedMoneyAlready(Exception):
    pass


class PartyIsTooBoring(Exception):
    pass


class IncorrectMoney(Exception):
    pass


class Spending:
    def __init__(self, member, amount):
        self.member = member
        self.amount = amount


class Party:
    def __init__(self, name: str, members: List[str]):
        self.name = name
        self.members = {m: 0 for m in members}

    def waste(self, member: str, amount: int):
        if member not in self.members:
            raise UnknownParticipant(member=member, party=self.name)

        self.members[member] += amount

    def add(self, member: str):
        if member in self.members:
            raise AlreadyMember(member=member, party=self.name)

        self.members[member] = 0

    def remove(self, member: str):
        if member not in self.members:
            raise NotAMember()

        if self.members[member] != 0:
            raise MemberWastedMoneyAlready()

        del self.members[member]

    def reset(self, member: str):
        if member not in self.members:
            raise NotAMember()

        self.members[member] = 0

    def members_list(self):
        return list(self.members.keys())

    def money(self):
        return self.members

    def payoff(self):
        if len(self.members) < 2:
            raise PartyIsTooBoring()

        overall = sum(amount for amount in self.members.values())
        if overall == 0:
            raise PartyIsTooBoring()

        every = overall / len(self.members)
        result = [Spending(m, amount - every) for m, amount in self.members.items()]

        debtors, creditors = _split(result, lambda s: s.amount < 0, lambda s: s.amount > 0)
        debtors.sort(key=lambda s: s.amount)
        creditors.sort(key=lambda s: s.amount)

        if not debtors and not creditors:
            raise PartyIsTooBoring()

        transactions = list()
        while debtors and creditors:
            d = debtors[0]
            c = creditors[0]

            transaction_cost = min(c.amount, -d.amount)
            transactions.append((d.member, c.member, round(transaction_cost, 1)))

            if c.amount > -d.amount:
                debtors.pop(0)
                c.amount -= transaction_cost
            else:
                creditors.pop(0)
                d.amount += transaction_cost

        return transactions


def _split(col, c1, c2):
    s1 = [e for e in col if c1(e)]
    s2 = [e for e in col if c2(e)]
    return s1, s2


def _to_money(text: str):
    try:
        return float(text)
    except ValueError:
        pass

    text = text.replace('к', 'k')
    if text.count('.') > 1 or text.count('k') > 1:
        raise IncorrectMoney(text)

    if not text.endswith('k'):
        raise IncorrectMoney(text)

    return float(text[:-1]) * 1000
