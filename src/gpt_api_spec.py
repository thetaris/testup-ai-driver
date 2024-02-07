

def payload_chat_completions_json(model, system_content, user_content, history_content=None):
    # Initialize the messages list with the history content
    messages = [{"role": "assistant", "content": f"{history_content}"}, {"role": "user", "content": user_content},
                {"role": "system", "content": system_content}]

    # Append the current user and system messages to the messages list

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


