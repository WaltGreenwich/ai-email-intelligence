import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import json
import time
import warnings

# Ocultar avisos para una terminal limpia para LinkedIn
warnings.filterwarnings("ignore", category=FutureWarning)

load_dotenv()

# Configuración con el modelo que confirmamos que funciona en tu cuenta
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('models/gemini-flash-latest')


def classify_email(email_from, subject, body):
    # Prompt mejorado para extraer los 4 campos de tu README
    prompt = f"""Analyze this email and provide a structured analysis.
    
    Email Details:
    From: {email_from}
    Subject: {subject}
    Content: {body}
    
    Respond ONLY in JSON format with these exact keys:
    {{
      "category": "Lead/Customer/Spam/Newsletter",
      "urgency": "High/Medium/Low",
      "intent": "Short description of what the sender wants",
      "suggested_action": "Recommended next step"
    }}"""

    try:
        response = model.generate_content(prompt)
        res_text = response.text
        # Limpieza de markdown
        if "{" in res_text:
            res_text = res_text[res_text.find("{"):res_text.rfind("}")+1]
        return res_text
    except Exception as e:
        return f"Error: {str(e)}"


def process_emails(csv_file):
    print("\n🤖 AI Email Intelligence (Powered by Gemini) - Processing...\n")

    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"❌ Error al leer CSV: {e}")
        return

    results = []
    for i, (_, row) in enumerate(df.iterrows(), 1):
        print(f"📧 Analyzing email {i}/{len(df)}...")

        analysis = classify_email(
            row['email_from'], row['subject'], row['body'])

        try:
            parsed = json.loads(analysis)
            formatted = json.dumps(parsed, indent=2)
        except:
            formatted = analysis

        results.append({
            'email_from': row['email_from'],
            'subject': row['subject'],
            'ai_analysis': formatted
        })
        # Pausa de seguridad para la cuota gratuita
        time.sleep(2)

    # Guardar resultados
    pd.DataFrame(results).to_csv('email_analysis_results.csv', index=False)

    print("\n" + "="*60)
    print("✨ Analysis completed successfully!")
    print("="*60)

    # Vista previa para tu captura de LinkedIn
    print("\n📋 DETAILED RESULTS PREVIEW:\n")
    for res in results[:2]:  # Mostramos los 2 mejores ejemplos
        print(f"From: {res['email_from']}")
        print(f"Analysis:\n{res['ai_analysis']}")
        print("-" * 40)


if __name__ == "__main__":
    process_emails('sample_emails.csv')
