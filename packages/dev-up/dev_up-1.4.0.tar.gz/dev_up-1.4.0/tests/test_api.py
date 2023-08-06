import os
from unittest import TestCase

from dev_up import DevUpAPI, models


class TestDevUpAPI(TestCase):

    def setUp(self) -> None:
        TOKEN = os.environ['TOKEN']
        self.api = DevUpAPI(TOKEN)

    def test_make_request(self):
        result = self.api.make_request("profile.get", dict())
        self.assertIn('response', result)

    def test_profile_get(self):
        profile = self.api.profile.get()
        self.assertIsInstance(profile, models.ProfileGetResponse)

    def test_vk_get_stickers(self):
        stickers = self.api.vk.get_stickers(1)
        self.assertIsInstance(stickers, models.VkGetStickersResponse)

    def test_vk_get_apps(self):
        apps = self.api.vk.get_apps(1)
        self.assertIsInstance(apps, models.VkGetAppsResponse)

    def test_vk_get_groups(self):
        groups = self.api.vk.get_groups(1)
        self.assertIsInstance(groups, models.VkGetGroupsResponse)

    def test_utils_md5_generate(self):
        md5 = self.api.utils.md5_generate("text")
        self.assertIsInstance(md5, models.UtilsMD5GenerateResponse)

    def test_utils_get_server_time(self):
        server_time = self.api.utils.get_server_time()
        self.assertIsInstance(server_time, models.UtilsGetServerTimeResponse)

    def test_utils_get_short_link(self):
        short_link = self.api.utils.get_short_link("https://vk.com/lordralinc")
        self.assertIsInstance(short_link, models.UtilsGetShortLinkResponse)

    def test_utils_notifications_links(self):
        short_link_not = self.api.utils.notifications_links(
            code="/4c251",
            status=models.LinkStatus.OFF
        )
        self.assertIsInstance(short_link_not, models.UtilsNotificationsLinksResponse)

