from django.core.urlresolvers import resolve
from django.http import HttpResponse, HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):
    def create_item_post_request(self, item_text):
        request = HttpRequest()
        request.method = "POST"
        request.POST["item_text"] = item_text
        return request

    def test_root_url_resolve_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_should_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string("home.html")
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_only_saves_item_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_can_save_POST_request(self):
        request = self.create_item_post_request('New Item')

        home_page(request)

        items = Item.objects.all()
        self.assertEqual(items.count(), 1)
        self.assertEqual(items[0].text, 'New Item')

    def test_home_page_should_redirect_after_POST(self):
        request = self.create_item_post_request('New Item')

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')


class ItemModelTest(TestCase):
    def test_save_and_restore_items_from_db(self):
        first_item = Item(text="Item 1")
        first_item.save()
        second_item = Item(text="Item 2")
        second_item.save()

        items = Item.objects.all()

        self.assertEqual(items.count(), 2)
        self.assertEqual(items[0].text, "Item 1")
        self.assertEqual(items[1].text, "Item 2")


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_lists_items(self):
        Item.objects.create(text="Item 1")
        Item.objects.create(text="Item 2")

        response = self.client.get("/lists/the-only-list-in-the-world/")

        self.assertContains(response, "Item 1")
        self.assertContains(response, "Item 2")

        # class NewListItemTest