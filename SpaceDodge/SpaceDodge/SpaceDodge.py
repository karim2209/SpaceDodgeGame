import pygame
import time
import random


pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

# Load sound effects and background music
collision_sound = pygame.mixer.Sound("collision_sound.wav")
pygame.mixer.music.load("space-120280.mp3")
pygame.mixer.music.set_volume(0.2)  

BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)

# Add player and explosion animation images
explosion_images = [pygame.image.load(f"explosion{i}.png") for i in range(1, 6)]
spaceship_images = [pygame.image.load(f"spaceship{i}.png") for i in range(1, 4)]


def draw_explosion(player):
    for explosion in explosion_images:
        WIN.blit(explosion, (WIDTH/2 - explosion.get_width()/2, HEIGHT/2 - explosion.get_height()/2))
        pygame.display.update()
        pygame.time.delay(100)

def draw(player_img, player, elapsed_time, stars, score):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    score_text = FONT.render(f"Score: {score}", 1, "white")
    WIN.blit(time_text, (10, 10))
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    WIN.blit(player_img, (player.x, player.y))

    for star in stars:
        pygame.draw.rect(WIN, "OrangeRed", star)

    pygame.display.update()

def game_instructions():
    run = True

    while run:
        WIN.blit(BG, (0, 0))

        game_text = FONT.render("SpaceDodge", 1, "white")
        gameinstructions_text = FONT.render("Game Instruction", 1, "white")
        instruction_text = FONT.render("Try to avoid enemies to win the game!", 1, "white")
        beginnerwin_text = FONT.render("Win condition for Beginner level: Score = 20", 1, "white")
        intermediatewin_text = FONT.render("Win condition for Intermediate level: Score = 40", 1, "white")
        professionalwin_text = FONT.render("Win condition for Professional level: Score = 60", 1, "white")
        continue_text = FONT.render("Press Enter to continue...", 1, "white")

        WIN.blit(game_text, (WIDTH / 2 - game_text.get_width() / 2, 100))
        WIN.blit(gameinstructions_text, (WIDTH / 2 - gameinstructions_text.get_width() / 2, 200))
        WIN.blit(instruction_text, (WIDTH / 2 - instruction_text.get_width() / 2, 300))
        WIN.blit(beginnerwin_text, (WIDTH / 2 - beginnerwin_text.get_width() / 2, 350))
        WIN.blit(intermediatewin_text, (WIDTH / 2 - intermediatewin_text.get_width() / 2, 400))
        WIN.blit(professionalwin_text, (WIDTH / 2 - professionalwin_text.get_width() / 2, 450))
        WIN.blit(continue_text, (WIDTH / 2 - continue_text.get_width() / 2, 500))
                  

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
    
def level_select():
    run = True
    selected_level = None

    while run:
        WIN.blit(BG, (0, 0))
        level_text = FONT.render("Select a Level:", 1, "white")
        beginner_text = FONT.render("1. Beginner", 1, "white")
        intermediate_text = FONT.render("2. Intermediate", 1, "white")
        professional_text = FONT.render("3. Professional", 1, "white")
                          
        WIN.blit(level_text, (WIDTH / 2 - level_text.get_width() / 2, 200))
        WIN.blit(beginner_text, (WIDTH / 2 - beginner_text.get_width() / 2, 300))
        WIN.blit(intermediate_text, (WIDTH / 2 - intermediate_text.get_width() / 2, 350))
        WIN.blit(professional_text, (WIDTH / 2 - professional_text.get_width() / 2, 400))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                selected_level = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_level = "beginner"
                    run = False
                elif event.key == pygame.K_2:
                    selected_level = "intermediate"
                    run = False
                elif event.key == pygame.K_3:
                    selected_level = "professional"
                    run = False

    return selected_level

def restart_game():
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        restart_text = FONT.render("Would you like to restart the game?", 1, "white")
        option_y_text = FONT.render("1. Yes", 1, "white")
        option_n_text = FONT.render("2. No", 1, "white")

        WIN.blit(restart_text, (WIDTH / 2 - restart_text.get_width() / 2, 300))
        WIN.blit(option_y_text, (WIDTH / 2 - option_y_text.get_width() / 2, 350))
        WIN.blit(option_n_text, (WIDTH / 2 - option_n_text.get_width() / 2, 400))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return True
                elif event.key == pygame.K_2:
                    run = False
                    return False

def main():
    pygame.mixer.init()
    
    game_instructions()
    
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    selected_level = level_select()

    if not selected_level:
        pygame.quit()
        return


    # Adjust game parameters based on the selected level
    if selected_level == "intermediate":
        STAR_VEL = 5
        PLAYER_VEL = 7
    elif selected_level == "professional":
        STAR_VEL = 7
        PLAYER_VEL = 9
    else:
        STAR_VEL = 3
        PLAYER_VEL = 5

    player_image = random.choice(spaceship_images)
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)                         
    player = player.inflate(-10, -10)  
    player_img = pygame.transform.scale(player_image, (player.width, player.height))
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0
    score_delay = 4

    stars = []
    hit = False
    
# Initialize score and play background music
    run = True
    score = 0
    pygame.mixer.music.play(loops=-1)  

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        
        if elapsed_time > score_delay:
        
           # Update score
           score = int(elapsed_time - score_delay)  # Points for every second survived

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)                                   
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                collision_sound.play()  # Play collision sound
                break

        if hit:
            # Play explosion animation
            for explosion in explosion_images:
                WIN.blit(explosion, (player.x, player.y))
                pygame.display.update()
                pygame.time.delay(100)
                draw_explosion(player)

            # Display "You Lost!" text
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
            
            restart = restart_game()
            if restart:
                main()  # Restart the game
            else:
                run = False  # Quit the game
            break
        
        elif selected_level == "beginner" and score >= 20:
            # Display "You Win!" text
            win_text = FONT.render("You Win!", 1, "white")
            WIN.blit(win_text, (WIDTH/2 - win_text.get_width()/2, HEIGHT/2 - win_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
            
            restart = restart_game()
            if restart:
                main()  # Restart the game
            else:
                run = False  # Quit the game
            break
        
        elif selected_level == "intermediate" and score >= 40:
            # Display "You Win!" text
            win_text = FONT.render("You Win!", 1, "white")
            WIN.blit(win_text, (WIDTH/2 - win_text.get_width()/2, HEIGHT/2 - win_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
            
            restart = restart_game()
            if restart:
                main()  # Restart the game
            else:
                run = False  # Quit the game
            break

        elif selected_level == "professional" and score >= 60:
            # Display "You Win!" text
            win_text = FONT.render("You Win!", 1, "white")
            WIN.blit(win_text, (WIDTH/2 - win_text.get_width()/2, HEIGHT/2 - win_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
            
            restart = restart_game()
            if restart:
                main()  # Restart the game
            else:
                run = False  # Quit the game
            break
        
        WIN.blit(BG, (0, 0))
        WIN.blit(player_img, (player.x, player.y))
        
        draw(player_img, player, elapsed_time, stars, score)
        
             

    pygame.mixer.music.stop()  # Stop background music

    pygame.quit()


if __name__ == "__main__":
    main()
