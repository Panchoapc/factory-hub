from .models import Product, SalesOrder, SalesOrderItem
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


class SalesOrderItemWriteSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())

    class Meta:
        model = SalesOrderItem
        fields = ["product", "quantity", "unit_price",
                  "unit_discount", "total_price"]
        extra_kwargs = {

            "unit_price": {"required": False},
            "unit_discount": {"required": False},
            "total_price": {"required": False},
        }


class SalesOrderItemReadSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.HyperlinkedRelatedField(
        view_name="product-detail",
        lookup_field="pk",
        read_only=True,
    )

    class Meta:
        model = SalesOrderItem
        fields = ["url", "id", "product", "quantity",
                  "unit_price", "unit_discount", "total_price"]
        extra_kwargs = {
            "url": {"view_name": "salesorderitem-detail", "lookup_field": "pk"}}


class SalesOrderSerializer(serializers.HyperlinkedModelSerializer):

    sales_order_items = SalesOrderItemWriteSerializer(
        many=True, write_only=True, required=False)

    items_detail = SalesOrderItemReadSerializer(
        source="sales_order_items",
        many=True,
        read_only=True,
    )

    class Meta:
        model = SalesOrder
        fields = [
            "url", "id", "client", "order_date", "delivery_date",
            "status", "sales_order_items", "items_detail", "total_amount", "order_discount",
        ]
        read_only_fields = ["order_date", "total_amount"]
        extra_kwargs = {
            "url": {"view_name": "salesorder-detail", "lookup_field": "pk"}}

    def create(self, validated_data):
        items_data = validated_data.pop("sales_order_items", [])

        running_total = 0
        prepared_items = []

        for item in items_data:
            product = item["product"]
            quantity = item.get("quantity", 1)

            unit_price = item.get("unit_price", product.price)
            unit_discount = item.get(
                "unit_discount", product.promotional_discount)
            total_price = item.get(
                "total_price", (unit_price - unit_discount) * quantity)

            running_total += total_price
            prepared_items.append({
                "product": product,
                "quantity": quantity,
                "unit_price": unit_price,
                "unit_discount": unit_discount,
                "total_price": total_price,
            })

        order_discount = validated_data.get("order_discount", 0)
        validated_data["total_amount"] = max(running_total - order_discount, 0)

        sales_order = SalesOrder.objects.create(**validated_data)

        SalesOrderItem.objects.bulk_create([
            SalesOrderItem(sales_order=sales_order, **pi) for pi in prepared_items
        ])

        return sales_order

    def update(self, instance, validated_data):
        items_data = validated_data.pop("sales_order_items", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:

            instance.sales_order_items.all().delete()

            running_total = 0
            prepared_items = []

            for item in items_data:
                product = item["product"]
                quantity = item.get("quantity", 1)
                unit_price = item.get("unit_price", product.price)
                unit_discount = item.get(
                    "unit_discount", product.promotional_discount)
                total_price = item.get(
                    "total_price", (unit_price - unit_discount) * quantity)

                running_total += total_price
                prepared_items.append({
                    "product": product,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "unit_discount": unit_discount,
                    "total_price": total_price,
                })

            SalesOrderItem.objects.bulk_create([
                SalesOrderItem(sales_order=instance, **pi) for pi in prepared_items
            ])

            instance.total_amount = max(
                running_total - instance.order_discount, 0)
            instance.save()

        return instance
