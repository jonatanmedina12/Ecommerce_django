from django.db import models
<<<<<<< Updated upstream
from store.models import Product


=======
from store.models import Product, Variation
from accounts.models import Account
>>>>>>> Stashed changes
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
<<<<<<< Updated upstream
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
=======
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
>>>>>>> Stashed changes
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    def sub_total(self):
<<<<<<< Updated upstream
        return self.producto.price * self.quantity
    def __str__(self):
        return self.producto.product_name  # Devuelve el nombre del producto
=======
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product
>>>>>>> Stashed changes
