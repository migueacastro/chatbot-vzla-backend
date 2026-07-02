from django.db import models

class MissingPerson(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
        ('U', 'Desconocido'),
    ]
    STATUS_CHOICES = [
        ('MISSING', 'Desaparecido'),
        ('FOUND_ALIVE', 'Encontrado con Vida'),
        ('FOUND_DECEASED', 'Encontrado Fallecido'),
        ('UNKNOWN', 'Desconocido'),
    ]

    case = models.OneToOneField(
        'core.Case',
        on_delete=models.CASCADE,
        related_name='missing_person',
        help_text="Caso asociado a esta persona desaparecida"
    )
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    second_last_name = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=400, blank=True, help_text="Nombre completo auto-generado o ingresado")
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    nationality = models.CharField(max_length=100, blank=True, null=True, default="Venezolana")
    document_number = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='MISSING')
    notes = models.TextField(blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-generar full_name si no se especifica
        if not self.full_name:
            parts = [self.first_name, self.middle_name, self.last_name, self.second_last_name]
            self.full_name = " ".join([p for p in parts if p]).strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.get_status_display()})"


class Alias(models.Model):
    person = models.ForeignKey(
        MissingPerson,
        on_delete=models.CASCADE,
        related_name='aliases'
    )
    alias = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Aliases"

    def __str__(self):
        return f"Alias: {self.alias} (para {self.person.full_name})"


class Relative(models.Model):
    person = models.ForeignKey(
        MissingPerson,
        on_delete=models.CASCADE,
        related_name='relatives'
    )
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100, help_text="Parentesco (ej. Madre, Padre, Hermano)")
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.relationship} de {self.person.full_name})"


class LocationHistory(models.Model):
    person = models.ForeignKey(
        MissingPerson,
        on_delete=models.CASCADE,
        related_name='location_history'
    )
    location = models.CharField(max_length=300, help_text="Descripción de la ubicación o dirección")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    source = models.CharField(max_length=200, help_text="Fuente de donde proviene el reporte de ubicación")
    reported_at = models.DateTimeField(help_text="Fecha y hora en que se reportó el avistamiento")

    class Meta:
        verbose_name_plural = "Location histories"

    def __str__(self):
        return f"Reporte en {self.location} el {self.reported_at.strftime('%Y-%m-%d %H:%M')}"
