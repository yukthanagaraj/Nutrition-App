from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from .views import AdminViewSet,UserViewSet,TestlabvaluesViewSet,FeedbackViewSet,MultiUserLoginView,DiseaseViewSet,NutritionrequirementsViewSet,CommonnutritionViewSet

router=DefaultRouter()
router.register(r'admins',AdminViewSet,basename="admin")
router.register(r'users',UserViewSet,basename="user")
router.register(r'disease',DiseaseViewSet,basename="diseases")
router.register(r'feedback',FeedbackViewSet,basename="feedbacks")
router.register(r'testlabvalues',TestlabvaluesViewSet,basename="Testlabvalues")
router.register(r'commonnutrition',CommonnutritionViewSet,basename="commonnutritions")
router.register(r'Nutritionrequirement',NutritionrequirementsViewSet,basename="Nutritionrequirements")


urlpatterns = [
    path('',include(router.urls)),
    path('testlabvalues/<int:user_id>/<int:disease_id>/', TestlabvaluesViewSet.as_view({'post': 'create_with_user_disease'})),
    path('loginverify', MultiUserLoginView.as_view(), name='loginverify'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)