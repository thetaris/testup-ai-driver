

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

def payload_chat_completions_claude_json(model, contents):
    messages = []
    is_first = True
    if contents:
        for content in contents:
            if content['role'] == "system":
                system = content['message']
            else:
                messages.append({"role": content['role'], "content": content['message']})
                if is_first:
                    messages.append({"role": "assistant", "content": "Ok, what is your task"})
                    is_first= False


    return {
        "system": system,
        "model": model,
        "messages": messages,
        "temperature": 0,
        "max_tokens": 2000
    }

api_map_json = {
    "gpt-3.5-turbo-1106": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "payload": payload_chat_completions_json
    },
    "gpt-3.5-turbo": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "payload": payload_chat_completions_json
    },
    "claude-3-opus-20240229": {
        "endpoint": "https://api.anthropic.com/v1/messages",
        "payload": payload_chat_completions_claude_json
    },
    "claude-3-haiku-20240307": {
        "endpoint": "https://api.anthropic.com/v1/messages",
        "payload": payload_chat_completions_claude_json
    },
    "claude-3-sonnet-20240229": {
        "endpoint": "https://api.anthropic.com/v1/messages",
        "payload": payload_chat_completions_claude_json
    }


}
