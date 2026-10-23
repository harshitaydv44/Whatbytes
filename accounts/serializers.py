from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import models
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="first_name", max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        trim_whitespace=False
    )

    class Meta:
        model = User
        fields = ["name", "email", "password"]

    def validate_name(self, value):
        stripped = value.strip()
        if not stripped:
            raise serializers.ValidationError("Name cannot be blank.")
        return stripped

    def validate_email(self, value):
        normalized = value.strip().lower()
        if User.objects.filter(models.Q(username__iexact=normalized) | models.Q(email__iexact=normalized)).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return normalized

    def create(self, validated_data):
        name = validated_data.pop("first_name", "").strip()
        email = validated_data.pop("email").strip().lower()
        password = validated_data.pop("password")

        user = User(
            username=email,
            email=email,
            first_name=name
        )

        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False
    )

    def validate(self, data):
        email = data["email"].strip().lower()
        password = data["password"]

        user_obj = User.objects.filter(
            models.Q(email__iexact=email) | models.Q(username__iexact=email)
        ).first()

        username = user_obj.username if user_obj else email

        user = authenticate(
            request=self.context.get("request"),
            username=username,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This account is inactive."
            )

        refresh = RefreshToken.for_user(user)

        return {
            "message": "Login successful.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
