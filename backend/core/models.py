from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('OPERATOR', 'Operador'),
        ('OSINT', 'Investigador OSINT'),
        ('DEVELOPER', 'Desarrollador'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='OPERATOR')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"


class Case(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Abierto'),
        ('INVESTIGATING', 'En Investigación'),
        ('RESOLVED_LOCATED', 'Cerrado - Localizado'),
        ('RESOLVED_NOT_LOCATED', 'Cerrado - No Localizado'),
        ('SUSPENDED', 'Suspendido'),
    ]
    PRIORITY_CHOICES = [
        ('LOW', 'Baja'),
        ('MEDIUM', 'Media'),
        ('HIGH', 'Alta'),
        ('CRITICAL', 'Crítica'),
    ]
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='OPEN')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_cases',
        help_text="Usuario interno responsable del seguimiento del caso"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Caso #{self.id} - {self.get_status_display()} ({self.get_priority_display()})"
