import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="📝", layout="centered")

st.title("📝 AI Content Assistant")
st.write("Generate tailored posts with captions and hashtags for any platform.")

# Sidebar for API Key
st.sidebar.header("Configuration")
groq_api_key = st.sidebar.text_input("Groq API Key:", type="password")

# Input Form
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        platform = st.selectbox(
            "Platform",
            ["LinkedIn", "Twitter / X", "Instagram", "Facebook", "Blog Post"]
        )
        content_type = st.selectbox(
            "Content Type",
            ["Educational", "Promotional", "Personal Story", "Announcement", "Industry Update"]
        )
        tone = st.selectbox(
            "Tone",
            ["Professional", "Casual & Friendly", "Persuasive", "Inspirational", "Humorous"]
        )

    with col2:
        topic = st.text_input("Topic", placeholder="e.g., Remote Work Productivity")
        target_audience = st.text_input("Target Audience", placeholder="e.g., Software Developers, Founders")

    submitted = st.form_submit_button("Generate Post")

# Content Generation Logic
if submitted:
    if not groq_api_key:
        st.error("Please enter your Groq API key in the sidebar.")
    elif not topic or not target_audience:
        st.warning("Please fill in both the Topic and Target Audience fields.")
    else:
        try:
            client = Groq(api_key=groq_api_key)
            
            prompt = f"""
            You are an expert social media content creator. Write a complete post based on the following details:

            - Platform: {platform}
            - Content Type: {content_type}
            - Topic: {topic}
            - Target Audience: {target_audience}
            - Tone: {tone}

            Structure the response clearly as follows:
            1. **Main Post Content / Hook**
            2. **Caption** (if applicable for the platform, or call-to-action)
            3. **Relevant Hashtags** (5 to 10 hashtags)
            """

            with st.spinner("Generating your content..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000,
                )
                
                generated_text = response.choices[0].message.content

            st.success("Generated Content:")
            st.markdown(generated_text)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
