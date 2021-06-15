from unittest.mock import patch, MagicMock

from mixer.backend.django import mixer
from django_elasticsearch_dsl.registries import registry
from django.urls import reverse

from breaking_brain_api.tests import BaseAPITest
from quizzes.models import Quiz, Question, Option, Lesson, Tag


class QuizTest(BaseAPITest):

    def setUp(self):
        self.quiz = mixer.blend(Quiz, title='something', is_free=True)
        self.question = mixer.blend(Question, quiz=self.quiz)
        self.option = mixer.blend(Option, question=self.question)
        self.lesson = mixer.blend(Lesson, quiz=self.quiz)
        self.user = self.create_and_login()

    def test_get_list_of_quizes(self):
        resp = self.client.get(reverse('quizzes-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['count'], 1)
        self.assertEqual(resp.data['results'][0]['id'], self.quiz.id)
        self.assertEqual(resp.data['results'][0]['title'], self.quiz.title)
        self.assertEqual(resp.data['results'][0]['lessons'][0]['id'], self.lesson.id)
        self.assertEqual(resp.data['results'][0]['lessons'][0]['title'], self.lesson.title)

    def test_get_list_of_quizes_when_logged_out(self):
        self.logout()
        resp = self.client.get(reverse('quizzes-list'))
        self.assertEqual(resp.status_code, 200)

    def test_search_quiz_by_its_title(self):
        registry.update(self.quiz)
        registry.update_related(self.quiz)
        url = f"{reverse('quizzes-search')}?q=something"
        url2 = f"{reverse('quizzes-search')}?q=else"
        resp = self.client.get(url)
        resp2 = self.client.get(url2)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data[0]['title'], self.quiz.title)
        self.assertEqual(resp.data[0]['id'], self.quiz.id)
        self.assertEqual(len(resp2.data), 0)
        registry.delete(self.quiz)
        registry.delete_related(self.quiz)

    def test_search_quiz_by_its_tag_title(self):
        self.quiz.tags.add(mixer.blend(Tag, label='tag-label'))
        registry.update(self.quiz)
        registry.update_related(self.quiz)
        url = f"{reverse('quizzes-search')}?q=tag-label"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data[0]['title'], self.quiz.title)
        self.assertEqual(resp.data[0]['id'], self.quiz.id)
        registry.delete(self.quiz)
        registry.delete_related(self.quiz)

    def test_get_single_quiz(self):
        resp = self.client.get(reverse('quizzes-detail', args=(self.quiz.id,)))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['id'], self.quiz.id)
        self.assertEqual(resp.data['title'], self.quiz.title)
        self.assertEqual(resp.data['lessons'][0]['id'],
                         self.lesson.id)

    def test_get_single_quiz_when_logout(self):
        self.logout()
        resp = self.client.get(reverse('quizzes-detail', args=(self.quiz.id,)))
        self.assertEqual(resp.status_code, 200)

    def test_get_non_existed_quiz(self):
        resp = self.client.get(reverse('quizzes-detail', args=(123123,)))
        self.assertEqual(resp.status_code, 404)

    def test_get_questions_from_quiz(self):
        resp = self.client.get(reverse('quizzes-questions', args=(self.quiz.id,)))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data[0]['id'], self.question.id)
        self.assertEqual(resp.data[0]['options'][0]['id'], self.option.id)
        self.assertEqual(len(resp.data), 1)

    def test_get_quesionts_from_non_existed_quiz(self):
        resp = self.client.get(reverse('quizzes-questions', args=(12311,)))
        self.assertEqual(resp.status_code, 404)

    def test_get_questions_from_quiz_when_logout(self):
        self.logout()
        resp = self.client.get(reverse('quizzes-questions', args=(self.quiz.id,)))
        self.assertEqual(resp.status_code, 401)

    def test_add_quiz_to_favorites(self):
        self.assertEqual(self.user.favorites.count(), 0)
        resp = self.client.post(reverse('quizzes-toggle-favorites', args=(self.quiz.id,)))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.user.favorites.count(), 1)
        self.assertTrue(self.user.favorites.filter(pk=self.quiz.id).exists())

    def test_remove_quiz_from_favorites(self):
        self.client.post(reverse('quizzes-toggle-favorites', args=(self.quiz.id,)))
        resp = self.client.post(reverse('quizzes-toggle-favorites', args=(self.quiz.id,)))
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(self.user.favorites.count(), 0)

    def test_get_list_of_favorites_quizzes(self):
        self.client.post(reverse('quizzes-toggle-favorites', args=(self.quiz.id,)))
        resp = self.client.get(reverse('quizzes-favorites'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data[0]['id'], self.quiz.id)
        self.assertEqual(resp.data[0]['title'], self.quiz.title)

    @patch('stripe.PaymentIntent.create')
    def test_buy_quiz_without_confirmation(self, create):
        self.quiz.is_free = False
        self.quiz.save()
        intent = MagicMock()
        intent.status = 'succeeded'
        create.return_value = intent
        data = {
            'confirmation': False,
            'payment_method_id': 'something'
        }
        resp = self.client.post(reverse('quizzes-buy', args=(self.quiz.id,)), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['id'], self.quiz.id)
        self.user.refresh_from_db()
        self.assertTrue(self.user.bought_quizzes.filter(pk=self.quiz.id).exists())

    @patch('stripe.PaymentIntent.create')
    def test_buy_quiz_should_be_confirmed(self, create):
        self.quiz.is_free = False
        self.quiz.save()
        intent = MagicMock()
        intent.status = 'requires_action'
        intent.next_action.type = 'use_stripe_sdk'
        create.return_value = intent
        data = {
            'confirmation': False,
            'payment_method_id': 'something'
        }
        resp = self.client.post(reverse('quizzes-buy', args=(self.quiz.id,)), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['requires_action'])

    @patch('stripe.PaymentIntent.confirm')
    def test_buy_quiz_after_confirmation(self, confirm):
        self.quiz.is_free = False
        self.quiz.save()
        intent = MagicMock()
        intent.status = 'succeeded'
        confirm.return_value = intent
        data = {
            'confirmation': True,
            'payment_method_id': 'something'
        }
        resp = self.client.post(reverse('quizzes-buy', args=(self.quiz.id,)), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['id'], self.quiz.id)
        self.user.refresh_from_db()
        self.assertTrue(self.user.bought_quizzes.filter(pk=self.quiz.id).exists())

    def test_invalid_data_on_buy_quiz(self):
        data = {
            'confirmation': 'something',
            'payment_method_id': None
        }
        resp = self.client.post(reverse('quizzes-buy', args=(self.quiz.id,)), data=data)
        self.assertEqual(resp.status_code, 400)

    def test_get_question_in_bought_quiz(self):
        self.user.bought_quizzes.add(self.quiz)
        self.quiz.is_free = False
        self.quiz.save()
        resp = self.client.get(reverse('quizzes-questions', args=(self.quiz.id,)))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data[0]['id'], self.question.id)

    def test_get_questions_in_non_free_quiz(self):
        self.quiz.is_free = False
        self.quiz.save()
        resp = self.client.get(reverse('quizzes-questions', args=(self.quiz.id,)))
        self.assertEqual(resp.status_code, 403)

    def test_add_bought_quiz_to_favorites(self):
        self.user.bought_quizzes.add(self.quiz)
        self.quiz.is_free = False
        self.quiz.save()
        self.assertEqual(self.user.favorites.count(), 0)
        resp = self.client.post(reverse('quizzes-toggle-favorites', args=(self.quiz.id,)))
        self.assertEqual(resp.status_code, 200)

    def test_add_non_free_quiz_to_favorites(self):
        self.quiz.is_free = False
        self.quiz.save()
        self.assertEqual(self.user.favorites.count(), 0)
        resp = self.client.post(reverse('quizzes-toggle-favorites', args=(self.quiz.id,)))
        self.assertEqual(resp.status_code, 403)
