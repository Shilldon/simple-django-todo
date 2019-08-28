from django.test import TestCase
from django.shortcuts import get_object_or_404
from .models import Item

class TestViews(TestCase):
    def test_get_home_page(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "todo_list.html")
    
    def test_get_add_item_page(self):
        page = self.client.get("/add")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "item_form.html")

    def test_get_edit_item_page(self):
        item = Item(name='Create a test') #to test the edit page we need to pass an id into the url. To get an ID we need to create an item in the database
        item.save() # item will be created in a test database and is destroyed at end of test.
        
        page = self.client.get("/edit/{0}".format(item.id)) # NB item 0 is used because there will only be one item in the database
        # if use a difference item instance we will get a 404 error because that is what the views.py says should happen if item can't be found:
        # item = get_object_or_404(Item, pk=id)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "item_form.html")
    
    def test_get_edit_page_for_item_that_does_not_exists(self):
        page = self.client.get("/edit/1")
        self.assertEqual(page.status_code, 404) # to check 404 error is generated if item does not exists.
        
    def test_post_create_an_item(self):
        response = self.client.post("/add", {"name": "Create a test"})
        item = get_object_or_404(Item, pk=1)
        self.assertEqual(item.done, False)

    def test_post_edit_an_item(self):
        item = Item(name="Create a test")
        item.save()
        id = item.id
        
        response = self.client.post("/edit/{0}".format(id),{"name" : "Updated create a test name"}) # testing the urls from urls.py
        item = get_object_or_404(Item, pk=id)
        self.assertEqual(item.name, "Updated create a test name")

    def test_toggle_status(self):
        item = Item(name="Create a test")
        item.save()
        id = item.id
        
        response = self.client.post("/toggle/{0}".format(id),{"done" : True})
        item = get_object_or_404(Item, pk=id)
        self.assertEqual(item.done, True)       