from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import AssetFile
from .serializers import AssetFileSerializer


class BaseTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            username='user', email='user@foo.com', password='pass')
        user.save()
        self.user = user

    def login(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(
            url,
            {'username': 'user', 'password': 'pass'}, format='json')
        token = response.data['access']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.client = client


class AssetFileViewSetAuthenticatedAccessTest(BaseTestCase):

    def test_create_view_unauthorized_access(self):
        response = self.client.post(reverse('assets-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_view_unauthorized_access(self):
        response = self.client.get(reverse('assets-detail', args=['1']))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_view_unauthorized_access(self):
        response = self.client.get(reverse('assets-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_view_unauthorized_access(self):
        response = self.client.delete(reverse('assets-detail', args=['1']))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AssetFileCreateViewTestCase(BaseTestCase):

    def test_invalid_upload(self):
        self.login()
        response = self.client.post(reverse('assets-list'), {
            'file': SimpleUploadedFile('teste.mp4', b'')
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AssetFileDetailViewTestCase(BaseTestCase):

    def setUp(self):
        super(AssetFileDetailViewTestCase, self).setUp()
        content = SimpleUploadedFile('teste.mp4', b'')
        asset_file = AssetFile(
            owner=self.user,
            name='teste.mp4',
            content=content)
        asset_file.save()
        self.asset_file = asset_file

    def test_valid_detail_asset_file(self):
        self.login()
        response = self.client.get(
            reverse('assets-detail', args=[self.asset_file.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_detail_asset_file(self):
        self.login()
        response = self.client.get(reverse('assets-detail', args=['1']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AssetFileDeleteViewTestCase(BaseTestCase):

    def setUp(self):
        super(AssetFileDeleteViewTestCase, self).setUp()
        content = SimpleUploadedFile('teste.mp4', b'')
        asset_file = AssetFile(
            owner=self.user,
            name='teste.mp4',
            content=content)
        asset_file.save()
        self.asset_file = asset_file

    def test_valid_delete_asset_file(self):
        self.login()
        response = self.client.delete(
            reverse('assets-detail', args=[self.asset_file.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_asset_file(self):
        self.login()
        response = self.client.delete(reverse('assets-detail', args=['1']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AssetFileListViewTestCase(BaseTestCase):

    def setUp(self):
        super(AssetFileListViewTestCase, self).setUp()
        content = SimpleUploadedFile('teste.mp4', b'')
        asset_file = AssetFile(
            owner=self.user,
            name='teste.mp4',
            content=content)
        asset_file.save()
        self.asset_file = asset_file

    @override_settings(MEDIA_URL='http://testserver')
    def test_list_user_asset_files(self):
        self.login()

        asset_files = AssetFile.objects.all()
        serializer = AssetFileSerializer(asset_files, many=True)

        response = self.client.get(reverse('assets-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
