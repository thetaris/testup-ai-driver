# README #

## How do I get set up?

* `pip install -r requirements.txt`

## How to run?

* `python src/app.py`

### How to test? ###

* `curl -X POST http://localhost:5000/api/prompt/device123 --data '<html>hello world</html>' -H 'Content-Type: plain/text'`

* `docker build . -t testup-prompt-service:<version>`

* `docker run -e API_KEY=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 -e GPT_MODEL=gpt-3.5-turbo-1106 -e GPT_CHECK_PROMPT="Is this action possible given the provided markdown" -p 5001:5000 docker push 757835444551.dkr.ecr.eu-central-1.amazonaws.com/base_default_testup_prompt_service:1.0.0`