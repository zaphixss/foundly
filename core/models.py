from django.db import models
from accounts.models import User

# Create your models here.

REPORT_TYPES = (
    ('lost', 'lost'),
    ('found', 'found '),
)


STATUS = (
    ('claimed', 'claimed'),
    ('open', 'open '),
    ('resolved', 'Found '),
)


class Category(models.Model):
    title = models.CharField(unique=True, max_length=400)

    def __str__(self):
        return self.title
    
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    report_type = models.CharField(choices=REPORT_TYPES, default='lost')
    status = models.CharField(choices=STATUS, default='open')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    item_name = models.CharField(max_length=100)
    colour = models.CharField(max_length=30)
    description = models.TextField()

    location = models.CharField(max_length=255) 
    date_incident = models.DateField(help_text="Date the item was lost or found")
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

