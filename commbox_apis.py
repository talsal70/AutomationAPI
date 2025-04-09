import json
from typing import TextIO

import requests

class CommboxApis:
    def __init__(self, api_key, url):
        self.api_key = api_key
        self.base_url = url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def create_object(self,
                     stream_id
                     ):
        url = f"{self.base_url}/streams/{stream_id}/objects"

        payload = {
            "data": {
                "Type": 4, # object type = conversation, why it is not a good name ?
                "StatusId": 1, # object status type = open
                "StreamProviderType": 1,
                "UserStreamProviderId": "tal.sa@commbox.io", # the email of the client
                "UserStreamProviderType": 5, # what is it? is it mail? why needed if the stream is known
                "SubStreamId": 35645, # what is it?
                "ManagerId": 5416672, # if you put this field, it will send it from agent, else from client. the number is not matter
                "Message": "first message from the agent create object",
                "Content": {
                    "subject": "Email test22224443",
                    "to": [
                        {
                            "address": "tal.sa@commbox.io"
                        }
                    ],
                    "attachments": [
                        {
                            "path": "https://ebigh.com/wp-content/uploads/2017/12/Basketball-Stars.jpg",
                            "name": "basketball.png"
                        }
                    ]
                },
                # "Content": { # more extended details
                #     "bank_id": 123,
                #     "branch_id": 456,
                #     "account_id": 789
                # },
                "User": { # another client details
                    "UniqueId": "999",
                    "LastName": "cohen",
                    "FirstName": "moshe",
                    "Phone1": "9999",
                    "Email": "kuku.kuku@commbox.io",
                    "Remarks": "some remark for user"
                }
            }
        }
        response = requests.post(url, json=payload, headers=self.headers)
        print(f"Stream {stream_id} Response: {response.status_code}, {response.json()}")
        if response.status_code == 200:
            return response.status_code, response.json()["data"]["Id"]
        else:
            return response.status_code



    def send_message_from_client_side(self,stream_id,object_id, message):
        url = f"{self.base_url}/streams/{stream_id}/objects/{object_id}/child"
        payload = {
            "data":
            {
                #"Type": 4, it is also known type
                "UserStreamProviderId": "client", # how it is id if i can put text?
                #"UserStreamProviderType": 4, also known
                "Message": message
            }
        }
        response = requests.post(url, json=payload, headers=self.headers)
        print(f"Stream {stream_id} Response: {response.status_code}, {response.json()}")
        if response.status_code == 200:
            return response.status_code, response.json()["data"]["id"]
        else:
            return response.status_code

    def send_message_from_agent_side(self,stream_id,object_id, message):
        url = f"{self.base_url}/streams/{stream_id}/objects/{object_id}/child"
        payload = {
              "data": {
                "IsManager": True,
                "UserIdentity": 591427,
                "ManagerId": 5416672, # what for ? if i know the user identity?
                #"ManagerId": 1,
                #"Type": 4, known
                "UserStreamProviderId": "i am the agent", #known
                "UserStreamProviderType": 4,#known
                "Message": message
              }
}
        response = requests.post(url, json=payload, headers=self.headers)
        print(f"Stream {stream_id} Response: {response.status_code}, {response.json()}")
        if response.status_code == 200:
            return response.status_code, response.json()["data"]["id"]
        else:
            return response.status_code


    def get_streams(self):
        response = requests.get(f"{self.base_url}/streams", headers=self.headers)
        streams_data = response.json().get("data", {}).get("streams", [])
        for stream in streams_data:
            print(stream)
        return streams_data

    def get_conversation(self,stream_id, object_id):
        response = requests.get(f"{self.base_url}/streams/{stream_id}/objects/{object_id}", headers=self.headers)
        data_result = response.json().get("data")
        children = data_result[0]["childs"]
        # for child in childs:
        #     print(child)
        # # Create and write the JSON data to the file
        file_path = "conversation.json"
        with open(file_path, "w", encoding="utf-8") as json_file:  # type: TextIO
            json.dump(children,json_file, indent=4)  # indent=4 makes the output pretty-printed

        print(f"JSON data has been written to {file_path}")
        return children

    def get_object(self, stream_id, obj_id):
        data_result = None
        response = requests.get(f"{self.base_url}/streams/{stream_id}/objects/{obj_id}", headers=self.headers)
        if response.status_code == 200:
            data_result = response.json().get("data")
        print(response.status_code)
        return data_result

    def get_tags(self):
        data_result = None
        response = requests.get(f"{self.base_url}/tags",headers=self.headers)
        if response.status_code == 200:
            data_result = response.json().get("data")
        print(response.status_code)
        for tag in data_result:
            print(tag)
        return data_result


    def set_obj_tag(self, stream_id, object_id, tag):
        data_result = None
        response = requests.post(f"{self.base_url}/streams/{stream_id}/objects/{object_id}/tags/{tag}",headers=self.headers)
        if response.status_code == 200:
            data_result = response.json().get("data")
        print(response.status_code)
        for tag in data_result:
            print(tag)
        return data_result
