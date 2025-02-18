from django.db import models
from django.contrib.auth.models import User

class GatePass(models.Model):
    pass_id = models.CharField(max_length=20, unique=True)
    date_time = models.DateTimeField(auto_now_add=True)
    institution = models.CharField(max_length=100)
    sub_department = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_quantity = models.IntegerField()
    product_serial_nos = models.CharField(max_length=100)
    product_description = models.TextField()
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    reason = models.TextField()
    expected_return_date = models.DateField(null=True, blank=True)
    employee_name = models.CharField(max_length=100)    
    employee_id = models.CharField(max_length=20)
    designation = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    return_status = models.CharField(max_length=50, default='Pending')
    actual_return_date = models.DateField(null=True, blank=True)

    # Approval-related fields
    approved_by_department_head = models.BooleanField(default=False)
    department_head_name = models.CharField(max_length=100, blank=True, null=True)  
    department_head_action_date = models.DateTimeField(null=True, blank=True)
    department_head_comments = models.TextField(blank=True, null=True)

    approved_by_security_head = models.BooleanField(default=False)
    security_head_name = models.CharField(max_length=100, blank=True, null=True)  
    security_head_action_date = models.DateTimeField(null=True, blank=True)
    security_head_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.pass_id

class ActionLog(models.Model):
    ACTION_TYPE_CHOICES = [
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending'),
    ]

    gate_pass = models.ForeignKey(GatePass, on_delete=models.CASCADE)
    action_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming action_by is a User instance
    action_type = models.CharField(max_length=50, choices=ACTION_TYPE_CHOICES)
    action_date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.action_type} by {self.action_by} on {self.gate_pass.pass_id}'

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Employee', 'Employee'),
        ('Department Head', 'Department Head'),
        ('Security Head', 'Security Head'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    institution = models.CharField(max_length=100, blank=True, null=True)  # Optional
    sub_department = models.CharField(max_length=100, blank=True, null=True)  # Optional
    department_head_name = models.CharField(max_length=100, blank=True, null=True)  # Optional for storing head's name
    security_head_name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.user.username


