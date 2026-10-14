#!/usr/bin/env python3
"""Bouwt docs/infra/chat-workflow.json (n8n-import) uit de leesbare JS-bronnen in deze map.
Run: python docs/infra/build-workflow.py   ->   daarna in n8n: Import from File, of `n8n import:workflow`.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ORIGINS = "https://thomashuybrechts.com,http://127.0.0.1:8765"  # merksites hier toevoegen zodra ze een adres hebben
LEAD_FROM = "hey@thomashuybrechts.com"
LEAD_TO = "__LEAD_TO__"  # placeholder: deploy-workflow.sh vult het echte adres in uit docs/infra/.env.local (niet in git)
SMTP_CRED = {"id": "HilLTRoKhYMXI62L", "name": "SMTP account"}  # verwijst naar de SMTP-instelling in n8n; None = geen lead-mail


def js(name):
    return (HERE / name).read_text(encoding="utf-8")


def node(name, type_, version, position, parameters, **extra):
    return {"parameters": parameters, "name": name, "type": type_, "typeVersion": version, "position": position, **extra}


nodes = [
    node("Webhook", "n8n-nodes-base.webhook", 2, [0, 0], {
        "httpMethod": "POST",
        "path": "chat",
        "responseMode": "responseNode",
        "options": {"allowedOrigins": ORIGINS},
    }, webhookId="th-chat"),
    node("Voorbereiden", "n8n-nodes-base.code", 2, [220, 0], {"jsCode": js("chat-voorbereiden.js")}),
    node("Geblokkeerd?", "n8n-nodes-base.if", 2, [440, 0], {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose"},
            "conditions": [{
                "id": "blocked",
                "leftValue": "={{ $json.blocked }}",
                "rightValue": "",
                "operator": {"type": "string", "operation": "notEmpty", "singleValue": True},
            }],
            "combinator": "and",
        },
    }),
    node("Groq", "n8n-nodes-base.httpRequest", 4.2, [660, 100], {
        "method": "POST",
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "groqApi",
        "sendBody": True,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify($json.payload) }}",
        "options": {"timeout": 15000},
    }, onError="continueRegularOutput", credentials={"groqApi": {"id": "RcCjzhXbcwSrxhdl", "name": "Groq account"}}),  # id verwijst naar de sleutel in n8n, de sleutel zelf staat nergens in de repo
    node("Antwoord", "n8n-nodes-base.code", 2, [880, 0], {"jsCode": js("chat-antwoord.js")}),
    node("Terugsturen", "n8n-nodes-base.respondToWebhook", 1.1, [1100, 0], {
        "respondWith": "json",
        "responseBody": "={{ { reply: $json.reply } }}",
    }),
]

# Lead-mail: pas ná het antwoord aan de bezoeker, zodat een trage of mislukte mail de chat niet ophoudt
if SMTP_CRED:
    nodes += [
        node("Lead?", "n8n-nodes-base.if", 2, [1320, 0], {
            "conditions": {
                "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose"},
                "conditions": [{
                    "id": "lead",
                    "leftValue": "={{ $('Antwoord').first().json.lead }}",
                    "rightValue": "",
                    "operator": {"type": "boolean", "operation": "true", "singleValue": True},
                }],
                "combinator": "and",
            },
        }),
        node("Lead-mail", "n8n-nodes-base.emailSend", 2.1, [1540, -100], {
            "fromEmail": LEAD_FROM,
            "toEmail": LEAD_TO,
            "subject": "=Nieuwe lead via de chatbot ({{ $('Antwoord').first().json.brand }}): {{ $('Antwoord').first().json.email }}",
            "emailFormat": "text",
            "text": "=Iemand liet een e-mailadres achter in de chat.\n\nE-mail: {{ $('Antwoord').first().json.email }}\nSite: {{ $('Antwoord').first().json.brand }}\n\n--- Gesprek ---\n\n{{ $('Antwoord').first().json.transcript }}",
            "options": {"appendAttribution": False},
        }, credentials={"smtp": SMTP_CRED}, onError="continueRegularOutput"),
    ]

connections = {
    "Webhook": {"main": [[{"node": "Voorbereiden", "type": "main", "index": 0}]]},
    "Voorbereiden": {"main": [[{"node": "Geblokkeerd?", "type": "main", "index": 0}]]},
    "Geblokkeerd?": {"main": [
        [{"node": "Antwoord", "type": "main", "index": 0}],
        [{"node": "Groq", "type": "main", "index": 0}],
    ]},
    "Groq": {"main": [[{"node": "Antwoord", "type": "main", "index": 0}]]},
    "Antwoord": {"main": [[{"node": "Terugsturen", "type": "main", "index": 0}]]},
}
if SMTP_CRED:
    connections["Terugsturen"] = {"main": [[{"node": "Lead?", "type": "main", "index": 0}]]}
    connections["Lead?"] = {"main": [[{"node": "Lead-mail", "type": "main", "index": 0}], []]}

workflow = {
    "id": "thChatWorkflow01",  # vast id: `n8n import:workflow` eist er een, en een herimport overschrijft dezelfde workflow
    "name": "Chat — thomashuybrechts.com + merksites",
    "nodes": nodes,
    "connections": connections,
    "settings": {"executionOrder": "v1"},
    "active": False,
}

out = HERE / "chat-workflow.json"
out.write_text(json.dumps(workflow, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(f"{out.name} geschreven ({len(nodes)} nodes)")
