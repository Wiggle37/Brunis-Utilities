from os import close
import sqlite3
import discord

class punishments:
    @staticmethod
    def banned(user_id):
        dbase = sqlite3.connect('settings.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT ban FROM bans WHERE user_id = '{user_id}'")
        result = cursor.fetchone()

        dbase.close()
        return result is not None

class heistmode:
    def heist():
        dbase = sqlite3.connect('settings.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT heistmode FROM heistmode")
        result = cursor.fetchone()

        if result is None:
            return False

        elif result[0] == 'True':
            return True

        elif result[0] == 'False':
            return False