# encoding: utf-8


from commands import *

import unittest
from unittest.mock import MagicMock

PARTY_NOT_STARTED = '🌞 🌞 Вечерина еще не началась :('
PARTY_ALREADY_STARTED = '🌞 🌞 Вечерина уже началась :('


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.bot = MagicMock()
        self.update = MagicMock()
        self.update.message.reply_text = MagicMock()
        self.chat_data = {}

    def tearDown(self):
        try:
            self.update.message.reply_text.assert_called_once()
        except AssertionError:
            self.update.message.reply_markdown.assert_called_once()

    def test_party_ok(self):
        args = ['party_name', ['a', 'b']]
        party(self.bot, self.update, args=args, chat_data=self.chat_data)
        self.assertEqual(self.chat_data['party'].name, 'party_name')

    def test_party_invalid_args(self):
        party(self.bot, self.update, args=['party_name'], chat_data=self.chat_data)
        self.assertTrue(self.usage_message(self.update.message.reply_text))
        self.assertException(lambda: self.chat_data['party'], KeyError)

    def test_party_when_already_started(self):
        self.chat_data['party'] = Party('123', ['a'])
        args = ['party_name', ['a', 'b']]
        party(self.bot, self.update, args=args, chat_data=self.chat_data)
        self.assertTrue(self.party_started_message(self.update.message.reply_text))

    def test_add_party_ok(self):
        self.chat_data['party'] = Party('123', ['a'])
        args = ['b']
        add(self.bot, self.update, args=args, chat_data=self.chat_data)
        self.assertFalse(self.party_not_started_message(self.update.message.reply_text))
        self.assertEqual(self.chat_data['party'].members_list(), ['a', 'b'])

    def test_add_party_not_started(self):
        args = ['b']
        add(self.bot, self.update, args=args, chat_data=self.chat_data)
        self.assertTrue(self.party_not_started_message(self.update.message.reply_text))

    def test_add_party_already_member(self):
        self.chat_data['party'] = Party('123', ['a'])
        args = ['a']
        add(self.bot, self.update, args=args, chat_data=self.chat_data)
        self.assertEqual(self.chat_data['party'].members_list(), ['a'])

    def test_song(self):
        song(self.bot, self.update)

    def usage_message(self, message):
        return message.call_args[0][0].startswith('⛔️ Usage:')

    def party_started_message(self, message):
        return message.call_args[0][0] == PARTY_ALREADY_STARTED

    def party_not_started_message(self, message):
        return message.call_args[0][0] == PARTY_NOT_STARTED

    def assertException(self, f, exception_class):
        with self.assertRaises(exception_class):
            f()

