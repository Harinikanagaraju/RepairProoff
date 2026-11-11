
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum

from .models import Appliance, RepairRecord
from .forms import ApplianceForm, RepairForm

def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                'Account created successfully!'
            )

            return redirect('dashboard')

    else:
        form = UserCreationForm()

    return render(
        request,
        'tracker/register.html',
        {'form': form}
    )

@login_required
def dashboard(request):

    appliances = Appliance.objects.filter(
        owner=request.user
    )

    total_appliances = appliances.count()

    active_warranties = sum(
        1 for appliance in appliances
        if appliance.warranty_status == 'Active'
    )

    expiring_warranties = sum(
        1 for appliance in appliances
        if appliance.warranty_status == 'Expiring Soon'
    )

    expired_warranties = sum(
        1 for appliance in appliances
        if appliance.warranty_status == 'Expired'
    )

    total_spent = appliances.aggregate(
        total=Sum('price')
    )['total'] or 0

    recent_appliances = appliances.order_by(
        '-created_at'
    )[:5]

    context = {
        'total_appliances': total_appliances,
        'active_warranties': active_warranties,
        'expiring_warranties': expiring_warranties,
        'expired_warranties': expired_warranties,
        'total_spent': total_spent,
        'recent_appliances': recent_appliances,
    }

    return render(
        request,
        'tracker/dashboard.html',
        context
    )

@login_required
def appliance_list(request):

    appliances = Appliance.objects.filter(
        owner=request.user
    ).order_by('-created_at')

    return render(
        request,
        'tracker/appliances.html',
        {'appliances': appliances}
    )

@login_required
def add_appliance(request):

    if request.method == 'POST':
        form = ApplianceForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            appliance = form.save(commit=False)
            appliance.owner = request.user
            appliance.save()

            messages.success(
                request,
                'Appliance added successfully!'
            )

            return redirect('appliances')

    else:
        form = ApplianceForm()

    return render(
        request,
        'tracker/appliance_form.html',
        {
            'form': form,
            'page_title': 'Add Appliance'
        }
    )

@login_required
def edit_appliance(request, pk):

    appliance = get_object_or_404(
        Appliance,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':
        form = ApplianceForm(
            request.POST,
            request.FILES,
            instance=appliance
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Appliance updated successfully!'
            )

            return redirect('appliances')

    else:
        form = ApplianceForm(instance=appliance)

    return render(
        request,
        'tracker/appliance_form.html',
        {
            'form': form,
            'page_title': 'Edit Appliance'
        }
    )

@login_required
def delete_appliance(request, pk):

    appliance = get_object_or_404(
        Appliance,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':
        appliance.delete()

        messages.success(
            request,
            'Appliance deleted successfully!'
        )

    return redirect('appliances')

@login_required
def repair_list(request):

    repairs = RepairRecord.objects.filter(
        appliance__owner=request.user
    ).select_related('appliance').order_by('-repair_date')

    return render(
        request,
        'tracker/repairs.html',
        {'repairs': repairs}
    )

@login_required
def add_repair(request):

    form = RepairForm(request.POST or None)

    form.fields['appliance'].queryset = Appliance.objects.filter(
        owner=request.user
    )

    if request.method == 'POST' and form.is_valid():
        form.save()

        messages.success(
            request,
            'Repair record added successfully!'
        )

        return redirect('repairs')

    return render(
        request,
        'tracker/repair_form.html',
        {'form': form}
    )