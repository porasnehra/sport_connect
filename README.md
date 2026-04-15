# Sport Connect 🏆

**Sport Connect** is a platform designed to bridge the gap between sports talent and local opportunities. It helps users discover local sports tournaments, register for events, and allows organizers to easily list their tournaments and manage registrations.

## Features

*   **🔍 Discover Tournaments**: Filter tournaments by sport and location.
*   **🏛️ Government Official Tournaments**: Dedicated section to find official tournaments sponsored by the government.
*   **📍 Find Nearest**: Automatically find the closest tournaments based on your current location using Geolocation.
*   **🏗️ Organizer Dashboard**: Allows organizers to host tournaments and view player registrations.
*   **🤖 AI Assistant**: Chat with an AI assistant to get recommendations, find specific tournaments, or query tournament details.
*   **🔔 Notifications**: Subscribe to email alerts for new tournaments in your area for your favorite sports.

## Tech Stack

*   **Frontend**: [Streamlit](https://streamlit.io/)
*   **Backend**: [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/)
*   **Database**: SQLite (via SQLAlchemy)
*   **AI Integration**: Google Generative AI (`google-generativeai`)
*   **Geolocation**: Geopy (`geopy`)

## Requirements

*   Python 3.8+
*   Dependencies listed in `requirements.txt`

## Installation & Setup

1.  **Clone the repository** (if applicable) or navigate to the project directory:
    ```bash
    cd sport_connect
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**:
    Create a `.env` file in the root directory and add the necessary environment variables.
    For example:
    ```env
    GEMINI_API_KEY=your_google_gemini_api_key
    BACKEND_URL=http://localhost:8000
    ```

## Running the Application

You can start both the FastAPI backend and the Streamlit frontend with a single command:

```bash
python run.py
```

This script will:
1. Start the FastAPI backend server using Uvicorn running on `http://localhost:8000`.
2. Start the Streamlit frontend running on default port (`http://localhost:8501`).

Alternatively, you can run them separately:
*   **Backend**: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
*   **Frontend**: `streamlit run frontend/app.py`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open-source and available under the [MIT License](LICENSE).
