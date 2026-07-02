from django.db import models
from django.conf import settings

class Source(models.Model):
    SOURCE_TYPES = [
        ('HOSPITAL', 'Hospital / Centro de Salud'),
        ('SHELTER', 'Refugio / Albergue'),
        ('RED_SOCIAL', 'Redes Sociales (X, Facebook, etc.)'),
        ('SHEET', 'Google Sheets Colaborativos'),
        ('API', 'API Externa / Base de Datos Pública'),
        ('OTHER', 'Otra fuente'),
    ]

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=30, choices=SOURCE_TYPES, default='OTHER')
    url = models.URLField(blank=True, null=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Investigation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('IN_PROGRESS', 'En Proceso'),
        ('COMPLETED', 'Completada'),
        ('FAILED', 'Fallida'),
    ]

    case = models.ForeignKey(
        'core.Case',
        on_delete=models.CASCADE,
        related_name='investigations',
        help_text="Caso asociado a la investigación"
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='investigations',
        help_text="Investigador u operador encargado de ejecutar la investigación"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Investigación #{self.id} - Caso #{self.case_id} ({self.get_status_display()})"


class SourceResult(models.Model):
    CONFIDENCE_CHOICES = [
        ('LOW', 'Baja'),
        ('MEDIUM', 'Media'),
        ('HIGH', 'Alta'),
    ]

    investigation = models.ForeignKey(
        Investigation,
        on_delete=models.CASCADE,
        related_name='results'
    )
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name='results'
    )
    title = models.CharField(max_length=300)
    content = models.TextField(help_text="Texto o información recuperada de la fuente")
    url = models.URLField(blank=True, null=True, help_text="Enlace directo a la información encontrada")
    confidence = models.CharField(
        max_length=10, 
        choices=CONFIDENCE_CHOICES, 
        default='MEDIUM',
        help_text="Nivel de confianza en que el resultado coincida con la búsqueda"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resultado en {self.source.name}: {self.title[:50]}... ({self.get_confidence_display()})"
