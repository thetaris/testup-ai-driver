

def payload_chat_completions_json(model, contents):
    messages = []

    if contents:
        for content in contents:
            messages.append({"role": content['role'], "content": content['message']})

    return {
        "model": model,
        "messages": messages,
        "temperature": 0
    }


def payload_chat_completions(model, system_content, user_content=""):
    return {
        "model": model,
        "messages": [
            {"role": "user", "content": user_content},
            {"role": "system", "content": system_content}
        ]
    }


api_map = {
    "gpt-3.5-turbo-1106": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "payload": payload_chat_completions_json
    },
    "gpt-3.5-turbo": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "payload": payload_chat_completions_json
    }
}

api_map_json = {
    "gpt-3.5-turbo-1106": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "payload": payload_chat_completions_json
    },
    "gpt-3.5-turbo": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "payload": payload_chat_completions_json
    }
}


