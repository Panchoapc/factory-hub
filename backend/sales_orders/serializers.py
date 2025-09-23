from rest_framework import serializers
from .models import SalesOrder, SalesOrderItem, Product, Client, STATUS_CHOICES


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    sales_orders = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='salesorder-detail'
    )

    class Meta:
        model = Client
        fields = ['url', 'id', 'name', 'email',
                  'phone', 'address', 'rut', 'sales_orders']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['url', 'id', 'product_type', 'brand', 'price',
                  'units_per_package', 'packages_per_box', 'promotional_discount']
        read_only_fields = ['name']


class SalesOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderItem
        fields = ['id', 'product', 'quantity',
                  'unit_price', 'unit_discount', 'total_price']


class SalesOrderSerializer(serializers.HyperlinkedModelSerializer):
    sales_order_items = SalesOrderItemSerializer(many=True)

    class Meta:
        model = SalesOrder
        fields = ['url', 'id', 'client', 'order_date', 'delivery_date',
                  'status', 'sales_order_items', 'total_amount', 'order_discount']
        read_only_fields = ['order_date', 'total_amount']

    def create(self, validated_data):
        items_data = validated_data.pop('sales_order_items')
        sales_order = SalesOrder.objects.create(**validated_data)
        total_amount = 0

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            unit_price = product.price
            unit_discount = product.promotional_discount
            total_price = (unit_price - unit_discount) * quantity

            SalesOrderItem.objects.create(
                sales_order=sales_order,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                unit_discount=unit_discount,
                total_price=total_price
            )

            total_amount += total_price

        sales_order.total_amount = total_amount - sales_order.order_discount
        sales_order.save()

        return sales_order
