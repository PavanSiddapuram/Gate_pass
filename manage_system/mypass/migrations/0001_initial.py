# Generated by Django 5.0.4 on 2024-09-16 09:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GatePass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pass_id', models.CharField(max_length=20, unique=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('institution', models.CharField(max_length=100)),
                ('sub_department', models.CharField(max_length=100)),
                ('product_name', models.CharField(max_length=100)),
                ('product_quantity', models.IntegerField()),
                ('product_serial_nos', models.CharField(max_length=100)),
                ('product_description', models.TextField()),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='product_images/')),
                ('reason', models.TextField()),
                ('expected_return_date', models.DateField(blank=True, null=True)),
                ('employee_name', models.CharField(max_length=100)),
                ('employee_id', models.CharField(max_length=20)),
                ('designation', models.CharField(max_length=100)),
                ('contact_info', models.CharField(max_length=100)),
                ('return_status', models.CharField(default='Pending', max_length=50)),
                ('actual_return_date', models.DateField(blank=True, null=True)),
                ('approved_by_department_head', models.BooleanField(default=False)),
                ('department_head_action_date', models.DateTimeField(blank=True, null=True)),
                ('department_head_comments', models.TextField(blank=True, null=True)),
                ('approved_by_security_head', models.BooleanField(default=False)),
                ('security_head_action_date', models.DateTimeField(blank=True, null=True)),
                ('security_head_comments', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Pending', 'Pending')], max_length=50)),
                ('action_date', models.DateTimeField(auto_now_add=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('action_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('gate_pass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mypass.gatepass')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Employee', 'Employee'), ('Department Head', 'Department Head'), ('Security Head', 'Security Head')], max_length=50)),
                ('institution', models.CharField(blank=True, max_length=100, null=True)),
                ('sub_department', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
