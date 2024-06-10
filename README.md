# Sad Gpt

This project is a Streamlit-based application that allows users to interact with Google's Generative AI (Gemini) to ask questions and receive detailed explanations. Chat histories are stored in a SQLite database.

## Features

- Start a new chat session or continue an existing one.
- Save and load chat histories.
- Stream responses from the model in real-time.

## Requirements

- Python 3.7+
- A Google API key with access to the Generative AI service (Gemini).

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/rag-study-app.git
    cd rag-study-app
    ```

2. **Create and activate a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Create a `.env` file** in the project root directory:
    ```bash
    touch .env
    ```

2. **Add your Google API key** to the `.env` file:
    ```plaintext
    GOOGLE_API_KEY=your_google_api_key_here
    ```

## Running the App

1. **Start the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

2. **Open your web browser** and navigate to `http://localhost:8501` to use the app.

## Project Structure

- `app.py`: Main application file.
- `requirements.txt`: List of required Python packages.
- `.env`: Environment variables file (not included in the repository, to be created by the user).
- `chat_sessions.db`: SQLite database for storing chat histories (created automatically).

## Usage

- Use the sidebar to start a new chat session or select an existing one.
- Enter your questions in the input field and press "Send" to receive responses from the model.
- Responses are streamed in real-time, providing a dynamic chat experience.
- Use the "Session Actions" in the sidebar to rename or delete chat sessions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Google Generative AI (Gemini)](https://ai.google.com/research/)
- [dotenv](https://github.com/theskumar/python-dotenv)

