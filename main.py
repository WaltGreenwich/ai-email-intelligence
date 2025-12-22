import os
import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


def classify_email(email_from, subject, body):
    """
    Uses Claude (Anthropic) to classify email and extract insights
    """

    prompt = f"""Analyze this email and provide:
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
}}"""

    try:
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=200,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.content[0].text

    except Exception as e:
        return f"Error: {str(e)}"


def process_emails(csv_file):
    print("🤖 AI Email Intelligence (powered by Claude) - Processing...\n")

    # Forzamos a que no use columnas como índice
    df = pd.read_csv(csv_file, index_col=False)

    results = []

    # 'i' será nuestro contador (empezando en 1)
    # 'row' contiene los datos de cada fila
    for i, (_, row) in enumerate(df.iterrows(), 1):
        total_emails = len(df)
        print(f"📧 Analyzing email {i} / {total_emails}...")

        analysis = classify_email(
            str(row['email_from']),
            str(row['subject']),
            str(row['body'])
        )

        # Try to parse JSON for better display
        try:
            parsed = json.loads(analysis)
            formatted_analysis = json.dumps(parsed, indent=2)
        except:
            formatted_analysis = analysis

        results.append({
            'email_from': row['email_from'],
            'subject': row['subject'],
            'ai_analysis': formatted_analysis
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
    for result in results[:3]:
        print(f"From: {result['email_from']}")
        print(f"Subject: {result['subject']}")
        print(f"Analysis:\n{result['ai_analysis']}\n")
        print("-" * 60 + "\n")


if __name__ == "__main__":
    process_emails('sample_emails.csv')
