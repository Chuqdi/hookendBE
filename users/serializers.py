from blocks.serailizers import BlockSerializer
from likes.serializers import LikeSerializer
from payments.serializers import AdvancedFilterSerializer, BoostedProfileSerializer, PremiumHookedSerializer, PremiumPlusSerializer, WildFeatureSerializer
from users.models import  User,UserAdvancedFilter
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.conf import settings


class UserAdvancedFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdvancedFilter
        fields = "__all__"


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length =8)
    liking = LikeSerializer(
        read_only=True,
        many=True,
    )
    my_likes = LikeSerializer(
        read_only=True,
        many=True,
    )
    premiumPlus = PremiumPlusSerializer(
        many=False,
        read_only=True,
    )

    premiumHooked = PremiumHookedSerializer(
        many=False,
        read_only=True,
    )

    wildFeature = WildFeatureSerializer(
        many=False,
        read_only=True,
    )
    advancedFilter = AdvancedFilterSerializer(
        many=False,
        read_only=True,
    )

    boostedProfile = BoostedProfileSerializer(
        many=False,
        read_only=True,
    )
    users_blocked= BlockSerializer(
        many=True,
        read_only=True,
    )
    advancedFilterValues =UserAdvancedFilterSerializer(
        many=False,
        read_only=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "full_name",
            "country",
            "is_active",
            "phone_number",
            "date_of_birth",
            "what_you_are_looking_for",
            "state",
            "sexual_orientation",
            "relationship_status",
            "interests",
            "age",
            "bio",
            "school",
            "work_title",
            "isOnline",
            "company_name",
            "latitude",
            "longitude",
            "drink",
            "drug",
            "kids",
            "language",
            "educationLevel",
            "relationshipGoal",
            "introvert",
            "starSign",
            "pets",
            "religion",
            "gender",
            "ethnicity",
            "primary_profile_image_index",
            "liking",
            "my_likes",
            "emailActivated",
            "profile_views",
            "first_profile_image",
            "second_profile_image",
            "third_profile_image",
            "fourth_profile_image",
            "fifth_profile_image",
            "users_blocked",
            "advancedFilterValues",
            "coin",
            "teddy",
            "rose",

            "premiumPlus",
            "premiumHooked",
            "wildFeature",
            "advancedFilter",
            "boostedProfile"
        ]
        extra_kwargs ={
            "users_blocked":{
                "many":True
            }
        }
       




    def validate(self, attrs):
        if User.objects.filter(email=attrs.get("email")).exists():
            raise ValidationError("User email already taken")

        return super().validate(attrs)
    
    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user
 