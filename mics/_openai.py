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


async def create_response(user_id: int | str, settings: str, text: str | int):
    try:
        answer = ""

        if not users_message.get(user_id):
            users_message[user_id] = [{"role": "system", "content": settings}]
            users_message[user_id].append({"role": "user", "content": text})
            print("hasnt message history")
        else:
            current_settings = users_message[user_id][0].get("content")
            print("checking message history")
            if settings != current_settings:
                users_message[user_id] = [
                    {"role": "user", "content": settings}]
            users_message[user_id].append({"role": "user", "content": text})

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=users_message[user_id],
            temperature=0.7,
            # max_tokens=300,
        )
        answer = response.choices[0].message.content
        users_message[user_id].append({"role": "assistant", "content": answer})
    except RateLimitError as ex:
        return "RateLimitError"
    except Exception as ex:
        users_message[user_id] = [
            {"role": "user", "content": settings}]
        create_response(user_id, settings, text)

    return answer
