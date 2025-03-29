import requests

access_token = 0

API_URL = "https://router.huggingface.co/hf-inference/models/google/tapas-base-finetuned-wtq"
headers = {"Authorization": "Bearer " + access_token}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": {
	"query": "How many stars does the transformers repository have?",
	"table": {
		"Repository": ["Transformers", "Datasets", "Tokenizers"],
		"Stars": ["36542", "4512", "3934"],
		"Contributors": ["651", "77", "34"],
		"Programming language": [
			"Python",
			"Python",
			"Rust, Python and NodeJS"
		]
	}
},
})

print output
