#Generate Steven Universe Lyrics:
#Web crawler that extracts all Steven Universe song lyrics from the Steven Universe wiki
#then uses MarkovChain to generate a 'new' Steven Universe song.

"""
1. from Songs home page, extracts urls for all song pages
2. extracts song lyrics from each page and saves into a single .txt file
3. generate Markov Chain and new song lyrics.
"""

import os, requests, webbrowser
from bs4 import BeautifulSoup
from markov_python.cc_markov import MarkovChain


BASE_URL = 'http://steven-universe.wikia.com'
LYRIC_DIRECTORY = 'song_lyrics'
#os.makedirs(LYRIC_DIRECTORY, exist_ok=True)
f = open('all_songs.txt', 'w')
song_string="" #I have moved this up here from below - writing to one file requires we empty string start outside the loop overall.

songs_list_url = 'http://steven-universe.wikia.com/wiki/Category:Songs'

#1 exract urls for all songs ***************************************************************

res = requests.get(songs_list_url)
res.raise_for_status()

soup = BeautifulSoup(res.text, 'html.parser')


#identify the 5 tables by <table class="article-table">
seasons = soup.find_all('table', {'class':"article-table"})

#extract each row so we can manipulate it as a Tag
count = 1
for table in seasons:
    print('Starting scrape of Steven Universe Song Lyrics for Season %d\n' % count)
    count+=1

    table_rows = []
    for row in table:
        table_rows.append(row)
    #print("rows extracted: %s" %len(table_rows)) #>>> 16. OH NO! we expect 8 rows for season 2.
    #For some reason it gives me twice as many objects as there are rows, and each of these extra objects is a NavigableString.
    #Solution:
    for row in table_rows[::2]:
        table_rows.remove(row)
        #print(type(item)) #>>> returns Tag for each item, when searching through [1::2], but returns NavigableString when searching through [::2]
    #print("correct rows extracted: %s" %len(table_rows)) # >>> 8 - success!

    #3. Get all the <td> from each row,
    #then filter out the <td> with links to songs (NOT links to episodes) and save those in correct url format:

    links = []
    for item in table_rows:
        td_resultset = item.find_all('td')
        for td in td_resultset:
            if (td_resultset.index(td)+1) % 3 == 0: #this picks out only every 3rd <td> (starting from index [2])
                a_resultset=td.find_all('a')
                for a in a_resultset:
                    #print(type(a)) #>>>Tag
                    href = a.attrs['href']
                    link = BASE_URL + href
                    links.append(link)

    print("no of song links: %s\n" %len(links))
    #checking
    #print(links)
    #for link in links:
    #    webbrowser.open(link)

#2 extract each song's lyrics, and loop to next***************************************************
    for link in links:
        print('Downloading: %s' % link)
        #download and make BeautifulSoup:
        res = requests.get(link)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        #Extract song title to use as filename. The Stronger Than You page title has html: <h1 class="page-header__title">Stronger Than You</h1>
        title = soup.find('h1', {'class':"page-header__title"})
        file_name = (title.text.replace(" ", "_") + '.txt')
        file_name = file_name.replace("?", "")    #I need to remove any '?' in the filename (such as in What's the Use of Feeling Blue?)
        fpath = os.path.join(LYRIC_DIRECTORY, file_name)

        #Extract the lyrics:
        lyrics_table = soup.find_all('table', {'class':"wikitable sortable"})

        #Extract the lyrics: attempting to get correct spacing with individual song lines.
        #print("lyrics_table: %s" % type(lyrics_table))
        #song_string = ""    #this line needs to be outside the loop below else each stanza clears the string! Same level as writing to file loop!
        for stanza in lyrics_table:
            #print("stanza: %s" % type(stanza))
            line_data = stanza.find_all('td')
            #print("line_data: %s" % type(line_data))
            #lines = [] #perhaps this should also be outside the lyrics loop

        #still not enough. i think i need to inncorporate the <br> tags...somehow add a new line for every <br>?
        #writes each <br> to new line and removes tags
            for line in line_data:
                #print("line: %s" %type(line))
                #x = str(line)
                x = str(line).replace('<br style="clear:both"/>', '\n')
                #for char in ['<td>', '</td>', '<br>', '</br>', '<b>', '</b>', '<p>', '</p>']:
                #    if char in x:
                #        x.replace(char, ' ')
                x = x.replace('<td>', ' ').replace('</td>', ' ').replace('<br>', ' ').replace('</br>', ' ').replace('<b>', ' ').replace('</b>', ' ').replace('<p>', ' ').replace('</p>', ' ')

                song_string+= x

#Write lyrics to files.

f.write(song_string)
f.close()

#3. Generate new song text*********************************************************************

mc = MarkovChain() #initialise a MarkovChain class object - REMEMBER brackets!

#read a file or string:
mc.add_file('all_songs.txt')

#generate text (list of words)
output_list = mc.generate_text(200)

#add a new line after every n words (to give appearance of lyric sheet)
n=10
i = n
while i<len(output_list):
    output_list.insert(i, '\n')
    i += (n+1)

#join list of words and newlines into a string
output_string = " ".join(output_list)

#Print to console or save to file
#print(output_string)
with open('chain.txt', 'w') as f:
    f.write(output_string)
