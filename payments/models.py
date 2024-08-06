from django.db import models

class ParentSub(models.Model):
    date_created = models.DateTimeField(null=True, blank=True)
    plan = models.CharField(null=True, blank=True, max_length=255)
    productId = models.CharField(null=True, blank=True,max_length=255)
    date_to_complete = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)



    class Meta:
        abstract = True





class BoostedProfile(ParentSub):
    class Meta:
        pass

class AdvancedFilter(ParentSub):
    class Meta:
        pass
    

    
class WildFeature(ParentSub):
    class Meta:
        pass    

class PremiumHooked(ParentSub):
    class Meta:
        pass   

class PremiumPlus(ParentSub):
    class Meta:
        pass