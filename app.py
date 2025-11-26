import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Dict, Generator, Union

# ---------------------------------------------------------
# 1. Configuration Class (The "Settings" Layer)
# ---------------------------------------------------------
class AppConfig:
    """
    Central configuration for the application.
    Separating config makes the app easier to maintain and deploy.
    """
    PAGE_TITLE: str = "Enterprise Insight Agent"
    PAGE_ICON: str = "🏢"  # Added icon for professional look
    
    # Enterprise-grade System Prompt
    # This defines the persona and boundaries of the AI
    SYSTEM_PROMPT: str = """
    You are an expert Enterprise Consultant specializing in Business Information Systems. 
    Your goal is to provide concise, data-driven insights to help decision-making. 
    Use professional business terminology.
    """
    
    MODEL_NAME: str = "gpt-4o"
    
    @staticmethod
    def get_api_key() -> str:
        """Retrieves and validates the API key from environment variables."""
        load_dotenv()
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            # In a real enterprise app, you would log this to a monitoring service (e.g., Sentry)
            return None
        return key

# ---------------------------------------------------------
# 2. Logic Manager (The "Backend" Layer)
# ---------------------------------------------------------
class LLMClient:
    """
    Encapsulates all interactions with the LLM Provider (OpenAI).
    This design pattern (Facade) hides the complexity of the API from the UI.
    """
    def __init__(self):
        api_key = AppConfig.get_api_key()
        if not api_key:
            # We handle missing keys gracefully in the UI, but here we ensure client isn't created invalidly
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)

    def get_streaming_response(self, messages: List[Dict[str, str]]) -> Union[Generator, str]:
        """
        Generates a streaming response from the OpenAI API.
        
        Args:
            messages: A list of message dictionaries (role, content).
            
        Returns:
            Generator: If successful, yields chunks of text.
            str: If an error occurs, returns the error message.
        """
        if not self.client:
            return "Error: OpenAI API Key is missing. Please check your .env file."

        try:
            stream = self.client.chat.completions.create(
                model=AppConfig.MODEL_NAME,
                messages=messages,
                stream=True,
            )
            return stream
        except Exception as e:
            return f"Connection Error: {str(e)}"

# ---------------------------------------------------------
# 3. UI Manager (The "Frontend" Layer)
# ---------------------------------------------------------
def initialize_session_state():
    """Initializes the chat history and other session variables."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", "content": AppConfig.SYSTEM_PROMPT}
        ]

def main():
    # --- UI Setup ---
    st.set_page_config(page_title=AppConfig.PAGE_TITLE, page_icon=AppConfig.PAGE_ICON)
    
    # Sidebar for controls (Professional UX)
    with st.sidebar:
        st.header(f"{AppConfig.PAGE_ICON} Controls")
        st.info("Connected to Enterprise Knowledge Base")
        
        # A "Clear Conversation" button is essential for testing and usability
        if st.button("Clear Conversation", type="primary"):
            st.session_state["messages"] = [
                {"role": "system", "content": AppConfig.SYSTEM_PROMPT}
            ]
            st.rerun()

    # Main Header
    st.title(AppConfig.PAGE_TITLE)
    st.caption("Strategic Decision Support System | Powered by GPT-4o")

    # --- Initialization ---
    initialize_session_state()
    llm_client = LLMClient() # Instantiate the backend logic

    # --- Display History ---
    # We re-draw the chat history every time the script runs
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # --- Handle Input ---
    if user_input := st.chat_input("Ask for strategic insights..."):
        
        # 1. Update UI immediately with user's question
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # 2. Get Response from Backend
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Use the LLMClient class to get the stream
            stream_or_error = llm_client.get_streaming_response(st.session_state.messages)
            
            # Error Handling: Check if the backend returned a string (Error) or a Generator (Success)
            if isinstance(stream_or_error, str):
                st.error(stream_or_error)
            else:
                # Process the stream
                for chunk in stream_or_error:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌") # Cursor effect
                
                # Final update without the cursor
                response_placeholder.markdown(full_response)
                
                # 3. Save assistant response to memory
                st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()