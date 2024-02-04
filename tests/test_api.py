

from uuid import uuid4
from fastapi.testclient import TestClient

from src.main import app
from src.models.subscription import Subscription


user_identifier = str(uuid4())
client = TestClient(app)

email_subscription = {
    'user_identifier': user_identifier,
    'sub_type': 'email',
    'sub_address': 'example@example.com',
    'is_promotion': True
}

sns_subscription = {
    'user_identifier': user_identifier,
    'sub_type': 'sns',
    'sub_address': '123456789',
    'is_promotion': False,
}

new_email = 'example_new@example.com'


class TestSubscription:

    # Create

    def test_create_email_subscription(self):
        resp = client.post(
            '/api/v1/subscribe',
            json=email_subscription
        )
        assert resp.status_code == 200
        result = resp.json()
        print(result)
        assert result['data']['user_identifier'] == user_identifier \
            and result['data']['sub_type'] == email_subscription['sub_type'] \
            and result['data']['sub_address'] == email_subscription['sub_address'] \
            and result['data']['is_promotion'] == email_subscription['is_promotion']


    def test_create_sns_subscription(self):
        resp = client.post(
            '/api/v1/subscribe',
            json=sns_subscription
        )
        assert resp.status_code == 200
        result = resp.json()
        assert result['data']['user_identifier'] == user_identifier \
            and result['data']['sub_type'] == sns_subscription['sub_type'] \
            and result['data']['sub_address'] == sns_subscription['sub_address'] \
            and result['data']['is_promotion'] == sns_subscription['is_promotion']


    # Get

    def test_get_subscriptions_by_user_identifier(self):
        resp = client.get(
            '/api/v1/subscriptions',
            params={
                'user_identifier': user_identifier
            }
        )
        assert resp.status_code == 200
        result = resp.json()
        assert len(result['data']) == 2
        

    def test_get_subscriptions_by_email(self):
        resp = client.get(
            '/api/v1/subscriptions',
            params={
                'email': email_subscription['sub_address']
            }
        )
        assert resp.status_code == 200
        result = resp.json()
        assert result['data'][0]['user_identifier'] == user_identifier \
            and result['data'][0]['sub_type'] == email_subscription['sub_type'] \
            and result['data'][0]['sub_address'] == email_subscription['sub_address']


    def test_get_subscriptions_by_mobile(self):
        resp = client.get(
            '/api/v1/subscriptions',
            params={
                'mobile': sns_subscription['sub_address']
            }
        )
        assert resp.status_code == 200
        result = resp.json()
        assert result['data'][0]['user_identifier'] == user_identifier \
            and result['data'][0]['sub_type'] == sns_subscription['sub_type'] \
            and result['data'][0]['sub_address'] == sns_subscription['sub_address']


    # Update

    def test_update_subscription(self):
        resp = client.post(
            '/api/v1/subscribe',
            json={
                'user_identifier': user_identifier,
                'sub_type': 'email',
                'sub_address': new_email
            }
        )
        assert resp.status_code == 200
        assert resp.json()['data']['sub_address'] == new_email


    # Unsubscribe

    def test_unsubscribe_by_user_identifier(self):
        resp = client.post(
            '/api/v1/unsubscribe',
            json={
                'user_identifier': user_identifier,
            }
        )
        assert resp.status_code == 200
        assert len(resp.json()['data']) == 2
        subscription_resp = client.get(
            '/api/v1/subscriptions',
            params={
                'user_identifier': user_identifier
            }
        )
        assert True not in [_sub['is_active'] for _sub in subscription_resp.json()['data']]


    def test_unsubscribe_by_mobile(self):
        resp = client.post(
            '/api/v1/unsubscribe',
            json={
                'mobile': sns_subscription['sub_address'],
            }
        )
        assert resp.status_code == 200
        sub_resp = client.get(
            '/api/v1/subscriptions',
            params={
                'mobile': sns_subscription['sub_address']
            }
        )
        assert not sub_resp.json()['data'][0]['is_active']

    def test_delete_data(self):
        import logging
        with app.state.session_factory() as session:
            session.query(Subscription).filter(
                Subscription.user_identifier == user_identifier
            ).delete()
            logging.info("Delete all test data")
            session.commit()
