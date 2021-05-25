# FreeSpotify_back
You are can download top rock tracks from db rocknations.su with info of Spotify with FreeSpotify!!!!!!!!!!!!!!  

**(This is backend)**

## USE
### AS SERVER:

Linux / Mac OS
```
python . runserver
```

WINDOWS
```
python3 . runserver
```

## AS TELEGRAM BOT
```
python3 . bot
```

### RUN SHELL
Linux / Mac OS
```
python3 . shell
```

WINDOWS
```
python . shell
```
## INSTALL
Linux / Mac OS
```
git clone https://github.com/semenInRussia/FreeSpotify_back.git
pip install -r requirements.txt
```

WINDOWS
```
git clone https://github.com/semenInRussia/FreeSpotify_back.git
pip install -r requirements.txt
```

## DEPENDECIES
We are use:
* Flask
* bs4 & requests
* aiogram
* settings-master

## DEV

### EXAMPLE OF USE ENTITIES
## Album
```
>>> from entities import Album
>>> album = Album("AC DC", "Back in black")
>>> album
AC/DC - Back In Black

>>> album.name
'Back In Black'

>>> album.release_date
'1980-07-25'

>>> album.link
'http://rocknation.su/mp3/album-9'

>>> album.link_on_img
'http://rocknation.su/upload/images/albums/9.jpg'

>>> from pprint import pprint
>>> pprint(album.tracks)
[AC/DC - 1.Hells Bells,
 AC/DC - 2.Shoot to Thrill,
 AC/DC - 3.What Do You Do for Money Honey,
 AC/DC - 4.Givin the Dog a Bone,
 AC/DC - 5.Let Me Put My Love Into You,
 AC/DC - 6.Back In Black,
 AC/DC - 7.You Shook Me All Night Long,
 AC/DC - 8.Have a Drink on Me,
 AC/DC - 9.Shake a Leg,
 AC/DC - 10.Rock and Roll Ain't Noise Pollution]
 
>>> album.artist
AC/DC
```

## Artist
```
>>> from entities import Artist
artist = Artist("queen")
>>> artist
Queen
>>> artist.name
'Queen'
>>> artist.link
'http://rocknation.su/mp3/band-61'

>>> artist.link_on_img
'http://rocknation.su/upload/images/bands/61.jpg'

>>> from pprint import pprint
>>> pprint(artist.top)
[Queen - 3.Another One Bites The Dust,
 Queen - 11.Bohemian Rhapsody,
 Queen - 12.Don't Stop Me Now,
 Queen - 11.Under Pressure,
 Queen - 1.We Will Rock You,
 Queen - 2.I Want To Break Free,
 Queen - 1.Radio Ga Ga,
 Queen - 5.Crazy Little Thing Called Love,
 Queen - 2.We Are The Champions,
 Queen - 6.Somebody To Love]
 ```
 ## Track
 ```
>>> from entities import Track
>>> track = Track("Deep Purple", "Burn", "Burn")
>>> track.link
'http://rocknation.su/upload/mp3/Deep%20Purple/1974%20-%20Burn/01.%20Burn.mp3'

>>> track.album
Deep Purple - Burn

>>> track.artist
Deep Purple

>>> track.name
'Burn'

>>> track.disc_number
1
 ```

### TESTS
```
pytest
```

or

WINDOWS
```
python . tests
```
Linux / Mac OS
```
python3 . tests
```
