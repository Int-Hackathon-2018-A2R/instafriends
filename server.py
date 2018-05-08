import sqlite3
from aiohttp import web
from secrets import *
from time import *

connection = sqlite3.connect("instafriends.db")
cursor = connection.cursor()

app = web.Application()

async def add_handler(request):
    print(request)
    z = await request.post()
    req_to_sql = """INSERT INTO users (id, name, vk, phone, email, vk_token)
    VALUES (NULL, ?, ?, ?, ?, ?);"""

    cursor.execute(req_to_sql, (z["name"], z["vk"], z["phone"], z["email"], z["vk_token"]))
    connection.commit()
    return web.Response(text="DONE")

async def gen_handler(request):
    print(request)
    z = await request.post()
    req = """SELECT id FROM users WHERE vk_token = ?"""
    print(req, z["vk_token"])
    id = cursor.execute(req, (z["vk_token"], )).fetchall()
    print(id)
    req = """INSERT INTO tokens (id, token, user_id, timestamp) VALUES (NULL, ?, ?, ?);"""
    tkn = token_hex(14)
    print(id)
    if len(id) == 0:
        return web.Response(text="Failed")

    TIME = "30" #z['time']
    cursor.execute(req, (tkn, int(id[0][0]), int(time()) + int(TIME)))
    print(tkn)
    connection.commit()
    return web.Response(text=tkn)

async def check_handler(request):
    cursor.execute("DELETE FROM tokens WHERE TIMESTAMP<" + str(int(time())))
    connection.commit()
    z = await request.post()
    tkn = z["token"]
    #print(cursor.execute("SELECT * FROM tokens").fetchall())
    #print(cursor.execute("SELECT * FROM tokens WHERE token=?", (z["token"], )).fetchall())

    data = cursor.execute("SELECT * FROM tokens WHERE token=?", (z["token"], )).fetchall()
    if len(data) == 0:
        return web.Response(text="{}")
    usr_id = int(data[0][2])
    print("USR_ID:", usr_id)
    data = cursor.execute("SELECT * FROM users WHERE id=?", (usr_id,)).fetchall()[0]
    resp = dict()
    resp["name"] = data[1]
    resp["vk"] = data[2]
    resp["phone"] = data[3]
    resp["email"] = data[4]
    print(resp)
    return web.Response(text=str(resp))

app = web.Application()
app.router.add_route('POST', '/enroll_service', add_handler)
app.router.add_route('POST', '/login', gen_handler)
app.router.add_route('POST', '/redeem_code', check_handler)
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])

web.run_app(app)