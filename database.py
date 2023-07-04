import sqlite3
import threading

lock = threading.Lock()

class DB:
    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.connection.isolation_level = None


    def get_user_info(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT status, bans_count FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result != None:
                    return result
                else:
                    return ["new", 0]
            except:
                self.connection.rollback()
            finally:
                lock.release()


    def get_permitions(self, permition):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT type FROM content WHERE permition=?', (permition, ))
                result = self.cursor.fetchall()
                return (result if result != None else [])
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def get_content_types(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT type, permition FROM content')
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def change_permition(self, contentType, permition):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE content SET permition=? WHERE type=?', (permition, contentType))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_banwords(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT word FROM banwords')
                try:
                    result = [row[0] for row in self.cursor.fetchall()]
                    return result
                except:
                    return []
            except:
                self.connection.rollback()
            finally:
                lock.release()
    

    def get_chats(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT chat_id FROM chats')
                result = self.cursor.fetchall()
                return (result if result != None else [])
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_chat(self, chatId):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO chats (chat_id) VALUES (?)', (chatId,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def del_chat(self, chatId):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('DELETE FROM chats WHERE chat_id=?', (chatId,))
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()


    def get_punishment(self, reason):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT punishment FROM punishMeasure WHERE reason=?', (reason, ))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def change_punishment(self, reason, punishment):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE punishMeasure SET punishment=? WHERE reason=?', (punishment, reason))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()
    

    def ban_user(self, user_id, user_info):
        with self.connection:
            try:
                lock.acquire(True)
                user_status = user_info[0]
                if user_status == "new":
                    self.cursor.execute('INSERT INTO users (user_id, status, bans_count) VALUES (?, ?, ?)', (user_id, "hasBanned", 1))
                else:
                    self.cursor.execute('UPDATE users SET bans_count=bans_count+1 WHERE user_id=?', (user_id, ))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def add_banword(self, word):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO banwords (word) VALUES (?)', (word,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def del_banword(self, word):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('DELETE FROM banwords WHERE word=?', (word,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def add_to_stat(self, user_id, chat_id, reason, reasonExplanation, punishment, banTime, violationDate, wasMessageSent):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO statistics (user_id, chat_id, reason, reasonExplanation, punishment, banTime, violationDate, wasMessageSent) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (user_id, chat_id, reason, reasonExplanation, punishment, banTime, violationDate, wasMessageSent))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_stat(self):
        with self.connection:
            try:
                lock.acquire(True)
                violations = [thing[0] for thing in self.cursor.execute('SELECT user_id FROM statistics').fetchall()]
                lastViolations = self.cursor.execute('SELECT violationDate, banTime FROM statistics WHERE id=?', (len(violations),)).fetchone()
                forBanWord = [thing[0] for thing in self.cursor.execute('SELECT user_id FROM statistics WHERE reason=?', ("banWord",)).fetchall()]
                forContentType = [thing[0] for thing in self.cursor.execute('SELECT user_id FROM statistics WHERE reason=?', ("contentType",)).fetchall()]
                bans = [thing[0] for thing in self.cursor.execute('SELECT user_id FROM statistics WHERE punishment=?', ("ban",)).fetchall()]
                deletes = [thing[0] for thing in self.cursor.execute('SELECT user_id FROM statistics WHERE punishment=?', ("delete",)).fetchall()]
                chats = [thing[0] for thing in self.cursor.execute('SELECT chat_id FROM statistics').fetchall()]
                banTimes = [thing[0] for thing in self.cursor.execute('SELECT banTime FROM statistics').fetchall()]
                messagesSent = [thing[0] for thing in self.cursor.execute('SELECT user_id FROM statistics WHERE wasMessageSent=True').fetchall()]
                violationsLastDay = [thing[0] for thing in self.cursor.execute('SELECT user_id FROM statistics WHERE violationDate<?', (86400,)).fetchall()]
                violationsLastWeek = [thing[0] for thing in self.cursor.execute('SELECT user_id FROM statistics WHERE violationDate<?', (604800,)).fetchall()]
                violationsLastMonth = [thing[0] for thing in self.cursor.execute('SELECT user_id FROM statistics WHERE violationDate<?', (2678400,)).fetchall()]
                violationsLastYear = [thing[0] for thing in self.cursor.execute('SELECT user_id FROM statistics WHERE violationDate<?', (31622400,)).fetchall()]
                return {"violations": violations, "forBanWord": forBanWord, "forContentType": forContentType,
                        "bans": bans, "deletes": deletes, "chats": chats, "banTimes": banTimes, "messagesSent": messagesSent,
                        "violationsLastDay": violationsLastDay, "violationsLastWeek": violationsLastWeek,
                        "violationsLastMonth": violationsLastMonth, "violationsLastYear": violationsLastYear, "lastViolations": lastViolations}
            except:
                self.connection.rollback()
            finally:
                lock.release()