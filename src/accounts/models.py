from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
import random
import os

def get_filename_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext

def upload_image_path(instance, filename):
	new_filename = random.randint(1,3910209312)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
	return "images/{new_filename}/{final_filename}".format(new_filename=new_filename,final_filename=final_filename)

class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not full_name:
            raise ValueError("Users must have a full name")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            email = self.normalize_email(email),
            full_name = full_name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staffuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email, 
            full_name=full_name,
            password=password, 
            is_staff=True
        )
        return user
    
    def create_superuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email, 
            full_name=full_name,
            password=password, 
            is_staff=True,
            is_admin=True
        )
        return user

class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255, unique=True)
    full_name   = models.CharField(max_length=255, null=True, blank=True)
    profile_pic = models.ImageField(upload_to=upload_image_path, null=True, blank=True, default="images/blank_avatar.png")
    active      = models.BooleanField(default=True)
    admin       = models.BooleanField(default=False)
    staff       = models.BooleanField(default=False)
    related     = models.CharField(max_length=255, blank=True, null=True)
    recent_searches      = models.CharField(max_length=255, blank=True, null=True)
    genres      = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_recent_searches(self):
        return self.recent_searches

    @property
    def is_admin(self):
        return self.admin

    # @property
    # def is_active(self):
    #     return self.active

    @property
    def is_staff(self):
        return self.staff

    def get_profile_pic(self):
        if (self.profile_pic):
            return self.profile_pic.url
        return None
    
    def get_genres(self):
        if self.genres is not None:
            genres =  self.genres.split(",")
            genres = [x for x in genres if x]
            return genres
        return []



