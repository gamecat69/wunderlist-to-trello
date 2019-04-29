#############################
#   Info

#   Register app here: https://developer.wunderlist.com/apps
#   Python Requests documentation: https://2.python-requests.org//en/master/api/#requests.Response
#   API documentation: https://developer.wunderlist.com/documentation

#############################

import json
import codecs
import req

#############################
#   Global variables
#############################

#   Base trello API URL
base = 'https://a.wunderlist.com/api/v1/'

#############################
#   Functions
#############################

def pretty_print(string, length):
    #   Shorten
    string = (string[:length] + '...') if len(string) > length else string

    #   Remove newlines with spaces
    string = string.replace('\n', ' ').replace('\r', '')
    return string

def _get_config(config_file):
    #   Gets config from config.json
    try:
        cfg  = json.load(open(config_file))
        return cfg
    except Exception as e:
        print("[ERR] Cannot get config from %s (%s)" % (config_file, e) )
        quit()

def get_wunderlist_lists_from_json(input_file):

    try:
        tasks = json.load(codecs.open(input_file, 'r', 'utf-8-sig'))
        return tasks
    except Exception as e:
        print("[ERR] Cannot open input file '%s' (%s)" % (input_file, e) )
        quit()

def get_lists():
    #   Returns an Array if board dictionary objects

    response_array_of_dict = []

    #   Get config
    cfg = _get_config('config.json')

    access_token = cfg['WUnderlistClientToken']
    client_id    = cfg['WunderlistClientId']

    # Build out the URL based on the documentation
    url = base + 'lists'

    #   Prepare data to send
    headers   = {'X-Access-Token': access_token, 'X-Client-ID': client_id, 'Content-Type' : 'application/json'}
    arguments = {}
    params    = {}

    r = req.request_json(url, params, arguments, 'get', headers)
    if 'response' in r:
        return r['response']
    else:
        print(r['error'])
        return []

def get_tasks(list_name, completed):
    #   Returns an Array if board dictionary objects

    response_array_of_dict = []

    #   Get config
    cfg = _get_config('config.json')

    access_token = cfg['WUnderlistClientToken']
    client_id    = cfg['WunderlistClientId']

    headers={'X-Access-Token': access_token, 'X-Client-ID': client_id, 'Content-Type' : 'application/json'}

    #   Get lists
    lists = get_lists()

    for list in lists:
        if list['title'] == list_name:
            #print("- Found list id [%d] '%s', getting tasks..." % ( list['id'], list['title'] ) )

            # Build out the URL based on the documentation
            url = base + 'tasks'

            #   Prepare data to send
            headers   = {'X-Access-Token': access_token, 'X-Client-ID': client_id, 'Content-Type' : 'application/json'}
            params    = {'list_id': list['id'], 'completed': completed}
            arguments = {}

            r = req.request_json(url, params, arguments, 'get', headers)
            if 'response' in r:
                return r['response']
            else:
                print(r['error'])
                return []

def get_task_notes(list_name, task_name):
    #   Returns an Array if board dictionary objects

    response_array_of_dict = []

    #   Get config
    cfg = _get_config('config.json')

    access_token = cfg['WUnderlistClientToken']
    client_id    = cfg['WunderlistClientId']

    #   Get lists
    tasks = get_tasks(list_name)

    for task in tasks:
        if task['title'] == task_name:
            #print("- Found task id [%d] '%s', getting notes..." % ( task['id'], task['title'] ) )

            # Build out the URL based on the documentation
            url = base + 'notes'

            #   Prepare data to send
            headers   = {'X-Access-Token': access_token, 'X-Client-ID': client_id, 'Content-Type' : 'application/json'}
            params    = {'task_id': task['id']}
            arguments = {}

            r = req.request_json(url, params, arguments, 'get', headers)
            if 'response' in r:
                return r['response']
            else:
                print(r['error'])
                return []

def get_task_comments(list_name, task_name):
    #   Returns an Array if board dictionary objects

    response_array_of_dict = []

    #   Get config
    cfg = _get_config('config.json')

    access_token = cfg['WUnderlistClientToken']
    client_id    = cfg['WunderlistClientId']

    headers={'X-Access-Token': access_token, 'X-Client-ID': client_id, 'Content-Type' : 'application/json'}

    #   Get lists
    tasks = get_tasks(list_name)

    for task in tasks:
        if task['title'] == task_name:
            #print("- Found task id [%d] '%s', getting comments..." % ( task['id'], task['title'] ) )

            # Build out the URL based on the documentation
            url = base + 'task_comments'

            #   Prepare data to send
            headers   = {'X-Access-Token': access_token, 'X-Client-ID': client_id, 'Content-Type' : 'application/json'}
            params    = {'task_id': task['id']}
            arguments = {}

            r = req.request_json(url, params, arguments, 'get', headers)
            if 'response' in r:
                return r['response']
            else:
                print(r['error'])
                return []

def get_task_comments_by_id(task_id):
    #   Returns an Array if board dictionary objects

    response_array_of_dict = []

    #   Get config
    cfg = _get_config('config.json')

    access_token = cfg['WUnderlistClientToken']
    client_id    = cfg['WunderlistClientId']

    # Build out the URL based on the documentation
    url = base + 'task_comments'

    #   Prepare data to send
    headers   = {'X-Access-Token': access_token, 'X-Client-ID': client_id, 'Content-Type' : 'application/json'}
    params    = {'task_id': task_id}
    arguments = {}

    r = req.request_json(url, params, arguments, 'get', headers)
    if 'response' in r:
        return r['response']
    else:
        print(r['error'])
        return []

def get_task_notes_by_id(task_id):
    #   Returns an Array if board dictionary objects

    response_array_of_dict = []

    #   Get config
    cfg = _get_config('config.json')

    access_token = cfg['WUnderlistClientToken']
    client_id    = cfg['WunderlistClientId']

    # Build out the URL based on the documentation
    url = base + 'notes'

    #   Prepare data to send
    headers   = {'X-Access-Token': access_token, 'X-Client-ID': client_id, 'Content-Type' : 'application/json'}
    params    = {'task_id': task_id}
    arguments = {}

    r = req.request_json(url, params, arguments, 'get', headers)
    if 'response' in r:
        return r['response']
    else:
        print(r['error'])
        return []

def get_tasks_by_id(list_id, completed):
    #   Returns an Array if board dictionary objects

    #   Get config
    cfg = _get_config('config.json')

    access_token = cfg['WUnderlistClientToken']
    client_id    = cfg['WunderlistClientId']

    # Build out the URL based on the documentation
    url = base + 'tasks'

    #   Prepare data to send
    headers   = {'X-Access-Token': access_token, 'X-Client-ID': client_id, 'Content-Type' : 'application/json'}
    params    = {'list_id': list_id, 'completed': completed}
    arguments = {}

    r = req.request_json(url, params, arguments, 'get', headers)
    if 'response' in r:
        return r['response']
    else:
        print(r['error'])
        return []
