#Evelyn Gao

from string import ascii_lowercase
from collections import defaultdict
import requests
import re


#frequency calculated by running Counter on the dictionary (after sorted)       
#listed from least to most frequent                                             
frequent = "qzxjvfwbykpmughdclrontsaie"

#runs the game 100 times
for x in range(0,100):
    r = requests.get("http://upe.42069.fun/2u4kJ")
    value = r.json().get("status")
    guesses = r.json().get("remaining_guesses")
    
    #keep track of which characters have been guessed and whether they were correct or incorrect  
    correct = []
    incorrect = []

    while (value == "ALIVE"):
        #create hash table of words of ceratin length  
        wordList = defaultdict(list)
        with open("dict") as f:
            for line in f:
                line = line.strip()
                length = len(line)
                wordList[length].append(line)
        
        #count the number of underscores in phrase and start guessing word with least underscores 
        phrase = r.json().get("state")
        edit_phrase = re.sub('[^A-Za-z_ ]+','',phrase)
        blanks = edit_phrase.split(" ")
        #which chars to exclude
        exclude = []
        for char in incorrect:
            exclude.append(char)
        #create pattern to use with regex to find all possible words to fit chosen guess    
        count = 100
        for word in blanks:
            underscore_counter = 0
            for x in range(0,len(word)):
                if("_" == word[x]):
                    underscore_counter+=1
            if(underscore_counter!=0 and underscore_counter < count):
                guess = word
                count = underscore_counter
                guess_length = len(guess)
        possible = []
        if (len(exclude)>0):
            str = "[^"
            for x in exclude:
                str+=x
            str+="]"
            #print str
        else:
            str = "[a-z]"
        pattern = re.compile(guess.replace("_", str))
        if guess_length in wordList:
            for word in wordList[guess_length]:
                matcher = pattern.match(word)
                if matcher: 
                    possible.append(word)
        #counts frequency of letters appearing in possible words to make the best guess 
        freq = {}
        for word in possible:
            chars = []
            for x in range(0,len(word)):
                if word[x] not in chars:
                    if word[x] not in freq:
                        freq[word[x]]=1
                    else:
                        freq[word[x]]+=1
        #print freq
        guess = 'a'
        frequency = 0
        letter_picked = 0
        for x in ascii_lowercase:
            if x not in correct and x not in incorrect:
                if x in freq:
                    if(freq[x] > frequency):
                        guess = x
                        frequency = freq[x]
                        letter_picked = 1
        #in case no letters are found, make educated guess based on frequency of letters appearing within dict  
        if(letter_picked == 0):
            for x in mostFrequent:
                if x not in correct and x not in incorrect:
                    guess = x
        lives = r.json().get("remaining_guesses")
        #print guess
        data = {'guess': guess}
        r = requests.post("http://upe.42069.fun/2u4kJ", data = data)
        updated_lives = r.json().get("remaining_guesses")
        #update guess as correct or incorrect based on whether or not we lost a guess            
        if(updated_lives == lives-1):
            incorrect.append(guess)
        else:
            correct.append(guess)
        value = r.json().get("status")
        guesses = r.json().get("remaining_guesses")
    print r.text
    #keep building dict based on the lyrics from new game  
    file = open("dict","a")
    lyric = r.json().get("lyrics")
    edited_lyric = re.sub('[^A-Za-z_ ]+','',lyric)
    words = edited_lyric.split(" ")
    for x in words:
        file.write(x)
        file.write("\n")
    file.close()
