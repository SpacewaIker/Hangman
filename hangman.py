import random


def hangman():
    word_to_guess = random.choice(open('sowpods.txt', 'r').readlines()).lower()
    word_to_guess = word_to_guess[:-1]
    revealing_word = ['_' for i in range(len(word_to_guess))]
    letters_guessed = []
    wrong_letters = []

    print('You have to guess a word!')

    for i in range(26):
        print(' '.join(revealing_word))
        print(f"The letters you already guessed: {', '.join(wrong_letters)}")

        guess = input('Guess a letter:    ').lower()
        appearances = [i for i, x in enumerate(word_to_guess) if x == guess]

        while (guess == '') or (guess in letters_guessed):
            if guess in letters_guessed:
                print('\nYou already guessed that letter!\n')
            elif guess == '':
                print('\nYou have to enter a letter!\n')
            guess = input('Guess a letter:    ').lower()

        if guess in word_to_guess:
            print('\nGood!\n')
            for i in appearances:
                revealing_word[i] = guess
        else:
            print(f'\n{guess} is not in the word!\n')
            wrong_letters.append(guess)

        letters_guessed.append(guess)

        if '_' not in revealing_word:
            print(f'\nYou found the word! =D    {word_to_guess}\n')
            break

        if len(wrong_letters) == 6:
            print('\nYou guessed wrong too many times... ' +
                  f':/\nThe word was {word_to_guess}')
            break


if __name__ == "__main__":
    hangman()
