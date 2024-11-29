import groq
from groq import Groq
from config.config import API_KEY_GROQ

client = Groq(api_key=API_KEY_GROQ)

conversation_history = [
    {
        "content": "Please try to provide useful, helpful and actionable answers.",
        "role": "system"
    }
]

def get_ai_response(messages):
    print(type(messages))
    print(API_KEY_GROQ)
    global conversation_history 

    conversation_history.append({
        "role": "user",
        "content": messages,
    })

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=conversation_history,
        temperature=0.1,
        max_tokens=2048,
        stream=True,
        top_p=1
    )
    print(completion)
    response = "".join(chunk.choices[0].delta.content or "" for chunk in completion)
    print(response)
    return response


