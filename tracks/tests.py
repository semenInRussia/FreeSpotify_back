import json

from django.test import TestCase


# Create your tests here.
class TracksTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_get_track_view(self):
        data = self.client.get('http://127.0.0.1:5555/tracks/AC-DC/back%20in%20black/back%20in%20black').content

        true_data = {"release_date": "1980-07-25", "name": "Back In Black", "album_name": "Back In Black",
                     "top_number": 1, "disc_number": 6, "artist_name": "AC/DC",
                     "link_on_rocknation": "https://rocknation.su/upload/mp3/AC-DC/1980%20-%20Back%20In%20Bl"
                                           "ack/06.%20Back%20In%20Black.mp3"}

        self.assertEqual(str(data), str(true_data))
