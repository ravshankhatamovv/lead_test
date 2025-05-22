from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

urlpatterns=[
     path('login/', 
          views.MyObtainTokenPairView.as_view(), 
          name='token_obtain_pair'),
     path('login/refresh/', 
          TokenRefreshView.as_view(), 
          name='token_refresh'),
     path('logout/', 
          TokenBlacklistView.as_view(), 
          name='token_blacklist'),
     path('me/', 
          views.UserMeAPIView.as_view(), 
          name='user_me'),
     path('employee/create/', 
          views.CreateUserAPIView.as_view(), 
          name='emplyee_create'),
     path('employee/list/', 
          views.ListUserAPIView.as_view(), 
          name='emplyee_list'),  
     path('employee/<uuid:id>/delete/', 
          views.DeleteUserAPIView.as_view(), 
          name='emplyee_update_delete'), 
     path('employee/<uuid:id>/retrieve/', 
          views.RetrieveUserAPIView.as_view(), 
          name='emplyee_retieve'), 

]


