from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Blog, BlogCategory


class BlogReadSerializer(serializers.ModelSerializer):

    imagen = serializers.SerializerMethodField(read_only=True)

    def get_imagen(self, obj):
        return obj.image.url if obj.image else settings.STATIC_URL + 'images/blog/default_image.png'

    class Meta:
        model = Blog
        depth = 1
        fields = [
            'uuid', 'title', 'user', 'image', 'text', 'category', 'publish_data'
        ]


class BlogWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'title', 'text', 'image', 'category', 'user'
        ]


class BlogFormSerializer(serializers.ModelSerializer):

    title = serializers.CharField(
        max_length=64,
        style={'template': 'components/forms/input.html'},
        error_messages={
            "required": "Este Campo es Requerido.",
        },
    )

    text = serializers.CharField(
        max_length=64,
        style={'template': 'components/forms/input.html'},
        error_messages={
            "required": "Este Campo es Requerido.",
        },
    )

    category = serializers.ChoiceField(
        choices=list(map(lambda x: [str(x['uuid']), x['category']], BlogCategory.objects.values('uuid', 'category'))),
        style={'template': 'components/forms/select.html'},
        error_messages={
            "required": "Este Campo es Requerido.",
        },
    )

    image = serializers.ImageField(
        style={'template': 'components/forms/file.html'},
        error_messages={
            "required": "Este Campo es Requerido.",
        },
    )

    class Meta:
        model = Blog
        fields = [
            'title', 'text', 'image', 'category'
        ]
