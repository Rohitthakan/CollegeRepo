from django.db import models

# Create your models here.
class Question(models.Model):
    email = models.CharField(max_length=40, default="rr21phe0016@student.nitw.ac.in")

    BRANCH_CHOICES = (
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('Chemical', "Chemical Engineering"),
        ('Civil', 'Civil Engineering'),
        ('MME', 'Metallurgical and Materials Engineering'),
        ('Biotech', 'Biotechnology'),
        ('IMSC', 'Integrated Msc')
    )
    branch = models.CharField(max_length=50, choices=BRANCH_CHOICES)

    SEMESTER_CHOICES = (
        ('1st', '1st Sem'),
        ('2nd', '2nd Sem'),
        ('3rd', '3rd Sem'),
        ('4th', '4th Sem'),
        ('5th', '5th Sem'),
        ('6th', '6th Sem'),
        ('7th', '7th Sem'),
        ('8th', '8th Sem')
    )
    semester = models.CharField(max_length=50, choices=SEMESTER_CHOICES)

    Exam_Type = (
        ('Minor-1', 'Minor-1'),
        ('Mid Sem', 'Mid Sem'),
        ('Minor-2', 'Minor-2'),
        ('End Sem', 'End Sem'),
    )
    exam_type = models.CharField(max_length=15, choices=Exam_Type, default="Minor-1")

    subject = models.CharField(max_length=200)
    document = models.FileField(upload_to='Question-Papers')
    time = models.DateTimeField(auto_now_add=True)
    token = models.BigAutoField(primary_key=True)

    def __str__(self):
        return self.subject

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' => ' + self.email


class ConfirmationData(models.Model):
    token = models.CharField(max_length=255, unique=True)
    branch = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    exam_type = models.CharField(max_length=100)
    document = models.FileField(upload_to='Question-Papers')
    user_email = models.EmailField()
    def __str__(self):
        return self.branch + "->" + self.subject
