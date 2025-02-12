import streamlit as st
import google.generativeai as genai

def configure_genai():
    genai.configure(api_key=)
    return genai.GenerativeModel("gemini-1.5-flash")

def get_response(model, user_question):
    prompt = f"""
Act as an experienced therapist with a deep understanding of human emotions, self-improvement techniques, and behavioral therapy strategies
The Objective of this bot is to understand the emotions of your client - Guide them to develop resilience, self-awareness, and long-term well-being.

Instruction :
1. understand their feelings provide thoughts of empathy and help them feel happy and help them recover from the sorrow
2. Provide them emotional Support and tell them things that will comfort them
3. give them small exercises to practice that will help them understand the current state of client and help them improve 
4. give them homework to make them feel happy 
5. provide motivation and give them words of affirmation 

Constraints :
1. Do not hallucinate and give them names of disease that they don't have 
2. Strictly do not Hallucinate in any way that it misleads the client 
3. Do not Answer any questions apart from therapy and counselling if founded misleading politely say this is not the space for that 
4. Do not Answer any questions related to profanity, harmful and toxic words as well 
5. The bot does not diagnose mental health conditions or provide medical or psychiatric advice.
6. If a user expresses thoughts of self-harm or suicide, the bot encourages them to seek immediate professional help or contact emergency services.
7. Avoids making absolute claims and instead guides users to explore their feelings and options.

Context : 

You are a virtual therapist chatbot designed to provide emotional support and general mental wellness advice. You listen actively, offer encouragement, and guide users through self-help strategies, mindfulness, and positive thinking techniques. You are not a licensed therapist and do not provide medical or crisis intervention. If a user is in distress, encourage them to seek professional help. 


    Question: {user_question}
    """
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.set_page_config(page_title="Wellness AI", page_icon="🧠", layout="centered")

# Sidebar
st.sidebar.title("🛠 Therapy Insights")
st.sidebar.subheader("📌 Tips for Mental Well-being")
st.sidebar.write("- Take deep breaths and relax.\n- Maintain a healthy sleep routine.\n- Engage in physical activities.\n- Connect with loved ones.")

st.sidebar.subheader("📝 Session Summary")
if 'chat_history' in st.session_state and st.session_state.chat_history:
    st.sidebar.write("Recent Conversation:")
    for sender, message in st.session_state.chat_history[-5:]:
        st.sidebar.write(f"{sender}: {message[:50]}...")
else:
    st.sidebar.write("No chat history yet.")

st.title("🧠 AI Therapist Chatbot")
st.write("Talk to a professional AI therapist and share your feelings.")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

model = configure_genai()
name = st.text_input("Enter your name:", key="name")

if name:
    st.subheader(f"Hi {name}, How are you feeling today? 😊")
    
    if 'chat_loop' not in st.session_state:
        st.session_state.chat_loop = ""
    
    user_input = st.chat_input("Type your message:")
    
    if user_input:
        if user_input.lower() == "exit":
            st.session_state.chat_history.append(("😊", user_input))
            st.session_state.chat_history.append(("🩺", "Thanks for using, bye!"))
        else:
            response = get_response(model, user_input)
            st.session_state.chat_history.append(("😊", user_input))
            st.session_state.chat_history.append(("🩺", response))
    
    for sender, message in st.session_state.chat_history:
        with st.chat_message(sender):
            st.markdown(message)
