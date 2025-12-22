import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def classify_email(email_from, subject, body):
    """
    Uses OpenAI to classify email and extract insights
    """

    prompt = f"""
Analyze this email and provide:
1. Category (Lead/Customer/Spam/Newsletter)
2. Urgency (High/Medium/Low)
3. Main intent (in 1 sentence)
4. Suggested action (in 1 sentence)

Email:
From: {email_from}
Subject: {subject}
Content: {body}

Respond ONLY in JSON format:
{{
  "category": "Lead/Customer/Spam/Newsletter",
  "urgency": "High/Medium/Low",
  "intent": "brief description",
  "suggested_action": "recommended action"
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that analyzes business emails and extracts useful insights."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


def process_emails(csv_file):
    print("🤖 AI Email Intelligence - Processing...\n")

    df = pd.read_csv(csv_file)
    results = []

    # Corregido: i es el contador numérico, (index, row) desempaqueta la fila
    for i, (index, row) in enumerate(df.iterrows()):
        print(f"📧 Analyzing email {i + 1}/{len(df)}...")

        analysis = classify_email(
            row['email_from'],
            row['subject'],
            row['body']
        )

        results.append({
            'email_from': row['email_from'],
            'subject': row['subject'],
            'ai_analysis': analysis
        })
        print(f"   ✅ Completed\n")

    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv('email_analysis_results.csv', index=False)

    print("=" * 60)
    print("✨ Analysis completed!")
    print(f"📊 Results saved to: email_analysis_results.csv")
    print("=" * 60)

    # Show preview
    print("\n📋 Results preview:\n")
    for result in results[:3]:  # Show first 3
        print(f"From: {result['email_from']}")
        print(f"Subject: {result['subject']}")
        print(f"Analysis: {result['ai_analysis']}\n")
        print("-" * 60 + "\n")


if __name__ == "__main__":
    process_emails('sample_emails.csv')
