from django.db import models
from django.core import validators
from PIL import *
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, userdata, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not userdata["name"]:
            raise ValueError('Users must have a username')
        user = self.model(
            username=userdata["name"],
        )
 
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        print("super1")
        user = self.create_user(
            userdata={
                "name":username,
            },
            password=password,
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
    email = models.EmailField(
        verbose_name="メールアドレス",
        max_length=255,
        unique=True,
        null=True,
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
    REQUIRED_FIELDS = []
 
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
 
    building = models.ForeignKey(
        Building,
        on_delete = models.CASCADE,
        null = True,
        blank=True,
    )

    vibration_data = models.FileField(
        upload_to='files/%s/' % (str(id_vibration_data)),
        blank=True,
        null=True,
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

def get_numberImage_path(instance, filename):
    return "files/%s/%s" % (instance.own_user.username, filename)

class NumberImage(models.Model):
    imageName = models.CharField(
        verbose_name = '画像ファイル名',
        max_length = 255,
    )

    own_user = models.ForeignKey(
        CustomUser,
        verbose_name = '管理者',
        on_delete = models.CASCADE,
        null=False,
    )

    image = models.ImageField(
        upload_to=get_numberImage_path,
    )

    number = models.PositiveSmallIntegerField(
        null = True,
        blank = True,
        validators=[validators.MinValueValidator(0),
                    validators.MaxValueValidator(9)],
    )

    def __str__(self):
        return str(self.imageName)