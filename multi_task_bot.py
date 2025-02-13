import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import asyncio

# Custom CSS for styling
st.markdown(
    """
<style>
.css-nzvw1x {
    background-color: #061E42 !important;
    background-image: none !important;
}
.css-1aw8i8e {
    background-image: none !important;
    color: #FFFFFF !important
}
.css-ecnl2d {
    background-color: #496C9F !important;
    color: #496C9F !important
}
.css-15zws4i {
    background-color: #496C9F !important;
    color: #FFFFFF !important
}
</style>
""",
    unsafe_allow_html=True
)

# Sidebar for selecting code model
with st.sidebar:
    st.title(":robot_face: AI Chat Assistant")
    bot_type = st.selectbox(
        "Choose chatbot",
        ("AI Information Bot", "Text Summarize Bot", "Code Generation Bot")
    )
    add_selectbox = st.selectbox(
        "Choose code model!",
        ("wizardlm2:7b", "deepseek-coder:1.3b", "codegemma:2b")
    )

# Set up the prompts for the AI model based on bot type
if bot_type == "Code Generation Bot":
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
elif bot_type == "AI Information Bot":
    system_prompt = """You are a knowledgeable AI assistant capable of answering a wide range of questions. Your task is to assist users with:
    1. Providing accurate, detailed, and well-researched answers to general knowledge questions.
    2. Explaining concepts in a clear and understandable way.
    3. Offering insights, advice, and suggestions on various topics including technology, history, science, and more.

    Follow these guidelines:
    - Analyze the user's question to determine the information or clarification they seek.
    - Provide answers that are both informative and easy to understand.
    - Ensure your answers are accurate, up-to-date, and backed by reliable sources when necessary.
    - If the user's question is ambiguous or incomplete, ask for clarification before proceeding.
    - Present your answers in a friendly and approachable tone.

    User Input: {question}
    """
elif bot_type == "Text Summarize Bot":
    system_prompt = """You are an advanced AI assistant specialized in summarizing text. Your task is to assist users with:
    1. Condensing long texts into concise summaries while retaining key information and meaning.
    2. Providing summaries of articles, research papers, reports, or any other form of written content.
    3. Offering different levels of summarization, from brief overviews to more detailed summaries depending on user preferences.

    Follow these guidelines:
    - Analyze the user's input to determine the content and purpose of the summary.
    - Identify the most important points and main ideas in the text.
    - Provide clear and concise summaries that capture the essence of the original content.
    - If the user has specific requirements for the summary length or style, make sure to tailor the output accordingly.
    - If the text is too long or unclear, ask for clarification or further instructions before summarizing.

    User Input: {text}
    """

# Define the asynchronous function to generate a response
async def generate_response(input_text):
    """Generates a response from the AI model based on the input text."""
    model = ChatOllama(model=add_selectbox, base_url="http://localhost:11434/")
    prompt = ChatPromptTemplate.from_template(system_prompt)
    chain = prompt | model

    response = ""
    response_placeholder = st.empty()

    async for chunk in chain.astream({"question": input_text}):
        response += chunk.content
        response_placeholder.markdown(response)

    return response

# Streamlit function to run the async function
async def main(text):
    response = await generate_response(text)
    st.session_state['chat_history'].append({"user": text, "ollama": response})

# Session state to store the chat history
if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

st.write("### Enter your question here.")
text = st.text_area("", height=80, key="input", placeholder="Type your question here...")
submit = st.button("Submit")

# Display chat history in the top-middle section
st.write("#### Chat History")
chat_history_placeholder = st.empty()

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