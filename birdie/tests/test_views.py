import pytest
from .. import views
from django.contrib.auth.models import AnonymousUser
from django.core import mail
from django.http import Http404
from django.test import RequestFactory
from mixer.backend.django import mixer
from mock import patch

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
        assert 'login' in resp.url, 'AnonymousUser cannot access'


    def test_superuser(self):
        user = mixer.blend('auth.user', is_superuser=True)
        req = RequestFactory().get('/')
        req.user = user
        resp = views.AdminView(req)
        assert resp.status_code == 200, 'Authenticated user can access'

class TestPostCreateView:
    def test_get(self):
        req = RequestFactory().get('/')
        resp = views.PostCreateView(req)
        assert resp.status_code == 200, 'Should be callable by anyone'
    
    def test_post(self):
        post = mixer.blend('birdie.Post')
        data = {'body': 'New Body Text!'}
        req = RequestFactory().post('/', data=data)
        resp = views.PostCreateView(req)
        assert resp.status_code == 302, 'Should redirect to success view'

class TestPostUpdateView:
    def test_get(self):
        req = RequestFactory().get('/')
        req.user = mixer.blend('auth.User', first_name='Zach')
        obj = mixer.blend('birdie.Post')
        resp = views.PostUpdateView(req, pk=obj.pk)
        assert resp.status_code == 200, 'Should be callable by anyone'

    def test_post(self):
        post = mixer.blend('birdie.Post')
        data = {'body': 'New Body Text!'}
        req = RequestFactory().post('/', data=data)
        req.user = mixer.blend('auth.User', first_name='Zach')
        resp = views.PostUpdateView(req, pk=post.pk)
        assert resp.status_code == 302, 'Should redirect to success view'
        post.refresh_from_db()
        assert post.body == 'New Body Text!', 'Should update the post'
   
    def test_security(self):
        user = mixer.blend('auth.User', first_name='Martin')
        post = mixer.blend('birdie.Post')
        req = RequestFactory().post('/', data={})
        req.user = user
        with pytest.raises(Http404):
            views.PostUpdateView(req, pk=post.pk)

class TestPaymentView:
    @patch('birdie.views.stripe')
    def test_payment(self, mock_stripe):
        mock_stripe.Charge.return_value = {'id': '234'}
        req = RequestFactory().post('/', data={'token': '123'})
        resp = views.PaymentView(req)
        assert resp.status_code == 302, 'Should redirect to success_url'
        assert len(mail.outbox) == 1, 'Should send an email'