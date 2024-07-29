# mypass/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import GatePass, UserProfile
from .forms import ReturnableGatePassForm, NonReturnableGatePassForm

def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'index.html', {'error': 'Invalid username or password'})
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def dashboard_view(request):
    gate_passes = GatePass.objects.filter(employee_id=request.user.username)
    return render(request, 'dashboard.html', {'gate_passes': gate_passes})

@login_required
def returnable_form_view(request):
    if request.method == 'POST':
        form = ReturnableGatePassForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ReturnableGatePassForm()
    return render(request, 'returnable_form.html', {'form': form})

@login_required
def nonreturnable_form_view(request):
    if request.method == 'POST':
        form = NonReturnableGatePassForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = NonReturnableGatePassForm()
    return render(request, 'nonreturnable_form.html', {'form': form})

@login_required
def approval_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.role == 'Department Head':
        gate_passes = GatePass.objects.filter(approved_by_department_head=False)
    elif user_profile.role == 'Security Head':
        gate_passes = GatePass.objects.filter(approved_by_department_head=True, approved_by_security_head=False)
    else:
        gate_passes = []
    return render(request, 'approval.html', {'gate_passes': gate_passes})

@login_required
def activity_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.role == 'Employee':
        gate_passes = GatePass.objects.filter(employee_id=request.user.username)
    else:
        gate_passes = GatePass.objects.all()
    return render(request, 'activity.html', {'gate_passes': gate_passes})

def forgot_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        # Logic to send password reset email
        return redirect('index')
    return render(request, 'forgot_password.html')
