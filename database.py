import sqlite3

def _connect():
    con = sqlite3.connect('astra.db')
    cur = con.cursor()
    return con, cur

class AstraDBConnection:
    # a question for my past self: why?
    _instance = None
    ind = 0
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            con, cur = _connect()
            cur.execute('create table if not exists quotes(user, msg, ind)')
            ind = cur.execute('select max(ind) from quotes').fetchall()[0][0]
            if ind is None:
                ind = 0
            cls.ind = ind
            print(f'Picking up at index {cls.ind}')
            con.close()
        return cls._instance
    
    @classmethod
    def add_quote(cls, user: int, msg: str):
        con, cur = _connect()
        cls.ind += 1
        cur.execute('insert into quotes values(?, ?, ?)', (user, msg, cls.ind))
        con.commit()
        con.close()
        
    @staticmethod
    def search_quote(fromUser: int, withMsg: str):
        con, cur = _connect()
        res = cur.execute('select ind from quotes where user = ? and msg = ?', (fromUser, withMsg)).fetchall()
        con.close()
        return res
    
    @staticmethod
    def read_quotes(fromUser: int):
        con, cur = _connect()
        res = cur.execute('select msg, ind from quotes where user=?', (fromUser,)).fetchall()
        con.close()
        return res
    
    @staticmethod
    def delete_quote(withIdent: int):
        con, cur = _connect()
        cur.execute('delete from quotes where ind = ?', (withIdent,))
        con.commit()
        con.close()