import requests
from requests.auth import HTTPBasicAuth
import pprint

# Config / Setup
base_url = "https://metadata.api.oclc.org"
client_id = "XxXXXXXXXXX"
client_secret = "XXXXXXXXXXXX"
#holdings_url = ("/worldcat/manage/institution/holding-codes")
holdings_url = ("/worldcat/search/bibs-summary-holdings")
token_url = "https://oauth.oclc.org/token"
# Scopes are space-separated (e.g., WorldCatMetadataAPI)
scope = "WorldCatMetadataAPI"# context:105513"

# Payload for the Client Credentials grant
payload = {
    'grant_type': 'client_credentials',
    'scope': scope
}

# Request the token
response = requests.post(
    token_url,
    data=payload,
    auth=HTTPBasicAuth(client_id, client_secret)
)

token_data = response.json()['access_token']
print(response.json())
print(token_data)
request_url = base_url + holdings_url

print(request_url)


# Example: Searching WorldCat
headers = {
    'Authorization': f'Bearer {token_data}',
    'Accept': 'application/json'
}


# Build request
params = {'oclcNumber':'1564252970', 'holdingsAllEditions':'1', 'heldInState':'US-WI'}
api_response = requests.get(request_url, headers=headers, params=params)

response = api_response.text
pprint.pprint(response)

#response = requests.get(url, headers=headers)

#print(response.status_code)

