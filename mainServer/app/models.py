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
        user = self.create_user(
            userdata={
                "name":username,
            },
            password=password,
        )
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
        return True
 
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
 
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

class ImageStorage(models.Model):
    id = models.AutoField(
        verbose_name = 'ファイル保存先ID',
        primary_key = True,
    )

    name = models.CharField(
        verbose_name = '保存先識別名',
        max_length = 255,
        null = False,
        blank = False,
    )

    own_user = models.ForeignKey(
        CustomUser,
        verbose_name = '所有者',
        on_delete = models.CASCADE,
        null=False,
    )

    server_type = models.CharField(
        verbose_name = "サーバタイプ",
        choices=[("ftp","ftp server"),("http", "http server")],
        max_length = 255,
    )

    enable_update = models.BooleanField(
        default = False,
    )

    _passwd = models.CharField(
        max_length = 255,
        null = True
    )

    ip = models.CharField(
        max_length = 255,
        default = "127.0.0.1"
    )

    user_ftp = models.CharField(
        max_length = 255,
        null = True
    )

    processing_type = models.CharField(
        max_length = 255,
        default = "nothing",
        choices=[("mnist","mnist number recognition"),("mosaic_YOLO", "assign mosaic using YOLO"),("nothing","do nothing")],
        null=True,
    )

    target = models.CharField(
        max_length = 255,
        choices=[("person", "person")],
        default = "person",
        null=True,
    )
 
    def __str__(self):
        return self.name

def get_numberImage_path(instance, filename):
    return "files/%s/%s" % (instance.own_user.username, filename)

class NumberImage(models.Model):
    imageName = models.CharField(
        verbose_name = '画像名',
        max_length = 255,
    )

    own_user = models.ForeignKey(
        CustomUser,
        verbose_name = '所有者',
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