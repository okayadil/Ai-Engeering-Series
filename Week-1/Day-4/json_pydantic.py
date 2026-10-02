import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key not found")

client = Groq(api_key = my_api_key)

model = "openai/gpt-oss-20b"

role = "user"

# structure it
from pydantic import BaseModel
class Ticket(BaseModel):
    name: str
    email: str
    issue: str

schema = Ticket.model_json_schema()

response_format = {
    "type": "json_object"
}

system_prompt = f"""
Extract the personal information from the ticket strictly based on this schema and give a json output.
{schema}
"""

message_system = {
    "role": "system",
    "content": system_prompt
}

text = "Hello my name is Ammar Adil. I have an iphone which is not working at all. my address is delhi my email is abc@gmail.com. my phone is 12345"
prompt = f"""
This is a customer ticket. Please extract the personal information from this.
{text}
"""

message = {
    "role": role,
    "content": prompt
}

messages = [message_system,message]

response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)

answers = response.choices[0].message.content
print(answers)

# isko padhte kaise hai
import json
raw_json = answers
data_file = json.loads(raw_json)
ticket = Ticket(**data_file)

# isko aage pass kar sakte ho
print(ticket.name)
print(ticket.email)
print(ticket.issue)