import requests
import pandas as pd

access_token = NULL

API_URL = "https://router.huggingface.co/hf-inference/models/google/tapas-base-finetuned-wtq"
headers = {"Authorization": "Bearer " + access_token}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def json_to_dict(output):
	return {}			# format llm response into dict; 

states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
	  "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", 
	  "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
	  "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
	  "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
	  "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
	  "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", 
	  "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming",
	  "United States of America"]

payload = {
	"inputs": {
		"query": "What is the response deadline for FOIA requests of each state listed in the table?",
		"table": {"States": states}
	},
}

output = query(payload)				#query llm
print output
response_times = json_to_dict(output)


df = pd.read_csv('agency_stats.csv')
df['response time policy'] = ''
len = len(df)

for i in range(len):
	state = df.loc[i, 'jurisdiction name']
	parent = df.loc[i, 'jurisdiction parent']

	if state in response_times:
		df.loc[i, 'response time policy'] = response_times[state]
	elif parent in response_times:
		df.loc[i, 'response time policy'] = response_times[parent]
	else:
		print("Could not find state")

df.to_csv('agency_stats.csv', index=False)



