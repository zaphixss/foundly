from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class RegisterView(APIView):

    def post(self, request):
        serilaizer = RegisterSerializer(data=request.data)
        serilaizer.is_valid(raise_exception=True)
        user = serilaizer.save()
        refresh = RefreshToken.for_user(user)

        response_data = {
            'user':{
                'email': user.email,
                'username': user.username,
                'password': user.password,
            },

            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

        return Response(response_data, status=status.HTTP_201_CREATED)



class LoginView(APIView):

    def post(self, request):
        serilaizer = LoginSerializer(data=request.data)
        serilaizer.is_valid(raise_exception=True)
        user = serilaizer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        response_data = {
            'user': {
                'email': user.email,
                'username': user.username,
                'password': user.password,
            },

            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

        return Response(response_data, status=status.HTTP_200_OK)
    


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"detail": "Refresh token is required to log out."},status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out. Refresh token has been blacklisted."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid or already blacklisted refresh token."},status=status.HTTP_400_BAD_REQUEST )




class RefreshView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"detail": "Refresh token is required!"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            response_data = {
                'access': str(token.access_token),
                'refresh': str(token),
            }
            return Response({"response": response_data, "detail": "Successfully refreshed!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid or already blacklisted refresh token."}, status=status.HTTP_400_BAD_REQUEST )
        

class MeView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user

        user_info = {
                'email': user.email,
                'username': user.username,
                'password': user.password,
            }

        return Response(user_info, status=status.HTTP_200_OK)
