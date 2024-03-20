# README #

## How do I get set up?

* `pip install -r requirements.txt`

## How to run?

* `python src/app.py`

### How to test? ###

* `curl -X POST http://localhost:5000/api/prompt/device123 --data '<html>hello world</html>' -H 'Content-Type: plain/text'`

* `docker build . -t testup-prompt-service:<version>`

* `docker run -e API_KEY=<api_key>  -p 5001:5000 docker push 757835444551.dkr.ecr.eu-central-1.amazonaws.com/base_default_testup_prompt_service:<version>`