from rest_framework import serializers
from .models import *

class userRegisterserializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=MyUser
        fields=['email','name','password','password2','tc']
        extra_kwargs={'password':{'write_only':True}}
    def validate(self,value):
        password=value.get('password')
        password2=value.get('password2')
        if password !=password2:
            raise serializers.ValidationError("Password Not matched")
        return value

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)


class userloginserilizer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=MyUser
        fields=['email','password']

class userprofileserializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields=['id','name','email','tc']


class filesserializer(serializers.Serializer):
    files=serializers.ListField(child=serializers.FileField(max_length=10000),allow_empty=False)
    folder=serializers.CharField(required=False)

    def create(self, validated_data):
        folder= Folder.objects.create()
        files=validated_data.pop('files')
        files_objs=[]
        for file in files :
            files_obj=files.objects.create(folder=folder,file=file)
            files_objs.append(files.obj)
        return {'files':{},'folder':str(folder.uid)}