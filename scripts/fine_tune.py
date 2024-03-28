import time
from pathlib import Path
from openai import OpenAI
import os
import argparse

parser = argparse.ArgumentParser(description='Fine-tune GPT-3.5 Turbo model with a specified training file.')
parser.add_argument('file_path', type=str, help='Path to the training file')

args = parser.parse_args()

file_path = args.file_path


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

response = client.files.create(
    file=Path(file_path),
    purpose="fine-tune",
)

print(response)
file_id = response.id


try:
    fine_tune_response = client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-3.5-turbo-1106",
    )
except openai.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except openai.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except openai.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)

print(fine_tune_response)

while True:

    first_page = client.fine_tuning.jobs.list(
        limit=20,
    )

    for job in first_page.data:
        print(job)
        if job.status == "succeeded":
            break
    time.sleep(1)

#job
# job.fine_tuned_model
#print command export GPT_MODEL=ft:gpt-3.5-turbo-1106:thetaris::97mA1Kg5