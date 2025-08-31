from celery import shared_task
from datetime import datetime
from graphene_django.settings import graphene_settings
from graphql import graphql_sync


@shared_task
def generate_crm_report():
    schema = graphene_settings.SCHEMA

    query = '''
    query {
        allCustomers
        allOrders
        allRevenue
    }
    '''

    result = graphql_sync(schema, query)
    data = result.data

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"{timestamp} - Report: {data['allCustomers']} customers, {data['allOrders']} orders, {data['allRevenue']} revenue\n"

    with open('/tmp/crm_report_log.txt', 'a') as f:
        f.write(log_line)
