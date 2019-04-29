import wunderlist

##  ------------------------------------------------
##  Example: Print all list data
##  ------------------------------------------------

lists = wunderlist.get_lists()

for list in lists:
    print("\n ===================================================")
    print("\n[LIST] %s" % (list['title']) )

    tasks = wunderlist.get_tasks_by_id(list['id'], False)
    #tasks = wunderlist.get_tasks(list['title'], False)

    for task in tasks:
        print("\n   [TASK] %s" % (task['title']) )

        notes = wunderlist.get_task_notes_by_id(task['id'])

        for note in notes:

            if len(notes) > 0:
                for note in notes:
                    if 'content' in note:
                        if note['content'] != "\n" and len(note['content']) > 0:
                            #   Shorten note for printing to console
                            c = wunderlist.pretty_print(note['content'], 35)
                            print("       [NOTE] %s" % (c) )

            comments = wunderlist.get_task_comments_by_id(task['id'])

            for comment in comments:
                #   Shorten comment for printing to console
                c = wunderlist.pretty_print(comment['text'], 35)
                print("       [COMMENT] %s" % (c) )
