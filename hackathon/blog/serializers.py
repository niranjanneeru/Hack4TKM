from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField

from .models import Blog, Tags


class BlogSerializer(ModelSerializer):
    tags = SerializerMethodField('get_tags')

    def get_tags(self, obj: Blog):
        return [str(x.name) for x in obj.tags.all()]

    class Meta:
        model = Blog
        read_only_fields = ('tags',)
        fields = ['author', 'url', 'created_at', 'title', 'description', 'rating', 'platform', 'image_link', 'tags']


class BlogWriteSerializer(ModelSerializer):
    tags = CharField(max_length=300)

    class Meta:
        model = Blog
        fields = ['author', 'url', 'title', 'description', 'platform', 'image_link', 'tags', ]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tags
        fields = ['name', ]
