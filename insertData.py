import sqlite3
import os
import csv
from parse import parseStartCheck


conn = sqlite3.connect('TestDB20230406.db')
cursor = conn.cursor()

# 存取舊資料
cursor.execute("SELECT * FROM GameRecord20230131")
old_data = cursor.fetchall()

cursor.close()

# 建立 cursor 物件
cursor = conn.cursor()

# 存取RoomID資料表
Room_map = {}
# ('Deal', '[ "A1" ]', 10029510, '1', '2023-01-31T00:00:00.006Z', '', '1675094400006159', '', '[ "DR", "A1", "A2", "A3", "A4", "A4", "A4", "A6", "A6", "A6", "A7", "A7", "A9", "A1" ]', 83, 10905005, 2, '2023-01-31', 14508821, 3, '106.14.245.225:5003-90329070-8951', '63d7e980d8c94279c9d4bffb', 'zeonmj-socket-03-prod_31177_10726433_1675094400006_GameRecord')
# print (Room_map[14508821][0])

# 根據RoundNo來分類舊資料
for row in old_data:
    RoomID = row[13]   # RoundNo在第14個欄位
    if RoomID not in Room_map:
        Room_map[RoomID] = []
    Room_map[RoomID].append(row)

# 玩法資料表
GameType_map = {}

# Level資料表
Level_map = {}

# 檢查每個房間的所有資料筆數內的ACT是否有Start
for roomID, data in Room_map.items():
    for row in data:
        Act = row[0]   # Act在第1個欄位
        if Act == 'StartCheck':
            # 取得玩法與廳館json
            # ex:["CrazyJoker8", "Beginner", 10, 99999] 
            _startstring = row[1]

            # 解析StartCheck
            gametype, level, basePoint, limitTai = parseStartCheck(_startstring)
            GameType_map[roomID] = gametype
            Level_map[roomID] = level

# 顯示 GameType_map
# print (GameType_map[14509676]) # Joker4
# print(Level_map[14509676]) # Beginner

# 根據玩法 分級 來寫入csv
# 分類完後，根據map的index, 寫入csv

# # 取得當前檔案所在的目錄路徑
current_directory = os.path.dirname(os.path.abspath(__file__))

for roomID, data in Room_map.items():
    if roomID in GameType_map:
        gametype = GameType_map[roomID]
        level = Level_map[roomID]

        # 建立玩法資料夾
        gametype_directory = os.path.join(current_directory, gametype)
        if not os.path.exists(gametype_directory):
            os.mkdir(gametype_directory)
        # 建立分級資料夾
        level_directory = os.path.join(gametype_directory, level)
        if not os.path.exists(level_directory):
            os.mkdir(level_directory)
        # 寫入 roomID.csv檔
        filename = f"round_{roomID}.csv"
        filepath = os.path.join(level_directory, filename)

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)