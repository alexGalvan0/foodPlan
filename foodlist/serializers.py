from rest_framework import serializers
from .models import Meal,Custom_user



class MealSerializer(serializers.ModelSerializer):
    class Meta:

        model = Meal
        fields = ['name','type','day','created','user','id']

class Custom_userSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom_user
        fields = ('__all__')

        #hide password from response
        extra_kwargs = {
            'password':{'write_only':True}
        }


    #hash password
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    