from whatsapp_api_client_python import API

class Watsapp:

    def __init__(self,IdInstance,ApiTokenInstance):
        self.IdInstance = IdInstance
        self.ApiTokenInstance =ApiTokenInstance
        self.greenAPI = API.GreenApi(IdInstance, ApiTokenInstance)
        self.sending = self.greenAPI.sending
        self.startReceivingNotifications = self.greenAPI.webhooks.startReceivingNotifications

    def get_me(self):
        import requests

        #The idInstance and apiTokenInstance values are available in your account, double brackets must be removed

        url = f"https://api.green-api.com/waInstance{self.IdInstance}/getWaSettings/{self.ApiTokenInstance}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text.encode('utf8').split(','))
        # return me
    
    def send_sync_message(self, text, phone,img_path=None):
        phone = self._convert_number(phone)
        
        if img_path:
            name = img_path.split("/")[-1]
            self.greenAPI.sending.sendFileByUpload(phone+"@c.us",path=img_path,fileName=name,caption=text)
        else:
            self.greenAPI.sending.sendMessage(phone+"@c.us", text)



