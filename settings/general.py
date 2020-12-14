from music_manger.implementations.RocknationAndSpotify.rocknation_and_spotify import RocknationAndSpotify
from settings.flask import default_port

description = "This is app for to download music from spotify."
epilog = 'Good luck!'
help_text_for_port = f"This is port, he will open. (default: {default_port})"

music_controller_impl = RocknationAndSpotify
