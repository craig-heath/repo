#!/bin/bash

#API="api.crowdstrike.com"
#API="api.us-2.crowdstrike.com"
API="api.eu-1.crowdstrike.com"

# store api client ID and Secret in the files APICLIENT.txt and APIKEY.txt

echo "Requesting Bearer Token" 1>&2
ACCESSTOKEN=$(curl -s -X POST "https://$API/oauth2/token" -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "client_id=$(cat ~/keys/APICLIENT.txt)&client_secret=$(cat ~/keys/APIKEY.txt)"|sed -n '2p' | sed 's/"access_token": \"//'| sed 's/^ //;s/",$//')

if [ -z "$ACCESSTOKEN" ]
    then
        echo "Requesting Token Failed" 1>&2
        exit 1
    else
        echo "Token retrieved" 1>&2
fi

echo "Find Hash for Sensor" 1>&2

# only the latest sensor for Mac, can play with the filters if needed

# install jq to parse json"

IDS=$( curl -X GET "https://$API/sensors/queries/installers/v2?limit=1&sort=release_date%7Cdesc&filter=platform%3A%22mac%22" \
    -H "Authorization: bearer $ACCESSTOKEN "\
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
     | /opt/homebrew/bin/jq -c '.["resources"]' | sed s/"\[\""// |  sed s/"\"\]"// )

echo "Hash is $IDS"

echo "Download Sensor" 1>&2
curl -X GET "https://$API/sensors/entities/download-installer/v1?id=$IDS" \
    -H "Authorization: bearer $ACCESSTOKEN" \
    -H "Content-Type: application/json" \
    --output LatestMacSensor
echo "done"
exit 1
