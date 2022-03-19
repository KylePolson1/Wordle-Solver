import Wordle as word

print("Welcome to Wordle Solver")

while(True) :
    print("The Best Word is - " + word.FindBestWord() )
    print('\n' + "... Input Greys")
    input1 = input()
    if(input1 == "escape") :
        break;
    if(input1 == "correct") :
        print("Congrats! Well Done")
        Working_Set = word.OnlyFiveLong();
        print("The Best Word is - " + word.FindBestWord() )
        print('\n' + "... Input Greys")
        input1 = input()

    if(input1 == "new") :
        print("Removing Word...")

        word.Working_Set.remove(word.FindBestWord())
        print(word.FindBestWord())
        print('\n' + "... Input Greys")
        input1 = input()
    

    Working_Set = set((word.UpdateGrey(input1)))
    print('\n' + "... Input Yellows Letters")
    yellow_letters = input()
    print('\n' + "... Input Yellows Indexes")
    yellow_indexes = input()

    Working_Set = set((word.UpdateYellow(yellow_letters,yellow_indexes)))

    print('\n' + "... Input Green Letters")
    green_letters = input()
    print('\n' + "... Input Green Indexes")
    green_indexes = input()

    Working_Set = set((word.UpdateGreen(green_letters,green_indexes)))
    print("Nice Work! ")





    