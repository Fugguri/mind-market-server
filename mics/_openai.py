import openai
from dotenv import dotenv_values
users_message = {}


config = dotenv_values(".env")
openai.api_key = config['openAi']


async def create_responce(user_id: int | str, settings: str, text: str | int):
    print(text)
    try:
        answer = ""
        try:
            users_message[user_id]
        except:
            users_message[user_id] = [{"role": "user", "content": settings}]
        users_message[user_id].append(
            {"role": "user", "content": text})
        responce = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=users_message[user_id],
            temperature=0.7
        )
        answer = responce['choices'][0]['message']['content']

        users_message[user_id].append({"role": "assistant", "content": answer})
    except openai.error.RateLimitError as ex:
        return "RateLimitError"
    except Exception as ex:
        print(ex)
        users_message[user_id] = []
        create_responce(user_id, text)
    return answer
