

def payload_chat_completions_json(model, final_content):
    return {
        "model": model,
        "messages": [{"role": "user", "content": final_content}],
        "response_format": {"type": "json_object"}
    }


def payload_chat_completions(model, final_content):
    return {
        "model": model,
        "messages": [{"role": "user", "content": final_content}]
    }

def payload_completions(model, final_content):
    return {
        "model": model,
        "prompt": final_content
    }

api_map = {
    "gpt-3.5-turbo-1106": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "payload": payload_chat_completions
    },
    "gpt-3.5-turbo-instruct": {
        "endpoint": "https://api.openai.com/v1/completions",
        "payload": payload_completions
    }
}

api_map_json = {
    "gpt-3.5-turbo-1106": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "payload": payload_chat_completions_json
    },
    "gpt-3.5-turbo-instruct": {
        "endpoint": "https://api.openai.com/v1/completions",
        "payload": payload_completions
    }
}
