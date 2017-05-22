# python imports

# django imports
from django.conf.urls import url

#local imports
from . import views

app_name = 'chimp_users'

urlpatterns = [
	url(r'^sign-up/$', views.SignUpView.as_view(), name = 'sign_up'),
	url(r'^logout/', views.LogoutView.as_view(), name = 'logout'),
	url(r'^sign-in/$', views.SignInView.as_view(), name='sign_in'),
	url(r'^edit-user-profile/(?P<pk>[0-9]+)/$',views.EditUserProfileView.as_view(), name = 'edit_user_profile'),
	url(r'^change-password/$', views.ChangePasswordView.as_view(), name = 'change_password'),
	url(r'^show-user-profile/$',views.UserProfileView.as_view(), name = 'show_user_profile'),

	
]