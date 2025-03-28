from time import sleep
import requests
import csv
import os
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('MUCKROCK_API_TOKEN')
url = 'https://www.muckrock.com/api_v1/'

headers = {'Authorization': 'Token %s' % token, 'content-type': 'application/json'}
next_ = url + 'agency'

fields = (
        "id",
        "name",
        "slug",
        "status",
        "twitter",
        "twitter_handles",
        "parent",
        "appeal_agency",
        "url",
        "foia_logs",
        "foia_guide",
        "public_notes",
        "absolute_url",
        "average_response_time",
        "fee_rate",
        "success_rate",
        "has_portal",
        "has_email",
        "has_fax",
        "has_address",
        "number_requests",
        "number_requests_completed",
        "number_requests_rejected",
        "number_requests_no_docs",
        "number_requests_ack",
        "number_requests_resp",
        "number_requests_fix",
        "number_requests_appeal",
        "number_requests_pay",
        "number_requests_partial",
        "number_requests_lawsuit",
        "number_requests_withdrawn"
        )
jurisdiction_fields = (
        'name',
        'parent',
        'level',
        )

page = 1

# make this true while exporting data to not crash on errors
SUPRESS_ERRORS = True

# This allows you to cach jurisdiction look ups
jurisdictions = {}

def get_jurisdiction(jurisdiction_id):
    global jurisdictions
    if jurisdiction_id in jurisdictions:
        return jurisdictions[jurisdiction_id]
    else:
        # print 'getting jurisdiction', jurisdiction_id
        sleep(0.1) # rate limit
        r = requests.get(url + 'jurisdiction/' + str(jurisdiction_id), headers=headers)
        jurisdiction_json = r.json()
        if jurisdiction_json['parent']: # USA has no paremt
            parent = get_jurisdiction(jurisdiction_json['parent'])
            jurisdiction_json['parent'] = parent['name'] # replace parent id with parent name in jurisdiction json
        jurisdictions[jurisdiction_id] = jurisdiction_json
        return jurisdiction_json

csv_file = open('agency_stats.csv', 'w')
csv_writer = csv.writer(csv_file)
jurisdiction_field_names = tuple('jurisdiction {}'.format(f) for f in jurisdiction_fields)
csv_writer.writerow(fields + jurisdiction_field_names)

while next_ is not None:
    r = requests.get(next_, headers=headers)
    try:
        json = r.json()
        next_ = json['next']
        for datum in json['results']:
            agency_values = [datum[field] for field in fields]
            jurisdiction = get_jurisdiction(datum['jurisdiction'])
            jurisdiction_values = [jurisdiction[field] for field in jurisdiction_fields]
            csv_writer.writerow(agency_values + jurisdiction_values)
        print('Page %d of %d' % (page, json['count'] / 20 + 1))
        page += 1
    except Exception as e:
        print('Error', e)
        if not SUPRESS_ERRORS:
            raise
