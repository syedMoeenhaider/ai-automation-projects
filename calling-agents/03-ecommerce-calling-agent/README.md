# E-commerce Calling Agent — Order Confirmation & COD Verification

AI voice agent that calls customers right after they place an online order to
confirm the order, verify the cash-on-delivery (COD) address, and confirm a
delivery day and time slot. Built with **Vapi** (voice) + **n8n**
(orchestration).

## What it does

1. Every 2 hours between 09:00 and 21:00, n8n reads the `Orders` Google
   Sheet.
2. Orders with status `new` are queued, one by one.
3. Vapi calls each customer with the E-commerce Order Confirmation
   assistant (Urdu-first voice, `ur-PK-AsadNeural`).
4. The assistant reads back the order ID, items and total, verifies the COD
   address, and confirms a delivery day and time slot. The customer can
   change the address, reschedule delivery, or cancel the order on the call.
5. When the call ends, Vapi sends an end-of-call report to n8n, which logs
   the outcome in the `CallLog` sheet. If the customer confirmed the order,
   the order status is updated to `confirmed` in the `Orders` sheet and the
   team is notified on Slack.

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
4. **Sheet columns** (`Orders`): `name`, `phone`, `email`, `orderId`,
   `orderTotal`, `address`, `status` (`new`/`confirmed`/`cancelled`).
5. Set the Vapi assistant's server URL / webhook to your n8n
   `vapi-call-report` webhook so end-of-call reports arrive.

## Safety rules (built into the assistant)

- Never asks for card details, bank details, PIN, OTP, or password —
  payment is cash on delivery only.
- Address changes and cancellations are confirmed once with the customer
  before the tool is used.
- Busy or complex cases end politely with a callback offer, never pressure.

## Test it

1. Add one test row to `Orders` with your own number.
2. Run the workflow once in n8n (Execute workflow).
3. Answer the call, confirm the order, hang up — check `CallLog`, the
   `Orders` sheet status, and Slack.
