from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.db import IntegrityError

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth import get_user_model

CustomUser = get_user_model()

from ..base.serializers import Base64FileField
# User serilazers for token, register, update and login

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        # Get the user model
        User = get_user_model()

        # Check if the user exists
        try:
            user = User.objects.get(username=attrs['username'])
        except User.DoesNotExist:
            raise NotFound(detail="User not found", code=404)

        # Check if the user is active
        if not user.is_active:
            raise ValidationError("You are not allowed to login")

        # Call the parent validate method for further validation
        data = super().validate(attrs)
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get('refresh')
        if not refresh_token:
            raise serializers.ValidationError("Refresh token is required.")
        return attrs

class UserMeSerializer(WritableNestedModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'company',
            'status',
        )    
        
class UserSerializer(WritableNestedModelSerializer):
    
    password = serializers.CharField(validators=[validate_password],
                                    required=False, 
                                    allow_null=True, )
    

    username=serializers.CharField(max_length=255, required=False)

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'password',
            'username',
            'first_name',
            'last_name',
            'status',
            'company',
        )
        

    def create(self, validated_data):
        password = validated_data.pop('password', None)  
        try:
            user = CustomUser.objects.create(**validated_data)  # Try creating the user
            if password:
                user.set_password(password)  # Hash the password
            user.save()
            return user
        except IntegrityError:
            raise serializers.ValidationError(
                {"error": "A user with this username"}
            )


    def update(self, instance, validated_data):
        # Handle password securely
        password = validated_data.pop("password", None)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # If a new password is provided, set it securely
        if password:
            instance.set_password(password)
        try:
            instance.save()
        except IntegrityError:
            raise serializers.ValidationError({"error": "A database integrity error occurred. Please check the uniqueness of fields."})

        return instance
        

class UserSelfUpdateSerializer(WritableNestedModelSerializer):


    class Meta:
        model = CustomUser
        fields = (
            'id',
    
            'first_name',
            'last_name',)

        read_only_fields = ["id"]


class PasswordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "password", "username"]
        read_only_fields = ["id"]

    def validate_password(self, value):
        """Validate the password field."""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def validate_username(self, value):
        """Ensure username is unique except for the current user."""
        request_user = self.instance  
        if CustomUser.objects.filter(username=value).exclude(id=request_user.id).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def update(self, instance, validated_data):
        """Handle password updates securely."""
        password = validated_data.pop("password", None)

        if not password:
            raise serializers.ValidationError({"password": "This field is required."})
        instance.set_password(password)  # Securely hash the password
        instance.save()

        # Blacklist user's tokens if blacklisting is enabled
        self.blacklist_user_tokens(instance)

        return instance

    def blacklist_user_tokens(self, user):
        """Blacklist all outstanding JWT tokens for the user."""
        try:
            outstanding_tokens = OutstandingToken.objects.filter(user=user)
            for token in outstanding_tokens:
                BlacklistedToken.objects.get_or_create(token=token)
        except Exception as e:
            print(f"Token blacklisting failed: {e}")  # Log for debugging

