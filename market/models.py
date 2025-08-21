from django.db import models

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
    telefone = models.CharField(max_length=13)
    endereco = models.CharField(max_length=200)

    def __str__(self):
        return f"Cliente {self.id}: {self.name}"
    

