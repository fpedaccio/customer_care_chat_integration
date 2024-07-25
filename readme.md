# FastAPI Slack Customer Service Application

This repository contains a FastAPI web application designed for managing customer service interactions using Slack and WebSockets. The application facilitates real-time communication between a web client and a FastAPI backend, allowing customer support agents to send and receive messages efficiently.

## Features

- **Real-time Messaging**: Uses WebSockets for instant message transmission and reception.
- **Slack Integration**: Sends messages to a specified Slack channel and manages threads for customer interactions.
- **SQLite Database**: Stores messages and their threads for easy management and retrieval.
- **CORS Support**: Allows communication between the frontend and backend from different domains.

## Technologies Used

- **FastAPI**: A modern, high-performance web framework.
- **Slack SDK**: A library for interacting with the Slack API.
- **SQLite**: A lightweight database for local storage.
- **HTML/CSS/JavaScript**: User interface for sending and receiving messages.
- **Uvicorn**: An ASGI server to run the FastAPI application.

## Installation

Follow these steps to set up and run the application locally:

### Prerequisites

- Python 3.7 or higher.
- Access to a Slack channel and a valid bot token.

### Dependency Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/your-username/repo-name.git
    cd repo-name
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. Create a `.env` file in the project's root directory with the following content:

    ```
    SLACK_BOT_TOKEN=your-slack-bot-token
    ```

2. Replace `your-slack-bot-token` with your actual Slack token.

### Running the Application

1. Start the application using Uvicorn:

    ```bash
    uvicorn main:app --reload
    ```

2. Open your browser and navigate to `http://127.0.0.1:8000` to access the user interface.

## Usage

- **Send a Message**: Enter your message in the input field and press the "Send" button. The message will be sent to the backend and then to the configured Slack channel.
- **Receive Messages**: New messages will appear in the interface in real-time thanks to WebSockets.

## Project Structure

├── main.py # Main application code
├── requirements.txt # Python dependencies list
├── static # Static files (HTML, CSS, JS)
│ ├── index.html # User interface
└── README.md # This file


## Contributing

Contributions are welcome! If you want to improve the application, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b new-feature`.
3. Make your changes and commit them: `git commit -m 'Add new feature'`.
4. Push your changes to the branch: `git push origin new-feature`.
5. Open a Pull Request on GitHub.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

