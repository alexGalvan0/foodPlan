from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import datetime, jwt
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import MealSerializer,Custom_userSerializer
from .models import Meal, Custom_user

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        permission_classes = (permissions.AllowAny,)
        serializer = Custom_userSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class Custom_userView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token,'secret',algorithm=['HS256'])
        except jwt.ExipredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = Custom_user.objects.filter(id=payload['id']).first()
        serializer = Custom_userSerializer(user)

        return Response(serializer.data)



class MealView(APIView):
    def get(self, request):

        id = Custom_userView.get(self,request).data['id']
        mealItems = Meal.objects.filter(user_id = id)

        serialzer = MealSerializer(mealItems,many=True)
        permision_classes = [permissions.IsAuthenticated,]
        token = request.COOKIES.get('jwt')

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
        pass