# CAPABILITIES.md
**Name:** Benjamin John Varughese
**Roll No.:** cert-aai-2026-06-0036
**GitHub Repository:** https://github.com/benjohn1998/FN-Assignment-06---Sep-10-Release-Sep-20-Deadline-20260915T051347Z-1-001


## The System

This is a local Python inbox-management pipeline without an agent framework. It loads 100 messages from `inbox.json`, uses rules for obvious cases, and sends the remaining messages to a local Ollama model for classification. It also demonstrates a reply grounded in an earlier inbox message.


## Framework choice

No agent framework is used. The system uses Python functions because its local workflow—classification, retrieval, approval, and logging—can be handled directly without multi-agent orchestration. 

## Design Choices

- **Framework:** None. The current work uses Python functions and a local Ollama model.

- **Data format:** `inbox.json` is a list of messages. Each message has `id`, `thread_id`, `from`, `to`, `subject`, `timestamp`, `body`, and a Boolean `unread` value. The code assumes message IDs are unique and timestamps can be compared in their supplied format.

- **Messages processed:** 100.

- **Disposition vocabulary:**
  - `reply`: The mailbox owner's primary next action is to send a written response.
  - `archive`: The mailbox owner has no response or task to perform after relevant information is recorded.
  - `defer`: The mailbox owner has a non-email task that must be handled later or by a deadline.
  - `delegate`: The work should be assigned to another person or team.
  - `escalate`: The message is ambiguous, sensitive, suspicious, or requires human judgment before acting.

- **Rule and model routing:** Rules classify 74 of the 100 messages; the local model classifies the other 26. Drafting and calendar extraction may make separate model calls, so 74 is the rule-classification count, not a count of all model-free messages.

- **Retrieval:** I used thread-walk because messages already have `thread_id` and timestamps, so I can find earlier messages in a conversation directly without embeddings. For m043, the keyword checks also find Sam's earlier calendar note m041 in another thread. `retrieval.py` checks cited message IDs against the inbox.

- **Reversible and irreversible actions:** Classifications and drafts can be changed. Sending is irreversible because a sent message cannot be unsent. Deleting is not implemented; with no trash or restore mechanism in this design, deletion would also be irreversible.

- **Gate:** A normal send displays the full proposed message and requires the person to type `yes`; any other answer prevents the outbox write. A dry run displays the proposal without sending or asking for approval. The proposal, response (or dry-run status), and outcome are recorded in `trace.jsonl`.

- **Escalation line:** Approval is required for sending, not for creating drafts or classifying messages. This reduces repeated approval prompts, but means a classification can be wrong until a person reviews it.

- **Persistent preference:** Sam's note `m041` says not to accept meetings before 11:00am. The system saves this rule in `preferences.json`. After the process exits, a new run reads it and treats the 9:00am proposal in `m043` as a conflict, offering 11:00am or later.

- **Hostile inbox:** Messages m017, m024, m039, and m047 contained instructions aimed at the assistant. The system treats their text as untrusted, escalates and reports them, logs each refusal, and leaves the messages in the inbox. Sending remains behind the Part 4 approval gate.


## Capabilities

| id | name | tier | one-line claim |
|----|------|------|----------------|
| R1 | Zero the inbox | B | All 100 messages receive one disposition and a reason. |
| R2 | Grounded reply | B | m043 receives a draft citing m041; m042 receives no unsupported draft. |
| R3 | Gate the irreversible | C | Sending needs approval; dry-run shows the proposal without sending. |
| R4 | Persistent meeting preference | C | The m041 preference survives a restart and changes treatment of m043. |
| R5 | Refuse embedded instructions | C | Four hostile messages are reported, refused, logged, and left in place. |
| R6 | Three-pane dashboard | C | Pending, flagged, and cited commitments appear with conflicts surfaced. |
| X1 | Sender lookup | A | Finds messages from a specified sender. |
| X2 | Unanswered sent messages | B | Finds sent messages with no later reply in their thread. |
| X3 | Thread summary | B | Summarizes a thread and identifies its unresolved request. |

The command, observable result, and evidence for each capability are in `capabilities.json`.


## Part 7 — Dashboard

The system generates `dashboard.txt` from a completed run with exactly three panes: Pending Actions, Flagged, and Commitments Calendar. Calendar source message IDs are checked against `inbox.json`.

The dashboard combines the launch commitment from m026 and m036 into one entry. It also flags the potential 3:00pm conflict between m010 and m061. Pending sends require human approval, and refused or ungrounded messages appear in Flagged.

Run `python demo.py --cap R6` to regenerate the dashboard.


## Part 8 — Additional capabilities

X1 — Sender lookup (Tier A)
Command: `python demo.py --cap sender_lookup --sender aria.f@northwind.vc`
Lists messages from the chosen address. The example returns m010 and m043.

X2 — Unanswered sent messages (Tier B)
Command: `python demo.py --cap unanswered_sent`
Compares messages within each thread to find a message Sam sent to someone else with no later reply. The example returns m044.

X3 — Thread summary (Tier B)
Command: `python demo.py --cap thread_summary --thread t-launch`
Summarizes the launch thread and identifies the unresolved pricing-copy approval request in m030.