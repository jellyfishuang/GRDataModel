import parse

class IGSPlayer:
    # set player's info
    def __init__(self, startcheck_str, begindeal_str, roomid, playerid, playeridx):
        self.roomID = roomid
        self.gameType = None
        self.gameLevel = None
        self.playerID = playerid
        self.playerIdx = playeridx
        self.isAI = False
        self.AIVIP = None # is AI: AI's name, not AI: real player's VIP
        self.handType = None
        self.haveMoney = -1

        self.hand = []
        self.typeshand = -1
        self.selectLack = None
        self.branchFactor = 0
        self.gameLength = 0
        self.afterHu = False
        self.isBankruptcy = False
        self.changeTilelog = []

        csv_playmode, csv_level, _, _ = parse.parseStartCheck(startcheck_str)
        self.gameType = csv_playmode
        self.gameLevel = csv_level

        isAI, Mode, Handmode, Money = parse.parseBeginDeal(begindeal_str)
        self.isAI = isAI
        self.AIVIP = Mode
        self.handType = Handmode
        self.haveMoney = Money
        
    # set player's hand and calculate hand's type
    def set_Hand(self, hand_str):
        self.hand = parse.parseHandTile(hand_str)
        self.typeshand = parse.CalculateHandTileKindOfPieces(self.hand)

    # set player's select lack
    def set_SelectLack(self, selectLack_str):
        self.selectLack = selectLack_str

    def set_ChangeTilelog(self, changeTilelog_str):
        self.changeTilelog.append(changeTilelog_str)

    # if one player discards tile, all player must add 1 to gameLength
    def add_GameLength(self):
        self.gameLength += 1

    # to the player who discard tile, add the value of calculating to branchFactor
    def action_Discard(self, discard_str, hand_str):
        self.hand = parse.parseHandTile(hand_str)
        self.typeshand = parse.CalculateHandTileKindOfPieces(self.hand)

        discard, is_notempty = parse.parseDiscard(discard_str)

        # if the player is in Ting, the player's branchFactor must have 1 (聽牌情況下只為一個分支)
        if is_notempty and not self.afterHu:
            self.branchFactor += 1
        # if the player is not in Ting, the player's branchFactor must have the value of calculating of hand's type
        elif not is_notempty and not self.afterHu:
            # add the tile of discard to hand, and calculate the value of calculating of hand's type
            before_hand = self.hand.copy()
            before_hand.append(discard)
            valueofhand = parse.CalculateHandTileKindOfPieces(before_hand)
            self.branchFactor += valueofhand

    # the player who do the action of Chi, Pong, Kong, Hu, the player's branchFactor must have add 1
    def action_pongkong(self):
        self.branchFactor += 1

    def action_hu(self):
        self.branchFactor += 1
        self.afterHu = True

    def action_bankruptcy(self):
        self.isBankruptcy = True

    def print_Player(self):
        print('roomID:', self.roomID)
        print('gameType:', self.gameType)
        print('gameLevel:', self.gameLevel)
        print('playerID:', self.playerID)
        print('playerIdx:', self.playerIdx)
        print('isAI:', self.isAI)
        print('AIVIP:', self.AIVIP)
        print('handType:', self.handType)
        print('haveMoney:', self.haveMoney)
        print('selectLack:', self.selectLack)
        print('branchFactor:', self.branchFactor)
        print('gameLength:', self.gameLength)
        print('isBankruptcy:', self.isBankruptcy)
        print('changeTilelog:', self.changeTilelog)

    def print_GR(self):
        print('branchFactor:', self.branchFactor)
        print('gameLength:', self.gameLength)



