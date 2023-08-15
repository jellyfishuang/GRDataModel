import os
import csv
from parse import parseStartCheck, parseBeginDeal, parseHandTile, parseDeal, parseDiscard
import model
import math

# 指定讀取資料夾路徑
Folder_path = 'Mining'

# 檢查玩家參數 (-1不起作用, 0~3指定檢查玩家)
CheckPlayer = -1

# 統計資料
arr_PossibleOptions = []
arr_GameLength = []
arr_GR = []

arr_AIPO = []
arr_AIGL = []
arr_AIGR = []

arr_HUPO = []
arr_HUGL = []
arr_HUGR = []

arr_BeginB = []
arr_BeginR = []
arr_BeginGR = []
arr_BeginCount = 0
arr_HumanbeginB = []
arr_HumanbeginR = []
arr_HumanbeginGR = []
arr_HumanbeginCount = 0
arr_AIbeginB = []
arr_AIbeginR = []
arr_AIbeginGR = []
arr_AIbeginCount = 0

arr_MidB = []
arr_MidR = []
arr_MidGR = []
arr_MidCount = 0
arr_HumanMidB = []
arr_HumanMidR = []
arr_HumanMidGR = []
arr_HumanMidCount = 0
arr_AIMidB = []
arr_AIMidR = []
arr_AIMidGR = []
arr_AIMidCount = 0

arr_HighB = []
arr_HighR = []
arr_HighGR = []
arr_HighCount = 0
arr_HumanHighB = []
arr_HumanHighR = []
arr_HumanHighGR = []
arr_HumanHighCount = 0
arr_AIHighB = []
arr_AIHighR = []
arr_AIHighGR = []
arr_AIHighCount = 0

arr_MasterB = []
arr_MasterR = []
arr_MasterGR = []
arr_MasterCount = 0
arr_HumanMasterB = []
arr_HumanMasterR = []
arr_HumanMasterGR = []
arr_HumanMasterCount = 0
arr_AIMasterB = []
arr_AIMasterR = []
arr_AIMasterGR = []
arr_AIMasterCount = 0

total_PossibleOptions = 0
total_GameLength = 0
total_PlayersCount = 0
total_GR = 0

# 遍歷資料夾中的檔案    
for root, dirs, files in os.walk(Folder_path):
    for filename in files:
        if filename.endswith('.csv'):
            file_path = os.path.join(root, filename)
            
            # 開啟CSV檔案
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                csv_players = [None, None, None, None]

                startcheck_str = None
                #print(file_path)
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

                        if CheckPlayer != -1 and playerIndex == CheckPlayer:
                            print(int(row[9]), "Discard", csv_players[playerIndex].branchFactor, csv_players[playerIndex].gameLength)
                        #print(csv_players[playerIndex].branchFactor, csv_players[playerIndex].gameLength)
                        continue

                    # set action pong, kong
                    if row[0] == 'Pong' or row[0] == 'Kong' or row[0] == 'AddKong' or row[0] == 'ConcealedKong':
                        playerIndex = int(row[14])
                        csv_players[playerIndex].action_pongkong()

                        if CheckPlayer != -1 and playerIndex == CheckPlayer:
                            print(int(row[9]), "pongkong", csv_players[playerIndex].branchFactor, csv_players[playerIndex].gameLength)
                        continue

                    # set action hu
                    # if player decide to hu, after hu his branchFactor must have add 0 (he have no options)
                    if row[0] == 'GunHu' or row[0] == 'CritSelfHu' or row[0] == 'GrabKongHu' or row[0] == 'CritGrabKongHu'\
                            or row[0] == 'SelfHu':
                        playerIndex = int(row[14])
                        csv_players[playerIndex].action_hu()

                        if CheckPlayer != -1 and playerIndex == CheckPlayer:
                            print(int(row[9]), "Hu", csv_players[playerIndex].branchFactor, csv_players[playerIndex].gameLength)
                        continue

                    # set action bankruptcy
                    if row[0] == 'Bankruptcy':
                        playerIndex = int(row[14])
                        csv_players[playerIndex].action_bankruptcy()
                        continue

                    if row[0] == 'EndCheck' or row[0] == 'RoundEnd':
                        break

                # 統合計算
                for i in range(4):
                    #csv_players[i].print_GR()
                    G, R, GR = csv_players[i].calculate_GR()
                    #print('G:', G, 'R:', R, 'GR:', GR)

                    # 極端情況跳過不計入
                    if GR == -1:
                        continue

                    total_PossibleOptions += G
                    total_GameLength += R
                    total_PlayersCount += 1
                    total_GR += GR
                    # 計算總GR
                    arr_PossibleOptions.append(G)
                    arr_GameLength.append(R)
                    arr_GR.append(GR)

                    # 計算AI GR 與真人 GR
                    if csv_players[i].isAI:
                        arr_AIPO.append(G)
                        arr_AIGL.append(R)
                        arr_AIGR.append(GR)
                    else:
                        arr_HUPO.append(G)
                        arr_HUGL.append(R)
                        arr_HUGR.append(GR)

                    # 計算玩家分級
                    if csv_players[i].gameLevel == 'Beginner':
                        arr_BeginB.append(G)
                        arr_BeginR.append(R)
                        arr_BeginGR.append(GR)
                        arr_BeginCount += 1
                        if csv_players[i].isAI:
                            arr_AIbeginB.append(G)
                            arr_AIbeginR.append(R)
                            arr_AIbeginGR.append(GR)
                            arr_AIbeginCount += 1
                        else:
                            arr_HumanbeginB.append(G)
                            arr_HumanbeginR.append(R)
                            arr_HumanbeginGR.append(GR)
                            arr_HumanbeginCount += 1
                    elif csv_players[i].gameLevel == 'Mid':
                        arr_MidB.append(G)
                        arr_MidR.append(R)
                        arr_MidGR.append(GR)
                        arr_MidCount += 1
                        if csv_players[i].isAI:
                            arr_AIMidB.append(G)
                            arr_AIMidR.append(R)
                            arr_AIMidGR.append(GR)
                            arr_AIMidCount += 1
                        else:
                            arr_HumanMidB.append(G)
                            arr_HumanMidR.append(R)
                            arr_HumanMidGR.append(GR)
                            arr_HumanMidCount += 1
                    elif csv_players[i].gameLevel == 'High':
                        arr_HighB.append(G)
                        arr_HighR.append(R)
                        arr_HighGR.append(GR)
                        arr_HighCount += 1
                        if csv_players[i].isAI:
                            arr_AIHighB.append(G)
                            arr_AIHighR.append(R)
                            arr_AIHighGR.append(GR)
                            arr_AIHighCount += 1
                        else:
                            arr_HumanHighB.append(G)
                            arr_HumanHighR.append(R)
                            arr_HumanHighGR.append(GR)
                            arr_HumanHighCount += 1
                    elif csv_players[i].gameLevel == 'Master':
                        arr_MasterB.append(G)
                        arr_MasterR.append(R)
                        arr_MasterGR.append(GR)
                        arr_MasterCount += 1
                        if csv_players[i].isAI:
                            arr_AIMasterB.append(G)
                            arr_AIMasterR.append(R)
                            arr_AIMasterGR.append(GR)
                            arr_AIMasterCount += 1
                        else:
                            arr_HumanMasterB.append(G)
                            arr_HumanMasterR.append(R)
                            arr_HumanMasterGR.append(GR)
                            arr_HumanMasterCount += 1

                    #print('====================')
  
# print('total_PossibleOptions:', total_PossibleOptions / total_PlayersCount)
# print('total_GameLength:', total_GameLength / total_PlayersCount)
# print('total_PlayersCount:', total_PlayersCount)
# print('total_GR:', total_GR / total_PlayersCount)
# print('====================')

# print('arr_PossibleOptions:', arr_PossibleOptions)
# print('arr_GameLength:', arr_GameLength)
# toPoss = sum(arr_PossibleOptions) / len(arr_PossibleOptions)
# toGame = sum(arr_GameLength) / len(arr_GameLength)
# print('toPoss:', toPoss)
# print('toGame:', toGame)

# toGR = sum(arr_GR) / len(arr_GR)
# print('toGR:', toGR)

toAIPO = sum(arr_AIPO) / len(arr_AIPO)
toAIGL = sum(arr_AIGL) / len(arr_AIGL)
print('toAIPO:', toAIPO)
print('toAIGL:', toAIGL)
toAIGR = sum(arr_AIGR) / len(arr_AIGR)
print('toAIGR:', toAIGR)
print('====================')

toHUPO = sum(arr_HUPO) / len(arr_HUPO)
toHUGL = sum(arr_HUGL) / len(arr_HUGL)
print('toHUPO:', toHUPO)
print('toHUGL:', toHUGL)
toHUGR = sum(arr_HUGR) / len(arr_HUGR)
print('toHUGR:', toHUGR)
print('====================')

toBeginB = sum(arr_BeginB) / len(arr_BeginB)
print('toBeginB:', toBeginB)
toBeginR = sum(arr_BeginR) / len(arr_BeginR)
print('toBeginR:', toBeginR)
toBeginGR = sum(arr_BeginGR) / len(arr_BeginGR)
print('toBeginGR:', toBeginGR)
print('toBeginCount:', arr_BeginCount)
print('====================')

huBeginB = sum(arr_HumanbeginB) / len(arr_HumanbeginB)
print('huBeginB:', huBeginB)
huBeginR = sum(arr_HumanbeginR) / len(arr_HumanbeginR)
print('huBeginR:', huBeginR)
huBeginGR = sum(arr_HumanbeginGR) / len(arr_HumanbeginGR)
print('huBeginGR:', huBeginGR)
print('huBeginCount:', arr_HumanbeginCount)
print('====================')

aiBeginB = sum(arr_AIbeginB) / len(arr_AIbeginB)
print('aiBeginB:', aiBeginB)
aiBeginR = sum(arr_AIbeginR) / len(arr_AIbeginR)
print('aiBeginR:', aiBeginR)
aiBeginGR = sum(arr_AIbeginGR) / len(arr_AIbeginGR)
print('aiBeginGR:', aiBeginGR)
print('aiBeginCount:', arr_AIbeginCount)
print('====================')

toMidB = sum(arr_MidB) / len(arr_MidB)
print('toMidB:', toMidB)
toMidR = sum(arr_MidR) / len(arr_MidR)
print('toMidR:', toMidR)
toMidGR = sum(arr_MidGR) / len(arr_MidGR)
print('toMidGR:', toMidGR)
print('toMidCount:', arr_MidCount)
print('====================')

huMidB = sum(arr_HumanMidB) / len(arr_HumanMidB)
print('huMidB:', huMidB)
huMidR = sum(arr_HumanMidR) / len(arr_HumanMidR)
print('huMidR:', huMidR)
huMidGR = sum(arr_HumanMidGR) / len(arr_HumanMidGR)
print('huMidGR:', huMidGR)
print('huMidCount:', arr_HumanMidCount)
print('====================')

aiMidB = sum(arr_AIMidB) / len(arr_AIMidB)
print('aiMidB:', aiMidB)
aiMidR = sum(arr_AIMidR) / len(arr_AIMidR)
print('aiMidR:', aiMidR)
aiMidGR = sum(arr_AIMidGR) / len(arr_AIMidGR)
print('aiMidGR:', aiMidGR)
print('aiMidCount:', arr_AIMidCount)
print('====================')

toHighB = sum(arr_HighB) / len(arr_HighB)
print('toHighB:', toHighB)
toHighR = sum(arr_HighR) / len(arr_HighR)
print('toHighR:', toHighR)
toHighGR = sum(arr_HighGR) / len(arr_HighGR)
print('toHighGR:', toHighGR)
print('toHighCount:', arr_HighCount)
print('====================')

huHighB = sum(arr_HumanHighB) / len(arr_HumanHighB)
print('huHighB:', huHighB)
huHighR = sum(arr_HumanHighR) / len(arr_HumanHighR)
print('huHighR:', huHighR)
huHighGR = sum(arr_HumanHighGR) / len(arr_HumanHighGR)
print('huHighGR:', huHighGR)
print('huHighCount:', arr_HumanHighCount)
print('====================')

aiHighB = sum(arr_AIHighB) / len(arr_AIHighB)
print('aiHighB:', aiHighB)
aiHighR = sum(arr_AIHighR) / len(arr_AIHighR)
print('aiHighR:', aiHighR)
aiHighGR = sum(arr_AIHighGR) / len(arr_AIHighGR)
print('aiHighGR:', aiHighGR)
print('aiHighCount:', arr_AIHighCount)
print('====================')

toMasterB = sum(arr_MasterB) / len(arr_MasterB)
print('toMasterB:', toMasterB)
toMasterR = sum(arr_MasterR) / len(arr_MasterR)
print('toMasterR:', toMasterR)
toMasterGR = sum(arr_MasterGR) / len(arr_MasterGR)
print('toMasterGR:', toMasterGR)
print('toMasterCount:', arr_MasterCount)
print('====================')

huMasterB = sum(arr_HumanMasterB) / len(arr_HumanMasterB)
print('huMasterB:', huMasterB)
huMasterR = sum(arr_HumanMasterR) / len(arr_HumanMasterR)
print('huMasterR:', huMasterR)
huMasterGR = sum(arr_HumanMasterGR) / len(arr_HumanMasterGR)
print('huMasterGR:', huMasterGR)
print('huMasterCount:', arr_HumanMasterCount)
print('====================')

aiMasterB = sum(arr_AIMasterB) / len(arr_AIMasterB)
print('aiMasterB:', aiMasterB)
aiMasterR = sum(arr_AIMasterR) / len(arr_AIMasterR)
print('aiMasterR:', aiMasterR)
aiMasterGR = sum(arr_AIMasterGR) / len(arr_AIMasterGR)
print('aiMasterGR:', aiMasterGR)
print('aiMasterCount:', arr_AIMasterCount)
print('====================')





