import player
import parse
import os
# handtile = ['A1', 'A2', 'A2', 'A5', 'A7', 'A8', 'A8', 'A9', 'B3', 'B4', 'B6', 'B6', 'B9']
# ans = player.CalculateHandTileKindOfPieces(handtile)
# print(ans)

# dealtile = '[ "A1" ]'
# dealtile = '[ "C7", "BeforeHu", [ "ASSIGN_DR", "MAIN_SUIT" ], true ]'
# Deal = parse.parseDeal(dealtile)
# print(Deal)


#discardtile = '[ "B5", [ ] ]'
# discardtile = '[ "C3", [ "C9", "DR", "C5" ] ]'
# Discard, is_notempty = parse.parseDiscard(discardtile)
# print(Discard, is_notempty)

# hand = '[ "DR", "DR", "B1", "B1", "B1", "B3", "B3", "B3", "B4", "C8", "C9", "C3", "C6" ]'
# handtile = parse.parseHandTile(hand)
# typestile = parse.CalculateHandTileKindOfPieces(handtile)
# hand_dict = {}
# for tile in handtile:
#     if tile not in hand_dict:
#         hand_dict[tile] = 1
#     else:
#         hand_dict[tile] += 1
# print(hand_dict)
# print(typestile)

# main_folder_path = 'Mining'
# for root, dirs, files in os.walk(main_folder_path):
#     print("root: ", root)
#     print("dirs: ", dirs)
#     print("files: ", files)
#     for filename in files:
#         if filename.endswith('.csv'):
#             file_path = os.path.join(root, filename)
            
#             # 開啟CSV檔案
#             with open(file_path, 'r') as file:
#                 # 在這裡進行檔案的分析與處理
#                 # 您可以將處理檔案的程式碼寫在這個區塊中
#                 pass  # 在這裡暫時使用 pass 作為示例，代表什麼都不做

begindeal = '[ 3, "QING_YI_SE_23", { "$numberLong" : "664000" } ]'
isAI, Mode, Handmode, Money = parse.parseBeginDeal(begindeal)
print(isAI, Mode, Handmode, Money)