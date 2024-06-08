from django.db import models

# Create your models here.
class Student(models.Model):
      name=models.CharField(max_length=50,default='John')
      email=models.CharField(max_length=50,default='example@gmail.com')
      dob=models.DateField(verbose_name=('Birthday'),null=True)
      English=models.IntegerField(default=0)
      Hindi=models.IntegerField(default=0)
      Maths=models.IntegerField(default=0)
      Science=models.IntegerField(default=0)
      Total_Score_10th=models.IntegerField(default=0)
      Physics=models.IntegerField(default=0)
      Chemistry=models.IntegerField(default=0)
      Maths2=models.IntegerField(default=0)
      Total_Score_12th=models.IntegerField(default=0)
      Overall_Score=models.IntegerField(default=0)
      Course=models.CharField(max_length=100,null=True)
      class Meta:
        db_table = 'student_records'