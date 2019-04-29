import req
import json

def _get_config(config_file):
    #   Gets config from config.json
    try:
        cfg  = json.load(open(config_file))
        return cfg
    except Exception as e:
        print("[ERR] Cannot get config from %s (%s)" % (config_file, e) )
        quit()

def get_test():

    base = 'https://trello.com/1/'

    #   Get config
    cfg = _get_config('config.json')

    #   Build out params
    params_key_and_token = {'key':cfg["TrelloAPIKey"],'token':cfg["TrelloAPIToken"]}
    url                  = base + 'members/me/boards'
    arguments            = {}

    #   get the URL
    r = req.request_json(url, params_key_and_token, arguments, 'get')
    if 'response' in r:
        print(r['response'])
    else:
        print(r['error'])

def post_test():

    base = 'https://trello.com/1/'

    #   Get config
    cfg = _get_config('config.json')

    #   Build out params
    params_key_and_token = {'key':cfg["TrelloAPIKey"],'token':cfg["TrelloAPIToken"]}
    url                  = base + 'boards'
    arguments            = {'name': 'Test Board2', 'desc': 'test description' }

    #   get the URL
    r = req.request_json(url, params_key_and_token, arguments, 'post')
    if 'response' in r:
        print(r['response'])
    else:
        print(r['error'])

get_test()
#post_test()
