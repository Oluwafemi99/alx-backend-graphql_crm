from datetime import datetime
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client
from django.utils import timezone


def log_crm_heartbeat():
    now = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_line = f"{now} CRM is alive\n"
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(log_line)

    # GraphQL hello field check using gql
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql("{ hello }")
        result = client.execute(query)
        hello_value = result.get("hello")
        if hello_value:
            msg = f"{now} GraphQL hello OK: {hello_value}\n"
        else:
            msg = f"{now} GraphQL hello FAIL: No hello field in response\n"
    except Exception as e:
        msg = f"{now} GraphQL hello ERROR: {e}\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(msg)


def update_low_stock():
    client = Client()
    mutation = '''
    mutation {
      updateLowStockProducts {
        success
        message
        updatedProducts {
          id
          name
          stock
        }
      }
    }
    '''
    response = client.post(
        "/graphql/",
        data={"query": mutation},
        content_type="application/json"
    )
    data = response.json().get("data", {}).get("updateLowStockProducts", {})
    log_path = "/tmp/low_stock_updates_log.txt"
    with open(log_path, "a") as f:
        f.write(f"\n[{timezone.now()}] {data.get('message')}\n")
        for prod in data.get("updatedProducts", []):
            f.write(f"  - {prod['name']} (ID: {prod['id']}): stock={prod['stock']}\n")
