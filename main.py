import trello
import wunderlist
import json

#############################
#   Functions
#############################

def _get_config(config_file):
    #   Gets config from config.json
    try:
        cfg  = json.load(open(config_file))
        return cfg
    except Exception as e:
        print("     [ERR] Cannot get config from %s (%s)" % (config_file, e) )
        quit()

def process_wunderlist_list(list, test_mode):

    trello_board = list['title']

    if test_mode == 'True':
        ##  Add for easy cleanup
        trello_board = 'Test Board'

    print("Creating a new board '%s'" % (trello_board) )
    #   Note, this automatically creates 'To Do' 'Doing' 'Done' Lists
    rc = trello.create_board(trello_board, 'Wunderlist List Id: ' + str(list['id']))
    if rc == 2:
        print("     [ERR] already exists")
    elif rc != 0:
        print("Error")

    #   Get NON COMPLETE tasks
    print("Getting active tasks...")
    tasks = wunderlist.get_tasks_by_id(list['id'], False)

    #   Check if completed tasks should be skipped
    if cfg['SkipCompletedTasks'] == 'True':
        print("Skipping completed tasks")
    else:
        #   Get COMPLETE tasks
        print("Getting completed tasks...")
        c_tasks = wunderlist.get_tasks_by_id(list['id'], True)
        tasks = (tasks + c_tasks)

    for task in tasks:

        #print(task)

        trello_assigned_team_member = ''
        trello_card = task['title']

        #print("\n [TASK] %s (Completed: %s) (Starred: %s)" % (trello_card, task['completed'], task['starred']) )

        if str(task['completed']) == 'True':
            trello_list = 'Done'
        else:
            if str(task['starred']) == 'True':
                #   Starred not completed = Doing
                trello_list = 'Doing'
                trello_assigned_team_member = cfg['TrelloTeamMemberId']
            else:
                #   Not starred not completed = To Do
                trello_list = 'To Do'

        #   Add wunderlist notes to the trello card description
        #   Need new code here

        notes = wunderlist.get_task_notes_by_id(task['id'])

        card_desc = ''
        if len(notes) > 0:
            for note in notes:
                if 'content' in note:
                    if note['content'] != "\n" and len(note['content']) > 0:
                        #print("Adding note to card: %s" % (note['content']))
                        card_desc = card_desc + note['content']
            # if notes[0]['content'] != '\n':
            #     card_desc = notes[0]['content']
            #     #print("     [Notes] %s" % (card_desc) )

        #   Create Trello Card
        closed = "false"
        print("Creating card '%s'" % (trello_card) )
        rc = trello.create_card(trello_board, trello_list, trello_card, card_desc, trello_assigned_team_member, closed)
        if rc['code'] == 2:
            print("     [ERR] already exists")
        elif rc['code'] != 0:
            print("Error")
        else:
            new_card_id = rc['id']

        #   Add comments as Trello actions
        #   Skip if Error 2 above to avoid duplicate actions
        if rc['code'] != 2:
            #print(task)
            comments = wunderlist.get_task_comments_by_id(task['id'])
            for comment in comments:
                if 'text' in comment:
                    commentString = "(From " + comment['author']['name'] + "): " + comment['text']

                    #print("     [COMMENT] %s)" % (comment['text']) )
                    print("     Adding action to [%s][%s][%s]" % (trello_board, trello_list, trello_card) )
                    #rc = trello.create_card_comment(trello_board, trello_list, trello_card, comment['text'])

                    #   Added for issue #3 from Github
                    rc = trello.create_card_comment(trello_board, trello_list, trello_card, commentString)
                    if rc['code'] != 0:
                        print("     [ERR] %s" % rc['error'])

            if cfg['ArchiveCompletedTasks'] == 'True' and trello_list == 'Done':
                print("     Archiving card '%s'" % (trello_card))
                trello.archive_card_by_id(new_card_id)

def process_wunderlist_list_from_json(list, test_mode):

    trello_board = list['title']

    if test_mode == 'True':
        ##  Add for easy cleanup
        trello_board = 'Test Board'

    print("Creating a new board '%s'" % (trello_board) )
    #   Note, this automatically creates 'To Do' 'Doing' 'Done' Lists
    rc = trello.create_board(trello_board, 'Wunderlist List Id: ' + str(list['id']))
    if rc == 2:
        print("     [ERR] already exists")
    elif rc != 0:
        print("Error")

    #   Cycle through tasks
    for task in list['tasks']:

        trello_assigned_team_member = ''
        trello_card = task['title']

        if cfg['SkipCompletedTasks'] == 'True' and str(task['completed']) == 'True':
            print("Skipping completed task '%s'" % task['title'])
        else:

            #print("\n [TASK] %s (Completed: %s) (Starred: %s)" % (trello_card, task['completed'], task['starred']) )

            if str(task['completed']) == 'True':
                trello_list = 'Done'
            else:
                if str(task['starred']) == 'True':
                    #   Starred not completed = Doing
                    trello_list = 'Doing'
                    trello_assigned_team_member = cfg['TrelloTeamMemberId']
                else:
                    #   Not starred not completed = To Do
                    trello_list = 'To Do'

            #   Add wunderlist notes to the trello card description
            if len(task['notes']) > 0:
                if task['notes'][0]['content'] != '\n':
                    card_desc = task['notes'][0]['content']
                    #print("     [Notes] %s" % (card_desc) )
            else:
                card_desc = ''

            #   Create Trello Card
            closed = "false"
            print("Creating card '%s'" % (trello_card) )
            rc = trello.create_card(trello_board, trello_list, trello_card, card_desc, trello_assigned_team_member, closed)
            if rc['code'] == 2:
                print("     [ERR] already exists")
            elif rc['code'] != 0:
                print("Error")
            else:
                new_card_id = rc['id']

            #   Add comments as Trello actions
            #   Skip if Error 2 above to avoid duplicate actions
            if rc['code'] != 2:
                for comment in task['comments']:
                    #print("     [COMMENT] %s)" % (comment['text']) )
                    print("     Adding action to [%s][%s][%s]" % (trello_board, trello_list, trello_card) )
                    rc = trello.create_card_comment(trello_board, trello_list, trello_card, comment['text'])
                    if rc['code'] != 0:
                        print("Error")

                if cfg['ArchiveCompletedTasks'] == 'True' and trello_list == 'Done':
                    print("Archiving card '%s'" % (trello_card))
                    rc = trello.archive_card_by_id(new_card_id)
                    if rc['code'] != 0:
                        print("Error")

################################################################
#   Example 1: Get data from Wunderlist API, push to Trello
################################################################

#   Get Config
cfg = _get_config('config.json')

#   Generate a frozenset of excluded lists in lower case
excluded_lists = ( a.strip() for a in cfg['ExcludedLists'].lower().split(",") )
excluded_lists = frozenset(excluded_lists)

print("Gettings lists from Wunderlist API")
lists = wunderlist.get_lists()

for list in lists:

    print("\n ===================================================")
    print("\n[LIST] %s" % (list['title']) )

    #  Skip if list is excluded
    if list['title'].lower() in excluded_lists:
        print("- Skipping excluded list: %s" % list['title'])
    else:
        #   test_mode always pushes to a Trello board named 'Test Board'
        print("Processing list from Wunderlist API...")
        process_wunderlist_list(list=list, test_mode='False')

quit()

# ###################################################################
# #   Example 2: Get data from Wunderlist json export, push to Trello
# ###################################################################
#
# #   Get Config
# cfg = _get_config('config.json')
#
# #   Sets the Trello board name to "Test Board" for easy cleanup
# test_mode = 'True'
#
# #   Generate a frozenset of excluded lists in lower case
# excluded_lists = ( a.strip() for a in cfg['ExcludedLists'].lower().split(",") )
# excluded_lists = frozenset(excluded_lists)
#
# #   Get data from Wunder list export file
# lists = wunderlist.get_wunderlist_lists_from_json(cfg['WunderlistExport'])
#
# #   Cycle through data (Lists, Tasks)
# for list in lists:
#
#     print("\n ===================================================")
#     print("\n[LIST] %s" % (list['title']) )
#
#     #  Skip if list is excluded
#     if list['title'].lower() in excluded_lists:
#         print("- Skipping excluded list: %s" % list['title'])
#     else:
#         #   test_mode always pushes to a Trello board named 'Test Board'
#         print("Processing list from json export...")
#         process_wunderlist_list_from_json(list=list, test_mode=test_mode)
