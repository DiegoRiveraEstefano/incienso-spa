from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import User


class UserWriteSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=64,
        style={'template': 'components/forms/input.html'},
        error_messages={
            "required": "Este Campo es Requerido.",
        },
        required=True
    )

    email = serializers.CharField(
        max_length=64,
        style={'template': 'components/forms/input.html', 'input_type': 'email'},
        error_messages={
            "required": "Este Campo es Requerido.",
        },
        required=True
    )

    first_name = serializers.CharField(
        max_length=64,
        style={'template': 'components/forms/input.html'},
        error_messages={
            "required": "Este Campo es Requerido.",
        },
    )

    last_name = serializers.CharField(
        max_length=64,
        style={'template': 'components/forms/input.html'},
        error_messages={
            "required": "Este Campo es Requerido.",
        },
    )

    password = serializers.CharField(
        max_length=64,
        style={'template': 'components/forms/input.html'},
        error_messages={
            "required": "Este Campo es Requerido.",
        },
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        ]


class UserLoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=64,
        style={'template': 'components/forms/input.html'},
        error_messages={
            "required": "Este Campo es Requerido.",
        },
    )

    password = serializers.CharField(
        max_length=64,
        style={'template': 'components/forms/input.html'},
        error_messages={
            "required": "Este Campo es Requerido.",
        },
    )

    class Meta:
        model = User
        fields = ['username', 'password']


class UserSerializer(serializers.ModelSerializer):
    registered_at = serializers.DateTimeField(format='%H:%M %d.%m.%Y', read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    short_name = serializers.SerializerMethodField(read_only=True)

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else settings.STATIC_URL + 'images/default_avatar.png'

    def get_full_name(self, obj):
        return obj.full_name

    def get_short_name(self, obj):
        return obj.short_name

    class Meta:
        model = User
        fields = ['email', 'avatar', 'full_name', 'short_name', 'registered_at', 'username']