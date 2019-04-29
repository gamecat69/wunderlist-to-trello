
#############################
#   Info

#   Get an API Key: https://trello.com/1/appKey/generate
#   Original project: https://github.com/bmccormack/trello-python-demo
#   Python Requests documentation: https://2.python-requests.org//en/master/api/#requests.Response
#   Trello API documentation: https://developers.trello.com/reference#listsidcards

#############################

import req
import json

#############################
#   Global variables
#############################

#   Base trello API URL
base = 'https://trello.com/1/'

#############################
#   Functions
#############################

def _get_config(config_file):
    #   Gets config from config.json
    try:
        cfg  = json.load(open(config_file))
        return cfg
    except Exception as e:
        print("[ERR] Cannot get config from %s (%s)" % (config_file, e) )
        quit()

def get_boards():

    #   Returns an Array of board dictionary objects

    #   Get config
    cfg = _get_config('config.json')
    params_key_and_token = {'key':cfg["TrelloAPIKey"],'token':cfg["TrelloAPIToken"]}

    # Build out the URL based on the documentation
    url = base + 'members/me/boards'

    #   Populate any required arguments
    arguments = {}
    headers   = {}

    #   Call the Trello API, passing params and arguments
    #   The Trello API returns an array of dicts
    r = req.request_json(url, params_key_and_token, arguments, 'get', headers)
    if 'response' in r:
        return r['response']
    else:
        print(r['error'])
        return []

def get_lists(board_name):
    #   Returns the lists associated with a board
    #print("Getting lists for board: %s" % (board_name) )

    board_found = 0

    #   Get config
    cfg = _get_config('config.json')
    params_key_and_token = {'key':cfg["TrelloAPIKey"],'token':cfg["TrelloAPIToken"]}

    #   Get the board ID
    #   Get boards
    boards = get_boards()

    for board in boards:
        if board['name'] == board_name:

            board_found = 1

            # Build out the URL based on the documentation
            url = base + '/boards/' + board['id'] + '/lists'

            #   Populate any required arguments
            arguments = {}
            headers   = {}

            #   Call the Trello API, passing params and arguments
            #   The Trello API returns an array of dicts
            r = req.request_json(url, params_key_and_token, arguments, 'get', headers)
            if 'response' in r:
                return r['response']
            else:
                print(r['error'])
                return []

    if not board_found:
        print("[ERR] Board '%s' not found" % board_name)
        return []

def get_cards(board_name, list_name):

    board_found = 0
    list_found  = 0

    cfg = _get_config('config.json')
    params_key_and_token = {'key':cfg["TrelloAPIKey"],'token':cfg["TrelloAPIToken"]}

    boards = get_boards()

    for board in boards:
      if board['name'] == board_name:

          board_found = 1

          #   Get lists
          lists = get_lists(board_name)
          for list in lists:
              if list['name'] == list_name:

                list_found  = 1

                #   Build URL
                url = base + '/lists/' + list['id'] + '/cards'

                # Define arguments
                arguments = {}
                headers   = {}

                #   Call the Trello API, passing params and arguments
                #   The Trello API returns an array of dicts
                r = req.request_json(url, params_key_and_token, arguments, 'get', headers)
                if 'response' in r:
                    return r['response']
                else:
                    print(r['error'])
                    return []

    if not board_found:
        print("[ERR] Board '%s' not found" % board_name)
        return []

    if not list_found:
        print("[ERR] List '%s' not found" % list_name)
        return []

def get_card_actions(board_name, list_name, card_name):

    card_found = 0

    cfg = _get_config('config.json')
    params_key_and_token = {'key':cfg["TrelloAPIKey"],'token':cfg["TrelloAPIToken"]}

    cards = get_cards(board_name, list_name)
    for card in cards:
        if card['name'] == card_name:

            card_found = 1

            url = base + '/cards/' + card['id'] + '/actions'

            #   Call the Trello API, passing params and arguments
            arguments = {}
            headers   = {}

            #   Call the Trello API, passing params and arguments
            #   The Trello API returns an array of dicts
            r = req.request_json(url, params_key_and_token, arguments, 'get', headers)
            if 'response' in r:
                return r['response']
            else:
                print(r['error'])
                return []

    if not card_found:
        print("[ERR] Card '%s' not found" % card_name)
        return []

def create_board(board_name, description):

    #   Get config
    cfg = _get_config('config.json')
    params_key_and_token = {'key':cfg["TrelloAPIKey"],'token':cfg["TrelloAPIToken"]}

    boards = get_boards()

    for board in boards:
      if board['name'] == board_name:
          #print("[ERR] Board '%s' already exists" % board_name)
          return 2

    arguments = {'name': board_name, 'desc': description }
    headers   = {}

    url = base + 'boards'

    #   Call the Trello API, passing params and arguments
    #   The Trello API returns an array of dicts
    r = req.request_json(url, params_key_and_token, arguments, 'post', headers)
    if 'response' in r:
        return 0
    else:
        print(r['error'])
        return 1

def create_list(board_name, list_name):
    #   Creates a new card in a given board

    #   Get config
    cfg = _get_config('config.json')
    params_key_and_token = {'key':cfg["TrelloAPIKey"],'token':cfg["TrelloAPIToken"]}

    board_found = 0

    boards = get_boards()

    for board in boards:
        if board['name'] == board_name:

            board_found = 1

            lists = get_lists(board_name)

            #   Check if list already exists
            if len(lists) > 0:
                for list in lists:
                    if list['name'] == list_name:
                        #print("[ERR] List '%s' already exists in board '%s'" % (list['name'],board['name']) )
                        return 2

            #   Build the new list data dict object
            arguments = {'name': list_name, 'pos': 0, 'idBoard': board['id'] }
            headers   = {}

            #   Build URL
            url = base + 'lists'

            #   Call the Trello API, passing params and arguments
            #   The Trello API returns an array of dicts
            r = req.request_json(url, params_key_and_token, arguments, 'post', headers)
            if 'response' in r:
                return 0
            else:
                print(r['error'])
                return 1

    if not board_found:
        print("[ERR] Board '%s' not found" % (board_name) )
        return 1

def create_card(board_name, list_name, card_name, card_description, card_members, closed):
    #   Creates a new card in a given board
    #print("\nCreating card: %s in board: %s, list: %s. Description: %s" % (card_name, list_name, board_name, card_description) )

    #   Get config
    cfg = _get_config('config.json')
    params_key_and_token = {'key':cfg["TrelloAPIKey"],'token':cfg["TrelloAPIToken"]}

    rc = {}
    list_found  = 0

    #   Get lists
    lists = get_lists(board_name)

    #   Quit if no lists returned
    if len(lists) < 1:
        print("[ERR] No list called %s found in board %s" % (list_name, board_name) )
        return 1

    for list in lists:
        if list['name'] == list_name:
            list_found  = 1
            #print("Found List: [%s] %s" % (list['id'], list['name']))

            cards = get_cards(board_name, list_name)
            for card in cards:
                #print("\nCard: %s. Closed: %s\n" % (card['name'], card['closed']) )
                if card['name'] == card_name:
                    #print("[ERR] Card '%s' already exists in list '%s'" % (card_name, list_name) )
                    rc['code'] = 2
                    return rc

            #   Build the new list data dict object
            arguments = {'name': card_name, 'desc': card_description, 'pos': "top", 'idList': list['id'], 'idMembers': card_members, 'closed': closed}
            headers   = {}

            #   Build URL
            url = base + 'cards'

            #   Call the Trello API, passing params and arguments
            #   The Trello API returns an array of dicts
            r = req.request_json(url, params_key_and_token, arguments, 'post', headers)
            if 'response' in r:
                card_dict = r['response']
                rc['code'] = 0
                rc['id'] = card_dict['id']
                return rc
            else:
                print(r['error'])
                rc['code'] = 1
                return rc

    if not list_found:
        print("[ERR] List '%s' not found" % (list_name) )
        rc['code'] = 1
        return rc

def create_card_comment(board_name, list_name, card_name, comment):

    cfg = _get_config('config.json')
    params_key_and_token = {'key':cfg["TrelloAPIKey"],'token':cfg["TrelloAPIToken"]}

    card_found  = 0
    rc = {}
    cards = get_cards(board_name, list_name)

    #   Quit if no cards returned
    if len(cards) < 1:
        print("[ERR] No card called '%s' found in list '%s' in board '%s'" % (card_name, list_name, board_name) )
        return 1

    for card in cards:
        if card['name'] == card_name:

            card_found  = 1

            #   Build the new list data dict object
            arguments = {'text': comment}
            headers   = {}

            #   Build URL
            url = base + '/cards/' + card['id'] + '/actions/comments'

            #   Call the Trello API, passing params and arguments
            #   The Trello API returns an array of dicts
            r = req.request_json(url, params_key_and_token, arguments, 'post', headers)
            if 'response' in r:
                resp_dict = r['response']
                rc['code'] = 0
                rc['id'] = resp_dict['id']
                return rc
            else:
                print(r['error'])
                rc['code'] = 1
                return rc

    if not card_found:
        print("[ERR] Card '%s' not found" % (card_name) )
        rc['code'] = 1
        return rc

def archive_card_by_id(card_id):
    #   Archives a card given a card id
    #   in Trello Archiving sets 'Closed' to 'true'

    #   Get config
    cfg = _get_config('config.json')
    params_key_and_token = {'key':cfg["TrelloAPIKey"],'token':cfg["TrelloAPIToken"]}

    rc = {}

    #   Build the new list data dict object
    arguments = {'id': card_id, 'closed': 'true'}
    headers   = {}

    #   Build URL
    url = base + 'cards/' + card_id

    #   Call the Trello API, passing params and arguments
    #   The Trello API returns an array of dicts
    r = req.request_json(url, params_key_and_token, arguments, 'put', headers)
    if 'response' in r:
        resp_dict = r['response']
        rc['code'] = 0
        rc['id'] = resp_dict['id']
        return rc
    else:
        print(r['error'])
        rc['code'] = 1
        return rc
