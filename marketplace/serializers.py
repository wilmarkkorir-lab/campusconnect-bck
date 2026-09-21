from rest_framework import serializers
from .models import MarketplaceListing, ListingImage, SavedListing


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = '__all__'


class MarketplaceListingSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.full_name', read_only=True)
    images = ListingImageSerializer(many=True, read_only=True)
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = MarketplaceListing
        fields = '__all__'
        read_only_fields = ('seller', 'created_at', 'updated_at')

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.saves.filter(user=request.user).exists()
        return False
