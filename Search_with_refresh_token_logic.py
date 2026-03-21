import csv, time, requests, json, pprint, os
from requests.auth import HTTPBasicAuth
from pathlib import Path
import pandas as pd
#import requests, json, pprint, os


# --- CONFIGURATION ---
client_id = 'XXXXXXXXXXXXXXXX'
client_secret = 'XXXXXXXXXXXXXX'
token_url = "https://oauth.oclc.org/token"
scope = "WorldCatMetadataAPI refresh_token"# context:105513"
list_path = Path.home() / "Desktop" / "1afar.csv"
endpoint = "https://metadata.api.oclc.org/worldcat/search/bibs-summary-holdings"
mpl_holdings = []
counter = 0
output_path = Path.home() / "Desktop" / "holdings.csv"


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

access_token = response.json()['access_token']
refresh_token = response.json()['refresh_token']
last_refresh = time.time()


print(access_token, refresh_token, last_refresh)
def refresh_if_needed(current_token, r_token, last_time):
    """Refreshes the token if it is older than 18 minutes (1080 seconds)."""
    if time.time() - last_time > 600:
        print("\n--- Token expiring, refreshing now... ---")
        auth = HTTPBasicAuth(client_id, client_secret)
        payload = {'grant_type': 'refresh_token', 'refresh_token': r_token}

        response = requests.post(token_url, params=payload, auth=auth)
        if response.status_code == 200:
            new_data = response.json()
            # Return new access token and reset the timer
            return new_data['access_token'], time.time()
        else:
            raise Exception(f"Refresh failed: {response.text}")
    return current_token, last_time

#test = refresh_if_needed(access_token, refresh_token, last_refresh)
#print(test)

with open(list_path, mode='r', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        counter += 1
        # 1. Check/Refresh token before every iteration
        access_token, last_refresh = refresh_if_needed(access_token, refresh_token, last_refresh)
        # 2. Use the token in your API call
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        params = {'oclcNumber': row, 'holdingsAllEditions': '1'}  # , 'HeldByLibraryType':'3'} #, 'heldInState':'US-WI'}
        try:
            response = requests.get(endpoint, headers=headers, params=params)
            if response.status_code == 200:
                response = response.json()
                print("writing record number ", counter)
                count = (response['briefRecords'][0]['institutionHolding']['totalHoldingCount'])  # Total Holdings
                oclc_no = (response['briefRecords'][0]['oclcNumber'])  # OCLC Number
                title = (response['briefRecords'][0]['title'])  # OCLC Number
                date = (response['briefRecords'][0]['date'])
                holding_data = [[oclc_no, title, date, count]]
                #mpl_holdings.append(holding_data)
                df = pd.DataFrame(holding_data, columns=['oclcNumber', 'title', 'date', 'count'])
                if not os.path.exists(output_path):
                    # File does not exist, write with header
                    df.to_csv(output_path, mode='w', index=False, header=True)
                else:
                    # File exists, append without header
                    df.to_csv(output_path, mode='a', index=False, header=False)
                #df.to_csv(output_path, mode='a', index=False, header=False)
                print(holding_data)
            else:
                print(f"Error processing {row}: {response.status_code}")
        except Exception as e:
            print(f"Request failed for {row}: {e}")
        #count += 1
        #print(row)
