import logging
from django.core import management
from django.test import TestCase
from django.forms import ValidationError
from django.core.files import File
from django.urls import reverse
from biostar.engine import models, views, auth, factory, forms, const
from biostar.engine import util as engine_util


from . import util

logger = logging.getLogger('engine')


class SiteAdminTest(TestCase):

    def setUp(self):
        logger.setLevel(logging.WARNING)

        self.user = models.User.objects.create_superuser(username="test", email="test@test.com",
                                                         password="test")
        self.user.save()

    def test_site_admin(self):
        "Test site admin page"

        url =  reverse("site_admin")
        request = util.fake_request(url=url, data={}, method="GET",user=self.user)

        response = views.site_admin(request=request)
        # admin page specific to biostar-engine.
        self.assertEqual(response.status_code, 200, "Can not load admin page")

    def test_bin_view(self):
        "Test recycle bin view"

        url = reverse('recycle_bin')
        request = util.fake_request(url=url, data={}, method="GET",user=self.user)
        response = views.recycle_bin(request=request)
        self.assertEqual(response.status_code, 200, "Can not load recyle bin")

class FactoryTest(TestCase):

    def setUp(self):
        logger.setLevel(logging.WARNING)


        owner = models.User.objects.filter(is_superuser=True).first()
        self.project = auth.create_project(user=owner, name="test",
                                           text="Text", summary="summary", uid="testing")

    def test_factory_fields(self):
        "Testing factory module that generates fields"

        # All valid field types.
        field_types = factory.get_field_types()

        for display_type in field_types:

            # Test that each field type can be rendered.
            json_data = dict(display=display_type)

            field = factory.dynamic_field(json_data)
            if not field:
                message = f"field generator for display={display_type} failed"
                self.assertFalse(message)


    def test_dynamic_field(self):
        "Test data generator"

        from biostar.engine import const

        data = auth.create_data(self.project, path=__file__)

        display_type = const.DROPDOWN

        json_data = dict(display=display_type, value=data.name,
                         source= 'PROJECT')

        field = factory.dynamic_field(json_data, project=self.project)

        if not field:
            self.assertFalse(f"field generator for display={display_type} failed")

    def test_data_generator(self):
        "Test data generator"

        field = factory.data_field_generator(field={}, project=self.project)


        if not field:
            self.assertFalse(f"data field generator failed")


class UtilTests(TestCase):

    def setUp(self):
        logger.setLevel(logging.WARNING)

    def test_smart_preview(self):

        collect = auth.findfiles("biostar/engine/test/data", collect=[])
        for fname in collect:

            text = engine_util.smart_preview(fname)
            self.assertTrue("error" not in text.split(), f"Preview error with {fname}")

            with self.assertRaises(ValidationError):
                forms.check_size(File(open(fname, "r")), maxsize=0.000001)

