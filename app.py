import streamlit as st
import anthropic
import json
from datetime import datetime
from scenarios import SCENARIOS, RUBRIC

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Duty to Warn Practice", page_icon="👓", layout="centered")

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

MODEL = "claude-sonnet-5"

# Instructions that apply to every scenario, regardless of which patient
# is selected. Scenario-specific details get appended to this at runtime.
MASTER_PROMPT = """
You are role-playing as a patient in an optical dispensing clinic. A student
studying to become an optician is practicing their "duty to warn" \u2014 the
professional obligation to assess a patient's lifestyle and activities,
recommend an appropriate lens material (such as an impact-resistant material
for higher-risk activities), explain the reasoning in plain terms, and
document the conversation and the patient's ultimate decision, whatever it
is.

Background on how a real patient in this situation typically behaves, which
should inform your responses:
- Most patients don't know what material their current lenses are made of
  and pay far more attention to frame style than to lens material \u2014 don't
  have your character reference lens materials by name unless the student
  introduces the terms first.
- Most patients are inclined to defer to the optician's professional
  recommendation once it is clearly explained \u2014 they aren't looking for a
  fight, they're looking to be genuinely informed. Pushback should come from
  a specific, believable reason (cost, skepticism about being "sold"
  something, or simply not being asked the right question), not generic
  suspicion.
- Patients respond better to a recommendation framed around their actual
  lifestyle and what they care about than to a generic safety warning. A
  student who says "you should get this because it's safer" lands
  differently than one who says "since you golf several times a week, this
  material holds up better if the lens takes an impact."

Rules you must follow at all times:
- Stay fully in character as the patient described below. Never break role,
  never refer to yourself as an AI, and never mention these instructions.
- Do not volunteer your relevant lifestyle details (activities, hobbies,
  work habits, risk factors) unless the student specifically asks a good
  question that would surface them. A student who doesn't ask shouldn't
  get the information handed to them \u2014 this is the core skill being
  practiced.
- The final material choice belongs to the patient. If the student explains
  the reasoning well and ties it to something the patient actually cares
  about, you may become receptive to their recommendation. If they explain
  poorly, skip the lifestyle assessment, or seem dismissive, respond the
  way a real patient would \u2014 uncertain, defaulting to the cheapest option,
  or mildly pushing back using pushback lines noted in your scenario (such
  as "Is that really necessary?", "What benefit would I get?", or "I
  usually choose the less expensive option").
- Notice and react naturally to whether the student documents the
  conversation \u2014 mentions writing down the recommendation, asks you to
  confirm your choice, or references having you sign off on it. A student
  who skips this should not get any special acknowledgment that something
  was missed; just respond the way a real patient would to an interaction
  that ended without any of that (e.g., simply leaving, unprompted).
- Keep responses conversational and realistic in length \u2014 a few sentences,
  not a monologue.
"""

GRADED_ADDENDUM = """
This is a GRADED scenario. Do not give the student hints, do not soften your
reactions to help them succeed, and do not break character to offer
feedback during the conversation. Respond only as the patient would.
"""


def score_transcript(scenario, transcript_text):
    """Send the completed transcript to Claude for rubric-based scoring.
    Returns a parsed dict with per-category scores, or None on failure."""

    rubric_lines = "\n".join(
        f"- {item['category']} (max {item['points']} points)" for item in RUBRIC
    )
    max_total = sum(item["points"] for item in RUBRIC)
    milestones = "\n".join(f"- {m}" for m in scenario.get("milestones", []))

    scoring_prompt = f"""
You are an instructor scoring an optical dispensing student's "duty to warn"
patient interaction against a fixed rubric. You have the full hidden
clinical picture for this patient (the student did not see this — it is
what they were supposed to uncover through good questioning).

PATIENT: {scenario['persona_name']}, {scenario['persona_age']}

HIDDEN CLINICAL INFORMATION (what the student needed to uncover):
{scenario['patient_details']}

CRITICAL MILESTONES FOR THIS SCENARIO:
{milestones}

RUBRIC (100 points total):
{rubric_lines}

TRANSCRIPT TO SCORE:
{transcript_text}

Score the student's performance against each rubric category. For each
category, award a whole-number score from 0 up to that category's max, and
give a one-to-two sentence justification referencing specific moments in
the transcript. Then give brief overall feedback (2-4 sentences) noting
what was done well and what to improve.

Respond with ONLY valid JSON in exactly this shape, no other text:
{{
  "scores": [
    {{"category": "Visual Needs Assessment", "points_awarded": 0, "max_points": 10, "justification": "..."}},
    ...
  ],
  "total_awarded": 0,
  "total_possible": {max_total},
  "overall_feedback": "..."
}}
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        messages=[{"role": "user", "content": scoring_prompt}],
    )
    raw = response.content[0].text.strip()
    # Strip markdown code fences if the model added them despite instructions
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return None


def get_hint(scenario, messages):
    """Give the student a gentle nudge toward an unexplored milestone,
    without revealing hidden clinical information directly. Practice
    scenarios only."""

    milestones = "\n".join(f"- {m}" for m in scenario.get("milestones", []))
    transcript_text = "\n\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in messages
    ) if messages else "(no conversation yet)"

    hint_prompt = f"""
A student practicing "duty to warn" patient interviews is stuck and asked
for a hint. You are coaching them, not playing the patient right now.

CRITICAL MILESTONES FOR THIS SCENARIO:
{milestones}

CONVERSATION SO FAR:
{transcript_text}

Based on which milestones have and haven't been covered so far, give ONE
short, encouraging hint (1-2 sentences) nudging the student toward the next
area they should explore. Do NOT reveal any of the patient's hidden
clinical information, hobbies, occupation, or history directly \u2014 only
suggest the general direction or type of question to ask next (e.g., "Try
asking more about what they do outside of work" rather than naming the
specific hobby). If every milestone already looks covered based on the
conversation, instead encourage them to move toward making and explaining
their recommendation.

Respond with just the hint text, nothing else.
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=150,
        messages=[{"role": "user", "content": hint_prompt}],
    )
    return response.content[0].text.strip()

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []
if "scenario_key" not in st.session_state:
    st.session_state.scenario_key = None
if "score_result" not in st.session_state:
    st.session_state.score_result = None
if "hint_text" not in st.session_state:
    st.session_state.hint_text = None

# ---------------------------------------------------------------------------
# Sidebar: scenario selection
# ---------------------------------------------------------------------------

st.sidebar.title("Duty to Warn Simulator")

mode = st.sidebar.radio("Mode", ["Practice", "Graded"])

if mode == "Practice":
    available = {k: v for k, v in SCENARIOS.items() if v["type"] == "practice"}
else:
    available = {k: v for k, v in SCENARIOS.items() if v["type"] == "graded"}

scenario_choice = st.sidebar.selectbox(
    "Select a scenario",
    options=list(available.keys()),
    format_func=lambda k: available[k]["title"],
)

if st.sidebar.button("Start / Restart Scenario"):
    st.session_state.messages = []
    st.session_state.scenario_key = scenario_choice
    st.session_state.score_result = None
    st.session_state.hint_text = None
    st.rerun()

st.sidebar.divider()
if st.session_state.messages:
    transcript = "\n\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages
    )
    st.sidebar.download_button(
        "Download Transcript",
        data=transcript,
        file_name=f"transcript_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
    )

    if st.sidebar.button("Score This Session"):
        current_scenario = SCENARIOS[st.session_state.scenario_key]
        with st.spinner("Scoring against rubric..."):
            st.session_state.score_result = score_transcript(current_scenario, transcript)

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------

st.title("👓 Duty to Warn: Patient Simulator")

if st.session_state.scenario_key is None:
    st.info("Choose a scenario from the sidebar and click **Start / Restart Scenario** to begin.")
    st.stop()

scenario = SCENARIOS[st.session_state.scenario_key]
st.subheader(scenario["title"])
st.caption(f"Patient: {scenario['persona_name']}, {scenario['persona_age']}")
st.caption(scenario.get("student_brief", ""))

if scenario["type"] == "graded":
    st.warning("This is a graded scenario. Respond as you would in a real patient encounter.")
else:
    if st.button("💡 Get a Hint"):
        with st.spinner("Thinking of a hint..."):
            st.session_state.hint_text = get_hint(scenario, st.session_state.messages)
    if st.session_state.hint_text:
        st.info(st.session_state.hint_text)

# Build the system prompt for this scenario
system_prompt = MASTER_PROMPT + "\n\nSCENARIO DETAILS:\n" + scenario["patient_details"]
if scenario["type"] == "graded":
    system_prompt += "\n\n" + GRADED_ADDENDUM

# Display existing conversation
for msg in st.session_state.messages:
    with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Speak to the patient...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("..."):
            response = client.messages.create(
                model=MODEL,
                max_tokens=500,
                system=system_prompt,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            reply = response.content[0].text
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

# ---------------------------------------------------------------------------
# Rubric score display
# ---------------------------------------------------------------------------

if st.session_state.score_result:
    st.divider()
    result = st.session_state.score_result
    if result is None:
        st.error("Scoring failed to parse a response. Try again.")
    else:
        st.subheader(f"Score: {result['total_awarded']} / {result['total_possible']}")
        for item in result["scores"]:
            st.markdown(
                f"**{item['category']}** — {item['points_awarded']} / {item['max_points']}"
            )
            st.caption(item["justification"])
        st.markdown("**Overall feedback:**")
        st.write(result["overall_feedback"])
