#!/usr/bin/python3
import urllib3 
import requests
#import os
import argparse
import string
import time
#import json
import sys
from pprint import pprint
from gophish import Gophish
#from gophish.models import *


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-g", "--gophish", required=True,
	help="Gophish URL (ex: https://gophishurl.com")
ap.add_argument("-k", "--apikey", required=True,
	help="Gophish API Key")
ap.add_argument("-sDA", "--dumpall", required=False,
	help="Switch: Dump every campaign details to standard output", action='store_true')
ap.add_argument("-oD", "--dump", required=False,
	help="Operation: Dump all details from a specific campaign <ID> to standard output" )
ap.add_argument("-sCL", "--campaignlist", required=False,
	help="Switch: Get every campaign details with ID", action='store_true')
ap.add_argument("-oR", "--results", required=False,
	help="Operation : Get results from specific campaign using <ID>")
ap.add_argument("-oT", "--timeline", required=False,
	help="Operation : Get timeline from specific campaign using <ID>")
ap.add_argument("-oST", "--stats", required=False,
	help="Operation : Get statistics from specific campaign using <ID>")
ap.add_argument("-oAR", "--allresults", required=False,
	help="Operation : Get results from all campaigns containing <PATTERN> in title")
ap.add_argument("-oAT", "--alltimelines", required=False,
	help="Operation : Get timelines from all campaigns containing <PATTERN> in title")
ap.add_argument("-oSTA", "--allstats", required=False,
	help="Operation : Get statistics from all campaigns containing <PATTERN> in title")
ap.add_argument("-v", "--verbose", required=False,
	help="Switch: verbose output", action='store_true')
ap.add_argument("-vv", "--vverbose", required=False,
	help="Switch: very verbose output", action='store_true')
args = vars(ap.parse_args())

gophishURL = args["gophish"]
if gophishURL[-1] != "/":
    gophishURL = gophishURL + "/"
    
apikey = args["apikey"]
#response = requests.get(gophishURL+"api/campaigns/?api_key="+apikey, verify=False)
#data = json.loads(response.text)

urllib3.disable_warnings()
api = Gophish(apikey, host=gophishURL, verify=False)

if args["stats"] is not None:
    try:
        campaign = api.campaigns.get(campaign_id=args["stats"])
        timeline = campaign.timeline
        for item in timeline:
            print(item.email + " | " + item.message)
    except (Exception, e):
        print(str(e))
    finally:
        exit()

if args["results"] is not None:
    try:
        campaign = api.campaigns.get(campaign_id=args["results"])
        results = campaign.results
        for result in results:
            verbose = ""
            if (args["verbose"] == True) or (args["vverbose"] == True):
                verbose = " | " + result.first_name + " " + result.last_name
            if args["vverbose"] == True :
                verbose = verbose + " | " + result.status
            print(str(result.id) + " | " + result.email + verbose)
    except (Exception, e):
        print(str(e))
    finally:
        exit()

if args["timeline"] is not None:
    try:
        campaign = api.campaigns.get(campaign_id=args["timeline"])
        timeline = campaign.timeline
        for item in timeline:
            sys.stdout.write(item.time + " | " + item.email + " | " + item.message + " | ")
            sys.stdout.flush()
            print(item.details)
    except (Exception, e):
        print(str(e))
    finally:
        exit()

if args["dump"] is not None:
    try:
        response = requests.get(gophishURL+"api/campaigns/"+args["dump"]+"?api_key="+apikey, verify=False)
        print(u''.join(response.text).encode('utf-8'))
    except (Exception, e):
        print(str(e))
    finally:
        exit()


if args["dumpall"] == True:
    try:
        response = requests.get(gophishURL+"api/campaigns/?api_key="+apikey, verify=False)
        print(u''.join(response.text).encode('utf-8'))
    except (Exception, e):
        print(str(e))
    finally:
        exit()


campaigns = api.campaigns.get()

if args["allresults"] is not None:
    try:
        for campaign in campaigns:
            if campaign.name.find(args["allresults"]) != -1:
                results = campaign.results
                for result in results:
                    verbose = ""
                    if (args["verbose"] == True) or (args["vverbose"] == True):
                        verbose = " | " + result.first_name + " " + result.last_name
                    if args["vverbose"] == True :
                        verbose = verbose + " | " + result.status
                    print(u''.join(str(result.id) + " | " + result.email + verbose).encode('utf-8'))
    except (Exception, e):
        print(str(e))
    finally:
        exit()

if args["alltimelines"] is not None:
    try:
        for campaign in campaigns:
            if campaign.name.find(args["alltimelines"]) != -1:
                timeline = campaign.timeline
                for item in timeline:
                    sys.stdout.write(item.time + " | " + item.email + " | " + item.message + " | ")
                    sys.stdout.flush()
                    print(item.details)
    except (Exception, e):
        print(str(e))
    finally:
        exit()

if args["campaignlist"] == True:
    for campaign in campaigns:
        verbose = ""
        if (args["verbose"] == True) or (args["vverbose"] == True):
            verbose = " | " + str(campaign.launch_date)
        if args["vverbose"] == True :
            verbose = verbose + ""
        print(str(campaign.id)+" | "+campaign.name + verbose)

            




