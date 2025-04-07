# main.py
import json
import random


from commbox_apis import CommboxApis


def read_conf():
    file_path = "config_qa_automation.json"
    print("Trying to open:", file_path)

    with open(file_path, "r") as f:
        config = json.load(f)
    env_config = config["environments"]["qa_automation"]
    url = env_config["api_url"]
    key_api = env_config["bearer_token"]
    return url, key_api


if __name__ == "__main__":
    # read configuration file
    api_url, api_key = read_conf()

    # base stream id that we know that exist. this stream is of type 6  = mailbox_connector
    stream_id = 17374

    # create apis class
    commbox_apis = CommboxApis(api_key,api_url)

    #commbox_apis.get_streams()

    commbox_apis.get_tags()



