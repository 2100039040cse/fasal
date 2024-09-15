from.import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
		path("",views.index, name="home"),
        path('signup/', views.signup, name='signup'),
        path('login/', views.user_login, name='login'),
        path('home/', views.home, name='home'),
        path('logout/',views.logout, name='logout'),
        path('profile/', views.profile, name='profile'),
        path('long_listening/', views.long_listening, name='long_listening'),
        path('text_to_speech/', views.text_to_speech, name='text_to_speech'),
        path('change_password/', views.change_password, name='change_password'),
        path('confirm_delete/', views.confirm_delete, name='confirm_delete'),
        path('delete_account/', views.delete_account, name='delete_account'),

		]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
