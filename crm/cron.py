from datetime import datetime
import requests


def log_crm_heartbeat():
    now = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_line = f"{now} CRM is alive\n"
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(log_line)

    # Optional: GraphQL hello field check
    try:
        resp = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if resp.ok and "hello" in resp.text:
            with open("/tmp/crm_heartbeat_log.txt", "a") as f:
                f.write(f"{now} GraphQL hello OK\n")
        else:
            with open("/tmp/crm_heartbeat_log.txt", "a") as f:
                f.write(f"{now} GraphQL hello FAIL\n")
    except Exception as e:
        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(f"{now} GraphQL hello ERROR: {e}\n")
