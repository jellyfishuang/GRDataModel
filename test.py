import player
import parse

# handtile = ['A1', 'A2', 'A2', 'A5', 'A7', 'A8', 'A8', 'A9', 'B3', 'B4', 'B6', 'B6', 'B9']
# ans = player.CalculateHandTileKindOfPieces(handtile)
# print(ans)

# dealtile = '[ "A1" ]'
# dealtile = '[ "C7", "BeforeHu", [ "ASSIGN_DR", "MAIN_SUIT" ], true ]'
# Deal = parse.parseDeal(dealtile)
# print(Deal)


#discardtile = '[ "B5", [ ] ]'
discardtile = '[ "C3", [ "C9", "DR", "C5" ] ]'
Discard, is_notempty = parse.parseDiscard(discardtile)
print(Discard, is_notempty)

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
