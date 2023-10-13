import openai 
users_message ={}

openai.api_key ="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"

def create_responce(user_id,text):
    try:
        try:
            users_message[user_id]
        except:
            users_message[user_id] = [{"role": "user", "content": "Ты девушка 20 лет зовут тебя Алена, тебе пишут люди чтобы пообщаться",}]
        users_message[user_id].append(
            {"role": "user", "content": text})        
        responce = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=users_message[user_id]
        )
        
        answer = responce['choices'][0]['message']['content']
        users_message[user_id].append(
            {"role": "assistant", "content": answer})
    except openai.error.RateLimitError as ex:
        print(ex)
        
    except Exception as ex:
        print(ex)
        users_message[user_id] = []

    return responce['choices'][0]['message']['content']
