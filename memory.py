import json
import sys
from datetime import datetime
from pathlib import Path

PREFERENCE_FILE = Path(__file__).with_name("preferences.json")
OWNER_EMAIL = "sam@paperjet.io"

def save_preference (source_message):
    if (
        source_message["from"].lower() != OWNER_EMAIL
        or source_message["to"].lower() != OWNER_EMAIL
    ):
        raise ValueError( "The selected message is not Sam's own note")


    body = source_message["body"].lower()
    phrase = "meetings before "

    if phrase not in body:
        raise ValueError("No earliest meeting time was found in this note.")

    earliest_time = body.split(phrase, 1)[1].split(",", 1)[0].strip()

    
    preference = {
        "earliest_meeting_time": earliest_time,
        "source_message_id": source_message["id"]
    }
    with PREFERENCE_FILE.open("w", encoding="utf-8") as file:
        json.dump(preference, file, indent=2)

    return preference

def load_preference():
    if not PREFERENCE_FILE.exists():
        return None

    with PREFERENCE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def handle_meeting(message, preference):
    if preference is None:
        return "No saved meeting preference; ask Sam before accepting."

    text = (message["subject"] + " " + message["body"]).lower()

    if not any(word in text for word in ("meeting", "slot", "call")):
        return "This message does not appear to be a meeting request."

    body = message["body"].lower()
    phrase = " at "

    if phrase not in body:
        return "No proposed meeting time found; ask Sam."

    proposed_text = body.split(phrase, 1)[1].split(",", 1)[0].strip()
    earliest_text = preference["earliest_meeting_time"]

    try:
        proposed = datetime.strptime(proposed_text, "%I:%M%p").time()
    except ValueError:
        return "No readable proposed meeting time found; ask Sam."

    earliest = datetime.strptime(earliest_text, "%I:%M%p").time()

    if proposed < earliest:
        return (
            f"{message['id']}: Do not accept {proposed_text}. "
            f"Offer {earliest_text} or later instead. "
            f"Preference saved from {preference['source_message_id']}."
        )

    return (
        f"{message['id']}: The proposed time does not conflict "
        "with the saved rule."
    )


def run():
    if len(sys.argv) != 3 or sys.argv[1] not in ("save", "apply"):
        print("Use: python memory.py save MESSAGE_ID")
        print("  or python memory.py apply MESSAGE_ID")
        return

    from main import load_inbox
    from retrieval import find_message_by_id

    messages = load_inbox()
    message = find_message_by_id(messages, sys.argv[2])

    if message is None:
        raise ValueError(f"Message {sys.argv[2]} was not found.")

    if sys.argv[1] == "save":
        preference = save_preference(message)
        print("Saved preference:", preference)
    else:
        print(handle_meeting(message, load_preference()))


if __name__ == "__main__":
    run()