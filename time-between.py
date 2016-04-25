import requests
import json
import base64
import sys
import getopt
import argparse
from datetime import datetime
from datetime import timedelta

JIRA_INSTALLATION = "jira.installation.com"
FIRST_STATE = "In Progress"
FINAL_STATE = "Done"

def main(argv):
    p=argparse.ArgumentParser(description="Gets a set of completed stories and list them with their implementation time.")
    p.add_argument('filter_id', help="Id of the filter that contains completed stories.")
    p.add_argument('-u', dest='username', help="JIRA username. Needs to have read access to all tickets returned from the search filter.")
    p.add_argument('-p', dest='password', help="Password for the JIRA user to use for API calls.")
    args = p.parse_args(argv)

    if len(argv)<3:
        print "Use with -u <username> -p <password> <JIRA-filter-id>."
        sys.exit(2)
    get_transition_times(args.username, args.password, args.filter_id)

def get_transition_times(username, password, filter, first_state=FIRST_STATE, final_state=FINAL_STATE):

    headers = {'Authorization':'Basic %s' % base64.b64encode(username + ':' + password),
               'Content-Type':'application/json'}

    all_issues = requests.get(url="https://"+JIRA_INSTALLATION+"/rest/api/2/search?jql=filter="+filter+"&fields=key", headers=headers, verify=False)
    if (all_issues.status_code!=200):
        print "Tried to get all isses for JIRA filter '"+filter+"' Status code returned: "+str(all_issues.status_code)
        sys.exit(2)

    issues = json.loads(all_issues.content)['issues']
    for issue in issues:
        issue_content = requests.get(url=issue['self']+"?expand=changelog&fields=changelog", headers=headers, verify=False)
        changelog = json.loads(issue_content.content)['changelog']
        histories = changelog['histories']

        start_time = datetime.now()-timedelta(days=365*1000) # :-) , sometime back in time
        end_time = datetime.now()-timedelta(days=365*1000)
        quick_transition = True

        for history in histories:
            item = history['items'][0]
            created = history['created']
            if (item['field']=="status"):
                if (item['toString']==first_state):
                    timeTransitioned = datetime.strptime((history['created'])[:-9], '%Y-%m-%dT%H:%M:%S') # -9 to trim UTC/mms
                    quick_transition = False
                    if (timeTransitioned>start_time):
                        start_time = timeTransitioned
                elif (item['toString']==final_state):
                    timeTransitioned = datetime.strptime((history['created'])[:-9], '%Y-%m-%dT%H:%M:%S') # -9 to trim UTC/mms
                    if (timeTransitioned>end_time):
                        end_time = timeTransitioned
                if (quick_transition):
                    start_time = end_time

        print str(issue['key'])+";"+str(issue['self'])+";"+str(end_time-start_time)

if __name__ == "__main__":
   main(sys.argv[1:])