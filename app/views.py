from django.http import JsonResponse
from django.shortcuts import render
from .models import RealEstate
from .serializers import (
    RealEstateLikedSerializer,
    RealEstateListSerializer,
    RealEstateDetailSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.http import require_GET
from .models import RealEstate, RealEstateLiked
from rest_framework.decorators import action
from rest_framework import status


@require_GET
def check_single_product_existence(request, real_estate):
    try:
        real_estate = RealEstate.objects.get(slug=real_estate)
        return JsonResponse(
            {"exists": True, "id": real_estate.id, "name": real_estate.title}
        )
    except RealEstate.DoesNotExist:
        return JsonResponse({"exists": False})


class RealEstateFavoriteViewSet(APIView):
    def get(self, request):
        query = RealEstate.objects.filter(active=True).order_by("?")[:3]
        serializer = RealEstateListSerializer(
            query, many=True, context={"request": request}
        )

        data = serializer.data

        return Response(data)


class RealEstateViewSet(ReadOnlyModelViewSet):
    serializer_class = RealEstateListSerializer
    detail_class_serializer = RealEstateDetailSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RealEstate.objects.filter(active=True)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_class_serializer
        return super().get_serializer_class()

    @action(detail=True, methods=["post"])
    def add_liked(self, request, pk=None):
        user = self.request.user
        real_estate = self.get_object()

        liked, created = RealEstateLiked.objects.get_or_create(
            user=user,
            real_estate=real_estate,
        )
        return Response(
            RealEstateLikedSerializer(liked).data, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["delete"])
    def remove_liked(self, request, pk=None):
        user = self.request.user
        real_estate = self.get_object()

        try:
            liked = RealEstateLiked.objects.get(user=user, real_estate=real_estate)
            liked.delete()
        except RealEstateLiked.DoesNotExist:
            return Response(
                {"message": "Le real estate n'existe pas ou n'est pas liké !"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckFavoriteExistenceView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, real_estate):
        real_estate = RealEstate.objects.get(slug=real_estate)
        print(real_estate)
        liked = RealEstateLiked.objects.filter(
            real_estate=real_estate, user=request.user
        )

        if liked:
            return Response({"exists": True, "id": liked[0].id})

        return Response({"exists": False})


class RealEstateLikedViewSet(ReadOnlyModelViewSet):
    serializer_class = RealEstateLikedSerializer
    # permissions_classes = [IsAuthenticated,]

    def get_queryset(self):
        return RealEstateLiked.objects.filter(active=True, user=self.request.user)


from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime
from django.utils.html import strip_tags

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt


class ContactPropertyAPIView(APIView):
    def post(self, request):
        # Récupérer les données envoyées via le formulaire
        property_title = request.data.get("property_title")
        name = request.data.get("name")
        email = request.data.get("email")
        message = request.data.get("message")

        # Valider les champs
        if not all([property_title, name, email, message]):
            return Response(
                {
                    "success": False,
                    "message": "Tous les champs du formulaire doivent être renseignés.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        print(property_title, name, email, message)
        
        try:
            # Envoi de l'email
            self.send_property_contact_email(property_title, name, email, message)
            return Response(
                {"success": True, "message": "E-mail envoyé avec succès."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def send_property_contact_email(self, property_title, name, email, message):
        """
        Envoie un e-mail avec les détails de contact concernant une propriété.

        :param property_title: Le titre de la propriété concernée.
        :param name: Le nom de la personne qui soumet le formulaire.
        :param email: L'e-mail de la personne qui soumet le formulaire.
        :param message: Le message soumis par l'utilisateur.
        """
        current_year = datetime.now().year

        # Nom du template pour l'e-mail
        template_name = "contact/contact.html"
        context = {
            "property_title": property_title,
            "name": name,
            "email": email,
            "message": message,
            "year": current_year,
        }

        # Génération du contenu HTML de l'email
        email_template = render_to_string(template_name, context)
        # plain_message = strip_tags(email_template)

        print("c'est fait 1")
        
        # Envoi de l'email        
        email_to_send = EmailMessage(
            subject=f"Contact concernant la propriété : {property_title}",
            body=email_template,
            from_email=settings.EMAIL_HOST_USER,
            to=[email]
        )
        
        email_to_send.content_subtype = "html"
        email_to_send.send(fail_silently=True)

        print("c'est fait 2")

