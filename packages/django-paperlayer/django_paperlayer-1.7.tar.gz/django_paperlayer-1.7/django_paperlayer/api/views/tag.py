from rest_framework import viewsets
from rest_framework import permissions
from django_paperlayer.api.models.tag import Tag
from django_paperlayer.api.serializers.tag import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
