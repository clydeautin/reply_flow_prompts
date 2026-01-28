from openai import OpenAI
import os
import json
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

load_dotenv()

# Initialize the client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not set")

client = OpenAI(api_key=api_key)

def load_email_from_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

SYSTEM_PROMPT = """
You are an intelligent email classifier for a restaurant/food truck business called "Mad Dumplings".
Your job is to categorize incoming emails and determine if they are safe for auto-reply.

OUTPUT FORMAT:
You must output a valid JSON object with the following fields:
{
  "category": "string",
  "confidence_score": float,
  "safe_to_auto_reply": boolean,
  "reasoning": "string"
}

CATEGORIES:
- "catering_inquiry": Requests for catering, food truck booking, events, large orders.
- "hours_location": Questions about where the truck is, opening hours, schedule.
- "menu_pricing": Questions about specific food items, prices, dietary restrictions (if not a catering request).
- "job_application": Resumes, asking for work, hiring inquiries.
- "spam_sales": SEO services, marketing offers, unsolicited sales pitches.
- "school_event": Requests from schools, PTAs, PTOs, parent-teacher associations, fundraisers,
  school fairs, carnivals, or student-related events that are NOT private catering.
- "other": Anything that doesn't fit the above (e.g., complaints, specific complicated questions, personal messages).

CONFIDENCE SCORE GUIDELINES:
- 0.90–1.00: Very clear signal, unambiguous keywords and intent.
- 0.70–0.89: Mostly clear, but potentially minor ambiguity or missing details.
- 0.50–0.69: Ambiguous, could belong to multiple categories or intent is vague.
- < 0.50: Unclear; defaulting to 'other'.

SAFE_TO_AUTO_REPLY RULES:
Set "safe_to_auto_reply": true ONLY if ALL of the following are true:
1. Category is ONE of: ["catering_inquiry", "hours_location", "menu_pricing"].
2. The email is NOT asking for sensitive info (passwords, financial data).
3. The email is NOT requesting payment or money.
4. The email is NOT legal or medical in nature.
5. The email is NOT hostile, threatening, or a serious complaint.
6. "school_event" emails are NEVER safe to auto-reply.
7. The confidence_score is >= 0.70.

Otherwise, set "safe_to_auto_reply": false.

"""
#school/fundraiser request would be uts own category
def classify_email(email_body, model="gpt-4o-mini"):
  response = client.chat.completions.create(
    model=model,
    messages=[
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": email_body}
    ],
    temperature=0.5, # Low temperature for deterministic classification
    response_format={"type": "json_object"}
  )
  return json.loads(response.choices[0].message.content)

if __name__ == "__main__":
  test_emails = [
    {
      "text": "Hi, I'd like to book your truck for a wedding on May 15th. We expect 100 guests.",
      "expected": "catering_inquiry"
    },
    {
      "text": "Where form are you guys located today? I'm craving dumplings.",
      "expected": "hours_location"
    },
    {
      "text": "Do you have any gluten-free options on the menu?",
      "expected": "menu_pricing"
    },
    {
      "text": "I am a SEO expert and can get your website to rank #1 on Google.",
      "expected": "spam_sales"
    },
    {
      "text": "Hi, are you hiring line cooks? I have 3 years of exp.",
      "expected": "job_application"
    },
    {
      "text": "I found a hair in my food yesterday and I'm very upset. I want a refund immediately.",
      "expected": "other (complaint -> unsafe)"
    },
    {
      "text": "Can you send me your bank details so I can wire the deposit?",
      "expected": "catering_inquiry (unsafe -> payment info)"
    },
    {
      "text": "Our middle school is planning a fundraiser next month and is looking for food trucks to participate.",
      "expected": "school_event"
    }
  ]

# Run the waterfront email file
waterfront_email = load_email_from_file("emails/waterfront_thread.txt")
result = classify_email(waterfront_email)
print("\n--- waterfront_thread.txt ---")
print(json.dumps(result, indent=2))

# Run the hardcoded test
for i, item in enumerate(test_emails, start=1):
  result = classify_email(item["text"])
  print(f"/n--- Test {i} (expected category: {item['expected']}) ---")
  print(json.dumps(result, indent=2))

