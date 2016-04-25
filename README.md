# jira-transition-times

## Getting JIRA transition times

For getting the transition time between two states for a list of JIRA tickets the 'time-between.py' script can be used. Given a created and publicly shared JIRA filter the script will look up and calculate the transition time between the default states In Progress and Done for all tickets that is returned by the filter query. 

### Adopt script to match your settings: 
* Which states to get data for
* JIRA API endpoint

### Run
```
$ python time-between.py -u <username> -p <password> <Public JIRA filter id>
```

Running the script will return a semi-colon delimited list of issues with the calculated transition time.

```
$ python time-between.py -u <username> -p <password> <Public JIRA filter id>
TICKET-1284;https://jira.installation.com/rest/api/2/issue/210113;1 day, 3:52:41
TICKET-1264;https://jira.installation.com/rest/api/2/issue/209537;2 days, 23:02:14
TICKET-1262;https://jira.installation.com/rest/api/2/issue/209426;8 days, 1:45:05
TICKET-1250;https://jira.installation.com/rest/api/2/issue/209253;0:00:30
TICKET-1230;https://jira.installation.com/rest/api/2/issue/208740;5 days, 17:33:45
TICKET-1207;https://jira.installation.com/rest/api/2/issue/200700;0:00:00
TICKET-1188;https://jira.installation.com/rest/api/2/issue/205938;1 day, 2:03:28
TICKET-1182;https://jira.installation.com/rest/api/2/issue/203009;27 days, 21:40:03
TICKET-1167;https://jira.installation.com/rest/api/2/issue/203244;21:47:0
```

## Dependencies
```
$ pip install requests
```
