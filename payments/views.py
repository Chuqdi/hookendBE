import stripe
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from utils.helpers import generateAPIResponse
from rest_framework import permissions
from django.utils import timezone
from users.serializers import SignUpSerializer



class UpdateUserPlan(APIView):
    def post(self, request, ):
        user = request.user
        plan = request.data.get("plan")
        print(plan)

        if plan == "PREMIUM":
            premium = user.premium 
            premium.is_active = True
            premium.date_created =timezone.now()
            premium.save()
        if plan == "WILD":
            wildFeature = user.wildFeature 
            wildFeature.is_active = True
            wildFeature.date_created =timezone.now()
            wildFeature.save()
        
        if plan == "FILTER":
            advancedFilter = user.advancedFilter 
            advancedFilter.is_active = True
            advancedFilter.date_created =timezone.now()
            advancedFilter.save()
        
        if plan == "PROFILE":
            boostedProfile = user.boostedProfile 
            boostedProfile.is_active = True
            boostedProfile.date_created =timezone.now()
            boostedProfile.save()

        user = SignUpSerializer(user)

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
            print(paymentIntent)
        except Exception as e:
            print(e)
            return
        


        return generateAPIResponse(
                paymentIntent, "Payment intent generated", status.HTTP_200_OK
        )

       
