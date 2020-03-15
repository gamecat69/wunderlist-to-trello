# Migrate data from Wunderlist to Trello

Microsoft have bought Wunderlist and announced they will be closing down Wunderlist. The next best alternative - in my opinion - with similar functionality is Trello. Currently there are no free tools available to export data from Wunderlist into Trello, so I built this.

# Instructions

## Clone this repo

``git clone https://github.com/gamecat69/wunderlist-to-trello.git``

##  Install required packages

``pip install -r requirements.txt``
or
``pip3 install -r requirements.txt``
or
``pip3 install requests==2.20.0 && pip3 install urllib3==1.24.2``

## Export data from Wunderlist (if using json method)

**This method is deprecated in favour of the Wunderlist API method**

1. Start an Export, then download zip from here https://export.wunderlist.com/
2. Extract the zip file and place the file Tasks.json in the same folder as this repo.

##  Get a Wunderlist ClientId and Token (if using API method)

1. Login here https://developer.wunderlist.com/apps.
2. Follow the additional link to create an App and get the ClientId and Token.

## Get a Trello API Key and Token

1. Login and get an API Key from here https://trello.com/app-key.
2. Follow the additional link to create an API Token.

## Create the config file

Create a file called config.json by copying and editing config-example.json:
- Add the Trello API Key and Token.
- Add the Wunderlist ClientId Token.
- Specify 'True' / 'False' for SkipCompletedTasks, this will exclude all completed tasks from Wunderlist
- Specify 'True' / 'False' for ArchiveCompletedTasks, this will archive all completed tasks from Wunderlist

*You dont need values for TrelloAPISecret or WunderlistClientSecret for this current version - we may need this later....*

**[todo]**
- Add get_team_members() to trello.py
- Add instructions for getting a Trello team member id and adding to TrelloTeamMemberId in config.json

## Test everything is OK

1. Play around with the code examples:
- example-trello.py
- example-wunderlist.py

## Import data into Trello from Wunderlisst
1. Run main.py

# Import Rules

- Wunderlist list = Trello Board
- Wunderlist task = Trello Card
- Wunderlist task notes = Trello Card description
- Wunderlist tasks comment = Trello Card Action

The destination Trello list is based on the following logic:

- If Wunderlist task is complete: Trello List = 'Done'
- If Wunderlist task is starred and not done: Trello List = 'Doing'
- If Wunderlist tasks is not starred and not done = 'To Do'

If a board of the same name already exists, Wunderlist tasks are imported into the existing board.

## Optional functionality - Assign a team member to starred tasks

In Trello, I like to have all Cards in a 'Doing' list visible in https://trello.com/username/cards.
To do this, all starred Wunderlist items are assigned to my Trello team member id. You can specify your team member Id in config.json in the field **TrelloTeamMemberId**. If you dont want this functionality, leave the value blank
