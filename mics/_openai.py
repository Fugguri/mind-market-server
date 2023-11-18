import httpx
from openai import RateLimitError
from openai import OpenAI
from dotenv import dotenv_values
config = dotenv_values(".env")
proxy = config["proxy"]
openai = OpenAI(
    api_key=config['openAi'],

    http_client=httpx.Client(
        proxies=proxy,
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)

users_message = {}


async def create_responce(user_id: int | str, settings: str, text: str | int):
    try:
        answer = ""

        if not users_message.get(user_id):
            users_message[user_id] = [{"role": "user", "content": settings}]
            users_message[user_id].append(
                {"role": "user", "content": text})
        else:
            current_settings = users_message[user_id][0].get("content")
            if settings != current_settings:
                users_message[user_id] = [
                    {"role": "user", "content": settings}]
                users_message[user_id].append(
                    {"role": "user", "content": text})

        response = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=users_message[user_id],
            temperature=0.7,
            max_tokens=100
        )

        answer = response.choices[0].message.content

        users_message[user_id].append({"role": "assistant", "content": answer})
    except RateLimitError as ex:
        return "RateLimitError"
    except Exception as ex:
        users_message[user_id] = []
        create_responce(user_id, text)

    return answer
