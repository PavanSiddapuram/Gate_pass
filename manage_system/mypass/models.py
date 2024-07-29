from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Employee', 'Employee'),
        ('Department Head', 'Department Head'),
        ('Security Head', 'Security Head'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username

class GatePass(models.Model):
    PASS_TYPE_CHOICES = [
        ('returnable', 'Returnable'),
        ('non_returnable', 'Non-Returnable'),
    ]

    pass_id = models.CharField(max_length=20, unique=True)
    date_time = models.DateTimeField(auto_now_add=True)
    institution_department = models.CharField(max_length=100)
    sub_department = models.CharField(max_length=100)
    material_product_name = models.CharField(max_length=100)
    material_product_quantity = models.IntegerField()
    product_material_serial_number = models.CharField(max_length=100)
    product_material_description = models.TextField()
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    reason = models.TextField()
    pass_type = models.CharField(max_length=20, choices=PASS_TYPE_CHOICES)
    expected_return_date = models.DateField(null=True, blank=True)
    employee_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    approved_by_department_head = models.BooleanField(default=False)
    approved_by_security_head = models.BooleanField(default=False)
    return_status = models.CharField(max_length=50, default='Pending')  # 'Returned', 'Overdue'

    def __str__(self):
        return self.pass_id
