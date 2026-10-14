#!/usr/bin/env bash
# Bouwt de chat-workflow en zet ze live in n8n (LXC 111 op pve). Run vanuit de repo-root: bash docs/infra/deploy-workflow.sh
set -euo pipefail
python docs/infra/build-workflow.py
# Lead-adres staat niet in de openbare repo: lokaal invullen, op de server laten landen
LEAD_TO=$(sed -n "s/^LEAD_TO=//p" docs/infra/.env.local 2>/dev/null)
[ -n "$LEAD_TO" ] || { echo "LEAD_TO ontbreekt in docs/infra/.env.local" >&2; exit 1; }
TMP=$(mktemp)
sed "s/__LEAD_TO__/$LEAD_TO/g" docs/infra/chat-workflow.json > "$TMP"
scp -q -o BatchMode=yes "$TMP" proxmox:/tmp/chat-workflow.json
rm -f "$TMP"
ssh -o BatchMode=yes proxmox 'pct push 111 /tmp/chat-workflow.json /opt/n8n/chat-workflow.json && rm /tmp/chat-workflow.json && pct exec 111 -- bash -c "
cd /opt/n8n
docker compose cp chat-workflow.json n8n:/tmp/chat-workflow.json >/dev/null 2>&1
docker compose exec -T n8n n8n import:workflow --input=/tmp/chat-workflow.json 2>&1 | grep -v TUNNEL
docker compose exec -T n8n n8n publish:workflow --id=thChatWorkflow01 2>&1 | grep -v TUNNEL | head -1
docker compose restart n8n >/dev/null 2>&1
for i in \$(seq 1 40); do code=\$(curl -s -o /dev/null -w %{http_code} http://127.0.0.1:5678/healthz); [ \"\$code\" = 200 ] && break; sleep 3; done
echo n8n healthz=\$code
"'
