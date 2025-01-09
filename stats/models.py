from django.db import models
from django.utils import timezone


class Institution(models.Model):
    """Base model for educational institutions"""
    otm_code = models.CharField(max_length=20, unique=True)
    otm_name = models.CharField(max_length=255)
    ownership_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.otm_code} - {self.otm_name}"[0:50]

    class Meta:
        ordering = ['id']


class StatisticsSnapshot(models.Model):
    """Daily snapshot of institution statistics"""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    snapshot_date = models.DateField(default=timezone.now)

    # Bachelor's degree statistics
    bachelor_full_time = models.IntegerField(default=0)
    bachelor_evening = models.IntegerField(default=0)
    bachelor_part_time = models.IntegerField(default=0)
    bachelor_special = models.IntegerField(default=0)
    bachelor_joint = models.IntegerField(default=0)
    bachelor_distance = models.IntegerField(default=0)

    # Secondary Higher Education statistics
    secondary_full_time = models.IntegerField(default=0)
    secondary_evening = models.IntegerField(default=0)
    secondary_part_time = models.IntegerField(default=0)

    # Master's degree statistics
    masters_full_time = models.IntegerField(default=0)
    masters_evening = models.IntegerField(default=0)
    masters_part_time = models.IntegerField(default=0)
    masters_special = models.IntegerField(default=0)
    masters_joint = models.IntegerField(default=0)
    masters_distance = models.IntegerField(default=0)

    # Total count
    total_students = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('institution', 'snapshot_date')
        indexes = [
            models.Index(fields=['snapshot_date']),
            models.Index(fields=['institution', 'snapshot_date']),
        ]
        ordering = ['id']

    def __str__(self):
        return f"{self.institution.otm_name} - {self.snapshot_date}"

    def save(self, *args, **kwargs):
        # Calculate total before saving
        self.total_students = sum([
            self.bachelor_full_time,
            self.bachelor_evening,
            self.bachelor_part_time,
            self.bachelor_special,
            self.bachelor_joint,
            self.bachelor_distance,
            self.secondary_full_time,
            self.secondary_evening,
            self.secondary_part_time,
            self.masters_full_time,
            self.masters_evening,
            self.masters_part_time,
            self.masters_special,
            self.masters_joint,
            self.masters_distance
        ])
        super().save(*args, **kwargs)
