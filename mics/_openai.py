import httpx
from openai import OpenAI
from dotenv import dotenv_values
config = dotenv_values(".env")

openai = OpenAI(
    api_key=config['openAi'],

    http_client=httpx.Client(
        proxies="http://9gfWr9:g0LSUy@131.108.17.194:9799/",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)

users_message = {}


async def create_responce(user_id: int | str, settings: str, text: str | int):
    # proxy = {
    #     "http": "http://9gfWr9:g0LSUy@131.108.17.194:9799/",
    #     "https": "http://9gfWr9:g0LSUy@131.108.17.194:9799/"
    # }
    try:
        answer = ""
        try:
            users_message[user_id]
        except:
            users_message[user_id] = [{"role": "user", "content": settings}]
        users_message[user_id].append(
            {"role": "user", "content": text})
        responce = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=users_message[user_id],
            temperature=0.7,
        )
        answer = responce.choices[0].message.content

        users_message[user_id].append({"role": "assistant", "content": answer})
    except openai.error.RateLimitError as ex:
        return "RateLimitError"
    except Exception as ex:
        print(ex)
        users_message[user_id] = []
        create_responce(user_id, text)
    return answer
