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
print("Going to wait until the fine tuning job starts")
time.sleep(60)
specific_job_running = False
count = 60
while True:
    first_page = client.fine_tuning.jobs.list(
        limit=20,
    )

    # Flag to check if the specific job is found and running
    job_found = False
    for job in first_page.data:
        # Check if the current job's training_file matches the specific file ID
        if job.training_file == file_id:
            job_found = True
            if job.status == "running":
                print(f"Job is still running. {count} seconds elapsed")
                specific_job_running = True
            elif job.status == "succeeded":
                specific_job_running = False
                print("Job has finished successfully")
                print(f"Fined Tuned Model={job.fine_tuned_model}")
                print(f"To use fined tune model, run export GPT_MODEL={job.fine_tuned_model}")
            else:
                specific_job_running = False
                print(f"Found the specific job, but its status is {job.status}.")
            break

    if not job_found:
        print("Unable to find job, please check openai cp")
        break

    if not specific_job_running:
        print("Going to stop since job is not running, please check openai cp")
        break

    count = count+1
    time.sleep(1)

