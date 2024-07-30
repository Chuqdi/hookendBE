from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from payments.models import AdvancedFilter, BoostedProfile, PremiumPlus, PremiumHooked, WildFeature




class DefaultFilterManager(models.Model):
    sexual_orientation = models.CharField(null=True, blank=True, max_length=300)
    what_you_are_looking_for = models.CharField(null=True, blank=True, max_length=300)
    relationship_status = models.CharField(null=True, blank=True, max_length=300)
    interests = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    school = models.TextField(null=True, blank=True)
    company_name = models.TextField(null=True, blank=True)
    work_title = models.TextField(null=True, blank=True)
    language = models.TextField(null=True, blank=True)
    drink = models.TextField(null=True, blank=True)
    drug = models.TextField(null=True, blank=True)
    kids = models.TextField(null=True, blank=True)
    introvert = models.TextField(null=True, blank=True)
    educationLevel = models.TextField(null=True, blank=True)
    relationshipGoal = models.TextField(null=True, blank=True)
    starSign = models.TextField(null=True, blank=True)
    pets = models.TextField(null=True, blank=True)
    gender = models.TextField(null=True, blank=True)
    religion = models.TextField(null=True, blank=True)
    ethnicity= models.TextField(null=True, blank=True)

    class Meta:
        abstract = True




class UserManager(BaseUserManager):
    def create(self, email,full_name,phone_number, password):
        if  not email:
            raise ValueError("Please enter your email")

        if  not phone_number:
            raise ValueError("Please enter your phone number")

        if password:
            raise ValueError("Please enter your password")

        user  = self.model(
            phone_number=phone_number, 
            full_name = full_name,
            email = self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    

    def  create_super_user(self, email, full_name,phone_number, password):
        user = self.create_user(email, full_name,phone_number, password)
        user.is_active=True
        user.is_superuser=True
        user.is_staff = True
        user.is_admin=True
        user.save(using=self._db)
        return user



class UserAdvancedFilter(DefaultFilterManager):
    class Meta:
        pass


class User(AbstractUser,DefaultFilterManager):
    username = models.CharField(null=True, blank=True,max_length=150)
    full_name = models.CharField(null=True, blank=True,max_length=150)
    phone_number =models.CharField(unique=True,null=False, blank=False,max_length=150)
    email  = models.EmailField(blank=False, null=False, unique=True,max_length=200, db_index=True)
    country = models.TextField(max_length=200, null=True, blank=True)
    state = models.TextField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    date_of_birth = models.CharField(null=True, blank=True, max_length=300)
    age = models.CharField(null=True, blank=True, max_length=300)
    latitude = models.TextField(null=True, blank=True)
    longitude = models.TextField(null=True, blank=True)
    isOnline = models.BooleanField(default=False)
    
    
    coin = models.IntegerField(default=0)
    rose = models.IntegerField(default=0)
    teddy = models.IntegerField(default=0)
    

    
    profile_views = models.IntegerField(default=0, null=True, blank=True)
    first_profile_image = models.ImageField(null=True, blank=True, upload_to="profile_images/")
    second_profile_image = models.ImageField(null=True, blank=True, upload_to="profile_images/")
    third_profile_image = models.ImageField(null=True, blank=True, upload_to="profile_images/")
    fourth_profile_image = models.ImageField(null=True, blank=True, upload_to="profile_images/")
    fifth_profile_image = models.ImageField(null=True, blank=True, upload_to="profile_images/")
    primary_profile_image_index = models.IntegerField(null=True, blank=True, default=0)
    


    advancedFilterValues = models.OneToOneField(UserAdvancedFilter, on_delete=models.CASCADE, null=True, blank=True)

    ##Subscriptions
    premiumPlus = models.OneToOneField(PremiumPlus, on_delete=models.CASCADE, related_name="premium", null=True, blank=True)
    premiumHooked = models.OneToOneField(PremiumHooked, on_delete=models.CASCADE, related_name="premium", null=True, blank=True)
    wildFeature =  models.OneToOneField(WildFeature, on_delete=models.CASCADE, related_name="premium", null=True, blank=True)
    advancedFilter = models.OneToOneField(AdvancedFilter,  on_delete=models.CASCADE, related_name="premium", null=True, blank=True)
    boostedProfile = models.OneToOneField(BoostedProfile,  on_delete=models.CASCADE, related_name="premium", null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=["phone_number"]



    def perm(self, *args, **kwargs):
        return True
    
    def perm_module(self, *args, **kwargs):
        return True
    
    
    
    

    


    def __str__(self) -> str:
        return str(self.email)






class UserEmailActivationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, null=False, blank=False)
    date_created = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.user.email
    
