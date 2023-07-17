import sqlite3
from parse import parseStartCheck
import os
import csv

conn = sqlite3.connect('TestDB20230406.db')
cursor = conn.cursor()

# cursor.execute("SELECT * FROM GameRecord20230131 LIMIT 1")
# result = cursor.fetchall()
# for row in result:
#     print(row)
#===============================================================================
# # 執行查詢以取得資料筆數
# cursor.execute("SELECT COUNT(*) FROM GameRecord20230131")

# # 擷取結果
# total_rows = cursor.fetchone()[0]

# print("資料筆數：", total_rows)
#===============================================================================

# # 執行查詢以取得欄位資訊
# cursor.execute("PRAGMA table_info(GameRecord20230131)")

# # 擷取結果
# columns = cursor.fetchall()

# # 輸出欄位名稱
# for column in columns:
#     print(column[0], column[1])

#===============================================================================

# # 取得當前檔案所在的目錄路徑
# current_directory = os.path.dirname(os.path.abspath(__file__))

# # Room 資料夾路徑
# room_directory = os.path.join(current_directory, 'Room')

# # 如果 Room 資料夾不存在，則建立該資料夾
# if not os.path.exists(room_directory):
#     os.makedirs(room_directory)

# # 生成map
# data_map = {}

# # map的key用RoundNo, value用 當筆資料list塞入
# # 遍歷所有資料
# cursor.execute("SELECT * FROM GameRecord20230131")
# result = cursor.fetchall()

# cursor.close()
# conn.close()

# # 根據RoundNo來分類
# for row in result:
#     RoundNo = row[13]   # RoundNo在第14個欄位
#     if RoundNo not in data_map:
#         data_map[RoundNo] = []
#     data_map[RoundNo].append(row)

# # 分類完後，根據map的index, 寫入csv
# # 寫檔進 Room 資料夾
# for round_no, data in data_map.items():
#     filename = f"round_{round_no}.csv"
#     filepath = os.path.join(room_directory, filename)
#     with open(filepath, 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerows(data)
#     print(f"已將資料寫入 {filepath}")

#===============================================================================

# 生成map
data_map = {}
joker_map = {}

# 遍歷所有資料
cursor.execute("SELECT * FROM GameRecord20230131")
result = cursor.fetchall()

cursor.close()
conn.close()

haveStart = 0
RoomCount = 0

# 根據RoundNo來分類
for row in result:
    RoundNo = row[13]   # RoundNo在第14個欄位
    if RoundNo not in data_map:
        data_map[RoundNo] = []
        RoomCount += 1
    data_map[RoundNo].append(row)

# 玩法紀錄
play = {}

# 根據廳館玩法分類
play_room_map = {}

# 廳館紀錄
room = {}

# 檢查每個房間的所有資料筆數內的ACT是否有Start
for round_no, data in data_map.items():
    for row in data:
        Act = row[0]   # Act在第1個欄位
        if Act == 'StartCheck':
            haveStart += 1

            # 取得玩法與廳館json
            # ex:["CrazyJoker8", "Beginner", 10, 99999] 
            _startstring = row[1]

            # 解析StartCheck
            _play, _room, score1, score2 = parseStartCheck(_startstring)

            if _play not in play:
                play[_play] = 0
            play[_play] += 1

            if _room not in room:
                room[_room] = 0
            room[_room] += 1

            # 玩法與廳館map
            if _play not in play_room_map:
                play_room_map[_play] = {}

            if _play == "CrazyJoker8":
                joker_map[round_no] = data

print(f"have {RoomCount} rooms")
print(f"have {haveStart} StartCheck")
print(f"play: {play}")
print(f"room: {room}")

# ==================================

# # 取得當前檔案所在的目錄路徑
# current_directory = os.path.dirname(os.path.abspath(__file__))

# # Room 資料夾路徑
# room_directory = os.path.join(current_directory, '8Joker')

# # 把8紅中的玩法房間資料取出來
# print(f"have {len(joker_map)} rooms")

# 分類完後，根據map的index, 寫入csv
# 寫檔進 Room 資料夾
# for round_no, data in joker_map.items():
#     filename = f"round_{round_no}.csv"
#     filepath = os.path.join(room_directory, filename)
#     with open(filepath, 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerows(data)
#     print(f"have written {filepath} done")