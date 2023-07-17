import csv

class Player:
    # 設置玩家資料
    def __init__(self, PlayerID, isAI, AI_name, PlayVIP, HandTilemode, Playmode, PlayerMoney):
        self.PlayerID = PlayerID
        self.isAI = isAI
        self.AI_name = AI_name
        self.PlayVIP = PlayVIP
        self.HandTilemode = HandTilemode
        self.Playmode = Playmode
        self.PlayerMoney = PlayerMoney

        # 設置GR值
        self.BranchFactor = 0
        self.Length = 0

        # 清空手牌
        self.hand = []

        # 紀錄
        self.record = {}

    # 寫入手牌
    def Set_hand(self, hand):
        self.hand = hand

    # 此玩家進牌
    def Draw_card(self, card):
        self.hand.append(card)

    # 確認手牌跟進牌後之手牌是否相同
    def Check_hand(self, inputhand):
        if self.hand == inputhand:
            return True
        else:
            return False

    # 此玩家動作後丟牌
    def Self_discard(self, card, csv_index):

        isOk = False
        # 計算GR value
        self.Length += 1
        # 計算手牌種類數量
        self.BranchFactor += CalculateHandTileKindOfPieces(self.hand)

        # 檢查此丟出的牌是否在手牌中
        if card not in self.hand:
            isOk = False
        else:
            self.hand.remove(card)
            isOk = True

        # 紀錄
        GR = []
        GR.append(self.BranchFactor)
        GR.append(self.Length)

        if csv_index not in self.record:
            self.record[csv_index] = GR

        return isOk

    # 其他玩家丟出來的牌，都會動作判定，遊戲長度增加
    def Other_discard(self, csv_index):
        self.Length += 1
        GR = []
        GR.append(self.BranchFactor)
        GR.append(self.Length)

        if csv_index not in self.record:
            self.record[csv_index] = GR

    # 在別人回合碰牌，BranchFactor增加
    def Action_Pong(self, handtiles, csv_index):
        self.BranchFactor += 1

        GR = []
        GR.append(self.BranchFactor)
        GR.append(self.Length)

        if csv_index not in self.record:
            self.record[csv_index] = GR

        # 更新玩家手牌
        self.hand = handtiles

    # 在別人回合槓牌，BranchFactor增加
    def Action_Kong(self, handtiles, csv_index):
        self.BranchFactor += 1
        self.Length += 1

        GR = []
        GR.append(self.BranchFactor)
        GR.append(self.Length)

        if csv_index not in self.record:
            self.record[csv_index] = GR

        # 更新玩家手牌
        self.hand = handtiles

    # 在自己回合暗槓
    def Action_ConcealKong(self, handtiles, csv_index):
        self.Length += 1
        # 自己回合暗槓 計算BranchFactor
        self.BranchFactor += 1

        GR = []
        GR.append(self.BranchFactor)
        GR.append(self.Length)

        if csv_index not in self.record:
            self.record[csv_index] = GR

        # 更新玩家手牌
        self.hand = handtiles

    # 在自己回合加槓
    def Action_AddKong(self, handtiles, csv_index):
        self.Length += 1
        # 自己回合加槓 計算BranchFactor
        self.BranchFactor += 1

        GR = []
        GR.append(self.BranchFactor)
        GR.append(self.Length)

        if csv_index not in self.record:
            self.record[csv_index] = GR

        # 更新玩家手牌
        self.hand = handtiles

    # 胡牌
    def Action_Hu(self, card, csv_index):
        self.BranchFactor += 1
        self.Length += 1

        GR = []
        GR.append(self.BranchFactor)
        GR.append(self.Length)

        if csv_index not in self.record:
            self.record[csv_index] = GR

    def Action_Bankruptcy(self, csv_index):

        if csv_index not in self.record:
            self.record[csv_index] = 'Bankruptcy'


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
