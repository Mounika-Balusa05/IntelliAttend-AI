import streamlit as st
def style_background_home():
    st.markdown("""
        <style>
            .stApp {
                background: #5865F2 !important;
            }

            .stApp div[data-testid="stColumn"] {
                background-color: #E0E3FF !important;
                padding: 1.5rem !important;
                border-radius: 2rem !important;
                margin: 0 0.5rem !important;
                text-align: center !important;        
                align-items: center !important;
            }

            /* ✅ center the image too */
            div[data-testid="stImage"] {
                display: flex !important;
                justify-content: center !important;
            }

            /* ✅ center the button */
            .stButton {
                display: flex !important;
                justify-content: center !important;
            }

            .stButton > button {
                width: auto !important;               
                padding: 10px 30px !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown("""
        <style>
            .stApp {
                background: #E0E3FF !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@100..900&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

            #MainMenu, footer, header {
                visibility: hidden;
            }

            .block-container {
                padding-top: 1rem !important;
            }

            h1 {
                font-family: 'Roboto Slab', sans-serif !important;
                font-size: 3.5rem !important;
                line-height: 0.7 !important;
                margin-bottom: 0.5rem !important;
                color: #E0E3FF !important;
            }

            h2 {
                font-family: 'Roboto Slab', sans-serif !important;
                font-size: 1.5rem !important;
                line-height: 0.9 !important;
                margin-bottom: 0.5rem !important;
                color: #3D3D3D !important;
                text-align: center !important; 
            }

            h3, h4, p {
                font-family: 'Outfit', sans-serif !important;
            }

            

            .stButton > button {
    border-radius: 1.5rem !important;
    background: #5865F2 !important;
    color: white !important;
    border: none !important;
    transition: transform 0.25s ease-in-out !important;

    width: 100% !important;     /* same width */
    height: 50px !important;    /* same height */
    padding: 0px 20px !important;
}

            .stButton > button:hover {
                transform: scale(1.05) !important;
                background: #4752C4 !important;
            }
            
                button[kind="secondary"] {
                background: #EB459E !important;
                color: white !important;
            }

            button[kind="secondary"]:hover {
                background: #c4307e !important;
            }
                button[kind="tertiary"] {
                background: black !important;
                color: white !important;
                border: 1px solid !important;
            }

            button[kind="tertiary"]:hover {
                background: black !important;
            }
            /* always show dataframe toolbar */
[data-testid="stDataFrameToolbar"] {
    visibility: visible !important;
    opacity: 1 !important;
    background: pink !important;
    border-radius: 8px !important;
    padding: 4px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
}

[data-testid="stDataFrameToolbar"] svg {
    fill: #444 !important;
}


        </style>
    """, unsafe_allow_html=True)