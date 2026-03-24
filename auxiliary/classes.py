from datetime import datetime

import aiosqlite
from loguru import logger

import auxiliary.messages as messages
import config

DB_NAME = config.DB_NAME

class User:
    def __init__(self, username=None, name='Незнакомец', age=0, email='no', tel='no', isAdmin=False, userID=None):
        self.username = username
        self.name = name
        self.age = age
        self.email = email
        self.tel = tel
        self.isAdmin = isAdmin
        self.userID = userID
    
    def __str__(self) -> str:
        return f'{self.name} (@{self.username}), {self.age}. Телефон: {self.tel}, почта: {self.email}'
    
    async def add(self) -> bool:
        """The function adds data from the 'User' class variable to the database."""
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute(
                "INSERT INTO users (username, name, age, email, tel, isAdmin) VALUES(?,?,?,?,?,?)",
                (self.username, self.name, self.age, self.email, self.tel, self.isAdmin)
                )
            await db.commit()
            logger.info(f'Пользователь {self.username} записан в БД')
            return True

    async def get_admins(self) -> list:
        """The function returns from the database a list of users marked as 'Admin'."""
        async with aiosqlite.connect(DB_NAME) as db:
            query = await db.execute(
                "SELECT username FROM users WHERE isAdmin = 1"
            )
            result = []
            items = await query.fetchall()
            for item in items:
                for username in item:
                    result.append(username)
            return result

    async def search(self, userID=None) -> User | bool:
        """The function searches for a user in the database by the 'userID' field.
           If the 'userID' value is not passed, the search is performed by the 'username' field."""
        async with aiosqlite.connect(DB_NAME) as db:
            if userID == None:
                item = await db.execute("SELECT * FROM users WHERE username = ?", (self.username,))
            else:
                item = await db.execute("SELECT * FROM users WHERE id = ?", (userID,))
            result = await item.fetchone()
            if result != None:
                self.userID = result[0]
                self.username = result[1]
                self.name = result[2]
                self.age = result[3]
                self.email = result[4]
                self.tel = result[5]
                self.isAdmin = result[6]
                return self
            else:
                return False

class Slot:

    TABLE = 'slots'

    def __init__(self, date='1970-01-01', time='00:00', new=0):
        self.date = date
        self.time = time
        self.new = new

    def __str__(self) -> str:
        date = datetime.strptime(self.date, '%Y-%m-%d')
        return f"{datetime.strftime(date, '%d.%m.%Y')} {self.time}"
    
    async def add(self) -> bool:
        """The function adds data from the 'Slot' class variable to the database."""
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute(
                f"INSERT INTO {self.TABLE} (date, time, new) VALUES(?,?,?)",
                (self.date, self.time, self.new)
            )
            await db.commit()
            logger.info(f'{messages.SLOT} {self.date} {self.time} {messages.RECORDED_ON_DB}')
            return True
    
    async def search(self) -> list | bool:
        """The function searches for a slot in the database:
           1) If the date and time are not specified, it returns all current slots
           2) If only the date is specified, it returns all slots for the specified date
           3) If the date and time are specified, it returns the specified slot
           If no slot is found, it returns False"""
        async with aiosqlite.connect(DB_NAME) as db:
            if self.date == '1970-01-01' and self.time == '00:00':
                slots = await db.execute(f'SELECT date FROM {self.TABLE} GROUP BY date ORDER BY date, time ASC')
            elif self.time == '00:00':
                slots = await db.execute(f"SELECT time FROM {self.TABLE} WHERE date = ?", (self.date,))
            else:
                slots = await db.execute(f"SELECT * FROM {self.TABLE} WHERE date = ? AND time = ?", (self.date, self.time))
            result = await slots.fetchall()
            if len(result) == 0:
                return False
            return result

    async def get_new(self) -> list | bool:
        """The function searches for new slots in the database (with a value of 1 in the "new" field)"""
        async with aiosqlite.connect(DB_NAME) as db:
            query = f"SELECT date, time FROM {self.TABLE} WHERE new=1"
            slot_lst = await db.execute(query)
            result = await slot_lst.fetchall()
            if len(result) == 0:
                return False
            return result

    async def unmark_new(self) -> bool:
        """This function removes the "new" mark from slots. It is called after new slots are sent to the admin chat."""
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute(
                f"UPDATE {self.TABLE} SET new = 0 WHERE new = 1"
            )
            await db.commit()
        return True
    
    async def delete(self) -> bool:
        """The function deletes a slot with a given date and time."""
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute(
                f"DELETE FROM {self.TABLE} WHERE date = ? and time = ?",
                (self.date, self.time)
            )
            await db.commit()
            if self.TABLE == 'slots':
                logger.info(f'{messages.SLOT} {self.date} {self.time} {messages.DELETED_FROM_DB}')
            else:
                logger.info(f'{messages.RECORD} {self.date} {self.time} {messages.ABORTED}')
        return True
    
    async def clear_old(self) -> bool:
        """The function removes slots whose date and time are less than the current one."""
        async with aiosqlite.connect(DB_NAME) as db:
            dtnow = datetime.now()
            slot_lst = await db.execute(
                f"SELECT date, time FROM {self.TABLE}"
            )
            slot_lst = await slot_lst.fetchall()
            for slot in slot_lst:
                dt = datetime.strptime(f'{slot[0]} {slot[1]}', '%Y-%m-%d %H:%M')
                if dt <= dtnow:
                    await db.execute(
                        f"DELETE FROM {self.TABLE} WHERE date = ? and time = ?",
                        (slot[0], slot[1])
                    )
                    await db.commit()
            if self.TABLE == 'slots':
                logger.info(f'{messages.OLD_SLOT_CLEAR}')
            else:
                logger.info(f'{messages.OLD_APOINT_CLEAR}')
        return True

class Apointment(Slot):

    TABLE = 'apointments'

    def __init__(self, date='1970-01-01', time='00:00', userID=0, new=1):
        super().__init__(date,time)
        self.userID = userID
        self.new = new
    
    def __str__(self) -> str:
        date = datetime.strptime(self.date, '%Y-%m-%d')
        return f"{datetime.strftime(date, '%d.%m.%Y')} {self.time} - userID: {self.userID}"

    async def add(self) -> bool:
        """The function adds data from the 'Apointment' class variable to the database."""
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute(
                f"INSERT INTO {self.TABLE} (date, time, userID, new) VALUES(?,?,?,?)",
                (self.date, self.time, self.userID, self.new)
            )
            await db.commit()
            logger.info(f'{messages.RECORD} {self.date} {self.time} - {self.userID} {messages.RECORDED_ON_DB}')
            return True

    async def search_user(self) -> list | bool:
        """The function searches for all user apointments (by the "userID" field)."""
        async with aiosqlite.connect(DB_NAME) as db:
            if self.userID != None:
                query = f"SELECT date, time FROM {self.TABLE} WHERE userID = {self.userID} ORDER BY date, time ASC"
                apoints = await db.execute(query)
                result = await apoints.fetchall()
            if len(result) == 0:
                return False
            return result

    async def get_new(self) -> list | bool:
        """The function searches for new apointment in the database (with a value of 1 in the "new" field)"""
        async with aiosqlite.connect(DB_NAME) as db:
            query = "SELECT apointments.date AS date, apointments.time AS time, users.username AS username, users.name AS name, users.age AS age, users.email AS email, users.tel AS tel FROM apointments INNER JOIN users ON apointments.userID = users.id WHERE apointments.new=1"
            apoint_lst = await db.execute(query)
            result = await apoint_lst.fetchall()
            if len(result) == 0:
                return False
            return result


# class Apointment:
#     def __init__(self, date='1970-01-01', time='00:00', userID=0, new=1):
#         self.date = date
#         self.time = time
#         self.userID = userID
#         self.new = new

#     async def add(self) -> bool:
#         """The function adds data from the 'Apointment' class variable to the database."""
#         async with aiosqlite.connect(DB_NAME) as db:
#             await db.execute(
#                 "INSERT INTO apointment (date, time, userID, new) VALUES(?,?,?,?)",
#                 (self.date, self.time, self.userID, self.new)
#             )
#             await db.commit()
#             logger.info(f'{messages.RECORD} {self.date} {self.time} - {self.userID} {messages.RECORDED_ON_DB}')
#             return True

#     async def search(self) -> list | bool:
#         """The function searches for a apointment in the database:
#            1) If the date and time are not specified, it returns all current apointments
#            2) If only the date is specified, it returns all apointments for the specified date
#            3) If the date and time are specified, it returns the specified apointment
#            If no slot is found, it returns False"""
#         async with aiosqlite.connect(DB_NAME) as db:
#             if self.date == '1970-01-01' and self.time == '00:00':
#                 apoints = await db.execute(f'SELECT date FROM apointment GROUP BY date ORDER BY date, time ASC')
#             elif self.time == '00:00':
#                 apoints = await db.execute("SELECT time FROM apointment WHERE date = ?", (self.date,))
#             else:
#                 apoints = await db.execute("SELECT * FROM apointment WHERE date = ? AND time = ?", (self.date, self.time))
#             result = await apoints.fetchall()
#             if len(result) == 0:
#                 return False
#             return result

#     async def search_user(self) -> list | bool:
#         """The function searches for all user apointments (by the "userID" field)."""
#         async with aiosqlite.connect(DB_NAME) as db:
#             if self.userID != None:
#                 apoints = await db.execute(
#                     f'SELECT date, time FROM apointment WHERE userID = ? ORDER BY date, time ASC',
#                     (self.userID)
#                 )
#                 result = await apoints.fetchall()
#             if len(result) == 0:
#                 return False
#             return result

#     async def get_new(self) -> list | bool:
#         """The function searches for new apointment in the database (with a value of 1 in the "new" field)"""
#         async with aiosqlite.connect(DB_NAME) as db:
#             query = "SELECT apointment.date AS date, apointment.time AS time, users.username AS username, users.name AS name, users.age AS age, users.email AS email, users.tel AS tel FROM apointment INNER JOIN users ON apointment.userID = users.id WHERE apointment.new=1"
#             apoint_lst = await db.execute(query)
#             result = await apoint_lst.fetchall()
#             if len(result) == 0:
#                 return False
#             return result
        
#     async def unmark_new(self) -> bool:
#         """This function removes the "new" mark from apointments.
#            It is called after new apointments are sent to the admin chat."""
#         async with aiosqlite.connect(DB_NAME) as db:
#             await db.execute(
#                 "UPDATE apointment SET new = 0 WHERE new = 1"
#             )
#             await db.commit()
#         return True

#     async def delete(self) -> bool:
#         """The function deletes a apointment with a given date and time."""
#         async with aiosqlite.connect(DB_NAME) as db:
#             await db.execute(
#                 "DELETE FROM apointment WHERE date = ? and time = ?",
#                 (self.date, self.time)
#             )
#             await db.commit()
#             logger.info(f'{messages.RECORD} {self.date} {self.time} {messages.ABORTED}')
#         return True

#     async def clear_old(self) -> bool:
#         """The function removes apointment whose date and time are less than the current one."""
#         async with aiosqlite.connect(DB_NAME) as db:
#             dtnow = datetime.now()
#             apoint_lst = await db.execute(
#                 "SELECT date, time FROM apointment"
#             )
#             apoint_lst = await apoint_lst.fetchall()
#             for apoint in apoint_lst:
#                 dt = datetime.strptime(f'{apoint[0]} {apoint[1]}', '%Y-%m-%d %H:%M')
#                 if dt <= dtnow:
#                     await db.execute(
#                         "DELETE FROM apointment WHERE date = ? and time = ?",
#                         (apoint[0], apoint[1])
#                     )
#                     await db.commit()
#             logger.info(f'{messages.OLD_APOINT_CLEAR}')
#         return True
