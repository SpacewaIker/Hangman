import pygame
import random

pygame.init()


def key(letter, position, state='normal'):
    if state == 'normal':
        image = 'images/BlankSquareKey (Custom).png'
    elif state == 'disabled':
        image = 'images/BlankSquareKey_disabled (Custom).png'

    screen.blit(pygame.image.load(image), (position))
    screen.blit(
        KEYS_FONT.render(letter, 1, (0, 0, 0)),
        (position[0] + 18, position[1] - 7)
    )


def keyboard(disabled):
    for letter in LETTERS:
        if letter in disabled:
            state = 'disabled'
        else:
            state = 'normal'

        x = LETTERS[letter][0] + 7
        y = LETTERS[letter][1] + 7

        key(letter, (x, y), state=state)


def init_hangman():
    global current_hang, revealing_word, letters_guessed, wrong_letters
    global word_to_guess, disabled, playing, word_color, language

    current_hang = 0
    disabled.clear()
    playing = True
    word_color = (0, 0, 0)

    if language == 'en':
        sowpods = 'sowpods.txt'
    elif language == 'fr':
        sowpods = 'sowpods_fr.txt'

    word_to_guess = random.choice(open(sowpods, 'r').readlines()).lower()
    word_to_guess = word_to_guess[:-1]  # to remove \n
    revealing_word = ['_' for i in range(len(word_to_guess))]


KEYS_FONT = pygame.font.SysFont('agency fb', 35)
WORD_FONT = pygame.font.SysFont('fira code', 45)
CIRCLE = pygame.image.load('images/circle (Custom).png')
LETTERS = {
        'q': (100, 300), 'w': (160, 300), 'e': (220, 300), 'r': (280, 300),
        't': (340, 300), 'y': (400, 300), 'u': (460, 300), 'i': (520, 300),
        'o': (580, 300), 'p': (640, 300), 'a': (130, 360), 's': (190, 360),
        'd': (250, 360), 'f': (310, 360), 'g': (370, 360), 'h': (430, 360),
        'j': (490, 360), 'k': (550, 360), 'l': (610, 360), 'z': (190, 420),
        'x': (250, 420), 'c': (310, 420), 'v': (370, 420), 'b': (430, 420),
        'n': (490, 420), 'm': (550, 420)
}

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption('Hangman')
pygame.display.set_icon(pygame.image.load('images/hangman_32.png'))

hang = [pygame.image.load(f'images/hang_{i} (Very small).jpg')
        for i in range(7)]

current_hang = 0
running = True
disabled = set()
playing = False
revealing_word = []
word_color = (0, 0, 0)
language = 'en'

while running:
    pygame.time.delay(50)
    screen.fill((255, 255, 255))

    mouse_pos = pygame.mouse.get_pos()

    keyboard(disabled=disabled)

    for event in pygame.event.get():
        if not playing:
            if (mouse_pos[0] >= 600) and (mouse_pos[0] < 700):
                if (mouse_pos[1] >= 60) and (mouse_pos[1] < 115):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        init_hangman()

        if event.type == pygame.QUIT:  # Quit
            running = False

        for letter in LETTERS:         # Keyboard
            key_x = LETTERS[letter][0]
            key_y = LETTERS[letter][1]

            if (mouse_pos[0] >= key_x) and (mouse_pos[0] < (key_x + 60)):
                if (mouse_pos[1] >= key_y) and (mouse_pos[1] < (key_y + 60)):
                    if (event.type == pygame.MOUSEBUTTONDOWN) and playing and (
                            letter not in disabled):
                        disabled.add(letter)

                        if letter in word_to_guess:  # good guess
                            appearances = [
                                i for i, x in enumerate(word_to_guess)
                                if x == letter
                            ]
                            for i in appearances:
                                revealing_word[i] = letter
                                if '_' not in revealing_word:
                                    playing = False

                        else:  # bad guess
                            current_hang += 1
                            if current_hang == 6:  # lost
                                revealing_word = [i for i in word_to_guess]
                                word_color = (255, 0, 0)
                                playing = False

        if (mouse_pos[0] >= 400) and (mouse_pos[0] < (450)):  # en
            if (mouse_pos[1] >= 60) and (mouse_pos[1] < (110)):
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    language = 'en'

        if (mouse_pos[0] >= 450) and (mouse_pos[0] < (500)):  # fr
            if (mouse_pos[1] >= 60) and (mouse_pos[1] < (110)):
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    language = 'fr'

    # Circle:
    for letter in LETTERS:
        key_x = LETTERS[letter][0]
        key_y = LETTERS[letter][1]

        if (mouse_pos[0] >= key_x) and (mouse_pos[0] < (key_x + 60)):
            if (mouse_pos[1] >= key_y) and (mouse_pos[1] < (key_y + 60)):
                circle_pos = (key_x, key_y)
                screen.blit(CIRCLE, circle_pos)

    # Hang picture:
    keys = pygame.key.get_pressed()

    screen.blit(hang[current_hang], (50, 50))

    # Hang word:
    screen.blit(
        WORD_FONT.render(''.join(revealing_word), 1, word_color),
        (325, 220)
    )

    # button:
    if not playing:
        button_img = 'images/play (Custom).png'
    else:
        button_img = 'images/play_dark (Custom).png'
    screen.blit(pygame.image.load(button_img), (600, 60))

    # language:
    screen.blit(pygame.image.load('images/en_fr (Custom).png'), (400, 60))
    if language == 'en':
        screen.blit(CIRCLE, (395, 60))
    elif language == 'fr':
        screen.blit(CIRCLE, (442, 60))

    pygame.display.update()

pygame.quit()
