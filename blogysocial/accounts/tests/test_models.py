from django.test import TestCase

from accounts.models import UserModel


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        UserModel.objects.create(
            username='user1',
            email='user1@user1.com',
            name='User One',
            password='1234567890'
        )

    def test_username_verbose_name(self):
        user = UserModel.objects.get(id=1)
        verbose_name = user._meta.get_field('username').verbose_name
        self.assertEqual(verbose_name, 'Username')

    def test_email_verbose_name(self):
        user = UserModel.objects.get(id=1)
        verbose_name = user._meta.get_field('email').verbose_name
        self.assertEqual(verbose_name, 'Email Address')

    def test_name_verbose_name(self):
        user = UserModel.objects.get(id=1)
        verbose_name = user._meta.get_field('name').verbose_name
        self.assertEqual(verbose_name, 'Name')

    def test_password_verbose_name(self):
        user = UserModel.objects.get(id=1)
        verbose_name = user._meta.get_field('password').verbose_name
        self.assertEqual(verbose_name, 'Password')

    def test_phone_verbose_name(self):
        user = UserModel.objects.get(id=1)
        verbose_name = user._meta.get_field('phone').verbose_name
        self.assertEqual(verbose_name, 'Phone Number')

    def test_photo_verbose_name(self):
        user = UserModel.objects.get(id=1)
        verbose_name = user._meta.get_field('photo').verbose_name
        self.assertEqual(verbose_name, 'Author Photo')

    def test_about_me_verbose_name(self):
        user = UserModel.objects.get(id=1)
        verbose_name = user._meta.get_field('about_me').verbose_name
        self.assertEqual(verbose_name, 'About me')

    def test_web_verbose_name(self):
        user = UserModel.objects.get(id=1)
        verbose_name = user._meta.get_field('web').verbose_name
        self.assertEqual(verbose_name, 'Author Website')

    def test_instagram_verbose_name(self):
        user = UserModel.objects.get(id=1)
        verbose_name = user._meta.get_field('instagram').verbose_name
        self.assertEqual(verbose_name, 'Author Instagram')

    def test_twitter_verbose_name(self):
        user = UserModel.objects.get(id=1)
        verbose_name = user._meta.get_field('twitter').verbose_name
        self.assertEqual(verbose_name, 'Author Twitter')

    def test_photo_help_text(self):
        user = UserModel.objects.get(id=1)
        help_text = user._meta.get_field('photo').help_text
        self.assertEqual(help_text, 'Upload photo')

    def test_username_max_length(self):
        user = UserModel.objects.get(id=1)
        max_length = user._meta.get_field('username').max_length
        self.assertEqual(max_length, 100)

    def test_email_max_length(self):
        user = UserModel.objects.get(id=1)
        max_length = user._meta.get_field('email').max_length
        self.assertEqual(max_length, 150)

    def test_name_max_length(self):
        user = UserModel.objects.get(id=1)
        max_length = user._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_password_max_length(self):
        user = UserModel.objects.get(id=1)
        max_length = user._meta.get_field('password').max_length
        self.assertEqual(max_length, 50)

    def test_phone_max_length(self):
        user = UserModel.objects.get(id=1)
        max_length = user._meta.get_field('phone').max_length
        self.assertEqual(max_length, 35)

    def test_about_me_max_length(self):
        user = UserModel.objects.get(id=1)
        max_length = user._meta.get_field('about_me').max_length
        self.assertEqual(max_length, 255)

    def test_web_max_length(self):
        user = UserModel.objects.get(id=1)
        max_length = user._meta.get_field('web').max_length
        self.assertEqual(max_length, 255)

    def test_instagram_max_length(self):
        user = UserModel.objects.get(id=1)
        max_length = user._meta.get_field('instagram').max_length
        self.assertEqual(max_length, 255)

    def test_twitter_max_length(self):
        user = UserModel.objects.get(id=1)
        max_length = user._meta.get_field('twitter').max_length
        self.assertEqual(max_length, 255)

    def test_username_unique(self):
        user = UserModel.objects.get(id=1)
        unique = user._meta.get_field('username').unique
        self.assertEqual(unique, True)

    def test_email_unique(self):
        user = UserModel.objects.get(id=1)
        unique = user._meta.get_field('email').unique
        self.assertEqual(unique, True)

    def test_phone_null(self):
        user = UserModel.objects.get(id=1)
        null = user._meta.get_field('phone').null
        self.assertEqual(null, True)

    def test_photo_null(self):
        user = UserModel.objects.get(id=1)
        null = user._meta.get_field('photo').null
        self.assertEqual(null, True)

    def test_about_me_null(self):
        user = UserModel.objects.get(id=1)
        null = user._meta.get_field('about_me').null
        self.assertEqual(null, True)

    def test_web_null(self):
        user = UserModel.objects.get(id=1)
        null = user._meta.get_field('web').null
        self.assertEqual(null, True)

    def test_instagram_null(self):
        user = UserModel.objects.get(id=1)
        null = user._meta.get_field('instagram').null
        self.assertEqual(null, True)

    def test_twitter_null(self):
        user = UserModel.objects.get(id=1)
        null = user._meta.get_field('twitter').null
        self.assertEqual(null, True)

    def test_deleted_at_null(self):
        user = UserModel.objects.get(id=1)
        null = user._meta.get_field('deleted_at').null
        self.assertEqual(null, True)

    def test_phone_blank(self):
        user = UserModel.objects.get(id=1)
        blank = user._meta.get_field('phone').blank
        self.assertEqual(blank, True)

    def test_photo_blank(self):
        user = UserModel.objects.get(id=1)
        blank = user._meta.get_field('photo').blank
        self.assertEqual(blank, True)

    def test_about_me_blank(self):
        user = UserModel.objects.get(id=1)
        blank = user._meta.get_field('about_me').blank
        self.assertEqual(blank, True)

    def test_web_blank(self):
        user = UserModel.objects.get(id=1)
        blank = user._meta.get_field('web').blank
        self.assertEqual(blank, True)

    def test_instagram_blank(self):
        user = UserModel.objects.get(id=1)
        blank = user._meta.get_field('instagram').blank
        self.assertEqual(blank, True)

    def test_twitter_blank(self):
        user = UserModel.objects.get(id=1)
        blank = user._meta.get_field('twitter').blank
        self.assertEqual(blank, True)

    def test_deleted_at_blank(self):
        user = UserModel.objects.get(id=1)
        blank = user._meta.get_field('deleted_at').blank
        self.assertEqual(blank, True)

    def test_photo_upload_to(self):
        user = UserModel.objects.get(id=1)
        upload_to = user._meta.get_field('photo').upload_to
        self.assertEqual(upload_to, 'images/authors/')

    def test_photo_default(self):
        user = UserModel.objects.get(id=1)
        default = user._meta.get_field('photo').default
        self.assertEqual(default, 'images/default.png')

    def test_remember_me_default(self):
        user = UserModel.objects.get(id=1)
        default = user._meta.get_field('remember_me').default
        self.assertEqual(default, False)

    def test_is_active_default(self):
        user = UserModel.objects.get(id=1)
        default = user._meta.get_field('is_active').default
        self.assertEqual(default, False)

    def test_is_staff_default(self):
        user = UserModel.objects.get(id=1)
        default = user._meta.get_field('is_staff').default
        self.assertEqual(default, False)

    def test_created_at_is_auto_now_add(self):
        user = UserModel.objects.get(id=1)
        auto_now_add = user._meta.get_field('created_at').auto_now_add
        self.assertEqual(auto_now_add, True)

    def test_updated_at_is_auto_now(self):
        user = UserModel.objects.get(id=1)
        auto_now = user._meta.get_field('updated_at').auto_now
        self.assertEqual(auto_now, True)
