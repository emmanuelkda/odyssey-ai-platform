# backend/app/brains/system.py

def handle_system_command(message: str) -> dict:
    msg = message.lower()

    if "reset" in msg:
        command = "reset_experience"
    elif "exit" in msg or "quit" in msg:
        command = "exit_experience"
    elif "help" in msg or "what can i do" in msg:
        command = "show_help"
    else:
        command = "unknown_system_command"

    return {
        "kind": "system",
        "command": command,
        "raw_message": message,
    }
