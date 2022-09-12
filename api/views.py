from rest_framework.routers import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import userRegisterserializer,userloginserilizer,userprofileserializer,filesserializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated




def get_tokens_for_user(user):
    refresh=RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }

class userregister(APIView):
    def post(self,request,format=None):
        serializer=userRegisterserializer(data=request.data)
        if serializer.is_valid():
            user= serializer.save()
            token=get_tokens_for_user(user)
            return Response({'Token':token ,'msg':'Register successful'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class userlogin(APIView):
    def post(self,request,format=None):
        serializer = userloginserilizer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                Token=get_tokens_for_user(user)
                return Response({'Token':Token,'msg': 'Login successful'}, status=status.HTTP_200_OK)

            else:
                return Response({'errors': {'non_fiels_errors': ['Email or password is not valid']}},
                                status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class userprofile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
         serilizer=userprofileserializer(request.user)
         return Response(serilizer.data,content_type='application/json',status=status.HTTP_200_OK)





class handlefiles(APIView):
    def post(self,request):
        try:
            serialier=filesserializer(data=request.data)
            if serialier.is_valid():
                serialier.save()
                return Response({'msg':'files uploaded'})
            return Response(serialier.errors)
        except Exception as e:
            print(e)
