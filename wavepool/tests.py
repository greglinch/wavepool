import random
import string

from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from wavepool.models import NewsPost


class TestBase(TestCase):
    fixtures = ['test_fixture', ]

    def _clean_text(self, text):
        return text.replace('\n', '').replace('\t', '')

    def _random_string(self, length):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))

    def _login_user(self):
        password = self._random_string(12)
        username = self._random_string(6)
        user = User.objects.create_superuser(
            username,
            '%s@industrydive.com' % username,
            password
        )
        user.save()
        client = self.client
        client.login(username=username, password=password)


class NewsPostViewTest(TestBase):

    def test_article_unique_urls(self):
        articles = NewsPost.objects.all()
        unique_article_urls = []
        for article in articles:
            self.assertNotIn(article.url, unique_article_urls)
            unique_article_urls.append(article.url)

    def test_article_page_content(self):
        articles = NewsPost.objects.all()
        for article in articles:
            page = self.client.get(article.url)
            page_html = BeautifulSoup(page.content, 'html.parser')
            rendered_title = page_html.find('h1', {'id': 'article-title'}).text
            rendered_body = page_html.find('div', {'id': 'article-body'}).text
            self.assertEqual(rendered_title, article.title)
            self.assertEqual(self._clean_text(rendered_body), self._clean_text(article.body))

    def test_article_body_render(self):
        articles = NewsPost.objects.all()
        for article in articles:
            page = self.client.get(article.url)
            page_html = BeautifulSoup(page.content, 'html.parser')
            self.assertNotIn('<p>', page_html.text)

    def test_visitor_not_sees_edit_link(self):
        articles = NewsPost.objects.all()
        for article in articles:
            page = self.client.get(article.url)
            page_html = BeautifulSoup(page.content, 'html.parser')
            edit_link = page_html.find('a', {'id': 'edit-link'})
            self.assertIsNone(edit_link)

    def test_cms_user_sees_edit_link(self):
        self._login_user()
        articles = NewsPost.objects.all()
        for article in articles:
            page = self.client.get(article.url)
            page_html = BeautifulSoup(page.content, 'html.parser')
            edit_link = page_html.find('a', {'id': 'edit-link'})
            edit_url = edit_link['href']
            self.assertEqual(edit_url, reverse('admin:wavepool_newspost_change', args=[article.pk]))


class FrontpageViewTest(TestBase):

    def test_top_stories(self):
        latest_four_stories = NewsPost.objects.all().order_by('publish_date')[:4]
        cover_story = latest_four_stories[2]
        cover_story.is_cover_story = True
        cover_story.save()

        top_stories = [latest_four_stories[0], latest_four_stories[1], latest_four_stories[3], ]

        front_page = self.client.get('')
        front_page_html = BeautifulSoup(front_page.content, 'html.parser')

        cover_story_div = front_page_html.find('div', {'id': 'coverstory'})
        cover_story_id = int(cover_story_div['data-story-id'])

        self.assertEqual(cover_story_id, cover_story.pk)

        rendered_top_stories = front_page_html.find_all('div', {'class': 'topstory'})
        self.assertEqual(len(rendered_top_stories), 3)

        top_story_1 = front_page_html.find(
            'div', {'class': 'topstory', 'data-top-story-placement': '1', }
        )
        top_story_1_id = int(top_story_1['data-story-id'])

        top_story_2 = front_page_html.find(
            'div', {'class': 'topstory', 'data-top-story-placement': '2', }
        )
        top_story_2_id = int(top_story_2['data-story-id'])

        top_story_3 = front_page_html.find(
            'div', {'class': 'topstory', 'data-top-story-placement': '3', }
        )
        top_story_3_id = int(top_story_3['data-story-id'])

        self.assertEqual(top_story_1_id, top_stories[0].pk)
        self.assertEqual(top_story_2_id, top_stories[1].pk)
        self.assertEqual(top_story_3_id, top_stories[2].pk)

    def test_archive_stories(self):
        all_stories = NewsPost.objects.all().order_by('publish_date')
        cover_story = all_stories[7]
        cover_story.is_cover_story = True
        cover_story.save()

        top_stories = [all_stories[0], all_stories[1], all_stories[2]]
        archive_stories = []
        for story in all_stories:
            if story not in top_stories and story != cover_story:
                archive_stories.append(story)

        front_page = self.client.get('')
        front_page_html = BeautifulSoup(front_page.content, 'html.parser')
        archive_story_divs = front_page_html.find_all('div', {'class': 'archived-story'})
        self.assertEqual(len(archive_story_divs), len(archive_stories))
        for div in archive_story_divs:
            story_id = int(div['data-archive-story-id'])
            self.assertIn(story_id, [s.id for s in archive_stories])


class CmsTest(TestBase):
    fixtures = ['test_fixture', ]

    def _get_news_list_page_rows(self):
        self._login_user()
        list_page_url = reverse('admin:wavepool_newspost_changelist')
        list_page = self.client.get(list_page_url)
        page_html = BeautifulSoup(list_page.content, 'html.parser')
        list_table = page_html.find('table', {'id': 'result_list'})
        admin_rows = list_table.tbody.find_all('tr')
        return admin_rows

    def test_title_shows_on_list_page(self):
        admin_rows = self._get_news_list_page_rows()
        for row in admin_rows:
            resolved_admin_url = resolve(row.find('a')['href'])
            obj_id = resolved_admin_url.kwargs['object_id']
            newspost = NewsPost.objects.get(pk=obj_id)
            self.assertIn(newspost.title, row.text)

    def test_pubdate_shows_on_list_page(self):
        admin_rows = self._get_news_list_page_rows()
        for row in admin_rows:
            resolved_admin_url = resolve(row.find('a')['href'])
            obj_id = resolved_admin_url.kwargs['object_id']
            newspost = NewsPost.objects.get(pk=obj_id)
            display_pub_date = newspost.publish_date.strftime('%b. %d, %Y')
            self.assertIn('{}'.format(display_pub_date), row.text)

    def test_displayed_in_order(self):
        admin_rows = self._get_news_list_page_rows()
        last_pubdate = None
        for row in admin_rows:
            resolved_admin_url = resolve(row.find('a')['href'])
            obj_id = resolved_admin_url.kwargs['object_id']
            newspost = NewsPost.objects.get(pk=obj_id)
            if last_pubdate:
                self.assertTrue(newspost.publish_date >= last_pubdate)
            last_pubdate = newspost.publish_date

    def test_only_one_cover_story(self):
        self._login_user()
        articles = NewsPost.objects.all()

        old_cover_story_article = articles[2]
        old_cover_story_article.is_cover_story = True
        old_cover_story_article.save()

        new_cover_story_article = articles[3]
        new_cover_story_article_change_url = reverse(
            'admin:wavepool_newspost_change', args=[new_cover_story_article.pk]
        )
        post_data = {
            'title': new_cover_story_article.title,
            'publish_date': new_cover_story_article.publish_date,
            'body': new_cover_story_article.body,
            'source': new_cover_story_article.source,
            'is_cover_story': True,
        }
        self.client.post(new_cover_story_article_change_url, post_data)

        new_cover_story_article = NewsPost.objects.get(pk=new_cover_story_article.pk)
        self.assertTrue(new_cover_story_article.is_cover_story)

        old_cover_story_article = NewsPost.objects.get(pk=old_cover_story_article.pk)
        self.assertFalse(old_cover_story_article.is_cover_story)
