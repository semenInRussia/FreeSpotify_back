from music_manger.implementations import RocknationAndSpotify
from settings.server import PORT

description = "This is app for to download music from spotify."
epilog = 'Good luck!'
help_text_for_port = f"This is port, he will open. (default: {PORT})"

music_manager_impl = RocknationAndSpotify
