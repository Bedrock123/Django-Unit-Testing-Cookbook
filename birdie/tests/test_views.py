import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from mixer.backend.django import mixer
from .. import views
pytestmark = pytest.mark.django_db



class TestHomeView:
    def test_anonymous(self):
        req = RequestFactory().get('/')
        resp = views.HomeView(req)
        assert resp.status_code == 200, 'Should be callable by anyone'

class TestAdminView:
    def test_anonymous(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.AdminView(req)
        assert 'login' in resp.url

    def test_superuser(self):
        user = mixer.blend('auth.user', is_superuser=True)
        req = RequestFactory().get('/')
        req.user = user
        resp = views.AdminView(req)
        assert resp.status_code == 200, 'Authenticated user can access'
