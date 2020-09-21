import pygame
import math
import random 

#starting pygame module
pygame.init()

#good practice if a variable is constant u should upper case them.
WIDTH, HEIGHT = 800, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game by EGOMEISTER")

#load images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

#buttons
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP)* 13)/2)
starty = 400
#character number for A is 65, B is 66 and so on
A = 65
#getting the position of the buttons
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])
    

#fonts
LETTER_FONT = pygame.font.SysFont("comicsans", 40)
WORD_FONT = pygame.font.SysFont("comicsans", 60)
TITLE_FONT = pygame.font.SysFont("comicsans", 70)

# game variables
hangman_status = 0
file = open("words.txt", "r")
f = file.readlines()
words = []
for word in f:
    words.append(word.strip())
word = random.choice(words).upper()
guessed = []


#background color
COLOR = (255, 255, 255)
BLACK = (0, 0, 0)

def draw():
     
    window.fill(COLOR)  
    #draw title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    window.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    
    #draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    window.blit(text, (400, 200))
    
    #draw buttons
    for letter in letters:
        x, y, ltr, visible= letter
        
        if visible:
            pygame.draw.circle(window, BLACK, (x, y), RADIUS, 3)
            
            #render the text
            text = LETTER_FONT.render(ltr, 1, BLACK)
            window.blit(text, (x - text.get_width()/2, y - text.get_width()/2))
        
    #blit means draw image
    window.blit(images[hangman_status], (150,100))
    
    #updates every second
    pygame.display.update()
    
def display_message(message):
    pygame.time.delay(1000)
    window.fill(COLOR)
    text = WORD_FONT.render(message, 1, BLACK)
    window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)
def main(): 
    #game fps
    FPS = 60
    #count 60 fps 
    clock = pygame.time.Clock()
    run = True

    while run:
        global hangman_status
        #This is necessary, make sure to run the fps
        clock.tick(FPS)

        #checking if there is any button press (event)(keyboard/mouse)
        for event in pygame.event.get():
            
            #if it pressed the X button
            if event.type == pygame.QUIT:
                run = False
                
            #getting the position of the mouse coordinate
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    dist = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                    if dist < RADIUS:
                        #why 3 ? because in the list, the 3rd item contains the visible variable
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            hangman_status += 1
                            
        draw()
        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        if won:
            display_message("YOU WON!")
            break
        if hangman_status == 6 :
            display_message("YOU SUCK!")
            break    
main()
pygame.quit()

