from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class User(models.Model):
    TYPES_USER = [
        ('owner', 'Owner'),
        ('manager', 'Manager'),
        ('cashier', 'Cashier'),
    ]

    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=30)
    tipo = models.CharField(max_length=15, choices=TYPES_USER)

    def __str__(self):
        return f"{self.username} - {self.get_tipo_display()}"
    
class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    cpf = models.CharField(max_length=11)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Cliente {self.id}: {self.name} - Saldo devedor: R${self.balance}. "

class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE) 
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.client.balance += self.total_value
            self.client.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venda de R${self.total_value} para {self.client.name}."


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    paid_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.client.balance <= 0:
            raise ValidationError("O cliente não tem saldo devedor.")
        
        if self.paid_value <= 0:
            raise ValidationError("O valor pago deve ser maior que 0.")
        
        if self.paid_value > self.client.balance:
            raise ValidationError("O valor pago não pode ser maior que o saldo devedor do cliente.")

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.client.balance -= self.paid_value
            self.client.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pagamendo de R${self.paid_value} feito por {self.client.name}."

