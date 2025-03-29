import requests

access_token = NULL

API_URL = "https://router.huggingface.co/hf-inference/models/google/tapas-base-finetuned-wtq"
headers = {"Authorization": "Bearer " + access_token}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
payload = {
	"inputs": {
	"query": "What is the deadline for FOIA requests of each state in the table?",
	"table": {
		"States": ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
			   "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", 
			   "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
			   "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
			   "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
			   "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
			   "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", 
			   "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming",
			   "United States of America"],
	}
	},
}
output = query()
print output


