import sqlite3

def _connect():
    con = sqlite3.connect('data/astra.db')
    cur = con.cursor()
    return con, cur

class AstraDBConnection:

    @staticmethod
    def initialize():
        con, cur = _connect()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS quotes(
                id INTEGER PRIMARY KEY,
                user INTEGER NOT NULL,
                msg TEXT NOT NULL
            )"""
        )
        con.commit()
        con.close()
    
    @staticmethod
    def add_quote(user: int, msg: str):
        con, cur = _connect()
        cur.execute('insert into quotes values(NULL, ?, ?)', (user, msg))
        con.commit()
        con.close()
        
    @staticmethod
    def search_quote(fromUser: int, withMsg: str):
        con, cur = _connect()
        res = cur.execute('select id from quotes where user = ? and msg = ?', (fromUser, withMsg)).fetchall()
        con.close()
        return res
    
    @staticmethod
    def read_quotes(fromUser: int):
        con, cur = _connect()
        res = cur.execute('select msg, id from quotes where user=? order by id desc', (fromUser,)).fetchall()
        con.close()
        return res
    
    @staticmethod
    def delete_quote(withId: int):
        con, cur = _connect()
        cur.execute('delete from quotes where id = ?', (withId,))
        con.commit()
        con.close()
        
    @staticmethod
    def query_all():
        con, cur = _connect()
        res = cur.execute('select msg from quotes').fetchall()
        return [v[0] for v in res]