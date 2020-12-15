from music_manger.implementations import RocknationAndSpotify, MockMusicManager
from settings.flask import default_port

description = "This is app for to download music from spotify."
epilog = 'Good luck!'
help_text_for_port = f"This is port, he will open. (default: {default_port})"

music_manager_impl = RocknationAndSpotify
