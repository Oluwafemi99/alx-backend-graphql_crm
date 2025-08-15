import django_filters
from .models import Customer, Product, Order


# django filter to name, email to Case-insensitive and partial matching
# date range filter is also added
class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains')
    email = django_filters.CharFilter(
        field_name='email', lookup_expr='icontains')
    created_at__gte = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte')
    created_at__lte = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte')
    phone_pattern = django_filters.CharFilter(method='filter_phone_pattern')

    def filter_phone_pattern(self, querryset, name, value):
        # Example: value = '+1' to match numbers starting with +1

        return querryset.filter(phone__startswith=value)

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_pattern']


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains')
    price_gte = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte')
    price_lte = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte')
    stock_gte = django_filters.NumberFilter(
        field_name='stock', lookup_expr='gte')
    stock_lte = django_filters.NumberFilter(
        field_name='stock', lookup_expr='lte')
    low_stock = django_filters.BooleanFilter(
        method='filter_low_stock')
    order_by = django_filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('stock', 'stock'),
            ('name', 'name'),
        )
    )

    def filter_low_stock(self, name, queryset, value):
        if value:
            return queryset.filter(stock__lt=10)
        return queryset

    class Meta:
        model = Product
        fields = ['name', 'price',
                  'stock', 'low_stock']


class OrderFilter(django_filters.FilterSet):
    total_amount_lte = django_filters.NumberFilter(
        field_name='total_amount', lookup_expr='lte'
    )
    total_amount_gte = django_filters.NumberFilter(
        field_name='total_amount', lookup_expr='gte'
    )
    order_date_lte = django_filters.DateFilter(
        field_name='order_date', lookup_expr='lte'
    )
    order_date_gte = django_filters.DateFilter(
        field_name='order_date', lookup_expr='gte'
    )
    customer_name = django_filters.CharFilter(
        field_name='customer__name', lookup_expr='icontains'
    )
    product_name = django_filters.CharFilter(
        field_name='products__name', lookup_expr='icontains'
    )

    product_id = django_filters.NumberFilter(method='filter_product_id')

    def filter_product_id(self, queryset, name, value):
        return queryset.filter(products__id=value)

    class Meta:
        model = Order
        fields = []

