# Restaurant Calling Agent — Food Order Confirmation

AI voice agent that calls restaurant customers right after they place a food
order to confirm the items, verify the delivery address, and give the
delivery ETA. Built with **Vapi** (voice) + **n8n** (orchestration).

## What it does

1. When a new order arrives, the `new-order` webhook fires and n8n reads
   the `Orders` Google Sheet.
2. Orders with status `new` are queued, one by one.
3. Vapi calls each customer with the Restaurant Order Confirmation
   assistant (Urdu-first voice, `ur-PK-AsadNeural`).
4. The assistant reads back the ordered items and total, verifies the
   delivery address (house/flat, street, landmark), and states the ETA.
   Small modifications or cancellation are allowed within 5 minutes of
   the order being placed.
5. When the call ends, Vapi sends an end-of-call report to n8n, which
   logs the outcome in the `CallLog` sheet. If the order is confirmed,
   the kitchen is notified on Slack (`#kitchen-orders`); otherwise the
   team is notified on `#restaurant-calls`.

## Files

| File | What it is |
|---|---|
| `workflow.json` | n8n workflow — import it in n8n (13 nodes) |
| `vapi-assistant.json` | Vapi assistant config — create it via the Vapi dashboard or API |
| `workflow.png` | Rendered workflow diagram |

## Setup

1. **Vapi**: create a phone number in Vapi, then create the assistant from
   `vapi-assistant.json` (dashboard → Assistants → Import, or
   `POST https://api.vapi.ai/assistant`). Copy the assistant ID and phone
   number ID into the n8n workflow.
2. **n8n**: import `workflow.json`. Connect your own credentials:
   Google Sheets, Vapi API key (HTTP Header Auth), Slack.
3. Replace the placeholders:
   - `YOUR_GOOGLE_SHEET_ID` — sheet with `Orders` and `CallLog` tabs
   - `YOUR_VAPI_ASSISTANT_ID`, `YOUR_VAPI_PHONE_NUMBER_ID`
   - `YOUR_N8N_URL` — your public n8n URL (webhook base) in the assistant tools
4. **Sheet columns** (`Orders`): `name`, `phone`, `address`, `items`,
   `orderTotal`, `status` (`new`/`confirmed`/`cancelled`).
5. Set the Vapi assistant's server URL / webhook to your n8n
   `vapi-call-report` webhook so end-of-call reports arrive, and point
   each tool's server URL at the matching n8n `vapi-tool-*` webhook.

## Safety rules (built into the assistant)

- Never asks for card details, bank details, PIN, OTP, or password.
- Payment is cash on delivery or already paid online — no payment details
  are collected on the call.
- Changes or cancellation are allowed only within 5 minutes of the order;
  after that the order is already being prepared.
- Unhappy or complex cases are offered a human agent, never argued with.

## Test it

1. Add one test row to `Orders` with your own number.
2. Send a POST to the `new-order` webhook (or run the workflow once in
   n8n with Execute workflow).
3. Answer the call, confirm the items and address, hang up — check
   `CallLog` and the `#kitchen-orders` Slack channel.
