
from django.db import models
from django.contrib.auth.models import User
from datetime import date
import calendar

def add_months(start_date, months):
    month = start_date.month - 1 + months
    year = start_date.year + month // 12
    month = month % 12 + 1

    day = min(
        start_date.day,
        calendar.monthrange(year, month)[1]
    )

    return date(year, month, day)

class Appliance(models.Model):

    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Kitchen', 'Kitchen'),
        ('Home Appliances', 'Home Appliances'),
        ('Other', 'Other'),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appliances'
    )

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100, blank=True)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    purchase_date = models.DateField()
    warranty_months = models.PositiveIntegerField(default=12)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    bill = models.FileField(
        upload_to='bills/',
        blank=True,
        null=True
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def warranty_end(self):
        return add_months(
            self.purchase_date,
            self.warranty_months
        )

    @property
    def warranty_status(self):
        today = date.today()
        end_date = self.warranty_end

        if end_date < today:
            return 'Expired'

        if (end_date - today).days <= 30:
            return 'Expiring Soon'

        return 'Active'

    def __str__(self):
        return f"{self.name} - {self.brand}"

class RepairRecord(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    appliance = models.ForeignKey(
        Appliance,
        on_delete=models.CASCADE,
        related_name='repairs'
    )

    issue = models.TextField()
    service_center = models.CharField(max_length=150, blank=True)

    repair_date = models.DateField()
    repair_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.appliance.name} - {self.status}"