
import re
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status, permissions, viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import MealSerializer,Custom_userSerializer
from .models import Meal, Custom_user
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from django_filters.rest_framework import DjangoFilterBackend

class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')

class CookieTokenObtainPairView(TokenObtainPairView):
  def finalize_response(self, request, response, *args, **kwargs):
    if response.data.get('refresh'):
        cookie_max_age = 3600 * 24 * 14 # 14 days
        response.set_cookie('access_token', response.data['access'], max_age=cookie_max_age, httponly=True )
        del response.data['refresh']
    return super().finalize_response(request, response, *args, **kwargs)

class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = CookieTokenRefreshSerializer



# Views
class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        serializer = Custom_userSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class MealsViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set

   

class RegisterMealItem(APIView):
    def post (self, request):
        
        serializer = MealSerializer(data = self.request.data)
        serializer.is_valid(raise_exception=True) 
        id = request.user.id

        serializer.save(user_id = id)
        return Response(serializer.data)










# Create your views here.
"""

class Custom_userView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):

        token = CookieTokenObtainPairView()

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token,'secret',algorithm=['HS256'])
        except jwt.ExipredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = Custom_user.objects.filter(id=payload['id']).first()
        serializer = Custom_userSerializer(user)
    

        return Response(serializer.data)


CREATED
class MealView(APIView):
    def get(self, request):

        id = Custom_userView.get(self,request).data['id']
        mealItems = Meal.objects.filter(user_id = id)

        serialzer = MealSerializer(mealItems,many=True)
        permision_classes = [permissions.IsAuthenticated,]
        token = CookieTokenObtainPairView().access

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        return Response (serialzer.data)

class RegisterMealItem(APIView):
    def post (self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        
        serializer = MealSerializer(data = self.request.data)
        serializer.is_valid(raise_exception=True) 

        id = Custom_userView.get(self,request).data['id']

        serializer.save(user_id = id)
        return Response(serializer.data)

class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = Custom_user.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User Not Found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password!')


        payload = {
            'id': user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        response = Response()

        response.set_cookie(key='jwt', value=token,httponly=True)
        response.data = {
            'jwt':token
        }

        return response

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'success'
        }
        return response

class DeleteMealItem(APIView):
    def post(self, request):
        pass"""