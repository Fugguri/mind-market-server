
from whatsapp_api_client_python import API


class GreenApi:
    def __init__(self,
                 ID_INSTANCE,
                 API_TOKEN_INSTANCE
                 ) -> None:

        self.api = API.GreenApi(ID_INSTANCE, API_TOKEN_INSTANCE)

    def send_message(self, number: int, message_text: str):
        result = self.api.sending.sendMessage(
            chatId=number+'@c.us',
            message=message_text)
        return result

    async def send_file_by_url(self, number: int, url: str, filename: str, caption: str):

        response = self.api.sending.sendFileByUrl(
            chatId=number+'@c.us',
            urlFile=url,
            fileName=filename,
            caption=caption
        )

        return response

    async def send_file__by_upload(self, number: int, path: str, caption: str):

        response = self.api.sending.sendFileByUpload(
            chatId=number+'@c.us',
            path=path,
            caption=caption
        )

        return response

    async def create_group_and_send_message(self, group_name: str, chat_ids: list[str]):
        create_group_response = self.api.groups.createGroup(
            groupName=group_name,
            chatIds=chat_ids
        )
        if create_group_response.code == 200:
            send_message_response = self.api.sending.sendMessage(
                create_group_response.data["chatId"], "Message text"
            )
            if send_message_response.code == 200:
                return send_message_response.data
            else:
                print(send_message_response.error)
        else:
            print(create_group_response.error)
