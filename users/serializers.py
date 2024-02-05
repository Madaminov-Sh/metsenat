from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User

    
class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'confirm_password')
        
    def validate(self, attrs):
        
        password = attrs.get('password', None)
        confirm_password = attrs.get('confirm_password', None)
        
        if password != confirm_password:
            raise ValidationError("password va confirm password ikki xil bo'lmasligi kerak")
        if self.context['request'].data.get('username') in password or self.context['request'].data.get('email') in password:
            raise ValidationError("password, email va usernamega o'xshash bo'lmasligi kerak")
        if len(password) <= 7:
            raise ValidationError("password 8 ta belgidan iborat bo'lmasligi kerak")
        if password.isdigit():
            raise ValidationError("password to'lig raqamdan iborat bo'lmaslig kerak")
        
        return attrs    
    
    def validate_email(self, email):
        if email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError('bu email ishlatilingan')
        if email is None:
            raise ValidationError("email maydoni bo'sh bo'lmasligi kerak")
        return email
    
    def validate_username(self, username):
        if username and User.objects.filter(username__iexact=username).exists():
            raise ValidationError("bu username allaqachon band qilingan")
        if username[0].isdigit():
            raise ValidationError("username raqam bilan boshlanmasligi kerak")
        if len(username) <= 4:
            raise ValidationError("username 5 belgidan kam bo'lmasligi kerak")
            
        return username

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        data.update(instance.token())
        return data
    
    
class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        username = attrs.get('username', None).lower()
        password = attrs.get('password', None)
        
        user = authenticate(request=self.context.get('request'), username=username, password=password)
            
        if not user:
            raise ValidationError("username yoki parolni qayta tekshiring")
        
        refresh = self.get_token(user)
        
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)
        
        return attrs
    