import streamlit as st
import pandas as pd
import google.generativeai as genai
import json
import io
import time

# Configuración de página
st.set_page_config(
    page_title="AI Email Intelligence",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS mejorado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #4285F4 0%, #34A853 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🤖 AI Email Intelligence</h1>',
            unsafe_allow_html=True)
st.markdown('<p class="subtitle">Intelligent email classification powered by Google Gemini 1.5</p>',
            unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    # Intentamos obtener la clave de los secretos (local o nube)
    secret_key = st.secrets.get("GEMINI_API_KEY")

    if secret_key:
        api_key = secret_key
        st.success("✅ API Key loaded securely")
    else:
        # Si no hay secretos, mostramos el input (útil para que otros prueben con su propia clave)
        api_key = st.text_input("Gemini API Key", type="password")

    st.markdown("---")
    st.markdown("### 🎯 Key Extraction")
    st.markdown("- **Category**: Sales, Support, Spam, etc.\n- **Urgency**: Priority scoring.\n- **Intent**: Core message extraction.\n- **Action**: Next steps.")

    st.markdown("---")
    st.markdown("### 🔧 Tech Stack")
    st.code("Gemini 1.5 Flash\nPython\nStreamlit\nPandas", language="text")

    st.markdown("### 👨‍💻 Built by")
    st.markdown("[Walter Greenwich](https://github.com/WaltGreenwich)")

# Lógica de la API
if not api_key:
    st.warning("👈 Please enter your Gemini API key in the sidebar to continue")
    st.info(
        "💡 **Don't have a key?** Get one for free at [aistudio.google.com](https://aistudio.google.com)")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-flash-latest')

    tab1, tab2 = st.tabs(["📤 Bulk Analysis", "✍️ Single Email"])

    with tab1:
        uploaded_file = st.file_uploader(
            "Upload CSV (email_from, subject, body)", type=['csv'])

        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.success(f"Loaded {len(df)} emails")

            if st.button("🚀 Run AI Analysis"):
                results = []
                progress_bar = st.progress(0)

                for index, row in df.iterrows():
                    prompt = f"""Return ONLY a JSON:
                    {{
                      "category": "Lead/Customer/Spam/Newsletter",
                      "urgency": "High/Medium/Low",
                      "intent": "1 sentence",
                      "action": "1 sentence"
                    }}
                    Email: From {row['email_from']}, Subject: {row['subject']}, Body: {row['body']}"""

                    try:
                        response = model.generate_content(prompt)
                        # Limpieza de la respuesta para asegurar JSON válido
                        clean_text = response.text.replace(
                            '```json', '').replace('```', '').strip()
                        parsed = json.loads(clean_text)
                        results.append({
                            'From': row['email_from'],
                            'Category': parsed.get('category'),
                            'Urgency': parsed.get('urgency'),
                            'Intent': parsed.get('intent'),
                            'Suggested Action': parsed.get('action')
                        })
                    except:
                        results.append(
                            {'From': row['email_from'], 'Error': 'Failed to parse'})

                    progress_bar.progress((index + 1) / len(df))
                    time.sleep(1)  # Respetar rate limits

                res_df = pd.DataFrame(results)
                st.dataframe(res_df, use_container_width=True)
                st.download_button("📥 Download Results", res_df.to_csv(
                    index=False), "results.csv", "text/csv")

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            e_from = st.text_input("Sender")
            e_subj = st.text_input("Subject")
        with col2:
            e_body = st.text_area("Content")

        if st.button("🔍 Analyze Now"):
            with st.spinner("AI is thinking..."):
                prompt = f"Analyze this email and return JSON with category, urgency, intent, action: {e_body}"
                response = model.generate_content(prompt)
                st.json(response.text.replace(
                    '```json', '').replace('```', '').strip())

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center;'>AI Email Intelligence | applied-ai-series</div>",
            unsafe_allow_html=True)
