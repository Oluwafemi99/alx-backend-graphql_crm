import asyncio
from datetime import datetime, timedelta, UTC
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/order_reminders_log.txt"

QUERY = gql("""
query GetRecentPendingOrders($fromDate: Date!) {
  allOrders(orderDateGte: $fromDate) {
    edges {
      node {
        id
        customer {
          email
        }
        orderDate
      }
    }
  }
}
""")


async def main():
    last_week = datetime.now(UTC) - timedelta(days=7)
    from_date = last_week.date().isoformat()
    transport = AIOHTTPTransport(url=GRAPHQL_ENDPOINT)
    async with Client(
        transport=transport,
        fetch_schema_from_transport=True
    ) as session:
        result = await session.execute(
            QUERY,
            variable_values={"fromDate": from_date}
        )
        orders = result.get("allOrders", {}).get("edges", [])
        with open(LOG_FILE, "a") as f:
            for edge in orders:
                order = edge["node"]
                log_line = (
                    f"{datetime.now().isoformat()} | "
                    f"Order ID: {order['id']} | "
                    f"Email: {order['customer']['email']}\n"
                )
                f.write(log_line)
    print("Order reminders processed!")

if __name__ == "__main__":
    asyncio.run(main())
