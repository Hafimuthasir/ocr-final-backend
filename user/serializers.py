from rest_framework import serializers
from .models import UserInfo,id_data
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = "__all__"

    def validate_Name(self, value):
        has_integer = False
        for char in value :
                if char.isdigit():
                    has_integer = True
                    break
        if has_integer:
            raise serializers.ValidationError("Name should only contain alphabets.")
        return value
        

    def validate_Email(self, value):
        try:
            UserInfo.objects.get(Email=value)
            raise serializers.ValidationError("Email already exists.")
        except UserInfo.DoesNotExist:
            pass

        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format.")
        return value
    
    
    def validate_phone(self, value):
        try:
            UserInfo.objects.get(phone=value)
            raise serializers.ValidationError("Phone number already exists.")
        except UserInfo.DoesNotExist:
            pass

        if not value.isdigit():
            raise serializers.ValidationError("Phone number should only contain digits.")
        if len(value) < 10 or len(value) > 12:
            raise serializers.ValidationError("Phone number should be between 10 to 12 digits.")
        return value
    

    def validate_id_proof(self, value):
        if value.size > 1024*1024*2:
            raise serializers.ValidationError("File size should not exceed 2MB.")
        return value



class DocumentSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = id_data
        fields = "__all__"
        extra_kwargs = {
            "id_no": {"required": False},
            "id_name": {"required": False},
            "id_dob": {"required": False},
            "id_fulldata": {"required": False},
            "id_type": {"required": False},
        }
        
        
class DataFetchSerializer(serializers.ModelSerializer):
    id_data = DocumentSaveSerializer()
    class Meta :
        model = UserInfo
        fields = "__all__"
    













# class MySerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100, validators=[lambda v: v.isalpha() or serializers.ValidationError("Name can only contain alphabets.")])
#     email = serializers.CharField(max_length=100, validators=[EmailValidator(message="Invalid email address.")])
#     phone = serializers.CharField(max_length=20, validators=[lambda v: v.isdigit() or serializers.ValidationError("Phone number can only contain digits.")])
#     country = serializers.CharField(max_length=100)
#     id_proof = serializers.FileField()

#     def validate(self, data):
#         if not data.get('name'):
#             raise ValidationError('Name is required.')
#         if not data.get('email'):
#             raise ValidationError('Email is required.')
#         if not data.get('phone'):
#             raise ValidationError('Phone is required.')
#         if not data.get('country'):
#             raise ValidationError('Country is required.')
#         if not data.get('id_proof'):
#             raise ValidationError('ID proof is required.')
#         return data