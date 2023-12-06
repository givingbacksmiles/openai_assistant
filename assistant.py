from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# get the OPENAI_API_KEY from the environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_API_KEY is None:
    raise Exception("The OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=OPENAI_API_KEY)  # Replace with your actual API key


#choose a model
model = "gpt-3.5-turbo-1106"

# choose your assistant
assistant_id = "asst_2wkyPuCP1sTaFitYHru8NgkP"

# or... create a new assistant

# Step 1: Create an Assistant
# assistant = client.beta.assistants.create(
#     model=model,
#     instructions="Your name is Corvus. You answer questions with precision based on the content within the files you have access to.",
#     name="Raven - The Great",
#     tools=[{"type": "retrieval"}, {"type": "code_interpreter"}],
# )
# assistant_id = assistant.id
# print(f"This is the assistant object: {assistant} \n")


# Step 2: Create a Thread
thread = client.beta.threads.create()
print(f"The thread: {thread} \n")

# Step 2.5 (Optional): Add a File to the Thread
# with open(filepath, 'rb') as file:  # Open in binary mode
#         file_content = file.read()

# # Use file_content with OpenAI API
# try:
#     asst_file = client.files.create(
#         file=file_content,
#         purpose="assistants"
#     )
# except Exception as e:
#     print(f"Error uploading file to OpenAI: {e}")

# Step 3: Add a Message to a Thread
thread_message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="What is Bold Crow?",
#   file_ids=[asst_file.id]
)
print(f"The message: {thread_message} \n")

# Step 4: Run the Assistant
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  model=model,
  assistant_id=assistant_id,
  instructions="Your name is Raven. You answer questions with precision based on the content within the files you have access to."
)
print(f"The run: {run} \n")

# Step 5: Periodically retrieve the Run to check on its status to see if it has moved to completed
while run.status != "completed":
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    print(f"Run status: {keep_retrieving_run.status}")

    if keep_retrieving_run.status == "completed":
        print("\n")
        break

# Step 6: Retrieve the Messages added by the Assistant to the Thread
all_messages = client.beta.threads.messages.list(thread_id=thread.id)

print("#################################################### \n")

print(f"User: {thread_message.content[0].text.value}")
print(f"Assistant: {all_messages.data[0].content[0].text.value}")