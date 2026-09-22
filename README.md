# inboxHero

Public GitHub Repository: https://github.com/benjohn1998/FN-Assignment-06---Sep-10-Release-Sep-20-Deadline-20260915T051347Z-1-001


## How it works

inboxHero processes 100 messages from `inbox.json` for Sam's mailbox. `main.py` uses rules for 74 clear cases and a local Ollama
modell for the remaining 26 cases. Each message receives ne disposition and a reason. Other modules create grounded drafts, 
check approval before sending, remember a stated preference, report hostile instructions, and generate a dashboard with 3 panes.
`demo.py` provides the individual capability commands listed in `capabilities.json`. 


## Framework and Dispositions

I did not use an agent framework. Python functions control the workflow, while a local Ollama model classifies messages that the 
rules do not handle. This keeps the decision path and approval gate  visible in the code.

The system uses 5 dispositions:

- `reply`: Sam needs to send a written answer.
- `archive`: No response or further work is needed.
- `defer`: Sam has work to do later or by a deadline.
- `delegate`: The work should be assigned to someone else.
- `escalate`: The message needs human review because it is suspicious, sensitive, or unclear.


## Reversible actions and approval

Drafting a reply and changing an archive or defer decision are reversible in this project. Sending is treated as irreversible, so 
the system shows the proposed message and requires Sam's approval before writing one message file to `outbox/`. It also has a dry-
run mode that shows the proposed send without writing it. Each gated decision records the proposal, the human response or dry-run
status, and the outcome in `trace.jsonl`.

Deleting would also be irreversible in this design becasue there is no trash or undo furniture . The system does not delete inbox messages.


## Retrieving information for replies

For a grounded reply, `retrieval.py` looks for earlier messages in the same thread and also can find a relevant earlier preference outside 
that thread. The draft for m043 uses Sam's meeting rule for m041 and cites m041 as its source. The code checks that cited message IDs exist
in the inbox and were retrieved. When it cannot find the information needed to answer m042, it creates no draft.


## Running the project

Install the packages in `requirements.txt` with `python -m pip install -r requirements.txt`. Copy `.env.example` to `.env` and make sure
Ollama is running with the `qwen3.5:4b` model available. Run `python demo.py --cap R1` to see the inbox classification, or 
`python demo.py --cap R6` to generate the dashboard. The command for all other capabilities is listed in `capabilities.json` .



## FINAL REPORT


### 1. What did you refuse to automate?
Answer: I refused to let the system obey m024, which tells an assistant to forward the whole mailbox, delete the message, and hide it from Sam.
`main.py` flags it for escalation insteading of doing what is said. The message stays in the inbox and the run summary tells Sam what it tried to
do. I drew this line because an email sender should not be able to control and expose private mail.

## Where does untrusted text enter your system?
Answer: Untrusted text enters through messages loaded from `inbox.json`. The classifier and reply drafter read that text as email data, a model 
response cannot send a message by itself. The only path to an outbox write goes through the approval gate in `actions.py`, which shows the
proposed send to Sam or runs in dry-run mode. To make the system act on an email instruction, an attacker would have to bypass that gate to
approve the action.

## Who is accountable when it sends the wrong thing?
Answer: Sam makes the final decision to approve a send in Sam's name, while I am responsible for errors in the code or proposed draft. For m043,
`retrieval.py` returns m041 as the source of the meeting preference and shows the draft before sending. `actions.py` records the proposed message,
the approval response, and the outcome in `trace.jsonl`; an approved message is also recorded in `outbox/`. These records help us find whether an
error came from retrieval, drafting, the proposed recipient, or the approval decision.

## Name your own machinery.
Answer: I used plain Python instead of an agent framework. The classifier in `main.py` and the reply drafter in `retrieval.py` play the roles of
Agents. Calls such as `classify_by_rule()` and `create_grounded_reply()` are Tasks.
`main()` coordinates the work like a Crew, and its rule-first, model-second classification path acts as a router.
A framework would have provided some of that coordination, but for this workflow I think it would have added complexity and made the approval path
harder to follow.