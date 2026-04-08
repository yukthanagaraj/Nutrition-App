from rest_framework import serializers
from .models import Admin,User,Commonnutrition,Disease,Nutritionrequirements,Testlabvalues,Feedback
from drf_extra_fields.fields import Base64ImageField


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'email', 'password']

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CommonnutritionSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta: 
    
        model = Commonnutrition
        fields = '__all__'


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'

class NutritionrequirementsSerializer(serializers.ModelSerializer):
    disease = DiseaseSerializer(read_only=True)  # for display
    disease_id = serializers.PrimaryKeyRelatedField(
        queryset=Disease.objects.all(), source='disease', write_only=True
    )

    class Meta:

        model = Nutritionrequirements
        fields = [
            'id', 'name', 'nutrient_type', 's_range', 'e_range',
            'description', 'date', 'disease', 'disease_id'
        ]

class TestlabvaluesSerializer(serializers.ModelSerializer):
    disease_name = serializers.CharField(source='diseases.name', read_only=True)
    disease_subtype = serializers.CharField(source='diseases.subtype', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Testlabvalues
        fields = ['id', 'lab_value', 'date', 'user', 'diseases', 'disease_name', 'disease_subtype', 'user_name']


class FeedbackSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True)         # for returning user data
    users_id = serializers.IntegerField(write_only=True)  # for accepting user ID

    class Meta:
        model = Feedback
        fields = ['id', 'feedback', 'date', 'users', 'users_id']

    def create(self, validated_data):
        user_id = validated_data.pop('users_id')
        user = User.objects.get(id=user_id)
        feedback = Feedback.objects.create(users=user, **validated_data)
        return feedback


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")