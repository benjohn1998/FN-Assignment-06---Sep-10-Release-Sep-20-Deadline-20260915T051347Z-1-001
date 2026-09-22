import json 
from pathlib import Path

def log_gate_decision(proposal, human_response, outcome):
    """Record a proposed action, the human answer, and the result"""

    record = {
        "proposed": proposal,
        "human_response": human_response,
        "outcome": outcome,     
    }

    with open("trace.jsonl", "a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n" )

def send_with_approval(target_message, draft, sender_email, dry_run=False):
    """Write a reply to the local outbox only after a human approval"""

    proposal ={
        "action": "send",
        "reply_to_id": target_message["id"],
        "from": sender_email,
        "to": target_message["from"],
        "subject": f"Re: {target_message['subject']}",
        "body": draft,
    }

    print("\nProposed send: ")
    print (json.dumps(proposal, indent =2))
    if dry_run:
        outcome = "not sent (dry-run)"
        log_gate_decision(proposal, "not asked (dry-run)", outcome)
        return outcome

    human_response= input("Say Yes to approve this send: ").strip().lower()

    if human_response != "yes":
        outcome = "not sent"
        log_gate_decision(proposal, human_response, outcome)
        return outcome

    outbox = Path("outbox")
    outbox_path= outbox / f"{target_message['id']}.json"

    try:
        outbox.mkdir(exist_ok=True)
        with outbox_path.open("x", encoding="utf-8") as file:
            json.dump(proposal, file, indent=2)
    except FileExistsError:
        outcome= "not sent: an outbox file for this message already exists"
    except OSError as error:
        outcome = f"not sent: {error}"
        log_gate_decision(proposal, human_response, outcome)
        raise
    else:
        outcome = f"written to {outbox_path}"

    log_gate_decision(proposal, human_response, outcome)
    return outcome