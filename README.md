![Python package](https://github.com/semenInRussia/FreeSpotify_back/workflows/Python%20package/badge.svg)

# FreeSpotify_back
You are can download top rock tracks from db rocknations.su with info of Spotify with FreeSpotify!!!!!!!!!!!!!!  

**(This is backend)**

USE (as server)
=====
```
python run.py
```
INSTALL
=====
```
git clone https://github.com/semenInRussia/FreeSpotify_back.git
pip install -r requirements.txt
```
# DEPENDECIES
We are use:
* Flask
* bs4 & requests

# DEV

## USE  entity ALBUM
```
>> album = Album("AC DC", "BACK IN BLACK")
>> album
'<Back In Black>'
>> album.name
'Back In Black'
>> album.tracks[0]
'1. AC/DC - Hells Bells'
```
