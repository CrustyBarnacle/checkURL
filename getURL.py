import requests
import re
from bs4 import BeautifulSoup
import sys, json


# def loadConfiguration(): # TBD



def getURL(url, headers, timeOut=30):
    print("Requesting URL... " + url)
    try:
        urlRequest = requests.get(url=url, timeout=timeOut, headers=headers, allow_redirects=True)
        if urlRequest.status_code != requests.codes.ok:
            urlRequest.raise_for_status()
        status = 'success'
        return urlRequest, status;
    except requests.Timeout: # Timeout will catch ConnectTimeout and ReadTimeout
        print('ERROR: Server TimeOut, ' + url)
    except requests.exceptions.SSLError as e:
        print('ERROR: ' + str(e))
    except requests.ConnectionError: # Unknown connection error occured
        print('ERROR: DNS failure or connection refused, ' + url)
    except requests.HTTPError:
        print(str(urlRequest.status_code) + 'ERROR: URL not found (' + url + ')')


def displayURL(urlRequest):
    try:
        print(urlRequest.url)
        print('Status Code: ' + str(urlRequest.status_code))
        print('Content-Type: ' + urlRequest.headers['content-type'])
        print('Response Time: ' +  str(urlRequest.elapsed))
    except Exception as e:
        print(e)

# Update will be needed to work with EM7/log to message server
# Currently only creates local log file
def logURL(urlRequest, logFile, level, status):
    try:
        with open(logFile, 'w') as logObject:
            logString = (str(urlRequest.status_code) + "\n" + str(urlRequest.elapsed)
            + "\n" + urlRequest.url + "\n" + status)
            logObject.write(logString)
    except: # Could not open/read/write to logFile
        print('Could not open logfile ' + logFile)


def searchString(myRequest, mySearchString):
    bsObj = BeautifulSoup(myRequest.content, 'lxml') # html.parser; html5lib; lxml
    if bsObj.find_all(string=re.compile(mySearchString)):
        return "Success"
    else:
        return "Failed"


# Define argument values
# To be pulled from configuration file using json format
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36'}

# Load Configuration for urlCheck
urlCheck = sys.argv[1] # Config file is the second argument, arvg[1] when called with python

with open(urlCheck) as data_file:
        jsonData = json.load(data_file)

# print (jsonData)
url = jsonData['url']
mySearchString = jsonData['string']

# Get URL, display URL, and log results
# Develop into function/s to allow using external configuration file
myRequest, status = getURL(url, headers)
displayURL(myRequest)
print("SearchString '%s': " % mySearchString + searchString(myRequest, mySearchString))
logURL(myRequest, 'test.log','Normal', status)
