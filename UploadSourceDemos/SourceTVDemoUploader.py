#!/usr/bin/python3

import base64
import json
import urllib.request
import requests
import hashlib
import sys
import os
import pathlib


def b2_authorize_account(account_id, account_key):

	id_and_key = '{}:{}'.format(account_id, account_key)
	id_and_key = str.encode(id_and_key)
	
	basic_auth_string = 'Basic ' + base64.b64encode(id_and_key).decode("utf-8")
	headers = { 'Authorization': basic_auth_string }

	request = urllib.request.Request(
		'https://api.backblazeb2.com/b2api/v2/b2_authorize_account',
		headers = headers
    )

	response = urllib.request.urlopen(request)
	response_data = json.loads(response.read().decode("utf-8"))
	response.close()
	
	return response_data


def b2_get_upload_url(bucket_id, api_url, authorization_token):
	
	request_url = u"{}/b2api/v1/b2_get_upload_url".format(api_url)
	headers = {
		"Authorization": authorization_token,
	}
	body = {
		"bucketId": bucket_id,
	}

	resp = requests.post(request_url, json=body, headers=headers)

	return resp.json()


def b2_upload_file(upload_url, authorization_token, file_name):
	#cd into SourceTVDemos directory so path doesn't show up in file name
	os.chdir(sourceTVDemos_path)
	
	with open(file_name, 'rb') as file:
		file_data = file.read()
		
		headers = {
			"Authorization": authorization_token,
			"X-Bz-File-Name": file_name,
			"Content-Type": "b2/x-auto",
			"X-Bz-Content-Sha1": hashlib.sha1(file_data).hexdigest()
		}
	
		resp = requests.post(upload_url, data=file_data, headers=headers)
		return resp.json()


sourceTVDemos_path = sys.argv[1]
id = sys.argv[2]
key = sys.argv[3]

response = b2_authorize_account(id, key)

bucketID = response['allowed']['bucketId']
AuthToken = response['authorizationToken']
apiURL = response['apiUrl']

response = b2_get_upload_url(bucketID, apiURL, AuthToken)

uploadURL = response['uploadUrl']
AuthToken = response['authorizationToken'] #slightly different than first auth key

for entry in os.scandir(sourceTVDemos_path):
	if entry.is_file():
		# sourceTV demos end in .gz and contain "auto" in the name
		if '.gz' in pathlib.Path(entry.name).suffixes and 'auto' in entry.name:
			response = b2_upload_file(uploadURL, AuthToken, entry.name)
			#print(response)
			if 'uploadTimestamp' in response:
				# Assume upload succeeded. Go ahead and delete locally
				print("Succeeded uploading {} . Removing file locally..".format(response['fileName']))
				os.remove(entry.name)
			else:
				print("Something went wrong when trying to upload entry.name\n response: " + response)