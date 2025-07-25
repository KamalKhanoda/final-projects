import socket
import threading
import json
import bcrypt
import os

HOST = "127.0.0.1"
PORT = 4444

USERS_FILE = "users.json"

clients = {}  # client_socket: {"username": ..., "profile_pic": ...}
user_sockets = {}  # username: client_socket

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)

def broadcast_message(message, exclude=None):
    for client in clients:
        if exclude and client == exclude:
            continue
        try:
            client.sendall(message.encode())
        except Exception as e:
            print(f"Error sending message to client: {e}")

def send_private_message(message, client):
    try:
        client.sendall(message.encode())
    except Exception as e:
        print(f"Error sending private message: {e}")

def handle_client(client_socket, addr):
    users = load_users()
    username = None
    profile_pic = None

    try:
        while True:
            data = client_socket.recv(4096).decode()
            if not data:
                break
            try:
                req = json.loads(data)
            except Exception:
                send_private_message("Invalid request format.", client_socket)
                continue

            action = req.get("action")
            if action == "signup":
                uname = req.get("username")
                pwd = req.get("password")
                pic = req.get("profile_pic")
                if uname in users:
                    send_private_message(json.dumps({"status": "error", "message": "Username already exists."}), client_socket)
                else:
                    hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
                    users[uname] = {"password": hashed, "profile_pic": pic}
                    save_users(users)
                    send_private_message(json.dumps({"status": "ok", "message": "Signup successful."}), client_socket)
            elif action == "login":
                uname = req.get("username")
                pwd = req.get("password")
                if uname not in users:
                    send_private_message(json.dumps({"status": "error", "message": "User not found."}), client_socket)
                else:
                    hashed = users[uname]["password"].encode()
                    if bcrypt.checkpw(pwd.encode(), hashed):
                        username = uname
                        profile_pic = users[uname].get("profile_pic", "")
                        clients[client_socket] = {"username": username, "profile_pic": profile_pic}
                        user_sockets[username] = client_socket
                        send_private_message(json.dumps({"status": "ok", "message": "Login successful.", "profile_pic": profile_pic}), client_socket)
                        # Notify others
                        broadcast_message(json.dumps({"action": "user_online", "username": username, "profile_pic": profile_pic}), exclude=client_socket)
                    else:
                        send_private_message(json.dumps({"status": "error", "message": "Incorrect password."}), client_socket)
            elif action == "set_profile_pic":
                if not username:
                    send_private_message(json.dumps({"status": "error", "message": "Not logged in."}), client_socket)
                else:
                    pic = req.get("profile_pic")
                    users[username]["profile_pic"] = pic
                    save_users(users)
                    clients[client_socket]["profile_pic"] = pic
                    send_private_message(json.dumps({"status": "ok", "message": "Profile picture updated."}), client_socket)
            elif action == "send_message":
                if not username:
                    send_private_message(json.dumps({"status": "error", "message": "Not logged in."}), client_socket)
                else:
                    msg = req.get("message")
                    recipients = req.get("recipients")  # list of usernames or "all"
                    if recipients == "all":
                        for sock in clients:
                            if sock != client_socket:
                                send_private_message(json.dumps({
                                    "action": "message",
                                    "from": username,
                                    "profile_pic": profile_pic,
                                    "message": msg
                                }), sock)
                    elif isinstance(recipients, list):
                        for uname in recipients:
                            sock = user_sockets.get(uname)
                            if sock and sock != client_socket:
                                send_private_message(json.dumps({
                                    "action": "message",
                                    "from": username,
                                    "profile_pic": profile_pic,
                                    "message": msg
                                }), sock)
                    else:
                        send_private_message(json.dumps({"status": "error", "message": "Invalid recipients."}), client_socket)
            elif action == "get_users":
                # Send list of online users with profile pics
                online = [{"username": v["username"], "profile_pic": v["profile_pic"]} for v in clients.values()]
                send_private_message(json.dumps({"action": "user_list", "users": online}), client_socket)
            else:
                send_private_message(json.dumps({"status": "error", "message": "Unknown action."}), client_socket)
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        if username:
            print(f"{username} disconnected.")
            broadcast_message(json.dumps({"action": "user_offline", "username": username}), exclude=client_socket)
            user_sockets.pop(username, None)
        clients.pop(client_socket, None)
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(20)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()