import sys
from pathlib import Path

import streamlit as st

from langchain_core.messages import HumanMessage


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# =========================================================
# APPLICATION IMPORTS
# =========================================================

from app.graph.workflow import build_workflow

from app.services.patient_service import (
    get_all_patients,
)

from frontend.components import (
    display_chat_message,
    render_empty_chat,
    render_example_questions,
    render_feature_cards,
    render_footer,
    render_header,
    render_patient_card,
    render_patient_selector,
    render_system_status,
)

from frontend.styles import (
    apply_custom_styles,
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Dental Appointment Assistant",
    page_icon="🦷",
    layout="centered",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM STYLING
# =========================================================

apply_custom_styles()


# =========================================================
# LOAD LANGGRAPH WORKFLOW
# =========================================================

@st.cache_resource
def get_workflow():

    return build_workflow()


graph = get_workflow()


# =========================================================
# LOAD PATIENTS
# =========================================================

@st.cache_data
def load_patients():

    return get_all_patients()


patients = load_patients()


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


if "thread_id" not in st.session_state:

    st.session_state.thread_id = "dental-chat-001"


if "patient_id" not in st.session_state:

    st.session_state.patient_id = None


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-title">
            🦷 Dental Assistant
        </div>

        <div class="sidebar-text">
            Manage dental appointments using
            an intelligent multi-agent system.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        """
        <div class="section-title">
            System
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.success("AI Assistant Online")

    st.caption(
        "LangGraph workflow connected"
    )

    st.caption(
        "MySQL database connected"
    )

    st.caption(
        "Agent tools available"
    )

    st.divider()

    st.markdown(
        """
        <div class="section-title">
            Session
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        f"Thread ID: {st.session_state.thread_id}"
    )

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# MAIN HEADER
# =========================================================

render_header()

render_system_status()


# =========================================================
# PATIENT SELECTION
# =========================================================

selected_patient_id = render_patient_selector(
    patients
)

st.session_state.patient_id = selected_patient_id


render_patient_card(
    st.session_state.patient_id,
    patients,
)


# =========================================================
# FEATURES
# =========================================================

render_feature_cards()

st.divider()


# =========================================================
# CHAT HISTORY
# =========================================================

if not st.session_state.messages:

    render_empty_chat()

else:

    for message in st.session_state.messages:

        display_chat_message(
            message["role"],
            message["content"],
        )


# =========================================================
# EXAMPLE QUESTIONS
# =========================================================

with st.expander(
    "💡 Example requests",
    expanded=False,
):

    render_example_questions()


# =========================================================
# USER INPUT
# =========================================================

user_input = st.chat_input(
    "Ask about your dental appointment..."
)


if user_input:

    # -----------------------------------------------------
    # Display user message
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    display_chat_message(
        "user",
        user_input,
    )


    # -----------------------------------------------------
    # LangGraph configuration
    # -----------------------------------------------------

    config = {

        "configurable": {

            "thread_id":
                st.session_state.thread_id

        }

    }


    # -----------------------------------------------------
    # Execute LangGraph
    # -----------------------------------------------------

    try:

        result = graph.invoke(

            {

                "messages": [

                    HumanMessage(
                        content=user_input
                    )

                ],

                "patient_id":
                    st.session_state.patient_id,

                "intent": None,

                "doctor_id": None,

                "appointment_id": None,

                "date": None,

                "time": None,

                "response": None,

            },

            config=config,

        )


        # -------------------------------------------------
        # Extract response
        # -------------------------------------------------

        response = result.get(

            "response",

            "Sorry, I couldn't process your request.",

        )


    except ValueError as e:

        response = str(e)


    except Exception:

        response = (
            "Sorry, something went wrong while "
            "processing your appointment request."
        )


    # -----------------------------------------------------
    # Store assistant response
    # -----------------------------------------------------

    st.session_state.messages.append(

        {

            "role": "assistant",

            "content": response,

        }

    )


    # -----------------------------------------------------
    # Display assistant response
    # -----------------------------------------------------

    display_chat_message(

        "assistant",

        response,

    )


# =========================================================
# FOOTER
# =========================================================

render_footer()