# Steven Universe lyrics webscrape and song generator

Scrapes all Steven Universe song lyrics from [the Steven Universe Wiki](http://steven-universe.wikia.com/wiki/Category:Songs),
then generates a *'new song'* based on frequency of words scraped.

python 3.6 required.

To run, navigate to Steven_Universe_lyrics directory, then:

$ python generate_steven_universe_lyrics.py

All original song lyrics are saved to a file in the current directory, called 'all_songs.txt'.

The newly generated song is then saved to a file in the current directory called 'chain.txt'.
