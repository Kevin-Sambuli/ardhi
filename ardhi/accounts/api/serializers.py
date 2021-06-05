from rest_framework import serializers
from accounts.models import Account


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'username', 'gender', 'kra_pin',
                  'id_no', 'dob', 'phone', 'password', 'password2']

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        account = Account(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            gender=self.validated_data['username'],
            kra_pin=self.validated_data['kra_pin'],
            id_no=self.validated_data['id_no'],
            dob=self.validated_data['dob'],
            phone=self.validated_data['phone'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account


class AccountPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'username', ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
