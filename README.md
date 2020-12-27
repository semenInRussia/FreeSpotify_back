# FreeSpotify_back
You are can download top rock tracks from db rocknations.su with info of Spotify with FreeSpotify!!!!!!!!!!!!!!  

**(This is backend)**

USE
=====
AS SERVER:

Linux / Mac OS
```
python . runserver
```

WINDOWS
```
python3 . runserver
```


RUN SHELL
Linux / Mac OS
```
python3 . sehll
```

WINDOWS
```
python . shell
```
INSTALL
=====
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

# DEPENDECIES
We are use:
* Flask
* bs4 & requests

# DEV

## EXAMPLE OF USE ENTITIES
```
>> album = Album("AC DC", "BACK IN BLACK")
>> album
'<Back In Black>'
>> album.name
'Back In Black'
>> album.tracks[0]
'1. AC/DC - Hells Bells'
```

## TESTS
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
