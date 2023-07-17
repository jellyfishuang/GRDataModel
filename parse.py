def parseStartCheck (_string):
    # [ "Joker4", "Beginner", 2000, 32 ]
    cleaned_data = _string.strip("[] ")
    data_list = cleaned_data.split(", ")
    username = data_list[0].strip('"')
    level = data_list[1].strip('"')
    score1 = int(data_list[2])
    score2 = int(data_list[3])
    return username, level, score1, score2

def parseBeginDeal (_string):
    # [ "AI_0", "QING_YI_SE_20", 910000.0 ]
    # [ 4, "QING_YI_SE_10", 2031000.0 ]
    cleaned_data = _string.strip("[] ")
    data_list = cleaned_data.split(", ")
    isAI = True
    if data_list[0].isdigit():
        isAI = False
        playerVIP = int(data_list[0])
        playerHandmodeID = data_list[1].strip('"')
        playerMoney = float(data_list[2])
        return isAI, playerVIP, playerHandmodeID, playerMoney
    else:
        AI_Mode = data_list[0].strip('"')
        playerHandmode = data_list[1].strip('"')
        playerMoney = float(data_list[2])
        return isAI, AI_Mode, playerHandmode, playerMoney
    
def parseHandTile (_string):
    # [ "DR", "A1", "A2", "A3", "A4", "A4", "A4", "A6", "A6", "A6", "A7", "A7", "A9", "A1" ]
    cleaned_data = _string.strip("[] ")
    data_list = cleaned_data.split(", ")
    # delete " "
    for i in range(len(data_list)):
        data_list[i] = data_list[i].strip('"')

    return data_list

def parseDeal(_string):
    # [ "A1" ]
    # [ "C7", "BeforeHu", [ "ASSIGN_DR", "MAIN_SUIT" ], true ]
    cleaned_data = _string.strip("[] ")
    data_list = cleaned_data.split(", ")
    
    # 刪除前後的引號
    for i in range(len(data_list)):
        data_list[i] = data_list[i].strip('"')

    # 提取最前面的那張牌
    if len(data_list) > 0:
        first_card = data_list[0]
    else:
        first_card = None
    
    return first_card

def parseDiscard(_string):
    # [ "B5", [ ] ]
    # [ "C3", [ "C9", "DR", "C5" ] ]

    cleaned_data = _string.strip("[] ")
    data_list = cleaned_data.split(", ")
    
    # 刪除前後的引號
    card = data_list[0].strip('"').rstrip(',')
    
    # 檢查是否有第二個元素並且不為空列表
    is_empty = len(data_list) > 1 and data_list[1].strip("[] ") != ''
        
    # 移除多餘的引號
    if card.endswith('"'):
        card = card[:-1]
    if card.startswith('"'):
        card = card[1:]
    
    return card, is_empty

def CalculateHandTileKindOfPieces(_handtiles):
    # ex: ['A1', 'A2', 'A2', 'A5', 'A7', 'A8', 'A8', 'A9', 'B3', 'B4', 'B6', 'B6', 'B9']
    # return : 10

    # 計算手牌種類數量
    Hand_dict = {}
    for tile in _handtiles:
        if tile not in Hand_dict:
            Hand_dict[tile] = 1
        else:
            Hand_dict[tile] += 1

    return len(Hand_dict)
