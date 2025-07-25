# Final-projects

# 1. Chat App

ChatiPY is a simple Python-based chat application with a graphical interface built using Tkinter. It allows users to sign up, log in, select a profile photo, see online users, and exchange messages in real time.

## Features

- **User Authentication:** Login and signup with username and password.
- **Profile Photo:** Option to select and display a profile photo.
- **Online Users List:** See who is online, with profile pictures.
- **Group and Private Messaging:** Select users to send messages to, or broadcast to all.
- **Modern UI:** Clean, user-friendly interface with message alignment and scrollable user list.

## Requirements

- Python 3.x
- [Pillow](https://pypi.org/project/Pillow/) (for image handling)

Install dependencies with:
```sh
pip install pillow
```

## Usage

1. **Start the Server:**  
   Make sure you have a compatible server running on `127.0.0.1:4444`.

2. **Run the Client:**  
   ```sh
   python client.py
   ```

3. **Login or Signup:**  
   - Enter your username and password.
   - (Optional) Select a profile photo.
   - Click "Login" or "Signup".

4. **Chat:**  
   - Select users from the sidebar to send private messages, or use "Select All" to broadcast.
   - Type your message and press Enter or click "Send".
   - 
## Customization

- **Profile Pictures:** Supported image formats: PNG, JPG, JPEG, GIF.
- **UI Colors and Fonts:** Easily customizable in the code.

## Notes

- This client expects a compatible server implementation.
- For demonstration and learning purposes; not intended for production use.

# 2. Python Voice Assistant

A simple voice assistant for Windows that can:
- Recognize your voice commands
- Search Google
- Play YouTube videos
- Open apps (Notepad, Calculator, Paint)
- Open any website
- Respond to greetings and exit commands

## Features

- **Say "hello"** – The assistant will greet you.
- **Say "search ... on google"** – Opens a Google search for your query.
- **Say "play ... on youtube"** – Plays the first YouTube video for your query.
- **Say "open notepad/calculator/paint"** – Opens the specified app.
- **Say "open [website]"** – Opens the website (e.g., "open google" or "open github.com").
- **Say "exit" or "quit"** – Closes the assistant.

## Requirements

- Python 3.7+
- [speech_recognition](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)
- [pytube](https://pypi.org/project/pytube/)
- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

Install dependencies with:

```bash
python -m pip install speechrecognition pyttsx3 pytube requests beautifulsoup4
```

## Usage

1. Make sure your microphone is connected.
2. Run the assistant:

```bash
python main.py
```

3. Speak your command when prompted.

## Example Commands

- `hello`
- `search python tutorials on google`
- `play relaxing music on youtube`
- `open notepad`
- `open github.com`
- `exit`

---

