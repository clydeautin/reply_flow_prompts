from openai import OpenAI
import os

# Initialize the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are acting as a catering assistant for Mad Dumplings, a food truck business.

PRIMARY OBJECTIVE
Respond to the customer’s initial catering inquiry with a polite, professional, and concise email that:
1. Confirms availability or interest.
2. States that the catering menu sheet is attached.
3. Clearly mentions base pricing ($16+ tax per guest).
4. Invites the customer to review the attached menu and reach out with any questions.

CONDITIONAL LOGIC
- If the customer has NOT provided a guest count, you may ask exactly ONE question requesting the estimated guest count.
- If a guest count IS already provided, do NOT ask any questions.

GUEST COUNT DETECTION (IMPORTANT)
- Treat these as the same thing: guest count, guests, attendees, attendance, headcount, people.
- If the customer message includes any of the above AND a number (e.g., "500 attendees"), then guest count IS PROVIDED.
- Only ask for an estimated guest count if NO such number is present.

STRICT CONSTRAINTS
- This is the FIRST reply in the conversation.
- Do NOT ask about menu preferences, dietary needs, or event logistics.
- Do NOT ask multiple questions.
- Do NOT request dates, times, or location clarification.
- Do NOT mention next steps beyond reviewing the menu and answering questions.
- Do NOT reference internal reasoning or assumptions.

ASSUMPTIONS YOU MAY MAKE
- Mad Dumplings operates food trucks.
- A catering menu PDF is attached to the email.
- Pricing starts at $16+ tax per guest.

TONE AND STYLE
- Friendly, warm, and professional.
- Short paragraphs.
- Clear and direct.
- No sales pressure.
- No emojis.

OUTPUT FORMAT
- Write a complete email.
- Include a greeting, body, and sign-off.
- Do not include a subject line.
"""

def generate_catering_response(user_inquiry, model="gpt-4o-mini"):
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
  test_inquiry1 = """
  Hello! I am reaching out to you on behalf of the La Puente City Foundation. 
  We are a nonprofit organization looking to support our community and 
  wondering if you are interested in participating in our 2026 Lunar New Year celebration. 
  It will occur onFebruary 22nd and set up time will be from 12:00-12:30pm. 
  The event itself has 500 attendees and lasts from 1:00pm-4:30pm at the La Puente park. 
  Please contact us through email if you are available, interested, and for further information! 
  Thank you so much for your time and
  """

 #Guest count present (attendees)#
  test_inquiry2 = """
    Hello! I’m reaching out on behalf of the Pasadena Community Center.
    We’re planning a summer fundraiser on July 10th and are exploring catering options.
    The event will have approximately 150 attendees and will run from 5:00pm–8:00pm.
    Let us know if you might be available and interested.
    Thank you!
  """
#Guest count present (guests)
  test_inquiry3 = """
    Hi there,
    We’re organizing a company appreciation lunch and are interested in catering.
    We expect around 75 guests and the event will be held outdoors.
    Please let us know if Mad Dumplings is available.
    Best,
  """
#Guest count present (people)
  test_inquiry4 = """
   Hello,
  I’m planning a birthday celebration at a local park and looking into food trucks.
  We’re expecting about 40 people.
  Would love to hear if you’re available.
  Thanks!
  """
#Guest count missing (explicit)
  test_inquiry5 = """
  Hi,
  I’m planning a community event in late August and wanted to ask about catering options.
  The event will be in the evening and held outdoors.
  Let me know if you’re interested and available.
  Thank you!
  """
# Guest count missing (vague wording)
  test_inquiry6 = """
  Hello Mad Dumplings,
  We’re hosting a neighborhood celebration and exploring food truck catering.
  It will be a medium-sized gathering at a public park.
  Please let us know if you’re available.
  """
#Ambiguous phrasing (no number)
  test_inquiry7 = """
  Hi,
  We’re planning an office event and expect a decent turnout.
  We’re considering food truck catering and wanted to learn more.
  Looking forward to hearing from you.
  """

# Range provided
  test_inquiry8 = """
  Hello,
  We’re organizing a school fundraiser and are expecting between 200–250 attendees.
  The event will be on a Saturday afternoon.
  Please let us know if you’re interested.
  Thanks!
  """

# Large event, nonprofit framing
  test_inquiry9 = """
  Hello,
  I’m reaching out on behalf of a local nonprofit organizing a cultural festival.
  We expect approximately 1,000 people throughout the afternoon.
  We’d love to know if Mad Dumplings might be interested in participating.
  Thank you for your time.
  """

# Casual, short inquiry (guest count missing)
  test_inquiry10 = """
  Hi!
  Quick question—do you do catering for private events?
  Looking to book a food truck later this year.
  Thanks!
  """
# Multiple numbers, but none are guests
  test_inquiry11 = """
  Hello,
  We’re hosting an event from 3:00pm–7:00pm at a local venue.
  Setup would start around 2:00pm.
  We’re exploring catering options and would love to connect.
  Best,
  """

  
#   print(f"--- Incoming Email ---\n{test_inquiry1}\n")
  
#   reply = generate_catering_response(test_inquiry1)
#   print(f"--- Draft Reply ---\n{reply}") # passed

#   print(f"--- Incoming Email ---\n{test_inquiry2}\n")
  
#   reply = generate_catering_response(test_inquiry2)
#   print(f"--- Draft Reply ---\n{reply}") # passed

#   print(f"--- Incoming Email ---\n{test_inquiry3}\n")
  
#   reply = generate_catering_response(test_inquiry3)
#   print(f"--- Draft Reply ---\n{reply}") #passed

#   print(f"--- Incoming Email ---\n{test_inquiry4}\n")
  
#   reply = generate_catering_response(test_inquiry4)
#   print(f"--- Draft Reply ---\n{reply}") # passed

#   print(f"--- Incoming Email ---\n{test_inquiry5}\n")
  
#   reply = generate_catering_response(test_inquiry5)
#   print(f"--- Draft Reply ---\n{reply}") # passed

#   print(f"--- Incoming Email ---\n{test_inquiry6}\n")
  
#   reply = generate_catering_response(test_inquiry6)
#   print(f"--- Draft Reply ---\n{reply}") # passed

#   print(f"--- Incoming Email ---\n{test_inquiry7}\n")
  
#   reply = generate_catering_response(test_inquiry7)
#   print(f"--- Draft Reply ---\n{reply}") #passed

#   print(f"--- Incoming Email ---\n{test_inquiry8}\n")
  
#   reply = generate_catering_response(test_inquiry8)
#   print(f"--- Draft Reply ---\n{reply}") # passed

#   print(f"--- Incoming Email ---\n{test_inquiry9}\n")
  
#   reply = generate_catering_response(test_inquiry9)
#   print(f"--- Draft Reply ---\n{reply}")

#   print(f"--- Incoming Email ---\n{test_inquiry10}\n")
  
#   reply = generate_catering_response(test_inquiry10)
#   print(f"--- Draft Reply ---\n{reply}") # passed

  print(f"--- Incoming Email ---\n{test_inquiry11}\n")
  
  reply = generate_catering_response(test_inquiry11)
  print(f"--- Draft Reply ---\n{reply}") # passed