from datetime import datetime
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client


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
