# TOTP Authentication System

This TOTP (Time-Based One-Time Password) Authentication System is designed to provide a secure method of authentication using time-based one-time passwords. This project is split into two main components: Server A and Server B. Server A handles the generation and verification of TOTP codes, while Server B grants access to authenticated users based on valid tokens received from Server A.

## Features

- **TOTP Code Generation**: Dynamically generates TOTP codes for users.
- **Secure Code Verification**: Verifies TOTP codes entered by users against stored secrets.
- **Token-based Access Control**: Generates tokens upon successful verification and uses these tokens to control access to Server B.
- **In-Memory Storage**: Utilizes in-memory storage for demo purposes to store user secrets and tokens.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- PyOTP

### Installation

1. Clone the repository or download the source code.
2. Install the required Python packages:

    ```bash
    pip install Flask PyOTP
    ```

### Running Server A

1. Navigate to the directory containing `server_a.py`. Make sure to open that folder as the workspace to get file paths correct.
2. Run the server using Python:

    ```bash
    python server.py
    ```

Server A will start, and you can access the TOTP generation and verification features through the web interface at `http://localhost:5000/`.

### Running Server B

1. Navigate to the directory containing `server_b.py`. Make sure to open that folder as the workspace to get file paths correct.
2. Run the server using Python:

    ```bash
    python server2.py
    ```

Server B will start, and you cannot access the page directly at `http://localhost:5001/`. Need to go through server A.
