import logging
import os
from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.urls import reverse

from biostar.engine import models, views, auth
from . import util

logger = logging.getLogger('engine')


class DataViewTest(TestCase):
    def setUp(self):
        logger.setLevel(logging.WARNING)

        # Set up generic owner
        self.owner = models.User.objects.create_user(username="test", email="test@l.com")
        self.owner.set_password("test")

        self.project = auth.create_project(user=self.owner, name="test", text="Text", summary="summary",
                                           uid="testing")
        self.project.save()

        # Set up generic data for editing
        self.data = auth.create_data(project=self.project, path=__file__)

    @patch('biostar.engine.models.Data.save', MagicMock(name="save"))
    def test_data_edit(self):
        "Test Data edit view with POST request"

        data = {'name': "new_data", 'summary': "summary", 'text': "testing",
                'sticky': True}

        url = reverse('data_edit', kwargs=dict(uid=self.data.uid))

        request = util.fake_request(url=url, data=data, user=self.owner)

        response = views.data_edit(request=request, uid=self.data.uid)

        obj = {}
        self.data.fill_dict(obj=obj)

        self.assertTrue("toc" in obj, "Table of content not added during fill_dict()")

        self.process_response(response=response, data=data, save=True)

    @patch('biostar.engine.models.Data.save', MagicMock(name="save"))
    def test_data_upload(self):
        "Test Data upload POST request"

        data = {
            'file': open(__file__, 'r'),
            'summary': 'summary',
            "text": "testing",
            "sticky": True
        }

        url = reverse('data_upload', kwargs=dict(uid=self.project.uid))

        # Create a new user and give them upload access
        user = models.User.objects.create_user(username="test2", email="test2@l.com")
        user.set_password("test")
        user.save()
        access = models.Access(access=models.Access.WRITE_ACCESS,
                               user=user,
                               project=self.project)
        access.save()

        request = util.fake_request(url=url, data=data, user=user)
        response = views.data_upload(request=request, uid=self.project.uid)

        self.process_response(response=response, data=data, save=True)

    def test_add_data(self):
        "Test adding data directory to a project using management commands "

        data_directory = auth.join(__file__, "..", "data")

        data = auth.create_data(project=self.project, path=data_directory)

        self.assertTrue(os.path.exists(data.get_data_dir()), "Directory not being linked")


    @patch('biostar.engine.models.Data.save', MagicMock(name="save"))
    def test_data_paste(self):
        "Test data paste view."

        data = {}

        url = reverse('data_paste', kwargs=dict(uid=self.project.uid))

        request = util.fake_request(url=url, data=data, user=self.owner)
        request.session["data_clipboard"] = [self.data.uid]

        response = views.data_paste(request=request, uid=self.project.uid)

        self.process_response(response=response, data=data, save=True)

    def test_engine_tags(self):
        "Test some template tags found in engine_tags.py"

        from biostar.engine.templatetags import engine_tags

        options = {"recipe_clipboard":dict(project=self.project),
                    "data_clipboard":dict(data=True, project=self.project),
                   "files_clipboard":dict(files=True, project=self.project)
                   }
        for o in options:
            paste_template = engine_tags.paste(**options[o])
            # Paste template needs to be rendered correctly for each clipboard
            self.assertTrue(o in paste_template["clear_url"], f"{o} : {paste_template}")

    def process_response(self, response, data, save=False):
        "Check the response on POST request is redirected"

        self.assertEqual(response.status_code, 302,
                         f"Could not redirect to project view after testing :\nresponse:{response}")

        if save:
            self.assertTrue( models.Data.save.called, "save() method not called")