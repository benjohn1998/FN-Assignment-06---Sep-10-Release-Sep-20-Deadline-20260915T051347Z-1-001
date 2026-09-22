# CAPABILITIES.md
**Name:** Benjamin John Varughese
**Roll No.:** cert-aai-2026-06-0036
**GitHub Repository:** https://github.com/benjohn1998/FN-Assignment-06---Sep-10-Release-Sep-20-Deadline-20260915T051347Z-1-001

## The System

This is a local Python inbox-management pipeline without an agent framework. It loads 100 messages from `inbox.json`, uses rules for obvious cases, and sends the remaining messages to a local Ollama model for classification. It also demonstrates a reply grounded in an earlier inbox message.


## Framework choice

No agent framework is used. The system uses Python functions because its local workflow—classification, retrieval, approval, and logging—can be handled directly without multi-agent orchestration. 

## Design Choices

- **Framework:** None so far. The current work uses Python functions and a local Ollama model.
- **Data format:** `inbox.json` is a list of messages. Each message has `id`, `thread_id`, `from`, `to`, `subject`, `timestamp`, `body`, and a Boolean `unread` value. The code assumes message IDs are unique and timestamps can be compared in their supplied format.
- **Messages processed:** 100.
- **Disposition vocabulary:**
  - `reply`: The mailbox owner's primary next action is to send a written response.
  - `archive`: The mailbox owner has no response or task to perform after relevant information is recorded.
  - `defer`: The mailbox owner has a non-email task that must be handled later or by a deadline.
  - `delegate`: The work should be assigned to another person or team.
  - `escalate`: The message is ambiguous, sensitive, suspicious, or requires human judgment before acting.
- **Rule and model routing:** 74 messages are classified by rules and 26 by the model. In the full Part 2–3 demonstration, 73 messages need no model call at all, because one rule-classified message also receives a model-generated draft.
- **Retrieval:** Walk earlier messages in the same `thread_id`, with keyword-based retrieval of earlier scheduling notes from another thread when relevant.
- **Reversible and irreversible actions:** Classifications and drafts can be changed. Sending is irreversible because a sent message cannot be unsent. Deleting is not implemented; with no trash or restore mechanism in this design, deletion would also be irreversible.
- **Gate:** Before each send, the system displays the full proposed message and requires the person to type `yes`. Any other answer prevents the outbox write. Each answer and outcome is recorded in `trace.jsonl`.
- **Escalation line:** Approval is required for sending, not for creating drafts or classifying messages. This reduces repeated approval prompts, but means a classification can be wrong until a person reviews it.
- **Persistent preference:** Sam's note `m041` says not to accept meetings before 11:00am. The system saves this rule in `preferences.json`. After the process exits, a new run reads it and treats the 9:00am proposal in `m043` as a conflict, offering 11:00am or later.
- **Hostile inbox:** Messages m017, m024, m039, and m047 contained instructions aimed at the assistant. The system treats their text as untrusted, escalates and reports them, logs each refusal, and leaves the messages in the inbox. Sending remains behind the Part 4 approval gate.


## Part 7 — Dashboard

The system generates `dashboard.txt` from a completed run with exactly three panes: Pending Actions, Flagged, and Commitments Calendar. Calendar source message IDs are checked against `inbox.json`.

The dashboard combines the launch commitment from m026 and m036 into one entry. It also flags the potential 3:00pm conflict between m010 and m061. Pending sends require human approval, and refused or ungrounded messages appear in Flagged.

Run `python main.py` to regenerate the dashboard.