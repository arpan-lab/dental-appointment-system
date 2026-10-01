import streamlit as st


def render_header():
    st.title("🦷 Dental Appointment Assistant")

    st.caption(
        "Your intelligent assistant for managing "
        "dental appointments."
    )

    st.info(
        "✨ AI-Powered · LangGraph · MySQL"
    )


def render_system_status():
    st.success(
        "🟢 AI Assistant is ready"
    )


def render_patient_selector(
    patients: list[dict],
) -> str:

    if not patients:
        st.error(
            "No patients found in the database."
        )
        return ""

    patient_options = {
        f"{patient['name']} · {patient['patient_id']}":
        patient["patient_id"]
        for patient in patients
    }

    selected_label = st.selectbox(
        "👤 Select Patient",
        options=list(patient_options.keys()),
        help="Select the patient for this appointment session.",
    )

    return patient_options[selected_label]


def render_patient_card(
    patient_id: str,
    patients: list[dict],
):

    patient = next(
        (
            patient
            for patient in patients
            if patient["patient_id"] == patient_id
        ),
        None,
    )

    if patient is None:
        return

    col1, col2 = st.columns([1, 5])

    with col1:
        st.markdown("### 👤")

    with col2:
        st.markdown(
            f"**{patient['name']}**"
        )

        st.caption(
            f"Current Patient · ID: {patient['patient_id']}"
        )


def render_feature_cards():

    st.subheader("What I can help with")

    columns = st.columns(4)

    features = [
        (
            "📅",
            "Book",
            "Schedule a new appointment.",
        ),
        (
            "❌",
            "Cancel",
            "Cancel an existing appointment.",
        ),
        (
            "🔄",
            "Reschedule",
            "Move your appointment.",
        ),
        (
            "🔎",
            "Information",
            "Find doctors and appointments.",
        ),
    ]

    for column, feature in zip(
        columns,
        features,
    ):

        icon, title, description = feature

        with column:

            st.markdown(f"### {icon}")

            st.markdown(
                f"**{title}**"
            )

            st.caption(description)


def render_example_questions():

    st.subheader("💡 Try asking")

    st.caption(
        "You can use natural language to interact "
        "with the assistant."
    )

    examples = [
        "What orthodontists are available?",
        "Book me with Dr. Michael Smith on 2026-10-17 at 10:00 AM.",
        "Show my appointments.",
        "Cancel my latest appointment.",
        "Reschedule my appointment to 2026-10-20 at 10:00 AM.",
    ]

    for example in examples:

        st.caption(
            f"💬 {example}"
        )


def display_chat_message(
    role: str,
    content: str,
):

    with st.chat_message(role):
        st.write(content)


def render_empty_chat():

    st.markdown("### 💬 Start a conversation")

    st.caption(
        "Ask me anything about your dental appointment."
    )


def render_footer():

    st.divider()

    st.caption(
        "🦷 Dental Appointment Assistant · "
        "Powered by LangGraph, SQLAlchemy and MySQL"
    )