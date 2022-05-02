from asyncio import format_helpers
from enum import unique
# from locale import ABMON_1
from statistics import mode
from time import timezone
from xml.parsers.expat import model
from django.db import models
import math

# Create your models here.

class User(models.Model):
    email= models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    otp = models.IntegerField(default=459)
    role=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)
    role=models.CharField(max_length=10)
    created_at=models.DateTimeField(auto_now_add=True,blank=False)
    updated_at=models.DateTimeField(auto_now=True,blank=False)
    

    def __str__(self):
        return self.email

class Chairman(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    contact_no=models.CharField(max_length=50)
    house_no=models.CharField(max_length=50)
    full_address=models.CharField(max_length=200)
    vehicle_type=models.CharField(max_length=50)
    vehicle_details=models.CharField(max_length=100)
    pic=models.FileField(upload_to='media/images/',default='media/images/no-images.png')
    
    def __str__(self):
        return self.name

class Societymember(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    chairman_id=models.ForeignKey(Chairman,on_delete=models.CASCADE,default="")
    name=models.CharField(max_length=50)
    email= models.EmailField(null=True)
    contact_no=models.CharField(max_length=50)
    house_no=models.CharField(max_length=50)
    full_address=models.CharField(max_length=200)
    job_profession=models.CharField(max_length=200)
    job_address=models.CharField(max_length=200)
    vehicle_type=models.CharField(max_length=50)
    vehicle_details=models.CharField(max_length=100)
    pic=models.FileField(upload_to='media/images/images/',default='media/images/no-images.png')
    
    def __str__(self):
        return self.name

class Watchman(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    email= models.EmailField(null=True)
    contact_no=models.CharField(max_length=50)
    full_address=models.CharField(max_length=200)
    age=models.CharField(max_length=50)
    status=models.CharField(max_length=50,default="pending")
    pic=models.FileField(upload_to='media/images/',default='media/images/no-images.png')
    
    def __str__(self):
        return self.name

class Events(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    chairman_id=models.ForeignKey(Chairman,on_delete=models.CASCADE,default="")
    event_title=models.CharField(max_length=50)
    event_date=models.DateField(null=True)
    event_discription=models.TextField(max_length=500)
    event_pic=models.FileField(upload_to='media/images/images/',default='media/images/no-images.png')
    created_at=models.DateTimeField(auto_now_add=True,blank=False)
    updated_at=models.DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.event_title

    def whenpublished(self):
        now = timezone.now()    
        diff= now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds         
            if seconds == 1:
                return str(seconds) +  "second ago"           
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + " minute ago"        
            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days       
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"

class Notice(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    chairman_id=models.ForeignKey(Chairman,on_delete=models.CASCADE,default="")
    notice_title=models.TextField(max_length=200)
    notice_date=models.DateField(null=True)
    notice_discription=models.TextField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True,blank=False)
    updated_at=models.DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.notice_title

class Photos(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    chairman_id=models.ForeignKey(Chairman,on_delete=models.CASCADE,default="" )
    c_pic=models.FileField(upload_to='media/images/images/',default='media/images/no-images.png')
    pic_name =models.CharField(max_length=50)
    pic_date=models.DateField(null=True)
    created_at=models.DateTimeField(auto_now_add=True,blank=False)
    updated_at=models.DateTimeField(auto_now=True,blank=False)
    def __str__(self):
        return self.pic_name

class Video(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    chairman_id=models.ForeignKey(Chairman,on_delete=models.CASCADE,default="" )
    video_name= models.CharField(max_length=500)
    video_file= models.FileField(upload_to='media/images/videos/', null=True, verbose_name="")
    created_at=models.DateTimeField(auto_now_add=True,blank=False)
    updated_at=models.DateTimeField(auto_now=True,blank=False)
    def __str__(self):
        return self.video_name + ": " + str(self.video_file)

class Complaints(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    member_id=models.ForeignKey(Societymember,on_delete=models.CASCADE,default="" )
    complaints_title=models.TextField(max_length=200)
    complaints_discription=models.TextField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True,blank=False)
    updated_at=models.DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.complaints_title

class Rentsell(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    member_id=models.ForeignKey(Societymember,on_delete=models.CASCADE,default="" )
    homevehicle_title=models.TextField(max_length=200)
    homevehicle_type=models.TextField(max_length=200)
    homevehicle_rentsell=models.TextField(max_length=200)
    homevehicle_discription=models.TextField(max_length=500)
    homevehicle_contactno=models.CharField(max_length=50)
    homevehicle_budget=models.CharField(max_length=50)
    homevehicle_address_no=models.CharField(max_length=200)
    homevehicle_preowned=models.CharField(max_length=50)
    pic=models.FileField(upload_to='media/images/images/',default='media/images/no-images.png')
    created_at=models.DateTimeField(auto_now_add=True,blank=False)
    updated_at=models.DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.homevehicle_title

class Maintenance(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    chairman_id=models.ForeignKey(Chairman,on_delete=models.CASCADE,default="" )
    year=models.TextField(max_length=50,default="")
    month=models.TextField(max_length=50)
    amount=models.TextField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True,blank=False)
    updated_at=models.DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.month

class Visitor(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    chairman_id=models.ForeignKey(Chairman,on_delete=models.CASCADE,default="" )
    house_no=models.TextField(max_length=50,default="")
    name=models.TextField(max_length=50)
    contact_no=models.TextField(max_length=50)
    email=models.TextField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True,blank=False)
    updated_at=models.DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.name
