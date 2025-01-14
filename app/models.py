import random
import string
from django.utils import timezone
import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField


User = get_user_model() # get the user 

# PolyModel
class PolyModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    

# Real Estate 
class RealEstate(PolyModel):
    PROPERTY_TYPES = [
        ("sale", "For Sale"),
        ("rent", "For Rent"),
    ]

    title = models.CharField(max_length=255)
    description = RichTextField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    real_estate_type = models.CharField(max_length=10, choices=PROPERTY_TYPES)
    area = models.DecimalField(
        max_digits=6, decimal_places=2, help_text="Area in square meters"
    )
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    
    has_pool = models.BooleanField(default=False)
    has_garden = models.BooleanField(default=False)
    
    is_available = models.BooleanField(default=True)

    image_first = models.ImageField(upload_to="images_properties/")
    image_second = models.ImageField(upload_to="images_properties/")

    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            random_suffix = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=6)
            )
            self.slug = (
                f"{slugify(self.title)}-{random_suffix}"
                if self.title
                else str(uuid.uuid4())
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# Bank of Image
class BankImage(PolyModel):
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="images_properties/")

# RealEstate Liked
class RealEstateLiked(PolyModel):
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.email} aime {self.real_estate.title}"