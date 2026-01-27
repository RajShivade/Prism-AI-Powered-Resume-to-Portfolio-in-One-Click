import streamlit as st
import os
import re
import zipfile
import json
from io import BytesIO
import google.generativeai as genai  # type: ignore
from PyPDF2 import PdfReader

from dotenv import load_dotenv
load_dotenv()


# Page Config
st.set_page_config(
    page_title="Prism | Professional Portfolio Architect",
    page_icon="🪄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Gemini Setup
# Uses the 'API_KEY' environment variable.
API_KEY = os.environ.get("gemini")
if API_KEY:
    genai.configure(api_key=API_KEY)

# =============================================================================
# Custom Aesthetic Styling (Image-Inspired Mesh Gradient)
# =============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

    /* Background Mesh Gradient mimicking user image */
    .stApp {
        background-color: #0f0c29;
        background-image: 
            radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
            radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), 
            radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%), 
            radial-gradient(at 0% 100%, hsla(260,31%,11%,1) 0, transparent 50%), 
            radial-gradient(at 100% 100%, hsla(320,62%,45%,1) 0, transparent 50%);
        background-attachment: fixed;
    }

    * {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Glassmorphism Card Style */
    div[data-testid="stVerticalBlock"] > div:has(div.element-container) {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1rem;
    }

    /* Header Styling */
    .main-title {
        font-size: 4.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(to right, #ffffff, #f472b6, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        letter-spacing: -0.05em;
    }
    
    .subtitle {
        color: rgba(255,255,255,0.6);
        font-size: 1.25rem;
        margin-bottom: 2.5rem;
    }
    .hero-container {
    padding: 0rem 2rem 3rem 2rem;
    max-width: 1100px;
    margin-left: 0;
}

.hero-title {
    font-size: 4rem;
    font-weight: 800;
    color: #ffffff;       /* pure white */
    margin-bottom: 1rem;
    letter-spacing: -0.03em;
}

.hero-subtitle {
    font-size: 1.35rem;
    font-weight: 400;
    color: #ffffff;       /* pure white */
    

    line-height: 1.7;
}
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 16px;
        font-weight: 700;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(168, 85, 247, 0.4);
        border: none;
        color: white;
    }

    /* Custom Input Styling */
    input, textarea, select {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# Header Section
# =============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Prism.</div>
    <div class="hero-subtitle">
        Illuminate your professional identity. Transform PDFs into immersive web experiences.
    </div>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# Main Layout
# =============================================================================
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("### Architect Settings")
    
    with st.container():
        title = st.text_input("Portfolio Title", value="Portfolio 2026")
        
        style_col1, style_col2 = st.columns(2)
        with style_col1:
            ethos = st.selectbox("Design Ethos", ["Futuristic Glass", "Minimalist Dark", "Corporate Neo"])
        with style_col2:
            accent_color = st.color_picker("Accent Color", "#ec4899")

        instructions = st.text_area(
            "Custom Persona & Vibes",
            placeholder="e.g., Make it look like a high-end Silicon Valley startup site with smooth scroll animations.",
            height=150
        )

with col2:
    st.markdown("### 📄 Blueprint Upload")
    
    uploaded_file = st.file_uploader("Drop your Resume (PDF)", type=["pdf"])

    resume_text = ""
    if uploaded_file:
        try:
            reader = PdfReader(uploaded_file)
            resume_text = "".join([page.extract_text() or "" for page in reader.pages]).strip()
            if resume_text:
                st.success("✨ Blueprint scanned successfully!")
                st.info(f"Detected {len(resume_text)} characters of professional data.")
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generation Logic
    if st.button("🚀 Construct My Website"):
        if not API_KEY:
            st.error("API Key missing. Set the API_KEY environment variable.")
        elif not resume_text:
            st.warning("Please upload a resume blueprint first.")
        else:
            with st.spinner("Prism AI is weaving your digital presence..."):
                try:
                    # Initialize Model
                    model = genai.GenerativeModel('gemini-2.5-flash-lite')
                    
                    prompt = f"""
                    Context: You are a world-class Frontend Developer and UI/UX Designer.
                    Task: Convert this resume into a stunning, one-page responsive portfolio website.

                    RESUME DATA:
                    {resume_text[:5000]}

                    USER PREFERENCES:
                    Title: {title}
                    Ethos: {ethos}
                    Accent Color: {accent_color}
                    Vibe: {instructions}

                    TECHNICAL REQUIREMENTS:
                    1. Use modern Tailwind CSS for all styling (via CDN).
                    2. Use Google Fonts (Plus Jakarta Sans).
                    3. Incorporate Lucide Icons for skills/contact (via CDN).
                    4. Sections: Hero (Glassmorphism), About, Experience Timeline, Skills Grid, Projects, and Contact.
                    5. Add smooth scroll animations and hover transitions.
                    6. Return a JSON object with keys: "html", "css", "js".

                    OUTPUT FORMAT:
                    Provide ONLY the JSON object.
                    """

                    response = model.generate_content(prompt)
                    
                    # Extraction (handling potential markdown code blocks)
                    raw_text = response.text
                    clean_json = re.search(r'\{.*\}', raw_text, re.DOTALL)
                    
                    if clean_json:
                        site_data = json.loads(clean_json.group())
                        html_content = site_data.get("html", "<h1>Generation Error</h1>")
                        css_content = site_data.get("css", "")
                        js_content = site_data.get("js", "")

                        # Create Standalone Package
                        zip_buffer = BytesIO()
                        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                            # Inject links if not present
                            if css_content and "styles.css" not in html_content:
                                html_content = html_content.replace("</head>", '<link rel="stylesheet" href="styles.css"></head>')
                            if js_content and "script.js" not in html_content:
                                html_content = html_content.replace("</body>", '<script src="script.js"></script></body>')
                                
                            zf.writestr("index.html", html_content)
                            if css_content: zf.writestr("styles.css", css_content)
                            if js_content: zf.writestr("script.js", js_content)

                        st.session_state.zip_file = zip_buffer.getvalue()
                        st.success("Digital Architecture Complete!")
                    else:
                        st.error("Could not parse AI response. Try again.")

                except Exception as e:
                    st.error(f"Generation failed: {str(e)}")

    if "zip_file" in st.session_state:
        st.download_button(
            label="📂 Download Production Ready Package",
            data=st.session_state.zip_file,
            file_name=f"Prism_Portfolio_{title.replace(' ', '_')}.zip",
            mime="application/zip"
        )


