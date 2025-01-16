from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.http import require_GET
from rest_framework.decorators import action
from rest_framework import status
from .models import CustomUser, UserResetPassword
from django.template.loader import render_to_string
from django.utils import timezone


# Create your views here.
def send_reset_password_email(email, token):
    """
    Envoie un e-mail avec les détails de contact concernant une propriété.

    :param property_title: Le titre de la propriété concernée.
    :param name: Le nom de la personne qui soumet le formulaire.
    :param email: L'e-mail de la personne qui soumet le formulaire.
    :param message: Le message soumis par l'utilisateur.
    """
    current_year = datetime.now().year

    # Nom du template pour l'e-mail
    template_name = "reset_pwd/reset_password.html"
    
    context = {
        "reset_password_url": f"{settings.URL_FRONTEND}/reset_password_confirm/?token={token}",
        "year": current_year,
    }

    # Génération du contenu HTML de l'email
    email_template = render_to_string(template_name, context)
    # plain_message = strip_tags(email_template)

    print("c'est fait 1")

    # Envoi de l'email
    email_to_send = EmailMessage(
        subject=f"Reinitialisation de votre mot de passe",
        body=email_template,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
    )

    email_to_send.content_subtype = "html"
    email_to_send.send(fail_silently=True)

    print("c'est fait 2")


class CreateResetPassword(APIView):
    # permission_classes = [IsAuthenticated]  # Si vous utilisez l'authentification

    def post(self, request):
        email = request.data.get("email")

        # Vérifier si l'utilisateur existe
        user = CustomUser.objects.filter(email=email).first()

        if not user:
            return Response(
                {"message": "L'email n'existe pas."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Vérifier s'il y a une demande de réinitialisation existante et si elle est expirée
        resetPassword = UserResetPassword.objects.filter(
            user=user, active=False
        ).first()

        if resetPassword:

            return Response(
                {
                    "message": "Un mail a déjà été envoyé. Veuillez vérifier votre boîte de réception."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Créer un nouveau lien de réinitialisation
        expires_at = timezone.now() + timedelta(
            minutes=2
        )  # Lien valide pendant 10 minutes

        resetPassword = UserResetPassword.objects.create(
            user=user,
            active=False,  # Le lien est inactif au début
            expires_at=expires_at,
        )

        # Envoyer l'email avec le token de réinitialisation
        send_reset_password_email(user.email, resetPassword.token)

        return Response(
            {"message": "Un email de réinitialisation a été envoyé."},
            status=status.HTTP_200_OK,
        )


# class ConfirmeResetPassword(APIView):
#     # permission_classes = [IsAuthenticated]

#     def post(self, request):
#         token = request.data.get('token')
#         email = request.data.get("email")
#         user = CustomUser.objects.filter(email=email)

#         if(len(user) <= 0):
#             return Response(
#                 {"message": "l'email n'existe pas."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         print("user: ", user)

#         resetPasswordList = UserResetPassword.objects.filter(user=user[0] , token = token , active = False).first()

#         if resetPasswordList is None :
#             return Response(
#                 {"message": "Ne correspond pas"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         resetPasswordList.active = True
#         resetPasswordList.save()

#         return Response(status=status.HTTP_204_NO_CONTENT)


from django.contrib.auth.hashers import make_password


class ConfirmeResetPassword(APIView):

    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        print("token: ", token)
        # Trouver l'utilisateur par email
        userReset = UserResetPassword.objects.filter(token=token).first()

        if not userReset:
            print("ICII")
            return Response(
                {"message": "Token existe pas"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = userReset.user

        # Vérifier le token de réinitialisation
        reset_password_request = UserResetPassword.objects.filter(
            user=user, token=token, active=False
        ).first()

        # Mettre à jour le mot de passe de l'utilisateur
        user.password = make_password(new_password)  # Hash du nouveau mot de passe
        user.save()

        # Marquer la demande de réinitialisation comme active
        reset_password_request.active = True
        reset_password_request.save()

        return Response(
            {"message": "Mot de passe réinitialisé avec succès."},
            status=status.HTTP_200_OK,
        )
