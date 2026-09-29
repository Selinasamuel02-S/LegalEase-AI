import streamlit as st
import requests, os
from dotenv import load_dotenv
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")
st.markdown("<h1 style='text-align:center'>⚖️ LegalEase</h1><hr>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    doc_type = st.selectbox("Document Type", ["Employment Contract","NDA (Non-Disclosure Agreement)","Lease Agreement","Freelance Work Contract"])
    parties = st.text_area("Parties", "Jane Doe (Provider), TechNova Inc (Client)")
    terms = st.text_area("Terms (use ;)", "Payment within 30 days; Confidentiality 2 years; 15 days notice")
    dates = st.text_input("Date", "2026-09-29")
with col2:
    generate = st.button("🚀 Generate Document", type="primary", use_container_width=True)

if generate:
    try:
        r = requests.post(f"{BACKEND_URL}/generate", json={"document_type":doc_type,"parties":parties,"terms":terms,"dates":dates}, timeout=60)
        if r.status_code==200:
            st.session_state['doc']=r.json()['document']
            st.session_state['meta']=(doc_type,parties,terms)
    except Exception as e:
        st.error(f"Start backend first: uvicorn legalEaseAPI.main:app --reload | {e}")

if 'doc' in st.session_state:
    st.markdown(f"<div style='background:#1e1e2f;color:#e0e0e0;padding:20px;border-radius:10px;white-space:pre-wrap'>{st.session_state['doc']}</div>", unsafe_allow_html=True)
    edited = st.text_area("Edit Document", st.session_state['doc'], height=300)
    st.download_button("Download TXT", edited, file_name=f"{st.session_state['meta'][0]}.txt")
