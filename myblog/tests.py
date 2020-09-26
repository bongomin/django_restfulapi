from rest_framework.test import APITestCase
from django.urls import reverse
from django.test import TestCase
from .models import Post, Tag
from .views import status


# Create your tests here.
class PostTestCase(TestCase):
    def test_post(self):
        self.assertEquals(
            Post.objects.count(),
            0
        )
        Post.objects.create(
            title='active', text='text', is_active=True
        )
        Post.objects.create(
            title='inactive', text='text', is_active=False
        )
        self.assertEquals(
            Post.objects.count(),
            2
        )
        active_posts = Post.objects.active()
        self.assertEquals(
            active_posts.count(),
            1
        )
        inactive_posts = Post.objects.inactive()
        self.assertEquals(
            inactive_posts.count(),
            1
        )

class TagTestCase(TestCase):
    def test_tag(self):
        self.assertEquals(
            Tag.objects.count(),
            0
        )
        Tag.objects.create(name='name')
        self.assertEquals(
            Tag.objects.count(),
            1
        )


class PostListCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('api-post-list', kwargs={'version': 'v1'})

    def test_create_post(self):
        self.assertEquals(
            Post.objects.count(),
            0
        )
        data = {
            'title': 'title',
            'text': 'text'
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(
            Post.objects.count(),
            1
        )
        post = Post.objects.first()
        self.assertEquals(
            post.title,
            data['title']
        )
        self.assertEquals(
            post.text,
            data['text']
        )

    def test_get_post_list(self):
        tag = Tag(name='tag_name')
        tag.save()
        post = Post(title='title1', text='text1')
        post.save()
        post.tags.add(tag)

        response = self.client.get(self.url)
        response_json = response.json()
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            len(response_json),
            1
        )
        data = response_json[0]
        self.assertEquals(
            data['title'],
            post.title
        )
        self.assertEquals(
            data['text'],
            post.text
        )
        self.assertEquals(
            data['tags'][0]['name'],
            tag.name
        )

# post Tests below
class PostDetailsAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.post = Post(title='title2', text='text2')
        self.post.save()
        self.url = reverse('api-post-details',
                           kwargs={'version': 'v1', 'pk': self.post.pk})

    def test_get_post_details(self):
        response = self.client.get(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        data = response.json()
        self.assertEquals(
            data['pk'],
            str(self.post.pk)
        )
        self.assertEquals(
            data['title'],
            self.post.title
        )
        self.assertEquals(
            data['text'],
            self.post.text
        )

    def test_update_post(self):
        response = self.client.get(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        data = response.json()
        data['title'] = 'new_title'
        data['text'] = 'new_text'
        response = self.client.put(self.url, data=data, format='json')
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.post.refresh_from_db()
        self.assertEquals(
            self.post.title,
            data['title']
        )
        self.assertEquals(
            self.post.text,
            data['text']
        )

    def test_delete_post(self):
        self.assertEquals(
            Post.objects.count(),
            1
        )
        response = self.client.delete(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEquals(
            Post.objects.count(),
            0
        )
