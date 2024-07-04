import sqlite3

def _connect():
    con = sqlite3.connect('astra.db')
    cur = con.cursor()
    return con, cur

class AstraDBConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            con, cur = _connect()
            cur.execute('create table if not exists quotes(user, msg, ind)')
            ind = cur.execute('select max(ind) from quotes').fetchall()[0][0]
            if ind is None:
                ind = 0
            cls._instance.ind = ind
            con.close()
        return cls._instance
    
    def add_quote(self, user: int, msg: str):
        con, cur = _connect()
        self.ind += 1
        cur.execute('insert into quotes values(?, ?, ?)', (user, msg, self.ind))
        con.commit()
        con.close()
        
    def read_quotes(self, fromUser: int):
        con, cur = _connect()
        res = cur.execute('select msg, ind from quotes where user=?', (fromUser,)).fetchall()
        con.close()
        return res