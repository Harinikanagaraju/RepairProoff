
from django.contrib import admin
from .models import Appliance, RepairRecord

@admin.register(Appliance)
class ApplianceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand',
        'category',
        'purchase_date',
        'warranty_months',
        'price',
    )

    search_fields = ('name', 'brand', 'model_number')
    list_filter = ('category',)

@admin.register(RepairRecord)
class RepairRecordAdmin(admin.ModelAdmin):
    list_display = (
        'appliance',
        'repair_date',
        'repair_cost',
        'status',
    )

    list_filter = ('status',)