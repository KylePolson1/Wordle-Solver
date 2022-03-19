from curses.ascii import isalpha
from os import remove
import english_words as ew
import PySimpleGUI as psg
import nltk 
from nltk.corpus import words

from english_words import english_words_lower_alpha_set

#allowed words in the wordle game and possible answers.
allowed_words =  set(open('venv\words\wordle-allowed-guesses.txt').read().split())
answers =  set(open('venv\words\wordle-answers-alphabetical.txt').read().split())


#Only when using a wordlist not meant for wordle. Removes all words that arent five letters long.
def OnlyFiveLong() :
    set1 = set((words.words()))
    set2 = set((english_words_lower_alpha_set))
    current_set = set1.union(set2)
    new_set = set((current_set))
    for i in current_set :
        if len(i) != 5:
            new_set.remove(i)

    current_set = set((new_set))
    for i in current_set :
        new_set.remove(i)
        new_set.add(str.lower(i))
    
    return new_set

#the allowed words does not include the answers. The union is all possible entries into the game.
# Using only the answers as the working set is better but that is cheating.
set1 = set((allowed_words))
set2 = set((answers))
Working_Set = set1.union(set2)

# Removes from possible answers any word with that character.
def __RemoveFromWorkingSet(original, character) :
    current_set = set((Working_Set))
    for i in current_set :
        if character in i:
            Working_Set.remove(i)
    return Working_Set
# Removes from possible answers any word without the character or having that character in the index (Yellow letters)
def __RequireFromWorkingSet(original,character,index) :
    current_set = set((Working_Set))
    for i in current_set :
        if character not in i :
            Working_Set.remove(i)
    for i in current_set :
        if i[index] == character :
            Working_Set.remove(i)
    return Working_Set

# Removes from possible answers any word without the character in its index.
def __RequireInIndex(original,character,index) :
    current_set = set((Working_Set))
    for i in current_set :
        if i[index] != character :
            Working_Set.remove(i)
    return Working_Set

#Removes all words with the letters in greys
def __UpdateGrey(original, greys) :
    new_set = set((original))
    for i in greys :
        new_set = __RemoveFromWorkingSet(new_set, i)
    
    Working_Set = set((new_set))
    return new_set
#Requires from working set all letters and their corresponding index.
def __UpdateYellow(original,letters,indexes) :
    new_set = set((original))
    for i in range(len(letters)) :
        new_set = __RequireFromWorkingSet(original, letters[i],int(indexes[i]))
    Working_Set = set((new_set))
    return new_set

# Requires in index all letters in letters in their corresponding index.
def __UpdateGreen(original,letters,indexes) :
    new_set = set((original))
    for i in range(len(letters)) :
        new_set = __RequireInIndex(original, letters[i],int(indexes[i]))
    Working_Set = set((new_set))
    return new_set

#Finds the frequencies of the letters in the set current_set.
def __FindLetterFrequencies(current_set) :
    total_letters = [0] * 26
    total = 0
    for i in current_set :
        total = total +5
        prev = ""
        for l in i :
            if str.isalpha(l):
                
                if ord(l)-ord('a') > -1 and l not in prev:
                    total_letters[ord(l)-ord('a')] += 1
                    total = total+1
                    prev += l
    letter_frequency = []
    for x in total_letters:
        if total > 0 :
            letter_frequency.append(x/total)
    if(len(letter_frequency) == 0) :
        letter_frequency = [0] * 26
    return letter_frequency

# Finds the word with the highest sum of frequencies of letters.
def __FindBestWord(letter_frequency, current_set) :
    best_value = 0
    if(len(current_set) == 0) :
        current_set = set1.union(set2)
    best_word = current_set.pop()
    current_set.add(best_word)
    for i in current_set :
        word_freq = 0
        prev = ""
        for l in i :
            if l not in prev:
                if (((ord(l)-ord('a')) > -1) and (str.isalpha(l)) and (ord(l) - ord('a') < 26)):
                    word_freq += letter_frequency[ord(l)-ord('a')]
                    prev += l
        if word_freq > best_value :
            best_value = word_freq
            best_word = i
    return best_word

# Finds the word that aquires the most information.
def __FindBestLetters(letter_frequency, current_set) :
    best_value = 10000
    set1 = set((allowed_words))
    set2 = set((answers))
    both = set1.union(set2)
    best_word = both.pop()
    allowed_words.add(best_word)
    #english_words_lower_alpha_set.add(best_word)
    for i in both :
        word_freq = 0
        prev = ""
        for l in i :
            if l in prev :
                word_freq += 100
            if l == "." :
                word_freq += 20000
            if l not in prev:
                if ord(l)-ord('a') > -1 and str.isalpha(l):
                    if letter_frequency[ord(l)-ord('a')] != .1:
                        #closest to .5 in order to try to remove half the set of possible answers.
                        word_freq += abs(.5-letter_frequency[ord(l)-ord('a')])
                    # Do not want to use letters that are already guessed.
                    if letter_frequency[ord(l)-ord('a')] > .095:
                        word_freq += 1000
                    #Do not want to use letters already guessed.
                    if letter_frequency[ord(l)-ord('a')] < .000001:
                        word_freq += 1000
                    prev += l
            
        # We want the smallest difference from .5
        if word_freq < best_value :
            best_value = word_freq
            best_word = i
            if(word_freq <= 1/len(Working_Set)) :
                best_word = __FindBestWord(__FindLetterFrequencies(Working_Set), Working_Set)
            
    return best_word





def WorkingSet() :
    return Working_Set

# If length > 3 Get more information if it is less than 3 guess words.
def FindBestWord() :
    #print("Possible Answers Remaining: ")
    #print(len(Working_Set))
    if len(Working_Set) > 3 :
        return __FindBestLetters(__FindLetterFrequencies(Working_Set), Working_Set)
    return __FindBestWord(__FindLetterFrequencies(Working_Set), Working_Set)

# Updates possible answers by inputting grey letters
def UpdateGrey(greys) :
    return __UpdateGrey(Working_Set,greys)

# Updates possible answers by inputting yellow letters
def UpdateYellow(letters, indexes) :
    return __UpdateYellow(Working_Set,letters,indexes)

# Updates possible answers by inputting green letters
def UpdateGreen(letters, indexes):
    return __UpdateGreen(Working_Set,letters,indexes)

# Resets possible answers to do another word.
def reset() :
    global Working_Set
    Working_Set = set1.union(set2)