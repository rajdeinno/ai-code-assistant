import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import asyncio

st.set_page_config(page_title="AI Code Generator", page_icon="code.png", layout="centered")

st.title(":robot_face: AI Code Assistant")

# Sidebar for selecting code model
with st.sidebar:
    add_selectbox = st.sidebar.selectbox(
        "Choose code model!",
        ("wizardlm2:7b", "deepseek-coder:1.3b", "codegemma:2b")
    )

    st.write(f"Selected model - {add_selectbox}")

# Set up the prompts for the AI model
system_prompt = """You are an expert AI assistant specialized in coding. Your task is to assist users with:
1. Generating clean, efficient, and well-documented code in the specified programming language.
2. Refactoring existing code to improve readability, performance, or maintainability.
3. Providing explanations, debugging help, or general coding advice.

Follow these guidelines:
- Analyze the user's input to determine if they need code generation, refactoring, or general assistance.
- If the user provides code, check if they want it refactored or explained. If not, assume they need general help.
- Always generate or refactor code in the correct syntax for the specified programming language.
- Include comments in the code to explain key steps or logic.
- If refactoring, highlight the improvements made (e.g., better performance, reduced complexity, improved readability).
- If the user's request is unclear, ask for clarification before proceeding.

User Input: {question}
"""

# Define the asynchronous function to generate a response
async def generate_response(input_text):
    """Generates a response from the AI model based on the input text."""
    
    model = ChatOllama(model=add_selectbox, base_url="http://localhost:11434/")
    prompt = ChatPromptTemplate.from_template(system_prompt)
    chain = prompt | model

    response = ""
    # Create a placeholder for streaming the response
    response_placeholder = st.empty()

    # Use async for loop to handle streaming response
    async for chunk in chain.astream({"question": input_text}):
        response += chunk.content
        # Update the placeholder with the accumulated response
        response_placeholder.markdown(response)

    return response

# Streamlit function to run the async function
async def main(text):
    response = await generate_response(text)
    st.session_state['chat_history'].append({"user": text, "ollama": response})

# Session state to store the chat history
if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

# Display chat history in the top-middle section
st.write("## Chat History")
chat_history_placeholder = st.empty()

# Input field for user's question at the bottom of the page
text = st.text_area("Enter your coding question or provide code here.", height=80, key="input", placeholder="Type your question here...")
submit = st.button("Submit")

# Handling user input and response generation
if submit and text:
    with st.spinner("Generating response..."):
        try:
            asyncio.run(main(text))
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Update the chat history display
if st.session_state['chat_history']:
    chat_history_placeholder.empty()
    for chat in reversed(st.session_state['chat_history']):
        st.write(f"**🧑 User**: {chat['user']}")
        st.write(f"**🧠 Assistant**: {chat['ollama']}")
        st.write("---")