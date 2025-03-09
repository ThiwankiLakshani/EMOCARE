import streamlit as st
import ollama
import base64

st.set_page_config(page_title="EmoCare")

# Load background image
def get_base64(background):
    with open(background, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bin_str = get_base64("background.png")

# Background styling
st.markdown(f"""
    <style>
        .main{{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

# Generate AI response
def generate_response(user_input):
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})

    try:
        response = ollama.chat(model="llama2:7b", messages=st.session_state['conversation_history'])
        ai_response = response['message']['content']
    except Exception as e:
        ai_response = "I'm having trouble generating a response. Please try again later."

    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
    return ai_response

# Affirmation generator
def generate_affirmation():
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed."
    try:
        response = ollama.chat(model="llama2:7b", messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        return "Sorry, I couldn't generate an affirmation at the moment."

# Meditation guide generator
def generate_meditation_guide():
    prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
    try:
        response = ollama.chat(model="llama2:7b", messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        return "Sorry, I couldn't generate a meditation guide at the moment."

# UI Layout
st.title("Mental Health Support Agent")

# Display conversation history
for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")

# User input
user_message = st.text_input("How can I help you today?")

if user_message:
    with st.spinner("Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")

# Affirmation and Meditation Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Give me a positive Affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("Give me a guided meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Guided Meditation:** {meditation_guide}")
