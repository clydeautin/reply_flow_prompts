from openai import OpenAI
client = OpenAI()
r = client.responses.create(model="gpt-4.1-mini", input="ping")
print(r.output_text)