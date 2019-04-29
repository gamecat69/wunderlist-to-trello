import trello

##  ------------------------------------------------
##  Example: Print all active boards->lists->cards
##  ------------------------------------------------

# print("\nGetting boards and lists...")
# boards = trello.get_boards()
# for board in boards:
#     if board['closed'] == True:
#         continue
#     else:
#         print("\n[%s] %s" % ('BOARD', board['name']))
#         lists = trello.get_lists(board['name'])
#         for list in lists:
#             if list['closed'] == True:
#                 continue
#             else:
#                 print("\n     [%s] %s" % ('LIST', list['name']))
#                 cards = trello.get_cards(board['name'], list['name'])
#                 for card in cards:
#                     if card['closed'] == "True2":
#                         continue
#                     else:
#                         print("         [%s] %s (Members: %s)" % ('CARD', card['name'], card['idMembers']))
#                         actions = trello.get_card_actions(board['name'], list['name'], card['name'])
#                         for action in actions:
#                             #print(action)
#                             if action['type'] == 'commentCard':
#                                 print("             [%s] (%s) : %s" % ('COMMENT', action['date'], action['data']['text']))

# ##  ------------------------------------------------
# ##  Example: Create a board
# ##  ------------------------------------------------
#
# board_name  = 'Test Board'
# description = 'New cool board :fist:'
#
# print("Creating a new board '%s'" % (board_name) )
# rc = trello.create_board(board_name, description)
#
# if rc == 0:
#     print("Created OK")
# elif rc == 2:
#     print("Error: already exists")
# else:
#     print("Error")
#
# ##  ------------------------------------------------
# ##  Example: Create a list in a board
# ##  ------------------------------------------------
#
# board_name = 'Test Board'
# list_name  = 'Ideas'
#
# print("\nCreating list: '%s' in board: '%s'" % (list_name, board_name) )
# rc = trello.create_list(board_name, list_name)
#
# if rc == 0:
#     print("Created OK")
# elif rc == 2:
#     print("Error: already exists")
# else:
#     print("Error")
#
# ##  ------------------------------------------------
# ##  Example: Create a card in a list
# ##  ------------------------------------------------
#
# board_name   = 'Test Board'
# list_name    = 'Ideas'
# card_name    = 'Test card'
# card_desc    = 'I made this card using the Trello API :fist:\nAnd this is a second line!'
# card_members = '54ded949cc085aa06375182a'
#
# print("\nCreating card: '%s' in list: '%s', in board '%s'" % (card_name, list_name, board_name) )
# rc = trello.create_card(board_name, list_name, card_name, card_desc, card_members)
#
# if rc == 0:
#     print("Created OK")
# elif rc == 2:
#     print("Error: already exists")
# else:
#     print("Error")
#
# ##  ------------------------------------------------
# ##  Example: Create a comment in a card
# ##  ------------------------------------------------
#
# board_name = 'Test Board'
# list_name  = 'Ideas'
# card_name  = 'Test card'
# comment    = 'Awesome comment! :thumbsup:'
#
# print("\nCreating Comment in card: '%s' in list: '%s', in board '%s'" % (card_name, list_name, board_name) )
# rc = trello.create_card_comment(board_name, list_name, card_name, comment)
# if rc == 0:
#     print("Created OK")
# elif rc == 2:
#     print("Error: already exists")
# else:
#     print("Error")
