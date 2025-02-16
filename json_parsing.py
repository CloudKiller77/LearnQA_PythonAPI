import json

json_format = '{"messages": [{"message": "This is the first message", "timestamp": "2021-06-04 16:40:53"},{"message": "And this is a second message", "timestamp": "2021-06-04 16:41:01"}]}'
message = json.loads(json_format)
print(message["messages"][1]["message"])