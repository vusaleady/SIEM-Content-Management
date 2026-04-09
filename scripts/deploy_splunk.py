import os
import requests
import json

SPLUNK_URL = os.getenv('SPLUNK_URL')
SPLUNK_TOKEN = os.getenv('SPLUNK_TOKEN')

def deploy_rule(rule_file):
    with open(rule_file, 'r') as f:
        rule_data = json.load(f)
    
    endpoint = f"{SPLUNK_URL}/servicesNS/admin/search/saved/searches?output_mode=json"
    headers = {"Authorization": f"Bearer {SPLUNK_TOKEN}"}
    
    payload = {
        "name": rule_data['name'],
        "search": rule_data['search'],
        "description": rule_data['description'],
        "alert_type": "number of events",
        "alert_comparator": "greater than",
        "alert_threshold": "0",
        "cron_schedule": rule_data['cron_schedule'],
        "is_scheduled": 1,
        "output_mode": "json"
    }
    
    response = requests.post(endpoint, headers=headers, data=payload, verify=False, timeout=10)
    if response.status_code == 201:
        print(f"Uğurlu: {rule_data['name']} yaradıldı!")
    else:
        print(f"Xəta: {response.text}")

if os.path.exists('splunk_rules'):
    for file in os.listdir('splunk_rules'):
        if file.endswith('.json'):
            deploy_rule(f'splunk_rules/{file}')
