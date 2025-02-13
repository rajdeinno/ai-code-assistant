# AI Code Assistant

This project provides an AI-powered code assistant built using Streamlit and LangChain. It assists users by generating, refactoring, or explaining code in multiple programming languages. Users can choose from different AI models for code generation and interact with the assistant through a simple web interface.

## Features

### Code Generation:

Generate clean, efficient, and well-documented code in various programming languages.

### Code Refactoring:

Refactor existing code to improve readability, performance, and maintainability.

### Code Explanation & Debugging:

Get explanations, debugging assistance, or general coding help.

### Real-Time Interaction:

Chat with the AI assistant and get instant responses.

### Multiple Models:

Choose from different AI models for generating code:

#### wizardlm2:7b

#### deepseek-coder:1.3b

#### codegemma:2b

## Installation

Follow these steps to set up the project locally:

Clone the repository:

```bash
git clone https://github.com/your-username/ai-code-assistant.git
```

Navigate into the project folder:

```bash
cd ai-code-assistant
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Ensure the Ollama server is running:

You need the Ollama server to interact with the AI models. Run the following command to start the server:

```bash
python -m ollama.server
```

Run the Streamlit app:

```bash
streamlit run app.py
```

This will start the Streamlit application in your browser.

## How to Use

#### Open the app:

The Streamlit application should open in your browser automatically.

#### Select a model:

Use the sidebar to select a code generation model.

#### Ask your question:

Type your coding question or provide code in the input field.

#### Submit your request:

Click the "Submit" button to generate a response.

#### Review chat history:

The chat history will display previous interactions, so you can track your questions and the assistant's responses.

#### Folder Structure

1. app.py: The main Streamlit app that handles the interface and logic.
2. requirements.txt: The list of Python packages required to run the app.
3. README.md: This file.

## Contributing

Contributions are welcome! If you have suggestions, improvements, or fixes, feel free to:
Fork the repository.
Create a new branch for your changes.
Open a pull request to the main branch.
