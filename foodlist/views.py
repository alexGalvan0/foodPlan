
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


#userInfoView
class UserViewSet(viewsets.ModelViewSet):
    queryset = Custom_user.objects.all()
    serializer_class = Custom_userSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(id = self.request.user.id)
        return query_set


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


class DeleteMealView(APIView):
    def post(self, request):
        id = request.data
        food = Meal.objects.filter(id=id['id']).delete()
        print(food)
        return Response(id)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            'message':'success'
        }
        return response
