from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import RealEstate, BankImage, RealEstateLiked


class CustomRegisterSerializer():
    pass

# RealEstate List Serializer
class RealEstateListSerializer(ModelSerializer):
    image_first = serializers.ImageField(use_url=True)
    image_second = serializers.ImageField(use_url=True)
    likes = serializers.SerializerMethodField()
    
    class Meta:
        model = RealEstate
        fields = [
            "id",
            "title",
            "description",
            "address",
            "area",
            "price",
            "image_first",
            "image_second",
            "slug",
            "real_estate_type",
            "likes",
            "is_available",
        ]
    
    def get_likes(self, instance):
        return len(instance.likes.filter(active = True))


# BankImage Serializer
class BankImageSerializer(ModelSerializer):
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = BankImage
        exclude = ["real_estate", "created_at", "updated_at"]
 
        
# RealEstate Detail Serializer
class RealEstateDetailSerializer(ModelSerializer):
    images = BankImageSerializer(many=True, read_only=True)

    class Meta:
        model = RealEstate
        fields = "__all__"
        read_only_fields = ["id", "active", "created_at", "updated_at"]

# RealEstateLiked Serializer
class RealEstateLikedSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")
    real_estate = serializers.SerializerMethodField()
    
    class Meta:
        model = RealEstateLiked
        fields = ["id", "user", "real_estate", "active", "created_at", "updated_at"]
        read_only_fields = ["id", "active", "created_at", "updated_at"]
    
    def get_real_estate(self, instance):
        return RealEstateListSerializer(instance.real_estate).data