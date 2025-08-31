#!/bin/bash
DELETED_COUNT=$(python3 /Users/Pro/Downloads/alx-backend-graphql_crm/manage.py shell << END
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta

cutoff_day = timezone.now() - timedelta(days=365)
inactive_customer = Customer.objects.filter(orders__isnull=True, created_at__lt=cutoff_day)
count = inactive_customer.count()
inactive_customer.delete()
print(count)
END
)

# Log the result with timestamp
echo "$(date): Deleted $DELETED_COUNT inactive_customer" >> /tmp/customer_cleanup_log.txt
