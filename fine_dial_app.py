import streamlit as st
import requests
import json

# Default values for the fields
DEFAULT_ROLE = "Developer"
DEFAULT_LANGUAGE = "English"
DEFAULT_TONE = "Formal"
DEFAULT_STYLE = "Descriptive"

# Lambda API URL
api_url = "https://r0oiv5svdc.execute-api.us-west-2.amazonaws.com/prod1/fine_dialing"

acc_cre = {1:"Low", 2:"Medium", 3:"High"}

def home_page():
    st.set_page_config(
        page_title="Fine Dialing | Home",
        page_icon="home",
        layout="wide",
    )
    st.title("Fine Dialing")
    st.write("""
    *By Jitendra Cheripally*
    
    ##### Don't need to use prompt engineering, use the below fields to give a character to the LLM.
    
    ##### Examples are provided in the fields, type in your own values and press enter. After updation, click on `Let's Chat` and start your conversation with your personalized agent.
    
    ##### Curious to know more about this, click on `Project Details`.
    """)
    
    # Fields with default values
    role = st.text_input("Role", value=DEFAULT_ROLE)
    language = st.text_input("Language", value=DEFAULT_LANGUAGE)
    tone = st.text_input("Tone", value=DEFAULT_TONE)
    style = st.text_input("Writing Style", value=DEFAULT_STYLE)
    
    # Dials for Accuracy and Creativity
    accuracy = st.select_slider("Accuracy", options=[1, 2, 3], value=2, format_func=lambda x: ["Low", "Medium", "High"][x-1])
    creativity = st.select_slider("Creativity", options=[1, 2, 3], value=2, format_func=lambda x: ["Low", "Medium", "High"][x-1])
    
    # Button to go to the chat page
    if st.button("Let's Chat"):
        st.session_state.role = role
        st.session_state.language = language
        st.session_state.tone = tone
        st.session_state.style = style
        st.session_state.accuracy = accuracy
        st.session_state.creativity = creativity
        st.session_state.page = "chat"
        st.rerun()
    
    if st.button("Project Details"):
        st.session_state.page = "details"
        st.rerun()

def chat_page():
    st.set_page_config(
        page_title="Fine Dialing | Chat",
        page_icon="message",
        layout="wide",
    )
    st.title("Fine Dialing")
    if st.button("< Home"):
        st.session_state.page = "home"
        st.rerun()

    st.write(f"**Role**: {st.session_state.role} | **Language**: {st.session_state.language} | **Tone**: {st.session_state.tone} | **Style**: {st.session_state.style} | **Accuracy**: {acc_cre[st.session_state.accuracy]} | **Creativity**: {acc_cre[st.session_state.creativity]}")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Your Question"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Send the request to the API
        payload = {
            "question": prompt,
            "role": st.session_state.role,
            "language": st.session_state.language,
            "tone": st.session_state.tone,
            "style": st.session_state.style,
            "accuracy": st.session_state.accuracy,
            "creativity": st.session_state.creativity
        }

        try:
            response = requests.post(api_url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
            response_data = response.json()
            answer = response_data

            # Display assistant's answer
            with st.chat_message("assistant"):
                st.markdown(answer)

            # Update chat history
            st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error(f"An error occurred: {e}")

def details_page():
    st.set_page_config(
        page_title="Fine Dialing | Project Overview",
        page_icon="book",
        layout="wide",
    )
    st.title("Project Overview")
    st.write("""
    This project allows users to interact with a language model (LLM) using a simplified interface. Instead of manually crafting prompts, users can specify the Role, Language, Tone, Writing Style, Accuracy, and Creativity of the agent. The system then automatically adjusts the model parameters to generate responses that match the user's specifications.

    ### How It Works:
    - **Role:** Defines the persona or expertise level of the agent.
    - **Language:** Specifies the language in which the responses will be generated.
    - **Tone:** Controls the emotional tone of the responses (e.g., Formal, Humorous, Urgent).
    - **Writing Style:** Adjusts the stylistic approach (e.g., Poetry, Technical, Narrative).
    - **Accuracy & Creativity:** These are used for fine-tuning the model's temperature and top-p parameters. The system balances these aspects to generate responses that are either more accurate or more creative based on the user's selection.
    
    ### Technical Details:
    The system uses an AWS Lambda function to interact with the Llama 3.1 8B hosted on Bedrock. The Lambda function dynamically adjusts the model's behavior based on the inputs provided by the user on the home page. The front-end is built using Streamlit, which provides a user-friendly interface for adjusting parameters and interacting with the LLM. The backend leverages the flexibility of AWS Lambda to execute lightweight, scalable functions that manage the interactions with the model. The API communication is done using HTTPS requests to ensure secure data transmission.

    ### Created by:
    Jitendra Cheripally
    - **Email:** jitendracheripally@gmail.com
    - **LinkedIn:** [jitendracheripally](https://www.linkedin.com/in/jitendracheripally)
    - **GitHub:** [jitendracheripally2003](https://github.com/jitendracheripally2003)
    """)

    if st.button("< Home"):
        st.session_state.page = "home"
        st.rerun()

def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "chat":
        chat_page()
    elif st.session_state.page == "details":
        details_page()

if __name__ == "__main__":
    main()
