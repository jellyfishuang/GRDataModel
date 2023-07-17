import os
import csv
import player
from parse import parseStartCheck, parseBeginDeal, parseHandTile, parseDeal, parseDiscard

# 指定資料夾路徑
folder_path = 'Mining'

# 遍歷資料夾中的檔案
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        
        # 開啟CSV檔案
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)

            csv_playmode = None         # 玩法
            csv_level = None            # 廳館分級
            csv_basePoint = 0           # 基本台對應遊戲幣
            csv_limitTai = 0            # 上限番數
            # init 4 player
            csv_players = [None, None, None, None]
            # csv log index
            csv_index = -1

            # 讀取每一行資料
            for row in csv_reader:
                # 在此處進行資料分析的相關處理
                # init room log
                if row[0] == 'StartCheck' and row[9] == '0':
                    csv_playmode, csv_level, csv_basePoint, csv_limitTai = parseStartCheck(row[1])
                    csv_index = 0 
                    continue

                # init player
                if row[0] == 'BeginDeal':
                    isAI, Mode, Handmode, Money = parseBeginDeal(row[1])
                    playerID = int(row[2])
                    csv_index = int(row[9])
                    playerIndex = int(row[14])
                    _player = None

                    # init player
                    if isAI:
                        _player = player.Player(playerID, isAI, Mode, -1, Handmode, csv_playmode, Money)
                    else:
                        _player = player.Player(playerID, isAI, -1, Mode, Handmode, csv_playmode, Money)
                    csv_players[playerIndex] = _player

                    continue

                if row[0] == 'ChangeSelect':
                    csv_index = int(row[9])
                    continue

                if row[0] == 'ChangeTake':
                    csv_index = int(row[9])
                    continue

                if row[0] == 'SelectLack':
                    # 有換三張時，手牌在定缺才被定下來
                    playerhandtiles_str = row[8]
                    playerIndex = int(row[14])
                    _player = csv_players[playerIndex]

                    # 設置遊戲局內玩家之手牌
                    playerhandtiles = parseHandTile(playerhandtiles_str)
                    player.Player.Set_hand(_player, playerhandtiles)
                    csv_index = int(row[9])
                    continue

                # 進牌
                if row[0] == 'Deal' or row[0] == 'KongDeal':
                    csv_index = int(row[9])
                    action_PlayerIndex = int(row[14])
                    action_Tile = parseDeal(row[1])
                    csv_players[action_PlayerIndex].Draw_card(action_Tile)

                    # check 
                    playerhandtiles_str = row[8]
                    #print("playerhandtiles_str:", playerhandtiles_str)
                    playerhandtiles = parseHandTile(playerhandtiles_str)
                    #print("playerhandtiles:", playerhandtiles)
                    _player = csv_players[action_PlayerIndex]
                    player.Player.Set_hand(_player, playerhandtiles)

                    # isOk = player.Player.Set_hand(csv_players[action_PlayerIndex], playerhandtiles)
                    # if not isOk:
                    #     print('Error: Deal', action_PlayerIndex, playerhandtiles, csv_players[action_PlayerIndex].hand)
                    continue

                # 丟牌
                if row[0] == 'Discard':
                    csv_index = int(row[9])
                    action_PlayerIndex = int(row[14])
                    action_Tile, is_empty = parseDiscard(row[1])
                    print("action_Tile:", action_Tile)
                    print("is_empty:", is_empty)
                    isOk = csv_players[action_PlayerIndex].Self_discard(action_Tile, csv_index)
                    if not isOk:
                        print('Error: Discard', action_PlayerIndex, action_Tile, csv_players[action_PlayerIndex].hand)

                    for _player in csv_players:
                        if _player.PlayerID == action_PlayerIndex:
                            continue
                        _player.Other_discard(csv_index)
                    continue

                # 碰牌
                if row[0] == 'Pong':
                    csv_index = int(row[9])
                    action_PlayerIndex = int(row[14])
                    action_Tile = row[1]
                    csv_players[action_PlayerIndex].Action_Pong(action_Tile, csv_index)
                    continue

                # 槓牌
                if row[0] == 'Kong':
                    csv_index = int(row[9])
                    action_PlayerIndex = int(row[14])
                    action_Tile = row[1]
                    csv_players[action_PlayerIndex].Action_Kong(action_Tile, csv_index)
                    continue

                # 加槓
                if row[0] == 'AddKong':
                    csv_index = int(row[9])
                    action_PlayerIndex = int(row[14])
                    action_Tile = row[1]
                    csv_players[action_PlayerIndex].Action_AddKong(action_Tile, csv_index)
                    continue
                    
                if row[0] == 'ConcealedKong':
                    csv_index = int(row[9])
                    action_PlayerIndex = int(row[14])
                    action_Tile = row[1]
                    csv_players[action_PlayerIndex].Action_ConcealedKong(action_Tile, csv_index)
                    continue

                if row[0] == 'GunHu' or row[0] == 'CritSelfHu':
                    csv_index = int(row[9])
                    action_PlayerIndex = int(row[14])
                    action_Tile = row[1]
                    csv_players[action_PlayerIndex].Action_GunHu(action_Tile, csv_index)
                    continue

                if row[0] == 'GrabKongHu' or row[0] == 'CritGrabKongHu':
                    csv_index = int(row[9])
                    action_PlayerIndex = int(row[14])
                    action_Tile = row[1]
                    csv_players[action_PlayerIndex].Action_GunHu(action_Tile, csv_index)
                    continue

                if row[0] == 'SelfHu' or row[0] == 'CritSelfHu':
                    csv_index = int(row[9])
                    action_PlayerIndex = int(row[14])
                    action_Tile = row[1]
                    csv_players[action_PlayerIndex].Action_GunHu(action_Tile, csv_index)
                    continue

                if row[0] == 'HuEnd':
                    csv_index = int(row[9])
                    action_PlayerIndex = int(row[14])
                    action_Tile = row[1]
                    csv_players[action_PlayerIndex].Action_GunHu(action_Tile, csv_index)
                    continue

                if row[0] == 'DanKong':
                    csv_index = int(row[9])
                    continue

                if row[0] == 'Bankruptcy':
                    csv_index = int(row[9])
                    action_PlayerIndex = int(row[14])
                    csv_players[action_PlayerIndex].Action_Bankruptcy(csv_index)
                    continue

                if row[0] == 'Resurrection':
                    csv_index = int(row[9])
                    continue

                if row[0] == 'MingPai':
                    csv_index = int(row[9])
                    continue

                if row[0] == 'EndBalance':
                    csv_index = int(row[9])
                    continue

                if row[0] == 'EndCheck' or row[0] == 'RoundEnd':
                    csv_index = int(row[9])
                    continue

            # example print
            for _player in csv_players:
                print(_player.PlayerID, _player.isAI, _player.AI_name, _player.PlayVIP, _player.HandTilemode, _player.Playmode, _player.PlayerMoney)
                print(_player.hand)
