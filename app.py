from google import genai
from google.genai import types
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
chat = client.chats.create(model="gemini-2.5-flash", config=types.GenerateContentConfig(
        temperature=0.9
    ))

# response = chat.send_message_stream("I have 2 dogs in my house.")
# # for chunk in response:
# #     print(chunk.text, end="")

# response = chat.send_message_stream("How many paws are in my house?")
# # for chunk in response:
#     print(chunk.text, end="")

# print("\n\nChat history:")
# for message in chat.get_history():
#     print(f'role - {message.role}', end=": ")
#     print(message.parts[0].text)


st.title("LLM App")
# api_key = st.text_input("Enter your Gemini API Key", type="password")
# Initialize chat history in session state if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Text area for user input
with st.form(key='my_form', clear_on_submit=True):
    user_prompt = st.text_area("Ask something", key="user_input")
    submit_button = st.form_submit_button("Generate")

# Create a unique key for the button to ensure it reruns on each click
if submit_button:
    if user_prompt:
        try:
            # Send message to model
            response = chat.send_message_stream(user_prompt)
            
            # Add the exchange to chat history
            st.session_state.chat_history.append(("You", user_prompt))
            for chunk in response:
                st.session_state.chat_history.append(("Model", chunk.text))
                st.write(f"**Model:** {chunk.text}")
            # Set a flag to trigger clearing on next rerun
            # Force a rerun to clear the input
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.error("Please enter a prompt.")



# Display chat history
st.subheader("Chat History")
for role, text in st.session_state.chat_history:
    st.write(f"**{role}:** {text}")