from django.db import models

class ParentSub(models.Model):
    date_created = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)



    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.date_created



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

class Premium(ParentSub):
    class Meta:
        pass