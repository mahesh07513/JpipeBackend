from __future__ import unicode_literals
from django.db import models
import django
from django import utils

from Crypto.Cipher import Blowfish
from django.conf import settings
import binascii
#from django_mysql.models import DynamicField, Model
# Create your models here.

class JP_Users(models.Model):
    UserId              = models.AutoField(primary_key=True)
    Fname               = models.CharField(max_length=50,null=True)
    Lname               = models.CharField(max_length=50,null=True)
    Username            = models.CharField(max_length=50,unique=True)
    Password            = models.CharField(max_length=100)
    TransPass           = models.CharField(max_length=50,null=True)
    Email               = models.CharField(max_length=50,null=True)
    MobileNo            = models.CharField(max_length=50,null=True)
    Address             = models.TextField(max_length=500,null=True)
    StatusActive        = models.BooleanField(default=True)
    Create_Date         = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Change_Date         = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    class Meta:
        db_table = "JP_Users"

class JP_Devices(models.Model):
    DeviceId            = models.AutoField(primary_key=True)
    DeviceName          = models.CharField(max_length=50,null=True)
    DeviceMac           = models.CharField(max_length=50,unique=True)
    DeviceSerial        = models.IntegerField(null=True)
    CUId                = models.ForeignKey('JP_Company_Users',db_column='CUId',on_delete=models.CASCADE,default=1)
    StatusActive        = models.BooleanField(default=True)
    Create_Date         = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Change_Date         = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    class Meta:
        db_table = "JP_Devices"

class JP_Device_Data(models.Model):
    DDId = models.AutoField(primary_key=True)
    DeviceId = models.ForeignKey('JP_Devices',db_column='DeviceId',on_delete=models.CASCADE)
    Device_Data  = models.TextField(null=True)
    # attrs = DynamicField(spec={
    #     'size': float,
    # })
    Voltage            = models.FloatField(null=True)

    StatusActive        = models.BooleanField(default=True)
    Create_Date         = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Change_Date         = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    class Meta:
        db_table = "JP_Device_Data"

class JP_User_Snipet(models.Model):
    SId = models.AutoField(primary_key=True)
    UserId     = models.ForeignKey('JP_Users',db_column='UserId',on_delete=models.CASCADE)
    SniptDesc           = models.TextField(null=True)
    StatusActive        = models.BooleanField(default=True)
    Create_Date         = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Change_Date         = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    class Meta:
        db_table = "JP_User_Snipet"


# Create your company models here.
class JP_Company(models.Model):
    CId             = models.AutoField(primary_key=True)
    CName           = models.CharField(max_length=50,unique=True)
    UserId          = models.ForeignKey('JP_Users',db_column='UserId',on_delete=models.CASCADE)
    CDesc           = models.CharField(max_length=200,null=True)
    CAddress        = models.TextField(max_length=500,null=True)
    StatusActive    = models.BooleanField(default=True)
    Create_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Change_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    class Meta:
        db_table = "JP_Company"

class JP_Company_Users(models.Model):
    CUId             = models.AutoField(primary_key=True)
    CUname           = models.CharField(max_length=50,null=True)
    CUsername        = models.CharField(max_length=50,unique=True)
    CPassword        = models.CharField(max_length=50)
    StatusActive    = models.BooleanField(default=True)
    Create_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Change_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    CId             = models.ForeignKey('JP_Company',db_column='CId',on_delete=models.CASCADE)

    class Meta:
        db_table = "JP_Company_Users"

class JP_Dconfig_Type(models.Model):
    CTid             = models.AutoField(primary_key=True)
    CTdesc           = models.CharField(max_length=50,unique=True)
    StatusActive    = models.BooleanField(default=True)
    Active_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Create_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Change_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    class Meta:
        db_table = "JP_Dconfig_Type"

class JP_DCType_Serial(models.Model):
    TSid             = models.AutoField(primary_key=True)
    TSdesc           = models.CharField(max_length=50,unique=True)
    CTid             = models.ForeignKey('JP_Dconfig_Type',db_column='CTid',on_delete=models.CASCADE,default=3)

    StatusActive    = models.BooleanField(default=True)
    Active_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Create_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Change_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    class Meta:
        db_table = "JP_DCType_Serial"

class JP_Dconfig_Operations(models.Model):
    COid             = models.AutoField(primary_key=True)
    COdesc           = models.CharField(max_length=50,unique=True)
    StatusActive    = models.BooleanField(default=True)
    Active_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Create_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Change_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    class Meta:
        db_table = "JP_Dconfig_Operations"

class JP_Device_Config(models.Model):
    ConfigId             = models.AutoField(primary_key=True)
    ConfigName           = models.CharField(max_length=50,unique=True)
    CId                  = models.ForeignKey('JP_Company',db_column='CId',on_delete=models.CASCADE)
    CUId               = models.ForeignKey('JP_Company_Users',db_column='CUId',on_delete=models.CASCADE)
    StatusActive    = models.BooleanField(default=True)
    Active_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Create_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Change_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    class Meta:
        db_table = "JP_Device_Config"

class JPD_Config_Details(models.Model):
    CDId            = models.AutoField(primary_key=True)
    ConfigId        = models.ForeignKey('JP_Device_Config',db_column='ConfigId',on_delete=models.CASCADE)
    CTid            = models.ForeignKey('JP_Dconfig_Type',db_column='CTid',on_delete=models.CASCADE)
    COid            = models.ForeignKey('JP_Dconfig_Operations',db_column='COid',on_delete=models.CASCADE)
    Frequency       = models.TimeField() 
    GpioPins        = models.CharField(max_length=50,null=True)
    StatusActive    = models.BooleanField(default=True)
    Active_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Create_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Change_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    class Meta:
        db_table = "JPD_Config_Details"

class JP_Device_Config_Mapping(models.Model):
    CMId            = models.AutoField(primary_key=True)
    DeviceId = models.ForeignKey('JP_Devices',db_column='DeviceId',on_delete=models.CASCADE)
    ConfigId        = models.ForeignKey('JP_Device_Config',db_column='ConfigId',on_delete=models.CASCADE)
    StatusActive    = models.BooleanField(default=True)
    Active_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Create_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Change_Date     = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    class Meta:
        db_table = "JP_Device_Config_Mapping"

################ Adaptar #########################################
class JP_Adapter(models.Model):
    AdapterId            = models.AutoField(primary_key=True)
    AdapterName          = models.CharField(max_length=50,null=True)
    AdapterMac            = models.CharField(max_length=50,null=True)
    #CUId                = models.ForeignKey('JP_Company_Users',db_column='CUId',on_delete=models.CASCADE,default=1)
    StatusActive        = models.BooleanField(default=True)
    Create_Date         = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    Change_Date         = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    class Meta:
        db_table = "JP_Adapter"








