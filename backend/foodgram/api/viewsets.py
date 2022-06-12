from rest_framework import mixins, viewsets

class RetrieveListViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    
    pass