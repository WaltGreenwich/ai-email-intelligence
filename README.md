# 🤖 AI-Email-Intelligence: Automated Classification & Analysis with Gemini 2.0

Intelligent email classification and analysis using **Google Gemini 2.0 Flash**. This system automatically categorizes emails, assesses urgency, extracts intent, and suggests actions—going beyond simple rule-based classification.

## 🎯 Problem It Solves

Sales and support teams receive hundreds of emails daily. Manual triage is:

- **Time-consuming**: 15–20 minutes per batch.
- **Inconsistent**: Subjective classification by different team members.
- **Surface-level**: Traditional rules miss deep insights and actual intent.

## 💡 Why AI for Email Triage?

AI excels where traditional filters fail:

- **Contextual Understanding**: Recognizes the difference between "I need help" and "I'm leaving if this isn't fixed."
- **Insight Extraction**: Goes beyond labels to provide summaries and next steps.
- **Scale**: Analyzes unstructured data at scale with zero fatigue.

This is a perfect use case for **LLMs** - analyzing unstructured data at scale.

## 🏗️ How It Works

```
Email CSV → Python Script → Google Gemini API → Structured Analysis → CSV Output
```

1. **Ingest**: Reads email data from a local CSV file using Pandas.
2. **Analyze**: Sends content to Gemini 2.0 Flash with a structured system prompt.
3. **Parse**: Extracts four key data points: category, urgency, intent, and suggested_action.
4. **Export**: Generates a results CSV ready for CRM or workflow automation.

## 🔧 Tech Stack

- **Google Gemini API** (models/gemini-flash-latest) - LLM for high-speed intelligent analysis.
- **Python 3.x** - Core application logic.
- **Pandas** - Efficient data manipulation and CSV handling.
- **Python-dotenv** - Secure management of API credentials.

## 🚀 Quick Start

1. Clone repo:

```bash
git clone https://github.com/WaltGreenwich/ai-email-intelligence
cd ai-email-intelligence
```

2. Install dependencies:

```bash
pip install pandas google-generativeai python-dotenv
```

3. Setup Credentials: Obtain your API Key from Google AI Studio and create a .env file:

```bash
GEMINI_API_KEY=your_google_api_key_here
```

4. Run:

```bash
python main.py
```

## 📊 Sample Output

```json
{
  "category": "Lead",
  "urgency": "High",
  "intent": "Interested in enterprise pricing and product capabilities",
  "suggested_action": "Forward to sales team, schedule demo within 24h"
}
```

## 🔮 Future Enhancements

- [ ] RAG integration for context from past conversations
- [ ] Fine-tuning on company-specific email patterns
- [ ] Real-time processing via webhook integration
- [ ] Sentiment analysis for customer emails
- [ ] Integration with CRM (Salesforce, HubSpot)
- [ ] n8n workflow for end-to-end automation

## 🧠 Why This Approach?

- **AI-First Design:** The intelligent analysis is the core value, not a side feature.

- **Cost-Efficient:** Uses the Flash model to balance high intelligence with low latency/cost.

- **Ready for Production:** Structured JSON output makes it easy to integrate into any modern tech stack.

## 📝 Use Cases

- **Sales Teams:** Instantly identify and prioritize "hot" leads.

- **Customer Support:** Route tickets based on actual technical intent.

- **Ops:** Filter noise and automated newsletters from human communications.

## 👨‍💻 Author

Built by Walter Greenwich - exploring applied AI in workflow automation.

Connect: [LinkedIn](https://www.linkedin.com/in/waltgreenwich/) | [Portfolio](https://TU_PORTFOLIO.com)

---

**Note**: This is a learning project demonstrating AI-first design. For production, add error handling, rate limiting, and cost optimization.


