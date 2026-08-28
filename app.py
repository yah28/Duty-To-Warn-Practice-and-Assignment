from datetime import datetime
import anthropic
import streamlit as st
from scenarios import SCENARIOS

# 1. Page Config
st.set_page_config(
    page_title="Optical Dispensing Clinical Simulation",
    page_icon="👓",
    layout="centered",
)

# 2. API Initialization
api_key = st.secrets.get("ANTHROPIC_API_KEY")
if not api_key:
    st.error("Missing ANTHROPIC_API_KEY in Streamlit Secrets.")
    st.stop()

client = anthropic.Anthropic(api_key=api_key)

# 3. Sidebar Setup & Scenario Selection
with st.sidebar:
    st.title("👓 Scenario Portal")

    # Select Scenario
    selected_scenario_name = st.selectbox(
        "Select Clinical Case:", options=list(SCENARIOS.keys())
    )

    scenario_data = SCENARIOS[selected_scenario_name]

    # Display Scenario Metadata
    if scenario_data["type"] == "Graded":
        st.error("🔴 GRADED EVALUATION MODE")
    else:
        st.success("🟢 PRACTICE MODE")

    st.caption(f"**Case Description:** {scenario_data['description']}")

    st.markdown("---")

    # Reset / Load Scenario Button
    if st.button(
        "Start / Reset Selected Scenario",
        use_container_width=True,
        type="primary",
    ):
        st.session_state.current_scenario = selected_scenario_name
        st.session_state.messages = [
            {"role": "assistant", "content": scenario_data["initial_message"]}
        ]
        if "last_hint" in st.session_state:
            del st.session_state["last_hint"]
        st.rerun()

    # Initialize current scenario in state if not set
    if "current_scenario" not in st.session_state:
        st.session_state.current_scenario = selected_scenario_name
        st.session_state.messages = [
            {"role": "assistant", "content": scenario_data["initial_message"]}
        ]

    # Download Transcript Button
    if len(st.session_state.messages) > 1:
        transcript_text = (
            f"SCENARIO: {st.session_state.current_scenario}\nDATE:"
            f" {datetime.now()}\n"
            + "=" * 50
            + "\n\n"
        )
        for msg in st.session_state.messages:
            role = (
                "OPTICIAN (STUDENT)"
                if msg["role"] == "user"
                else "PATIENT / INSTRUCTOR"
            )
            transcript_text += (
                f"[{role}]\n{msg['content']}\n\n" + "-" * 40 + "\n\n"
            )

        st.download_button(
            label="📄 Download Session Transcript",
            data=transcript_text,
            file_name=(
                "clinical_transcript_"
                f"{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            ),
            mime="text/plain",
            use_container_width=True,
        )

    # Instructor Hints Section
    st.markdown("---")
    st.header("💡 Clinical Coach")

    if scenario_data["instructor_hint_prompt"] is None:
        st.warning("🔒 Hints are disabled during Graded Evaluation mode.")
    else:
        if st.button("Get Clinical Hint", use_container_width=True):
            with st.spinner("Analyzing clinical progression..."):
                hint_response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=300,
                    system=scenario_data["instructor_hint_prompt"],
                    messages=st.session_state.messages,
                    temperature=0.3,
                )
                st.session_state.last_hint = hint_response.content[0].text

        if "last_hint" in st.session_state:
            st.info(st.session_state.last_hint)

# 4. Main App Interface
st.title("👓 Clinical Simulation: Optical Dispensing")
st.markdown(f"**Active Case:** `{st.session_state.current_scenario}`")

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Chat Input
if user_input := st.chat_input("Type your clinical response..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # API Call with Active System Prompt
    active_prompt = SCENARIOS[st.session_state.current_scenario][
        "system_prompt"
    ]

    with st.chat_message("assistant"):
        with st.spinner("Patient responding..."):
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                system=active_prompt,
                messages=st.session_state.messages,
                temperature=0.3,
            )
            bot_reply = response.content[0].text
            st.markdown(bot_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )

    if "last_hint" in st.session_state:
            st.info(st.session_state.last_hint)
