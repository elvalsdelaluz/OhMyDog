from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AdministradorDeCuenta(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("Los usuarios deben tener una cuenta de correo")
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password):
        user = self.model(
            email = self.normalize_email(email),
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class Cuenta(AbstractBaseUser):
    email = models.EmailField(verbose_name="email",max_length=60,unique=True)
    dni = models.CharField(verbose_name="DNI",max_length=10)
    numero = models.CharField(verbose_name="numero",max_length=10)
    nombre = models.CharField(verbose_name="nombre",max_length=40)
    edad = models.IntegerField(verbose_name="edad", null=True)
    date_joined = models.DateTimeField(verbose_name="date_joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last_login",auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = AdministradorDeCuenta()

    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True