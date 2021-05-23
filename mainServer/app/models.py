from django.db import models
from django.core import validators
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have a username')
            print("create")
        user = self.model(
            username=username,
            date_of_birth=date_of_birth,
        )
 
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, date_of_birth, password=None):
        print("super1")
        user = self.create_user(
            username,
            password=password,
            date_of_birth=date_of_birth,
        )
        print("super2")
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):

    user_id = models.AutoField(
        verbose_name = 'ユーザID',
        primary_key=True,
    )
    username = models.CharField(
        verbose_name='ユーザ名',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(
        blank = True,
        null = True,
    )
    is_active = models.BooleanField(
        default=True
    )
    is_admin = models.BooleanField(
        default=False
    )

 
    manager = CustomUserManager()
 
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['date_of_birth']
 
    def __str__(self):
        return self.username
 
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
 
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
 
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Building(models.Model):
    
    id_building = models.AutoField(
        verbose_name = '建物ID',
        primary_key=True,
    )

    name_building = models.CharField(
        verbose_name = '建物名',
        max_length = 255,
    )

    address_lat = models.DecimalField(
        verbose_name = '緯度',
        max_digits=10, 
        decimal_places=7,
        default=0
    )

    address_lon = models.DecimalField(
        verbose_name = '経度',
        max_digits=10, 
        decimal_places=7,
        default=0
    )

    risk_rate = models.IntegerField(
        verbose_name = '危険度',
        blank = True,
        null = True,
        default = -1,
    )

    own_user = models.ForeignKey(
        CustomUser,
        verbose_name = '管理者',
        on_delete = models.CASCADE,
        null=True,
    )

    def __str__(self):
        return self.name_building



class VibrationData(models.Model):
    id_vibration_data = models.AutoField(
        verbose_name = '揺れデータ',
        primary_key = True,
    )

    vibration_data = models.FileField(
        upload_to='file/%Y/%m/%d',
        blank=True,
        null=True,
    )
 
    building = models.ForeignKey(
        Building,
        on_delete = models.CASCADE,
        null = True,
        blank=True,
    )

    def __str__(self):
        return str(self.id_vibration_data)


class Frequency(models.Model):
    Frequency = models.FloatField(
        verbose_name = "FFT結果",
        blank = True,
        null = True,
        default = -1,
    )

    source = models.ForeignKey(
        VibrationData,
        on_delete=models.CASCADE,
        null = True,
        blank = True,
    )
