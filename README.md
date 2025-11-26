# Enterprise Insight Agent 🏢

A professional-grade Streamlit application that serves as a strategic decision support system, powered by OpenAI's GPT-4o. This agent is designed to provide concise, data-driven business insights.

## Features

- **Enterprise Persona**: configured as an expert Enterprise Consultant.
- **Streaming Responses**: Real-time text generation with a typewriter effect.
- **Session Management**: Maintains chat history within the session.
- **Clean Architecture**: Separated Configuration, Logic, and UI layers.
- **Professional UI**: Sidebar controls, clear conversation capability, and polished styling.

## Prerequisites

- Python 3.8+
- OpenAI API Key

## Installation

1.  **Clone the repository** (or download the files):
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies**:
    ```bash
    pip install streamlit openai python-dotenv
    ```

3.  **Environment Setup**:
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=sk-your-api-key-here
    ```

## Usage

Run the application using Streamlit:

```bash
streamlit run app.py
```

The application will open in your default web browser.

## Project Structure

- `app.py`: Main application file containing:
    - `AppConfig`: Centralized configuration settings.
    - `LLMClient`: Handles OpenAI API interactions.
    - `main`: UI rendering and application logic.

## Customization

You can modify the `AppConfig` class in `app.py` to change:
- `PAGE_TITLE`: The title of the application.
- `SYSTEM_PROMPT`: The persona and behavior of the AI.
- `MODEL_NAME`: The OpenAI model to use (default: `gpt-4o`).
