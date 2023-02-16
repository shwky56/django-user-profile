import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from profiles.api.serializers import *
from profiles.api.views import *
from profiles.models import *


class RegistrationTestCase(APITestCase):
    
    def test_registration(self):
        data = {
            "username": "shwky",
            "email": "shwkym54@gmail.com",
            "password1": "asafkjsfdfja@efsdfja24235324",
            "password2": "asafkjsfdfja@efsdfja24235324",
        }
        response = self.client.post("/api/rest-auth/registration/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProfileViewSetTestCase(APITestCase):
    
    list_url = reverse("profile-list")
    
    def setUp(self):
        self.user = User.objects.create_user(username="shwky", 
                                             password="fasasfjpasikm4@$#JOOsaspfog")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
    
    def test_profile_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_profile_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_profile_detail_retrieve(self):
        response = self.client.get(reverse("profile-detail", kwargs={"pk":1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], "shwky")
    
    def test_profile_update_by_owner(self):
        response = self.client.put(reverse("profile-detail", kwargs={"pk":1}),
                                   {  
                                        "id": 1,
                                        "user": "shwky",
                                        "bio": "masdfsdgdgdn",
                                        "city": "egypt",
                                        "gender": 1,
                                        "phone": "2323",
                                        "address": "sfsdfsd"
                                    })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         {
                            "id": 1,
                            "user": "shwky",
                            "avatar": None,
                            "bio": "masdfsdgdgdn",
                            "city": "egypt",
                            "gender": 1,
                            "phone": "2323",
                            "address": "sfsdfsd"
                         })
    
    def test_profile_update_by_owner_only(self):
        user = User.objects.create_user(username="random_user", password="qsdlkjfahkdfskjl;f;atjioerfjlkjtgf")
        self.client.force_authenticate(user=user) 
        response = self.client.put(reverse("profile-detail", kwargs={"pk":1}),
                                   {"city":"Egypt", "bio":"test bio"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ProfileStatusViewSetTestCase(APITestCase):
    
    list_url = reverse("status-list")
    
    def setUp(self):
        self.user = User.objects.create_user(username="shwky", 
                                             password="fasasfjpasikm4@$#JOOsaspfog")
        self.status = ProfileStatus.objects.create(user_profile=self.user.profile, 
                                                   status_content="test status")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_status_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_profile_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_status_creat(self):
        data = {"status_content": "hi i am heeersdfas s"}
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status_content"], "hi i am heeersdfas s")
        self.assertEqual(response.data["user_profile"], "shwky")
    
    def test_status_detail_retrieve(self):
        response = self.client.get(reverse("status-detail", kwargs={"pk":1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_profile"], "shwky")
    
    def test_profile_update_by_owner(self):
        response = self.client.put(reverse("status-detail", kwargs={"pk":1}),
                                   {"status_content": "new update"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(json.loads(response.content),
        #                  {"id":1, "user":"shwky", "city":"Egypt", "bio":"test bio", "avatar":None})
    
    def test_profile_update_by_owner_only(self):
        user = User.objects.create_user(username="random_user", password="qsdlkjfahkdfskjl;f;atjioerfjlkjtgf")
        self.client.force_authenticate(user=user) 
        response = self.client.put(reverse("profile-detail", kwargs={"pk":1}),
                                   {"status_content": "new update"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
