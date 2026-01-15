from openai import OpenAI
import os

# Initialize the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a friendly and professional restaurant owner.
Your goal is to help customers with catering inquiries over email.
You should be polite, concise, and helpful.

Here is an example of your tone:
"Hi Michelle,
Perfect!
Yes — we are able to accommodate the rush and your employees/guests.
If you are ready to move forward, we can send out an invoice and get the menu finalized.
Let me know if this works!
Thank you."

If you need more information to give a quote, ask for it.
If the customer wants to book, explain the next steps (invoice, menu finalization).
"""

def generate_catering_response(user_inquiry, model="gpt-41-mini"):
  response = client.chat.completions.create(
    model=model,
    messages=[
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": user_inquiry}
    ],
    temperature=0.7, # Slightly higher for more natural tone
  )
  return response.choices[0].message.content

if __name__ == "__main__":
  test_inquiry = """
  Hello! I am reaching out to you on behalf of the La Puente City Foundation. 
  We are a nonprofit organization looking to support our community and 
  wondering if you are interested in participating in our 2026 Lunar New Year celebration. 
  It will occur onFebruary 22nd and set up time will be from 12:00-12:30pm. 
  The event itself has 500 attendees and lasts from 1:00pm-4:30pm at the La Puente park. 
  Please contact us through email if you are available, interested, and for further information! 
  Thank you so much for your time and
  """
  print(f"--- Incoming Email ---\n{test_inquiry}\n")
  
  reply = generate_catering_response(test_inquiry)
  print(f"--- Draft Reply ---\n{reply}")