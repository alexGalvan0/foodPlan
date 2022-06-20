from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from foodlist import views
from rest_framework_simplejwt import views as jwt_views
from foodlist.views import( MealsViewSet,
                            RegisterView,
                            CookieTokenObtainPairView,
                             RegisterMealItem,
                             LogoutView,
                             DeleteMealView,
                             UserViewSet

                            )
router = routers.DefaultRouter()
router.register(r'userMeals', views.MealsViewSet,basename='MyModel')

# router.register(r'specificConnections', views.ConnectionSpecificViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),

    path('register/',RegisterView.as_view(),name='create_user'),
    path('user/meals/', MealsViewSet.as_view({'get': 'list'}),name="get_user_meals"),
    path('register/meal/',RegisterMealItem.as_view(),name='register_meals'),
    path('delete/meal/',DeleteMealView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('user/',UserViewSet.as_view({'get': 'list'})),
    
    path('user/login/', CookieTokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)