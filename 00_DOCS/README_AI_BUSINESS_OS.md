# AI Business OS — n8n Operational Pack (V1)

This pack gives you an autonomy-ready **kernel** built entirely as **n8n workflows** + a Postgres schema:
- Event ingest webhook -> events/tasks
- Cron dispatcher -> policy gate -> routing
- Policy gate (sub-workflow) -> approval request if blocked
- Approval request -> writes approvals + optional Slack notify
- Approval decision webhook -> unblocks or fails tasks
- Content factory sub-workflow -> generates a brief + queues publish tasks
- Finance gate sub-workflow -> reconciliation check + hold/approval path + ledger reservation
- Kill switch sub-workflow -> opens incident + optional Slack notify
- Hourly metrics snapshot workflow

## 1) Prereqs
- n8n (self-hosted recommended)
- Postgres (required)
- Optional: Slack credential in n8n

## 2) Install
1. Create a Postgres database (e.g. `ai_business_os`).
2. Run `schema.sql`.
3. In n8n, create a **Postgres credential** named however you like and set it as default for Postgres nodes (or open each node and select it).
4. Import all JSON workflows in this folder.

## 3) Required environment variables (n8n)
These are read in Execute Workflow nodes / Slack message links:

- `AIOS_WF_POLICY_GATE_ID` = workflow id of "AI-OS 03 - Policy Gate (Sub-workflow)"
- `AIOS_WF_APPROVAL_REQUEST_ID` = workflow id of "AI-OS 04 - Approval Request (Create + Notify)"
- `AIOS_WF_CONTENT_FACTORY_ID` = workflow id of "AI-OS 06 - Content Factory (Brief -> Queue Publish)"
- `AIOS_WF_FINANCE_GATE_ID` = workflow id of "AI-OS 07 - Finance Gate (Reconcile -> Hold/Approve)"
- `AIOS_WF_KILL_SWITCH_ID` = workflow id of "AI-OS 08 - Incident Kill Switch"
- `AIOS_BASE_URL` = your n8n public base URL (for approval links), e.g. https://n8n.yourdomain.com
- Optional:
  - `AIOS_SLACK_APPROVAL_CHANNEL`
  - `AIOS_SLACK_INCIDENT_CHANNEL`

## 4) First run test
Send an event:
POST /webhook/ai-os/event-ingest
Body:
{
  "business_name": "LSN",
  "event_type": "content.request",
  "payload": { "topic": "Product demo", "platform": "tiktok" }
}

It should create a task. The dispatcher will pick it up and run policy gate -> content factory.

## 5) Approvals test
Create a policy (cap) and send a big payout request.

Example policy insert:
INSERT INTO policies(business_id, policy_key, policy_json)
SELECT id, 'finance_caps', '{"max_payout_cents_without_approval": 25000}'::jsonb
FROM businesses WHERE name='LSN';

Trigger:
event_type = finance.payout.request
payload = { "payee_id": "creator_123", "amount_cents": 99000, "external_ref": "abc" }

It should create an approval and block the task.
Approve via:
GET /webhook/ai-os/approve?approval_id=<id>&decision=approved

## 6) Next upgrade hooks (recommended)
- Add real reconciliation matching (Stripe/Xero/Shopify payouts)
- Add publish workflow (TikTok/YouTube/IG posting) behind 'content.publish'
- Add fraud/risk scoring into Policy Gate
- Add Ops Console UI (optional) reading from the same Postgres tables
