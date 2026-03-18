import requests
from requests.auth import HTTPBasicAuth
import pprint

# Config / Setup
base_url = "https://metadata.api.oclc.org"
client_id = "xxxxxxxxxx"
client_secret = "xxxxxxxxxxxxxxxx"
#holdings_url = ("/worldcat/manage/institution/holding-codes")
holdings_url = ("/worldcat/search/bibs-summary-holdings")
token_url = "https://oauth.oclc.org/token"
# Scopes are space-separated (e.g., WorldCatMetadataAPI)
scope = "WorldCatMetadataAPI"# context:105513"
mpl_holdings = []

#####################

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

# Example: Searching WorldCat
headers = {
    'Authorization': f'Bearer {token_data}',
    'Accept': 'application/json'
}

# Build request
test_list = [1564252970, 1564252971, 1564252972, 1234125411111] # OCLC numbers
for i in test_list:
    params = {'oclcNumber':i, 'holdingsAllEditions':'1'}#, 'heldInState':'US-WI'}
    api_response = requests.get(request_url, headers=headers, params=params)
    response = api_response.json()
    num_records = (response['numberOfRecords'])
    if num_records > 0:
        #pprint.pprint(response)

        count = (response['briefRecords'][0]['institutionHolding']['totalHoldingCount']) # Total Holdings
        oclc_no = (response['briefRecords'][0]['oclcNumber']) # OCLC Number
        title = (response['briefRecords'][0]['title']) # OCLC Number
        holding_data = [oclc_no, title, count]
        mpl_holdings.append(holding_data)
        holding_data = []
print(mpl_holdings)
