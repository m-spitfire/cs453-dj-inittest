from rest_framework import serializers
from publications.models import Publication, Article



class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ("id", "title", "articles")

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ("id", "headline", "publications")
