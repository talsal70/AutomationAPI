# main.py
import json
import random
from deepdiff import DeepDiff
import messages
from commbox_apis import CommboxApis
from datetime import datetime
from html import escape




def read_conf():
    file_path = "config_qa_automation.json"
    print("Trying to open:", file_path)

    with open(file_path, "r") as conf_f:
        config = json.load(conf_f)
    env_config = config["environments"]["qa_automation"]
    url = env_config["api_url"]
    key_api = env_config["bearer_token"]
    return url, key_api

def create_conversation():
    # create object
    r_code, o_id = commbox_apis.create_object(stream_id)

    if r_code == 200:
        data_result = commbox_apis.get_object(stream_id, o_id)
        print("object:" + str(data_result) + "\n")
    return r_code, o_id

def debug_exist_conversation(o_id):
    # send message from client side
    commbox_apis.send_message_from_client_side(stream_id, o_id,"message")
    # send message from agent side
    commbox_apis.send_message_from_agent_side(stream_id, o_id,"message")


def create_new_conversation_test():
    #object_id = None
    object_ids = []
    for i in range(3):
        # create the conversation object
        response_code, object_id  = create_conversation()
        object_ids.append(object_id)

        # make conversation between client and agent
        commbox_apis.send_message_from_agent_side(stream_id, object_id, random.choice(messages.agent_messages))
        commbox_apis.send_message_from_client_side(stream_id, object_id, random.choice(messages.client_messages))
        commbox_apis.send_message_from_client_side(stream_id, object_id, random.choice(messages.client_messages))
        commbox_apis.send_message_from_agent_side(stream_id, object_id, random.choice(messages.agent_messages))

    # return the expected conversation
    #return commbox_apis.get_object(stream_id, object_id), object_id
    return object_ids


def play_conversation_test(in_obj_id):
    # # create the object conversation first time
    response_code, object_id  = create_conversation()
    children = commbox_apis.get_conversation(stream_id, in_obj_id)

    for child in children:
        if child["user"]["isManager"]:
            # send message from agent side
            commbox_apis.send_message_from_agent_side(stream_id, object_id, child["message"])
        else:
            # send message from client side
            commbox_apis.send_message_from_client_side(stream_id, object_id, child["message"])
    return object_id

def print_all_streams():
    # get all streams in env
    streams = commbox_apis.get_streams()
    count = 0

    # print stream of the object id
    for stream in streams:
        count+=1
        print("stream:" + str(stream))
    print("number of streams:" + str(count))


def find_streams_by_module_object(module_id, obj_id):
    # get all streams in env
    streams = commbox_apis.get_streams()
    print("find couple of stream and object = 3546987534722900")
    count = 0
    for stream in streams:
        count+=1
        if stream["moduleId"] == module_id:
            stream_id_inner = stream["id"]
            data_result = commbox_apis.get_object(stream_id_inner,obj_id)
            if data_result is not None:
                print("object:" + str(data_result) + "\n")
                print("stream:" + str(stream))


def report():
    # Format timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Test Diff Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            h1 {{ color: #333; }}
            .diff {{ white-space: pre-wrap; background: #f6f6f6; padding: 10px; border-radius: 6px; }}
            .pass {{ color: green; }}
            .fail {{ color: red; }}
        </style>
    </head>
    <body>
        <h1>Test Diff Report</h1>
        <p><strong>Timestamp:</strong> {timestamp}</p>
    """

    if not diff:
        html += "<p class='pass'>✅ Test Passed — No differences found.</p>"
    else:
        html += "<p class='fail'>❌ Test Failed — Differences detected:</p>"
        html += f"<div class='diff'>{escape(diff.pretty())}</div>"

    html += "</body></html>"

    # Save to file
    with open("diff_report.html", "w", encoding="utf-8") as report:
        report.write(html)


if __name__ == "__main__":
    # read configuration file
    api_url, api_key = read_conf()

    # base stream id that we know that exist. this stream is of type 6  = mailbox_connector
    stream_id = 17374

    # create apis class
    commbox_apis = CommboxApis(api_key,api_url)

    # full cycle test
    #exp, exp_obj_id = create_new_conversation_test()
    act_obj_ids = []
    act = []
    exp = []
    exp_obj_ids = create_new_conversation_test()
    for exp_obj_id in exp_obj_ids:
        act_obj_id = play_conversation_test(exp_obj_id)
        act_obj_ids.append(act_obj_id)
        act_data = commbox_apis.get_object(stream_id, act_obj_id)
        act.append(act_data)
        exp_data = commbox_apis.get_object(stream_id, exp_obj_id)
        exp.append(exp_data)

    # Write 'exp' to exp.json or exp.txt
    with open("exp.json", "w", encoding="utf-8") as f_exp:
        json.dump(exp, f_exp, ensure_ascii=False, indent=2)

    # Write 'act' to act.json or act.txt
    with open("act.json", "w", encoding="utf-8") as f_act:
        json.dump(act, f_act, ensure_ascii=False, indent=2)


    # Load from files
    with open("exp.json", "r", encoding="utf-8") as f:
        exp = json.load(f)

    with open("act.json", "r", encoding="utf-8") as f:
        act = json.load(f)

    # List of dynamic keys to remove
    # Define dynamic keys + stringified JSON fields
    dynamic_keys = {
        "id", "objectId", "object_id", "createdTime", "updatedTime",
        "firstResponseTime", "lastResponseTime", "session_id", "message_id",
        "streamProviderId", "Item2", "sequence_start_time"
    }
    json_string_keys = {"content"}


    def remove_dynamic_keys(obj, keys_to_exclude, json_string_keys=None):
        if isinstance(obj, dict):
            new_obj = {}
            for k, v in obj.items():
                if k in keys_to_exclude:
                    continue
                # Try to parse JSON-encoded strings and clean inside them
                if json_string_keys and k in json_string_keys and isinstance(v, str):
                    try:
                        parsed = json.loads(v)
                        cleaned = remove_dynamic_keys(parsed, keys_to_exclude, json_string_keys)
                        new_obj[k] = json.dumps(cleaned, ensure_ascii=False)
                    except Exception:
                        new_obj[k] = v  # leave unchanged if not valid JSON
                else:
                    new_obj[k] = remove_dynamic_keys(v, keys_to_exclude, json_string_keys)
            return new_obj
        elif isinstance(obj, list):
            return [remove_dynamic_keys(item, keys_to_exclude, json_string_keys) for item in obj]
        else:
            return obj


    # Clean the objects
    filtered_act = remove_dynamic_keys(act, dynamic_keys, json_string_keys)
    filtered_exp = remove_dynamic_keys(exp, dynamic_keys, json_string_keys)

    diff = DeepDiff(filtered_exp, filtered_act, ignore_order=False, report_repetition=True)

    if not diff:
        print("✅ Test passed (excluding dynamic fields)")
    else:
        print("❌ Differences found:")
        print(diff)

    with open("matched_clean.json", "w", encoding="utf-8") as f:
        json.dump(filtered_exp, f, ensure_ascii=False, indent=2)

    print("✅ Cleaned, matched content saved to matched_clean.json")

    report()

