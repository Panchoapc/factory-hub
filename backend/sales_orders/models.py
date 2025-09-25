from django.db import models
from django.core.exceptions import ValidationError


class Product(models.Model):
    product_type = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    units_per_package = models.IntegerField()
    packages_per_box = models.IntegerField()
    promotional_discount = models.PositiveIntegerField(default=0)

    @property
    def name(self):
        return f"{self.brand} {self.product_type}"

    def __str__(self):
        return self.name


def rut_is_valid(rut: str) -> None:
    rut = rut.replace(".", "").replace("-", "").upper()
    cuerpo, digito_verificador = rut[:-1], rut[-1]

    suma = 0
    multiplo = 2
    for digit in reversed(cuerpo):
        suma += int(digit) * multiplo
        multiplo = 2 if multiplo == 7 else multiplo + 1

    resto = 11 - (suma % 11)

    digito_verificador_calc = ""
    if resto == 11:
        digito_verificador_calc = "0"
    elif resto == 10:
        digito_verificador_calc = "K"
    else:
        digito_verificador_calc = str(resto)

    if digito_verificador != digito_verificador_calc:
        raise ValidationError(f"{rut} no es un RUT válido")


class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    rut = models.CharField(max_length=20, unique=True,
                           validators=[rut_is_valid])

    def __str__(self):
        return self.name


STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('SHIPPED', 'Shipped'),
    ('DELIVERED', 'Delivered'),
    ('CANCELLED', 'Cancelled'),
]


class SalesOrder(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField()
    total_amount = models.PositiveIntegerField(default=0)
    order_discount = models.PositiveIntegerField(default=0)
    status = models.CharField(choices=STATUS_CHOICES,
                              default=STATUS_CHOICES[0][0])

    def __str__(self):
        return f"Order #{self.id} for {self.client.name}"  # type: ignore


class SalesOrderItem(models.Model):
    sales_order = models.ForeignKey(
        SalesOrder, on_delete=models.CASCADE, related_name="sales_order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    unit_discount = models.PositiveIntegerField(default=0)
    total_price = models.PositiveIntegerField()
