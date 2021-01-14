from unittest.mock import patch

from breaking_brain_api.tasks import send_email
from breaking_brain_api.tests import BaseAPITest


class TestTasks(BaseAPITest):

    def setUp(self):
        self.mail_data = {
            'subject': 'ChooseOne activate user',
            'template': 'notifications/activate_user.html',
            'context': {'url': 'http://localhost:8000/'},
            'recipients': ['test@mail.com'],
        }

    @patch('mailjet_rest.client.api_call')
    def test_send_email_task(self, send_email_task):
        def return_mock_class(*args, **kwargs):
            class MockRequest:
                status_code = 200

            return MockRequest()

        send_email_task.side_effect = return_mock_class
        send_email(**self.mail_data)
        send_email_task.assert_called_once()
