import os
import requests
import json
import urllib3

# SSL xəbərdarlıqlarını gizlətmək üçün
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SPLUNK_URL = os.getenv('SPLUNK_URL')
SPLUNK_TOKEN = os.getenv('SPLUNK_TOKEN')

def deploy_rule(rule_file):
    with open(rule_file, 'r') as f:
        rule_data = json.load(f)

    # DÜZGÜN ENDPOINT: nobody istifadə edirik ki, hər kəs görə bilsin
    endpoint = f"{SPLUNK_URL}/servicesNS/nobody/search/saved/searches?output_mode=json"
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
        "disabled": 0
    }

    # verify=False əlavə edirik ki, SSL sertifikatı problem yaratmasın
    response = requests.post(endpoint, headers=headers, data=payload, verify=False)
    
    if response.status_code == 201:
        print(f"UĞURLU: {rule_data['name']} yaradıldı.")
    elif response.status_code == 409:
        print(f"MƏLUMAT: {rule_data['name']} artıq mövcuddur.")
    else:
        print(f"XƏTA ({response.status_code}): {response.text}")

# splunk_rules qovluğundakı bütün JSON-ları yoxla
rules_path = 'splunk_rules'
for filename in os.listdir(rules_path):
    if filename.endswith('.json'):
        deploy_rule(os.path.join(rules_path, filename))
