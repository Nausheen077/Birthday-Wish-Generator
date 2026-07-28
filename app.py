import streamlit as st

st.set_page_config(page_title="Birthday Wish Generator", page_icon="🎂", layout="centered")

st.title("🎉 Birthday Wish Generator")
st.caption("A cheerful chatbot that builds a personalized birthday wish step by step.")

if "profile" not in st.session_state:
    st.session_state.profile = {}
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I can help you create a birthday wish. What is the birthday person's name?",
        }
    ]


def build_wish(name, relation, tone, age, extra_detail):
    relation_text = {
        "friend": "friend",
        "sibling": "sibling",
        "parent": "parent",
        "partner": "partner",
        "colleague": "colleague",
    }.get(relation.lower(), "special person")

    tone_templates = {
        "funny": [
            f"Happy Birthday, {name}!",
            "Hope your day is filled with cake, laughter, and zero responsibilities.",
            "May this year bring you amazing surprises and plenty of reasons to smile.",
        ],
        "heartfelt": [
            f"Happy Birthday, {name}!",
            "On your special day, I hope you feel loved, appreciated, and celebrated.",
            "You deserve all the joy and happiness this year has to offer.",
        ],
        "sweet": [
            f"Happy Birthday, {name}!",
            "Wishing you a day full of love, warmth, and beautiful memories.",
            "May your year ahead be bright, peaceful, and full of happiness.",
        ],
        "short": [
            f"Happy Birthday, {name}!",
            "Wishing you a fantastic day and a wonderful year ahead.",
        ],
    }

    template = tone_templates.get(tone.lower(), tone_templates["sweet"])
    lines = [template[0], template[1]]
    if len(template) > 2:
        lines.append(template[2])

    if age:
        lines.append(f"Hope your {age}th birthday is extra special!")

    if extra_detail:
        lines.append(extra_detail)

    lines.append(f"With lots of love from your {relation_text}.")
    return "\n".join(lines)


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Type your reply here...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    user_input = prompt.strip()
    lower_input = user_input.lower()

    if "name" not in st.session_state.profile:
        st.session_state.profile["name"] = user_input
        reply = "Lovely! How are you related to them? Choose friend, sibling, parent, partner, colleague, or other."
    elif "relation" not in st.session_state.profile:
        st.session_state.profile["relation"] = lower_input
        reply = "Great. What tone do you want? Choose funny, heartfelt, sweet, or short."
    elif "tone" not in st.session_state.profile:
        st.session_state.profile["tone"] = lower_input
        reply = "Perfect. What age are they turning? You can also reply with 'skip'."
    elif "age" not in st.session_state.profile:
        if lower_input in {"skip", "none", "no", ""}:
            st.session_state.profile["age"] = ""
        else:
            st.session_state.profile["age"] = user_input
        reply = "Wonderful. Any extra detail you want included? You can say 'none' or skip."
    else:
        if lower_input in {"none", "skip", "no", ""}:
            st.session_state.profile["extra_detail"] = ""
        else:
            st.session_state.profile["extra_detail"] = user_input

        wish = build_wish(
            st.session_state.profile["name"],
            st.session_state.profile["relation"],
            st.session_state.profile["tone"],
            st.session_state.profile.get("age", ""),
            st.session_state.profile.get("extra_detail", ""),
        )
        reply = f"Here’s your birthday wish:\n\n{wish}\n\nIf you want, I can make it funnier, shorter, or more heartfelt."
        st.session_state.profile = {}
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)
        st.stop()

    
