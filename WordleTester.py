from cgi import test
import Wordle as wordle
import random

#allowed words in the wordle game and possible answers.
allowed_words =  set(open('venv\words\wordle-allowed-guesses.txt').read().split())
answers =  set(open('venv\words\wordle-answers-alphabetical.txt').read().split())

#Counts the number of guesses (FindBestWord()) to guess the solution word.
def GuessCount(solution) :
    guess_count = 0
    solved = False
    guess = wordle.FindBestWord()
    while (guess_count < 6 and not solved) :
        if(solution == guess) :
            solved = True
        else :
            TestAll(solution,guess)
            guess = wordle.FindBestWord()
            if(guess_count == 5) :
                guess_count = 6
        guess_count+=1
    
    return guess_count
# Tests if the letters of guess are in solution. If they arent't update grey letters.
def TestGrays(solution,guess):
    grays = ""
    for l in guess :
        if l not in solution :
            grays += l
            wordle.UpdateGrey(l)
# Tests if the letters of guess are in solution and if they are in the wrong spot. If they are update yellow letters.
def TestYellow(solution, guess) :
    yellows = ""
    indexes = ""
    for i in range(5) :
        if (solution[i] != guess[i]  and (guess[i] in solution)):
            yellows += (guess[i])
            indexes += (str(i))

    wordle.UpdateYellow(yellows, indexes)
#Tests if the letters of guess are in solution in the correct spot. If they are update green letters.
def TestGreen(solution,guess) :
    greens = ""
    indexes = ""
    for i in range(5) :
        if solution[i] == guess[i] :
            greens += (guess[i])
            indexes += (str(i))

    wordle.UpdateGreen(greens, indexes)

# Tests all color letters.
def TestAll(solution,guess) :
    TestGrays(solution,guess)
    TestYellow(solution,guess)
    TestGreen(solution,guess)

# Prints the number of fails and  the calculated average number of guesses for  10002 randomly selected words from the answer set.
# Takes about 25 minutes to run 10000 tests.
# One result of this function running is 4.221055788842231 guesses on average and 192 fails (1.919616%).
def AnswersTest() :

    total_count = 0
    test_count = 10002
    fails = 0
    for i in range(test_count) :
        wordle.reset()
        solution = random.choice(list(answers))
        count = GuessCount(solution)
        if(count == 7):
            fails += 1
        else:
            total_count += count
        print("Test #")
        print(i)
    
    
    print("Average Number of Guesses: ")
    print(total_count/test_count)

    print("Number of Fails: ")
    print(fails)


AnswersTest()
