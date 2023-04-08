import os
import pygame
import random
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
GRAVITY = 0.1
FLAP_STRENGTH = 1
PIPE_GAP = 10
PIPE_DISTANCE = 250
PIPE_SPEED = 2

# Load images
bird_images = [pygame.image.load("bird1.png"), pygame.image.load("bird2.png"), pygame.image.load("bird3.png")]
bird_width, bird_height = 50, 50  # Set desired dimensions for bird images
bird_images = [pygame.transform.scale(image, (bird_width, bird_height)) for image in bird_images]

pipe_image = pygame.image.load("pipe.png")
pipe_width, pipe_height = 80, 500  # Set desired dimensions for pipe image
pipe_image = pygame.transform.scale(pipe_image, (pipe_width, pipe_height))

bg_image = pygame.image.load("bg.png")
bg_width, bg_height = SCREEN_WIDTH, SCREEN_HEIGHT  # Set desired dimensions for background image
bg_image = pygame.transform.scale(bg_image, (bg_width, bg_height))

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravity = GRAVITY
        self.velocity = 0
        self.tick_count = 0
        self.image_count = 0
        self.image = bird_images[0]

    def jump(self):
        self.velocity = -FLAP_STRENGTH
        self.tick_count = 0  # Reset tick_count to 0 when bird jumps

    def move(self):
        # Calculate how many frames have passed since last move
        self.tick_count += 1

        # Calculate displacement (how many pixels the bird is moving up or down)
        displacement = self.velocity * self.tick_count + 0.5 * self.gravity * self.tick_count ** 2

        # Set terminal velocity (max speed)
        if displacement >= 16:
            displacement = 16

        # Move bird up a bit when jumping (makes jumping look smoother)
        if displacement < 0:
            displacement -= 2

        # Update y position based on displacement
        self.y += displacement

        # Update image based on velocity (flap wings when going up)
        if self.velocity < 0:
            self.image_count += 1
            if self.image_count < 5:
                self.image = bird_images[0]
            elif self.image_count < 10:
                self.image = bird_images[1]
            elif self.image_count < 15:
                self.image = bird_images[2]
            elif self.image_count < 20:
                self.image_count = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = PIPE_GAP // 2 + random.randint(-100,100)
        self.top_pipe_pos = -pipe_image.get_height() + self.height
        self.bottom_pipe_pos = SCREEN_HEIGHT - pipe_image.get_height() - PIPE_GAP + self.height
        self.passed = False  # Add passed attribute and initialize to False

    def move(self):
        self.x -= PIPE_SPEED

    def draw(self, screen):
        screen.blit(pipe_image, (self.x, self.top_pipe_pos))
        screen.blit(pygame.transform.flip(pipe_image, False, True), (self.x, self.bottom_pipe_pos))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(pipe_image)
        bottom_mask = pygame.mask.from_surface(pygame.transform.flip(pipe_image, False, True))

        top_offset = (self.x - bird.x, int(self.top_pipe_pos - round(bird.y)))
        bottom_offset = (self.x - bird.x, int(self.bottom_pipe_pos - round(bird.y)))

        top_collision_point = bird_mask.overlap(top_mask,top_offset)
        bottom_collision_point= bird_mask.overlap(bottom_mask,bottom_offset)

        if top_collision_point or bottom_collision_point:
            return True

def draw_window(screen,bird,pipes,score):
    screen.blit(bg_image,(0,0))
    for pipe in pipes:
      pipe.draw(screen)
    text=font.render("Score: "+str(score),1,(255,255,255))
    screen.blit(text,(SCREEN_WIDTH-10-text.get_width(),10))
    bird.draw(screen)
    pygame.display.update()

def main():
    global font 
    font=pygame.font.SysFont("comicsans",50)
    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock=pygame.time.Clock()
    
    # Load and play background music
    pygame.mixer.music.load("background_music.wav")
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
    
    score=0
    
    bird=Bird(SCREEN_WIDTH//2-50,(SCREEN_HEIGHT//2)-50)
    
    pipes=[Pipe(700)]
    
    run=True
    
    while run:
      clock.tick(30)
      for event in pygame.event.get():
          if event.type==pygame.QUIT:
              run=False
          if event.type==pygame.KEYDOWN:
              if event.key==pygame.K_SPACE:
                  bird.jump()
                  
      bird.move()
      
      add_pipe=False
      rem=[]
      
      for pipe in pipes:
          if pipe.collide(bird):
              pass
          
          if pipe.x+pipe_image.get_width()<0:
              rem.append(pipe)
              
          if not pipe.passed and pipe.x<bird.x:
              pipe.passed=True
              add_pipe=True
              
          pipe.move()
          
      if add_pipe:
          score+=1
          pipes.append(Pipe(SCREEN_WIDTH))
          
      for r in rem:
          pipes.remove(r)
          
      if bird.y>SCREEN_HEIGHT-50 or bird.y<0:
          pass
      
      draw_window(screen,bird,pipes,score)
      
    pygame.quit()
    quit()

main()