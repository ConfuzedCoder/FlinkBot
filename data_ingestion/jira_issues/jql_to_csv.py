import requests
import csv
import os
import argparse
import getpass

# https://confluence.atlassian.com/jirakb/exporting-jira-s-issues-using-csv-in-batches-1071829731.html

parser = argparse.ArgumentParser(description='Calls a JQL query and export it to CSV files.\nWe suggest that the JQL queries end with "ORDER BY key"')
parser.add_argument('-j','--jql', nargs='?', default='ORDER BY key', metavar='JQL_query', help='JQL query - default query is "ORDER BY key"')
parser.add_argument('-u', required=True, metavar='username', help='Username')
parser.add_argument('-p', nargs='?', default='', metavar='password', help='Password. If parameter is not passed, the password will be prompted')
parser.add_argument('-n', nargs='?', default=1000, metavar='Number_of_issues', help='Number of issues per CSV batch. Default of 1000 in line with Jiras default. For more details, check https://confluence.atlassian.com/jirakb/filter-export-only-contains-1000-issues-in-jira-server-191500982.html')
parser.add_argument('-U','--url', required=True, metavar='Base_URL', help='Jira''s base URL. For example, https://jira.mycompany.com')

args = parser.parse_args()

jql = args.jql
username = args.u
password = args.p
step = int(args.n)
baseurl = args.url

if password == '':
    password = getpass.getpass()
#print(args)

start=7500

url = baseurl+'/sr/jira.issueviews:searchrequest-csv-all-fields/temp/SearchRequest.csv?jqlQuery='+jql

while True:
    print(str(start)+' issues exported')
    theurl = url+'&tempMax='+str(step)+'&pager/start='+str(start)
    temp_url = f"https://issues.apache.org/jira/sr/jira.issueviews:searchrequest-csv-all-fields/temp/SearchRequest.csv?jqlQuery=project+%3D+FLINK+ORDER+BY+created+DESC&delimiter=,DESC&tempMax={str(step)}&pager/start={str(start)}"
    print(temp_url)
    resp = requests.get(temp_url, verify=False)

    f = open('output.csv', 'w')
    f.write(resp.text)
    f.close()

    f = open('output.csv','r',newline='')
    reader = csv.DictReader(f)
    try:
        row = reader.__next__()
    except:
        break

    firstkey = row['Issue key']

    count=1
    try:
        for r in reader:
            row = r
            count+=1
    except Exception as e:
        print(e)
        count+=1
        
    f.close()

    lastkey = row['Issue key']

    os.rename('output.csv',(str(start)+'-'+str(start + step)+'.csv'))

    if count < step:
        print(str(start+count)+' issues exported')
        break
    
    start+=step



    # Referance : https://confluence.atlassian.com/jirakb/exporting-jira-s-issues-using-csv-in-batches-1071829731.html
    # https://issues.apache.org/jira/sr/jira.issueviews:searchrequest-csv-all-fields/temp/SearchRequest.csv?jqlQuery=project+%3D+FLINK+ORDER+BY+created+DESC&delimiter=,
    # Base URL : https://issues.apache.org/jira
    # JQL query : project = FLINK ORDER BY created DESC
    # --jql "project = FLINK ORDER BY created DESC" 

    # https://issues.apache.org/jira/sr/jira.issueviews:searchrequest-csv-all-fields/temp/SearchRequest.csv?jqlQuery=project+%3D+FLINK+ORDER+BY+created+DESC&delimiter=,DESC&tempMax=500&pager/start=7500]

    # python jql_to_csv.py --url "https://issues.apache.org/jira"  --jql "project = FLINK ORDER BY created DESC" -n 500 -u "test" 
    