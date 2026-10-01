import streamlit as st


def apply_custom_styles():

    st.markdown(
        """
        <style>

        .main .block-container {
            max-width: 1000px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1 {
            font-weight: 800;
        }

        h2, h3 {
            font-weight: 700;
        }

        [data-testid="stChatMessage"] {
            border-radius: 12px;
        }

        [data-testid="stChatInput"] {
            border-radius: 12px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )