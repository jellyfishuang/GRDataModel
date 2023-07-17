import sqlite3
# 編一個新的資料庫

conn = sqlite3.connect('TestDB20230406.db')

cursor = conn.cursor()

# 建立對局資料表
cursor.execute('''CREATE TABLE Room (
                    RoomID integer,
                    Act text,
                    GameType text,
                    _level text,
                    basePoint integer,
                    limitTai integer,
                    ArkId text,
                    Seat integer,
                    AutoType text,
                    CreateDay text,
                    CreateTime text,
                    CreatrTS text,
                    HandTile text,
                    _index integer,
                    PreArkId integer,
                    PreSeat integer,
                    TableID text,
                    _id text,
                    i17game_send_key text
                    )''')

conn.commit()

# 建立玩家資料表
cursor.execute('''CREATE TABLE Player (
                    PlayerID integer,
                    isAI boolean,
                    AI_name text,
                    PlayTimes integer,
                    )''')
conn.commit()

cursor.close()
conn.close()