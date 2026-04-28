import streamlit as st
import base64

def header_home():
    with open("src/assets/image.jpg", "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode()

    st.markdown(f"""
        <div style='display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px;'>
            <img src='data:image/jpeg;base64,{img_base64}' width='150' style='border-radius:30%; overflow:hidden;'/>
            <h1 style='color:#E0E3FF; font-size:2.5rem;'>IntelliAttend AI</h1>
        </div>
    """, unsafe_allow_html=True)


def header_dashboard():
    with open("src/assets/image.jpg", "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode()

    st.markdown(f"""
        <div style='display:flex; align-items:center; justify-content:center; gap:10px;'>
            <img src='data:image/jpeg;base64,{img_base64}' width='150' style='border-radius:10%; overflow:hidden;'/>
            <h2 style='text-align:left; color:#5865F2; font-size:0.2rem;'>IntelliAttend AI</h2>
        </div>
    """, unsafe_allow_html=True)