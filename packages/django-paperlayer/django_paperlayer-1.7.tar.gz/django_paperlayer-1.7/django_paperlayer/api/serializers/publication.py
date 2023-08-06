from rest_framework import serializers
from django_paperlayer.api.models.publication import Publication


class PublicationSerializer(serializers.ModelSerializer):
    """
    Publication serializer
    """

    class Meta:
        model = Publication
        fields = '__all__'
