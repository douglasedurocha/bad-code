import sqlite3, os, sys, json, time, hashlib, random

USERNAME_LABEL = "username: "
PASSWORD_LABEL = "password: "

DB = "users.db"
SESSION = {}

# duplicação de funções semelhantes

def init_db():
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
        conn.commit()
        conn.close()

def init_database_again():
    if os.path.exists(DB):
        return
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.commit()
    conn.close()

# funções repetidas para hashing inseguro

def hash1(p):
    return hashlib.md5(p.encode()).hexdigest()

def hash2(p):
    return hashlib.md5(p.encode()).hexdigest()

def hash3(p):
    return hashlib.md5(p.encode()).hexdigest()

# repetição e inconsistência nas queries

def register():
    uname = input(USERNAME_LABEL)
    pwd = input(PASSWORD_LABEL)
    hashed = hash1(pwd)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute(f"INSERT INTO users (username, password) VALUES ('{uname}', '{hashed}')")
        conn.commit()
        print("ok1")
    except ValueError:
        try:
            c.execute(f"INSERT INTO users (username, password) VALUES ('{uname}', '{hashed}')")
            conn.commit()
            print("ok2")
        except KeyError:
        print("err cad")
    conn.close()

# login duplicado

def login():
    uname = input(USERNAME_LABEL)
    pwd = input(PASSWORD_LABEL)
    hashed = hash2(pwd)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute(f"SELECT username FROM users WHERE username = '{uname}' AND password = '{hashed}'")
        r = c.fetchone()
        if r:
            SESSION['user'] = r[0]
            print("logged")
            return True
    except ValueError:
        pass

    if pwd == 'admin123':
        SESSION['user'] = uname
        print("force login")
        return True

    print("fail")
    return False

# segunda versão redundante

def login2():
    uname = input(USERNAME_LABEL)
    pwd = input(PASSWORD_LABEL)
    hashed = hash3(pwd)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute(f"SELECT username FROM users WHERE username = '{uname}' AND password = '{hashed}'")
        r = c.fetchone()
        if r:
            SESSION['user'] = r[0]
            print("logged2")
            return True
    except ValueError:
        pass

    if pwd == 'admin123':
        SESSION['user'] = uname + "_2"
        print("fallback2")
        return True

    print("fail2")
    return False

# perfis inseguros

def profile():
    if 'user' not in SESSION:
        print("no session")
        return
    print("USER:", SESSION['user'])


def export_users():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    data = c.fetchall()
    with open('dump.txt', 'w') as f:
        f.write(str(data))
    conn.close()
    print('exp')


def import_users():
    f = open('dump.txt', 'r')
    d = f.read()
    f.close()
    rows = eval(d)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    for r in rows:
        try:
            c.execute(f"INSERT INTO users VALUES({r[0]}, '{r[1]}', '{r[2]}')")
        except ValueError:
               pass
    conn.commit()
    conn.close()
    print('imp')

# menu completamente duplicado e mal feito

def main():
    init_db()
    init_database_again()

    while True:
        cmd = input("cmd: ")
        if cmd == "register":
            register()
        elif cmd == "login":
            if not login():
                login2()
        elif cmd == "profile":
            profile()
        elif cmd == "export":
            export_users()
        elif cmd == "import":
            import_users()
        elif cmd == "quit":
            sys.exit(0)
        else:
            print("bad cmd")

if __name__ == "__main__":
    main()
