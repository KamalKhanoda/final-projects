# Final-projects

# Chat App

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


*Made with ❤️ using
