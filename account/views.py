from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from account.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from django.http import Http404


# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if not request.user.is_admin:
            return Response({'msg': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Optionally set user as admin based on serializer data
        if serializer.validated_data.get('is_admin'):
            user.is_admin = True
            user.save()

        # Generate tokens for the registered user
        token = get_tokens_for_user(user)

        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)

    def get(self, request, pk=None):
        if pk:
            # If pk is provided, return specific profile detail
            profile = self.get_object(pk)
            if request.user == profile or request.user.is_admin:
                serializer = UserProfileSerializer(profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'You do not have permission to view this profile.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            # If no pk, return list of all profiles (for admins only)
            if request.user.is_admin:
                profiles = User.objects.all()
                serializer = UserProfileSerializer(profiles, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'You do not have permission to view all profiles.'}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        profile = self.get_object(pk)
        if request.user == profile or request.user.is_admin:
            serializer = UserProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        try:
            profile = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'msg': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_admin:
            profile.delete()
            return Response({'msg': 'Profile deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'msg': 'You do not have permission to delete this profile.'}, status=status.HTTP_403_FORBIDDEN)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = serializer.validated_data.get('uid')
        token = serializer.validated_data.get('token')
        return Response({'uid': uid, 'token': token}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)

