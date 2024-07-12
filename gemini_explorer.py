import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part,Content, ChatSession
project="gemini-exploer"
vertexai.init(project=project)
config=generative_models.GenerationConfig(
    temperature=0.4

)
#Load model with Configuration
model=GenerativeModel(
    "gemini-pro",
    generation_config=config
)
chat=model.start_chat()

def llm_function(chat: ChatSession, query, user_name=None):
    
    response=chat.send_message(query)
    output=response.candidates[0].content.parts[0].text
    
    if user_name:
        output=f"{user_name} {output}"
    
    with st.chat_message("model"):
        st.markdown(output)
    
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )
    st.session_state.messages.append(
        {
            "role":"model",
            "content":output
        }
    )
    
st.title("Gemini Explorer")

if "messages" not in st.session_state:
    st.session_state.messages =[]

for index, message in  enumerate(st.session_state.messages):
    content=Content(
        role=message["role"],
        parts=[Part.from_text(message["content"])]
        
    )
    if index!=0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    chat.history.append(content)

user_name=st.text_input("Enter user name")
if len(st.session_state.messages) == 0 and user_name:
    # Pirate Speak
    initial_prompt = f"Arrr matey {user_name}! Introduce yourself as ReX, the assistant powered by Google Gemini. Ye use emojis to be interactive. ⚓️🦜"

    # GenZ Speak
    #initial_prompt = "Hey fam! I'm ReX, your lit assistant powered by Google Gemini. I use emojis to keep things 💯 and interactive. Let's vibe! 😎✨"

    # Friendly Introduction
    # initial_prompt = "Hello! I'm ReX, your friendly assistant powered by Google Gemini. I use emojis to make our conversation fun and interactive. 😊✨"

    llm_function(chat, initial_prompt,user_name)
    
    
query=st.chat_input("Gemini Explorer")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat,query,user_name)
