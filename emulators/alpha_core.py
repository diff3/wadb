#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bot for connecting Discord and Alpha-core emulator

Written by Entropy 2021
"""


import hashlib
from network.mysqld import Mysqld
import re


RACES = [
    "Human",
    "Orc",
    "Dwarf",
    "Night Elf",
    "Undead",
    "Tauren",
    "Gnome",
    "Troll"
]

CLASSES = [
    "Warrior",
    "Paladin",
    "Hunter",
    "Rogue",
    "Priest",
    "Shaman",
    "Mage",
    "Warlock",
    "Druid"
]

ADDRESS = "entropy.nu"
RE_PATTERN = r"[A-Za-z0-9!@#$%^&+=öäåÅÄÖ]+"
PATTERN = "A-Za-z0-9!@#$%^&+=öäåÅÄÖ"


class Alpha:
    @staticmethod
    def account_create(message):
        id = message.author.id
        lst = message.content.split(' ')

        if len(lst) < 3:
            return 'You need to provide username and password'

        if Alpha.account_exists(lst[1]):
            return 'Account name exists'

        if not Alpha.test_string_for_bad_char(lst[1]) or not Alpha.test_string_for_bad_char(lst[2]):
            return 'Username or password contains bad letters. Use: {}'.format(PETTERN)

        encoded = lst[2].encode()
        pwd = hashlib.sha256(encoded).hexdigest()

        SQL = "INSERT INTO accounts (name, password, ip, gmlevel) VALUES (%s, %s, %s, %s)"
        tpl = (lst[1], pwd, "0.0.0.0", 0)

        accountid = Mysqld("alpha_realm").insert(SQL, tpl)

        SQL = "INSERT INTO discord (account, discord_id, emulator) VALUES (%s, %s, %s)"
        tpl = (accountid, id, "alpha-core")

        Mysqld("wadb").insert(SQL, tpl)
        return "Your account was successfully created. Please set your realmlist to 'set realmlist {}'! Have fun!".format(ADDRESS)

    @staticmethod
    def account_delete(message):
        lst = message.content.split(' ')

        if len(lst) < 2:
            return 'You most provide an account name'

        if not Alpha.test_string_for_bad_char(lst[1]):
            return 'Username contains bad letters. Use: {}'.format(PATTERN)

        account = lst[1]
        id = message.author.id

        if not Alpha.account_exists(account):
            return 'Unknown account'

        if not (Alpha.account_is_perhaps_yours(id, account)):
            return "Unknown account"

        SQL = """DELETE discord, accounts
            FROM wadb.discord discord
            INNER JOIN alpha_realm.accounts accounts
            ON discord.account = accounts.id
            WHERE discord.discord_id = %s
            AND accounts.name =%s
            AND discord.emulator = 'alpha-core'"""

        tpl = (id, account)
        result = Mysqld("alpha_realm").insert(SQL, tpl)

        return 'Account deleted'

    @staticmethod
    def account_exists(account):
        SQL = "SELECT count(name) FROM accounts WHERE name = %s"
        tpl = (account, )

        result = Mysqld("alpha_realm").query(SQL, tpl)

        if int(result[0][0]) > 0:
            return True

        return False

    @staticmethod
    def account_is_perhaps_yours(id, account):
        SQL = """SELECT count(a.name) FROM alpha_realm.accounts a
                    INNER JOIN wadb.discord w
                    ON w.account = a.id
                    WHERE w.discord_id = %s
                    AND a.name = %s"""

        tpl = (id, account)
        yours = Mysqld("alpha_realm").query(SQL, tpl)

        if yours[0][0] <= 0:
            return False

        return True

    @staticmethod
    def account_list(message):
        id = message.author.id

        SQL = "SELECT name FROM wadb.discord as w, alpha_realm.accounts as ara WHERE ara.id in (w.account) AND w.discord_id = %s"
        tpl = (id, )

        result = Mysqld("alpha_realm").query(SQL, tpl)

        if len(result) <= 0:
            return 'You have no account'

        acc = str()

        for row in result:
            acc += ", {}".format(row[0])

        return "Your account: {}".format(acc[1:])

    @staticmethod
    def account_password(message):
        id = message.author.id
        lst = message.content.split(' ')

        if len(lst) < 3:
            return 'You most provide an account name and password'

        if not Alpha.test_string_for_bad_char(lst[1]) or not Alpha.test_string_for_bad_char(lst[2]):
            return 'Username or password contains bad letters. Use: {}'.format(PATTERN)

        account = lst[1]

        if not Alpha.account_exists(account):
            return 'Unknown account'

        if not (Alpha.account_is_perhaps_yours(id, account)):
            return "Unknown account"

        encoded = lst[2].encode()
        pwd = hashlib.sha256(encoded).hexdigest()

        SQL = """UPDATE alpha_realm.accounts, wadb.discord
                    SET alpha_realm.accounts.password = %s
                    WHERE wadb.discord.account = alpha_realm.accounts.id
                    AND alpha_realm.accounts.name = %s
                    AND wadb.discord.discord_id = %s"""

        tpl = (pwd, account, id)
        result = Mysqld("alpha_realm").insert(SQL, tpl)

        return 'Password updated'

    @staticmethod
    def curent_weather():
        return "It's sunny. It's always sunny."

    @staticmethod
    def get_discord_id(id):
        SQL = "SELECT discord.discord_id FROM wadb.discord INNER JOIN alpha_realm.accounts account ON account.id = discord.account WHERE account.name = %s"
        tpl = (id, )
        result = Mysqld("wadb").query(SQL, tpl)
        print()

        return result[0][0]

    @staticmethod
    def help_text():
        lst = [
            "I don't understand you. Here is a list of commands\n",
            "!account <username> <password>",
            "!delete <username>",
            "!help",
            "!list",
            "!online",
            "!password <username> <password>",
            "!weather"
        ]

        return '\n'.join(lst)

    @staticmethod
    def test_string_for_bad_char(msg):
        pat = re.compile(RE_PATTERN)

        if re.fullmatch(pat, msg):
            return True

        return False

    @staticmethod
    def num_player_online():
        result = Mysqld("alpha_realm").query("SELECT COUNT(online) FROM characters WHERE online='1'") # noqa
        return "with {} online".format(result[0][0])

    @staticmethod
    def who_is_online():
        result = Mysqld("alpha_realm").query("SELECT name, race, class, level, online FROM characters WHERE online='1'")

        msg = str()
        for row in result:
            msg += "{} the {} {} ({}) are {}\n".format(row[0], RACES[row[1] -1], CLASSES[row[2] -1], row[3], "online")

        return msg
