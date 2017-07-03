from rest_framework import serializers

from .models import Webcam


class WebcamSerializer(serializers.ModelSerializer):
    """ Webcam Serializer
    """
    random_url = serializers.SerializerMethodField()

    class Meta:
        model = Webcam
        fields = (
            'id',
            'name',
            'slug',
            'technology',
            'description',
            'latitude',
            'longitude',
            'url',
            'web',
            'active',
            'random_url',
        )

    def get_random_url(self, webcam):
        request = self.context.get('request')
        return request.build_absolute_uri(webcam.random_url())
