from datetime import datetime
from django.db import models
from profil.models import CustomUser



class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.CharField(max_length=255, help_text="Comma-separated list of skills required")
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    location = models.CharField(blank=False, null=False, default='Morocco')
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='jobs')
    def __str__(self):
        return self.title
    

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    talent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='job_applications')
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(default=datetime.now)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)  # New field for uploading CVs
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Application by {self.talent.username} for {self.job.title}"
