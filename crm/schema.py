import graphene
import re
from .models import Customer, Product, Order
from graphene_django.types import DjangoObjectType
from django.db import transaction
from django.utils import timezone


# create GraphQl types for Mutation
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = '__all__'


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock']


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_date', 'total_amount']

    # To ensure nested objects (e.g. orders with customer
    # and product details) are supported:
    customer = graphene.Field(lambda: CustomerType)
    products = graphene.List(lambda: ProductType)


# Creating Mutation
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)

    customer = graphene.Field(CustomerType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, name, email, phone):
        if Customer.objects.filter(email=email).exists():
            return CreateCustomer(
                success=False, message="Email already exists.")
        if phone and not re.match(r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4}|\d{10,15})$', phone):
            return CreateCustomer(
                success=False, message='Invalid phone format.')
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer, success=True,
                              message='Customer created successfully.')


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(graphene.JSONString, required=True)
    created_customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, customers):
        # make a list for Created customers and Errors made
        created = []
        errors = []

        with transaction.atomic():
            for idx, data in enumerate(customers):

                try:
                    name = data.get('name')
                    email = data.get('email')
                    phone = data.get('phone')

                    if not name or not email:
                        return ValueError('Missing required fields.')

                    if phone and not re.match(r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4}|\d{10,15})$', phone):
                        return ValueError('invalid phone format')

                    if Customer.objects.filter(email=email).exists():
                        return ValueError('Email already exist')

                    customer = Customer(name=name, email=email, phone=phone)
                    customer.save()
                    created.append(customer)
                except Exception as e:
                    errors.append(f'Record {idx+1} : {str(e)}')
        return BulkCreateCustomers(created_customers=created, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int()

    success = graphene.Boolean()
    message = graphene.String()
    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock):
        if price < 0:
            return CreateProduct(success=False,
                                 message='Price must be positive')
        if stock < 0:
            return CreateProduct(success=False,
                                 message='Stock must be positive')
        product = Product(name=name, price=price, stock=stock)
        product.save()
        return CreateProduct(product=product, success=True,
                             message='Product succesfully Created')


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.DateTime()

    order = graphene.Field(OrderType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, customer_id, product_ids, order_date):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return CreateOrder(success=False, message='invalid customer_id')

        if not product_ids:
            return CreateOrder(
                success=False, message='one product must be selected')

        products = Product.objects.filter(id__in=product_ids)
        if products.count() != len(product_ids):
            return CreateOrder(
                success=False, message='One or more product IDs are invalid.')
        total_price = sum(p.price for p in products)
        order = Order(customer=customer,
                      order_date=order_date or timezone.now(),
                      total_price=total_price)
        order.save()
        order.products.set(products)
        return CreateOrder(order=order, success=True,
                           message='Order created successfully.')


# creating Mutation
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()


# creating Query feilds
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    all_products = graphene.List(ProductType)
    all_orders = graphene.List(OrderType)

    customer = graphene.Field(CustomerType, id=graphene.ID(required=True))
    product = graphene.Field(ProductType, id=graphene.ID(required=True))
    order = graphene.Field(OrderType, id=graphene.ID(required=True))

    def resolve_all_customers(root, info):
        return Customer.objects.all()

    def resolve_all_products(root, info):
        return Product.objects.all()

    def resolve_all_orders(root, info):
        return Order.objects.all()

    def resolve_customer(root, id, info):
        return Customer.objects.get(pk=id)

    def resolve_product(root, id, info):
        return Product.objects.get(pk=id)

    def resolve_order(root, id, info):
        return Order.objects.get(pk=id)
