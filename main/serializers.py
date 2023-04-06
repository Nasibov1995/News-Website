from rest_framework import serializers
from . models import Newsdata

class NewsdataSerializers(serializers.ModelSerializer):
    link = serializers.CharField(max_length=50)
    basliq = serializers.CharField(max_length=50)
    foto = serializers.CharField(max_length=50)
    metn = serializers.CharField(max_length=50)
    kateqoriya = serializers.CharField(max_length=50)
    temp = serializers.CharField(max_length=50)
    tarix = serializers.CharField(max_length = 50)

    class Meta:
        model = Newsdata
        fields = ('__all__')
        
    
