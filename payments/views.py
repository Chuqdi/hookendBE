import stripe
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from payments.models import PremiumPlus
from utils.helpers import generateAPIResponse
from rest_framework import permissions
from django.utils import timezone
from users.serializers import SignUpSerializer



from datetime import datetime, timedelta

def add_days_to_current_date(days):
    current_date = datetime.now().date()
    

    future_date = current_date + timedelta(days=days)
    
    return future_date


class UpdateUserPlan(APIView):
    def post(self, request, ):
        user = request.user
        plan = request.data.get("plan")
        count = request.data.get("count")
        planLengthInDays = request.data.get("planLengthInDays")

        date_to_complete = add_days_to_current_date(planLengthInDays)
        if plan == "PREMIUM":
            premium = user.premiumHooked 
            premium.is_active = True
            premium.date_created =timezone.now()
            premium.date_to_complete = date_to_complete
            premium.save()
        
        if plan == "PREMIUMPLUS":
            premiumPlus = user.premiumPlus
            if not premiumPlus:
                print("Setting premium plus")
                premiumPlus = PremiumPlus.objects.create()
                user.premiumPlus
                user.save()
            premiumPlus.is_active = True
            premiumPlus.date_created =timezone.now()
            premiumPlus.date_to_complete = date_to_complete
            premiumPlus.save()
            
            
        if plan == "WILD":
            wildFeature = user.wildFeature 
            wildFeature.is_active = True
            wildFeature.date_created =timezone.now()
            wildFeature.date_to_complete = date_to_complete
            wildFeature.save()
        
        if plan == "FILTER":
            advancedFilter = user.advancedFilter 
            advancedFilter.is_active = True
            advancedFilter.date_created =timezone.now()
            advancedFilter.date_to_complete = date_to_complete
            advancedFilter.save()
        
        if plan == "PROFILE":
            boostedProfile = user.boostedProfile 
            boostedProfile.is_active = True
            boostedProfile.date_to_complete = date_to_complete
            boostedProfile.date_created =timezone.now()
            boostedProfile.save()
        
        if plan == "COIN":
            user.coin = user.coin + int(count)
            user.save()
        if plan == "TEDDY":
            user.teddy = user.teddy + int(count)
            user.save()
        if plan == "ROSE":
            user.rose = user.rose + int(count)
            user.save()



        user = SignUpSerializer(user)
        print(user.data)

        return generateAPIResponse(
            user.data,
            "User subscription subscribed",
            status.HTTP_201_CREATED
        )



class InitializePaymentIntentView(APIView):
    permission_classes = [ permissions.IsAuthenticated ]
    def post(self, request, *args, **kwargs):
        data = request.data
        amount = data.get("amount")
        user = request.user
        stripe.api_key = settings.STRIPE_KEY
        
        try:
            customer = stripe.Customer.create(
            email=user.email,
            name=user.full_name,
    
        )
            paymentIntent = stripe.PaymentIntent.create(
            amount= int(amount) *100,
            receipt_email=user.email,
            customer=customer,
            currency="gbp",
            automatic_payment_methods={"enabled": True},
            )
        except Exception as e:
            return
        


        return generateAPIResponse(
                paymentIntent, "Payment intent generated", status.HTTP_200_OK
        )

       
