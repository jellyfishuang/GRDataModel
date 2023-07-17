import os
import csv
from parse import parseStartCheck, parseBeginDeal, parseHandTile, parseDeal, parseDiscard
import model

# 指定資料夾路徑
folder_path = 'Mining'

# 遍歷資料夾中的檔案
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        
        # 開啟CSV檔案
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            csv_players = [None, None, None, None]

            startcheck_str = None

            for row in csv_reader:
                if row[0] == 'StartCheck':
                    startcheck_str = row[1]
                    continue

                # set player
                if row[0] == 'BeginDeal':
                    begindeal_str = row[1]
                    playerID = int(row[2])
                    roomID = int(row[13])
                    playerIndex = int(row[14])

                    csv_players[playerIndex] = model.IGSPlayer(startcheck_str, begindeal_str, roomID, playerID, playerIndex)
                    #print(csv_players[playerIndex].haveMoney)
                    continue

                # set change tile log
                if row[0] == 'ChangeSelect' or row[0] == 'ChangeTake':
                    playerIndex = int(row[14])
                    csv_players[playerIndex].set_ChangeTilelog(row[1])
                    continue

                # set select lack
                if row[0] == 'SelectLack':
                    playerIndex = int(row[14])
                    csv_players[playerIndex].set_SelectLack(row[1])
                    continue

                # set action discard
                if row[0] == 'Discard':
                    playerIndex = int(row[14])
                    #print(row[1], row[8])
                    for i in range(4):
                        csv_players[i].add_GameLength()
                    csv_players[playerIndex].action_Discard(row[1], row[8])
                    #print(csv_players[playerIndex].branchFactor, csv_players[playerIndex].gameLength)
                    continue

                # set action pong, kong
                if row[0] == 'Pong' or row[0] == 'Kong' or row[0] == 'AddKong' or row[0] == 'ConcealedKong'\
                      or row[0] == 'GunHu' or row[0] == 'CritSelfHu' or row[0] == 'GrabKongHu' or row[0] == 'CritGrabKongHu'\
                        or row[0] == 'SelfHu' or row[0] == 'HuEnd':
                    playerIndex = int(row[14])
                    csv_players[playerIndex].action_pongkonghu()
                    continue

                # set action hu
                # if player decide to hu, after hu his branchFactor must have add 0 (he have no options)
                if row[0] == 'GunHu' or row[0] == 'CritSelfHu' or row[0] == 'GrabKongHu' or row[0] == 'CritGrabKongHu'\
                        or row[0] == 'SelfHu':
                    playerIndex = int(row[14])
                    csv_players[playerIndex].action_pongkonghu()
                    continue

                # set action bankruptcy
                if row[0] == 'Bankruptcy':
                    playerIndex = int(row[14])
                    csv_players[playerIndex].action_bankruptcy()
                    continue

                if row[0] == 'EndCheck' or row[0] == 'RoundEnd':
                    break

            for i in range(4):
                print(csv_players[i].print_GR())

