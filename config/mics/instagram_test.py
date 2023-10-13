import threading
from InstagramAPI import InstagramAPI
username = ''
password = 'Neskazu_38'

api = InstagramAPI(username, password)
api.login()
api
# api.setProxy("dGC5o8:zcf7tx@45.92.171.19:8000")
thread = threading.Thread()
thread.start()
api.getv2Threads(thread)
# inbox = api.getSelfUsernameInfo()
# print(inbox)
api.s
for key, value in api.LastJson.items():
    print(key, value)
    print()
#     # if key == "aymf":
# for key, value in api.LastJson["aymf"].items():
#     for val in value:
#         print(val)
#         print()

# threads = api.LastJson['inbox']['threads']
# for thread in threads:
#     for item in thread['items']:
#         sender = item['user_id']
#         message = item['text']
#         print(f"From: {sender}, Message: {message}")
