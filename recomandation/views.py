from django.shortcuts import render
from rest_framework import viewsets,status
from .models import Admin,User,Commonnutrition,Disease,Nutritionrequirements,Testlabvalues,Feedback
from .serializers import AdminSerializer,UserSerializer,CommonnutritionSerializer,DiseaseSerializer,NutritionrequirementsSerializer,TestlabvaluesSerializer,FeedbackSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.shortcuts import redirect



# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer  
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email']

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        phone = request.data.get('phone')

        # Check if email or phone already exists
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already registered"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(phone=phone).exists():
            return Response(
                {"error": "Mobile number already registered"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)


class MultiUserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        usertype = request.data.get('usertype')  # Admin or User

        if usertype == 'Admin':
            admin = Admin.objects.filter(email=email, password=password).first()
            if not admin:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({
                "message": "Admin login successful",
                "usertype": "Admin",
                "id": admin.id,
                "email": admin.email
                # No name field for admin
            }, status=status.HTTP_200_OK)

        elif usertype == 'User':
            user = User.objects.filter(email=email, password=password).first()
            if not user:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({
                "message": "User login successful",
                "usertype": "User",
                "id": user.id,
                "email": user.email,
                "name": user.name   # Only users have name
            }, status=status.HTTP_200_OK)

        else:
            return Response({"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer  

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer  
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email']  # Fix the typo here


class DiseaseViewSet(viewsets.ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer  

class NutritionrequirementsViewSet(viewsets.ModelViewSet):
    queryset = Nutritionrequirements.objects.all()
    serializer_class = NutritionrequirementsSerializer  

class CommonnutritionViewSet(viewsets.ModelViewSet):
    queryset = Commonnutrition.objects.all()
    serializer_class = CommonnutritionSerializer  

class TestlabvaluesViewSet(viewsets.ModelViewSet):
    queryset = Testlabvalues.objects.all()
    serializer_class = TestlabvaluesSerializer

    # Custom POST for creating with user and disease
    @action(detail=False, methods=['post'], url_path='(?P<user_id>[^/.]+)/(?P<disease_id>[^/.]+)')
    def create_with_user_disease(self, request, user_id=None, disease_id=None):
        data = request.data.copy()
        data['user'] = user_id
        data['diseases'] = disease_id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("Test lab values added successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Get test lab values by user ID
    @action(detail=False, methods=['get'], url_path='GetTestlabvaluesByUserId/(?P<user_id>[^/.]+)')
    def get_by_user_id(self, request, user_id=None):
        testlabvalues = Testlabvalues.objects.filter(user__id=user_id)
        serializer = self.get_serializer(testlabvalues, many=True)
        return Response(serializer.data)
    queryset = Testlabvalues.objects.all()
    serializer_class = TestlabvaluesSerializer

    @action(detail=False, methods=['post'], url_path='(?P<user_id>[^/.]+)/(?P<disease_id>[^/.]+)')
    def create_with_user_disease(self, request, user_id=None, disease_id=None):
        data = request.data.copy()
        data['user'] = user_id
        data['diseases'] = disease_id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("Test lab values added successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='by-user/(?P<user_id>[^/.]+)')
    def get_by_user(self, request, user_id=None):
        lab_values = Testlabvalues.objects.filter(user_id=user_id)
        serializer = self.get_serializer(lab_values, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer