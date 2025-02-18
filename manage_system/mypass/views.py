from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
import uuid
from .models import GatePass, UserProfile
from .forms import ReturnableGatePassForm, NonReturnableGatePassForm
from django.contrib import messages


def generate_unique_gate_pass_id():
    """Generate a unique gate pass ID."""
    return 'MAHE-' + str(uuid.uuid4()).split('-')[0].upper()

def index_view(request):
    """Render the landing page (login page)."""
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after successful login
        else:
            messages.error(request, "Wrong username or password, Try Again.")  # Add an error message

    return render(request, 'index.html')  # Render the login page again if authentication fails

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def dashboard_view(request):
    """Display the dashboard based on the user's role."""
    user_profile = UserProfile.objects.get(user=request.user)
    role = user_profile.role

    # Retrieve gate passes based on user role
    if role == 'Employee':
        # Show up to 5 most recent gate passes created by the employee
        gate_passes = GatePass.objects.filter(employee_id=request.user.username).order_by('-date_time')[:5]
    elif role == 'Department Head':
        # Show gate passes in the department that are not yet approved by the Department Head
        gate_passes = GatePass.objects.filter(
            sub_department=user_profile.sub_department,
            approved_by_department_head=False
        ).order_by('-date_time')
    elif role == 'Security Head':
        # Show gate passes approved by Department Head but not yet approved by Security Head
        gate_passes = GatePass.objects.filter(
            approved_by_department_head=True,
            approved_by_security_head=False
        ).order_by('-date_time')
    else:
        # If the role is not recognized, show no gate passes
        gate_passes = GatePass.objects.none()  

    # Determine the status and class for each gate pass
    for gate_pass in gate_passes:
        if gate_pass.approved_by_security_head:
            gate_pass.status = 'Approved'
            gate_pass.status_class = 'badge-success'
        elif gate_pass.approved_by_department_head:
            gate_pass.status = 'Pending Security Approval'
            gate_pass.status_class = 'badge-warning'
        else:
            gate_pass.status = 'Pending Department Approval'
            gate_pass.status_class = 'badge-warning'

    # Prepare context for rendering the template
    context = {
        'gate_passes': gate_passes,
        'user_profile': user_profile,
    }

    return render(request, 'dashboard.html', context)


@login_required
def gatepass_form_view(request):
    if request.method == 'POST':
        form_type = request.POST.get('type')  # Get selected form type from the dropdown
        if form_type == 'returnable':
            form_class = ReturnableGatePassForm
        elif form_type == 'nonreturnable':
            form_class = NonReturnableGatePassForm
        else:
            messages.error(request, "Invalid gate pass type selected.")
            return redirect('gatepass_form')

        form = form_class(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            gate_pass = form.save(commit=False)
            gate_pass.employee_id = request.user.username
            gate_pass.pass_id = generate_unique_gate_pass_id()
            gate_pass.save()
            notify_approvers(gate_pass)
            return redirect('dashboard')
        else:
            # Re-render the form with validation errors and selected type
            return render(request, 'gatepass_form.html', {
                'form': form,
                'form_type': form_type,
            })
    else:
        # Initial GET request: show the form with type selection
        return render(request, 'gatepass_form.html', {'form_type': None})

@login_required
def approval_view(request):
    """Handle approval requests based on user role."""
    user_profile = UserProfile.objects.get(user=request.user)
    role = user_profile.role

    # Fetch pending gate passes based on user role
    if role == 'Department Head':
        gate_passes = GatePass.objects.filter(
            approved_by_department_head=False,
            sub_department=user_profile.sub_department
        )
    elif role == 'Security Head':
        gate_passes = GatePass.objects.filter(
            approved_by_department_head=True,
            approved_by_security_head=False
        )
    else:
        gate_passes = GatePass.objects.none()

    if request.method == 'POST':
        gate_pass_id = request.POST.get('gate_pass_id')
        action = request.POST.get('action')
        gate_pass = get_object_or_404(GatePass, id=gate_pass_id)

        # Handle approval and rejection
        if action == 'approve':
            if role == 'Department Head':
                gate_pass.approved_by_department_head = True
                gate_pass.department_head_name = user_profile.department_head_name  # Use the stored name
                gate_pass.department_head_action_date = timezone.now()
                messages.success(request, f'Gate pass {gate_pass.pass_id} approved by {gate_pass.department_head_name}.')
            elif role == 'Security Head':
                gate_pass.approved_by_security_head = True
                gate_pass.security_head_name = user_profile.security_head_name  # Use the stored name
                gate_pass.security_head_action_date = timezone.now()
                messages.success(request, f'Gate pass {gate_pass.pass_id} approved by {gate_pass.security_head_name}.')

        elif action == 'reject':
            if role == 'Department Head':
                gate_pass.approved_by_department_head = False
                gate_pass.department_head_action_date = timezone.now()
                messages.warning(request, f'Gate pass {gate_pass.pass_id} rejected by Department Head {user_profile.department_head_name}.')
            elif role == 'Security Head':
                gate_pass.approved_by_security_head = False
                gate_pass.security_head_action_date = timezone.now()
                messages.warning(request, f'Gate pass {gate_pass.pass_id} rejected by Security Head {user_profile.security_head_name}.')

        gate_pass.save()
        return redirect('approval')

    return render(request, 'approval.html', {
        'gate_passes': gate_passes,
        'user_profile': user_profile,
    })



@login_required
def activity_view(request):
    """Display activity logs based on user role."""
    user_profile = UserProfile.objects.get(user=request.user)
    role = user_profile.role

    if role == 'Employee':
        gate_passes = GatePass.objects.filter(employee_id=request.user.username)
    elif role == 'Department Head':
        gate_passes = GatePass.objects.filter(sub_department=user_profile.sub_department)
    elif role == 'Security Head':
        gate_passes = GatePass.objects.filter(approved_by_department_head=True)
    else:
        gate_passes = GatePass.objects.none()

    return render(request, 'activity.html', {'gate_passes': gate_passes, 'user_role': role})

def notify_approvers(gate_pass):
   #Notify Department Head and Security Head about the gate pass request.
    department_head = UserProfile.objects.filter(
        role='Department Head', sub_department=gate_pass.sub_department
    ).first()
    security_head = UserProfile.objects.filter(role='Security Head').first()

    if department_head:
        send_mail(
            'Gate Pass Approval Needed',
            f'Please review the gate pass request: {gate_pass.pass_id}',
            'from@example.com',  # Use a proper 'from' email
            [department_head.user.email],
        )

    if security_head:
        send_mail(
            'Gate Pass Approval Needed',
            f'Please review the gate pass request: {gate_pass.pass_id}',
            'pavanroyalsbsc3@gmail.com',  # Use a proper 'from' email
            [security_head.user.email],
        ) 

@login_required
def view_details_view(request, gate_pass_id):
    """View details of a specific gate pass."""
    gate_pass = get_object_or_404(GatePass, id=gate_pass_id)
    return render(request, 'view_details.html', {'gate_pass': gate_pass})

@login_required
def print_request_view(request, id):
    """Print details of a specific gate pass request."""
    gate_pass = get_object_or_404(GatePass, id=id)
    return render(request, 'print_request.html', {'gate_pass': gate_pass})

@login_required
def request_details(request, pk):
    """Fetch and display details of a gate pass request."""
    gate_pass = get_object_or_404(GatePass, pk=pk)
    context = {'gate_pass': gate_pass}
    return render(request, 'request_details.html', context)
