from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    OPERATING_SYSTEMS = [
        ('windows', 'Windows'),
        ('linux', 'Linux'),
        ('macos', 'macOS'),
    ]
    
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    hostname = models.CharField(max_length=255, unique=True)
    os_type = models.CharField(max_length=20, choices=OPERATING_SYSTEMS)
    ip_address = models.GenericIPAddressField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline')
    last_checkin = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hostname} ({self.os_type})"

class SoftwarePackage(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    file_path = models.FileField(upload_to='packages/')

    def __str__(self):
        return f"{self.name} - {self.version}"

class Deployment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    package = models.ForeignKey(SoftwarePackage, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Deployment of {self.package.name} to {self.client.hostname}"