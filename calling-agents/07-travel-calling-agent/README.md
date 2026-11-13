# Travel Calling Agent — Hotel & Flight Booking Confirmation

AI voice agent that calls travellers to confirm hotel and flight bookings,
verifies travel dates and guest details, and handles date changes or
cancellations. Built with **Vapi** (voice) + **n8n** (orchestration).

## What it does

1. Every day at 10:00 AM, n8n reads the `Bookings` Google Sheet.
2. Bookings with status `new` are queued, one by one.
3. Vapi calls each traveller with the Travel Booking Confirmation
   assistant (Urdu-first voice, `ur-PK-AsadNeural`).
4. The assistant reads back the booking type (hotel or flight), travel
   dates, guest count and total, verifies the traveller's details, and
   asks for confirmation.
5. If the traveller wants new dates, the assistant offers a date change
   as per policy; if they want to cancel, it explains the cancellation
   policy and records it only after they clearly agree. Complex changes
   go to a human travel agent.
6. When the call ends, Vapi sends an end-of-call report to n8n, which
   logs the outcome in the `CallLog` sheet. If the booking is confirmed,
   the itinerary is emailed to the traveller and the team is notified on
   Slack.

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
   Google Sheets, Vapi API key (HTTP Header Auth), Gmail, Slack.
3. Replace the placeholders:
   - `YOUR_GOOGLE_SHEET_ID` — sheet with `Bookings` and `CallLog` tabs
   - `YOUR_VAPI_ASSISTANT_ID`, `YOUR_VAPI_PHONE_NUMBER_ID`
   - `YOUR_N8N_URL` — your public n8n URL (webhook base) in the assistant tools
4. **Sheet columns** (`Bookings`): `name`, `phone`, `email`,
   `bookingType` (`hotel`/`flight`), `checkIn` (YYYY-MM-DD — for flights,
   the departure date), `checkOut` (YYYY-MM-DD — for flights, the return
   date), `status` (`new`/`done`).
5. Set the Vapi assistant's server URL / webhook to your n8n
   `vapi-call-report` webhook so end-of-call reports arrive.

## Safety rules (built into the assistant)

- Never invents prices, dates, hotel names, or flight numbers — only
  states what the booking tools return.
- Cancellations are recorded only after the traveller clearly agrees,
  and the policy is explained first.
- Never shares other travellers' booking details.
- Angry or complex cases (route changes, group bookings) go to a human
  travel agent, never argued with.

## Test it

1. Add one test row to `Bookings` with your own number.
2. Run the workflow once in n8n (Execute workflow).
3. Answer the call, confirm the booking, hang up — check `CallLog`,
   your email inbox, and Slack.
