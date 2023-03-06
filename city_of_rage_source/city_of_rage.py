import pygame,sys
from pygame.locals import *
import animation, enemies, bosses



BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
RED=pygame.color.THECOLORS["red"]
GREEN=pygame.color.THECOLORS["green"]
BLUE=pygame.color.THECOLORS["blue"]
YELLOW=pygame.color.THECOLORS["yellow"]
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
CENTER_X= int(320/2)


def load_sprite_data(sprite_file):
    sprites = {'rect':[], 'axis_shift':[], 'offense_box':[], 'defense_box':[]}
    with open(sprite_file, 'r') as file:
         data=file.read()
         data=data.split(';')
         del(data[-1])
         for i in range(len(data)):
             data[i] = data[i].split(",")
             for j in range(len(data[i])):
                 data[i][j] = data[i][j].split(" ")
                 for k in range(len(data[i][j])):
                     data[i][j][k] = int(data[i][j][k])
             sprites['rect'].append(data[i][0])
             sprites['axis_shift'].append(data[i][1])
             sprites['offense_box'].append(data[i][2])
             sprites['defense_box'].append(data[i][3])
    return sprites

def load_animation_data(animation_file):
    animations = None
    with open(animation_file, 'r') as file:
         data=file.read()
         data=data.split(',')
         del(data[-1])
         for i in range(len(data)):
             data[i] = data[i].split(" ")
             if data[i][0] == "-1":
                del(data[i][0])
             else:
                data[i].append(-1)
             for j in range(len(data[i])):
                 data[i][j] = int(data[i][j])
         animations = data
    return animations
   
def title_screen(display_surface, screen):
    title = pygame.image.load('data\\title.png').convert()   
    title = pygame.transform.scale(title, (640,480))
    background = pygame.image.load('data\\City Street.gif').convert()
    font = pygame.font.SysFont('Arial', 25, bold = True)
    text = font.render("Hit any key to play", True, YELLOW)
    text_pos = [320 - int(text.get_width() / 2), 360]
    text_flash_time = 0
   
    while True:
        #loop speed limitation
        #30 frames per second is enought
        pygame.time.Clock().tick(30)

        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                  pygame.quit()
                  sys.exit()
               else:
                  sounds['done'].play()
                  screen_transition(screen, "exit")
                  display_surface.blit(background, (0, 0))
                  scaled_display_surface = pygame.transform.scale(display_surface,(640,480))
                  screen.blit(scaled_display_surface, (0,0))
                  screen_transition(screen, "intro")
                  pygame.mixer.music.set_volume(0.5)
                  pygame.mixer.music.load('data\\sounds\\BGM16.mid')
                  pygame.mixer.music.play()
                  return
               
        screen.fill(BLUE)
        screen.blit(title, (0, 0))
        text_flash_time += 1
        if text_flash_time < 10:
           screen.blit(text, text_pos)
        elif text_flash_time > 20:
           text_flash_time = 0
        pygame.display.flip()
        
def end(surface, end_type):
    surface_copy = surface.copy()
    pygame.mixer.music.stop()
    if end_type == "win":
       text = pygame.image.load('data\\win.png').convert()
       pygame.mixer.music.load('data\\sounds\\BGM02.mid')
    elif end_type == "lose":
       text  = pygame.image.load('data\\lose.png').convert()
       pygame.mixer.music.load('data\\sounds\\BGM14.mid')
    size = (int(text.get_width() * 1.3), int(text.get_height() * 1.3))
    text = pygame.transform.scale(text, size)   
    text.set_colorkey(text.get_at((0, 0)))
    text.set_alpha(1)
    text_pos = [320 - int(text.get_width() / 2), 220]
    pygame.mixer.music.play()
    for i in range(300):
        if i > 255:
           text.set_alpha(i)
        surface.blit(text, text_pos)
        pygame.display.flip()
    #timer = 0
    while True:  #timer < 100:
        #timer += 1
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                  pygame.quit()
                  sys.exit()
               else:
                  return

def screen_transition(surface, transition):
    surface_copy = surface.copy()
    fading_surface = pygame.Surface(surface.get_size()).convert()
    fading_surface.fill(BLACK)
    fading_surface.set_alpha(1)
    if transition == "exit":    
       for i in range(300):
           surface.blit(fading_surface, (0, 0))
           pygame.display.flip()
    elif transition == "intro":
       for i in range(300-1, -1, -1):
           surface.blit(surface_copy, (0, 0))
           fading_surface.set_alpha(i)
           surface.blit(fading_surface, (0, 0))
           pygame.display.flip()
           
def pause(surface):
    pygame.mixer.music.unpause()
    font = pygame.font.SysFont('Arial', 30, bold = True)
    text = font.render("- Pause -", True, WHITE)
    text_pos = [320 - int(text.get_width() / 2), 220]
    surface.blit(text, text_pos)
    pygame.display.flip()
    while True:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                  pygame.quit()
                  sys.exit()
               elif event.key == K_p:
                  pygame.mixer.music.unpause() 
                  return
    
def load_sounds():
    path = "data\\sounds\\"
    sounds = {}
    sounds['attack'] = pygame.mixer.Sound(path+'wp_alwa.wav')
    sounds['player_hit'] = pygame.mixer.Sound(path+'hit1.wav')
    sounds['enemy_hit'] = pygame.mixer.Sound(path+'001.wav')
    sounds['knocked_down'] = pygame.mixer.Sound(path+'BodyFall_001.wav')
    sounds['player_die'] = pygame.mixer.Sound(path+'argh1.wav')
    sounds['enemy_die'] = pygame.mixer.Sound(path+'Groan_007a.wav')
    sounds['special_move1'] = pygame.mixer.Sound(path+'045.wav')
    sounds['special_move2'] = pygame.mixer.Sound(path+'moveF10.wav')
    sounds['done'] = pygame.mixer.Sound(path+'done.wav')
    sounds['player_die'].set_volume(0.3)
    sounds['special_move1'].set_volume(0.3)
    sounds['special_move2'].set_volume(0.3)
    return sounds
   
def collisions(player, enemies):
    hit_connect = False
    for enemy in enemies:
        if player.attack_type != None and not player.hit_connect:
           if enemy.current_state not in ('throwed', 'death') \
           and player.current_sprite['offense_box']!= [0, 0, 0, 0] \
           and enemy.current_sprite['defense_box']!= [0, 0, 0, 0] \
           and abs(player.z_pos - enemy.z_pos) < 9:
              offense_box = player.current_sprite['offense_box']
              offense_box = [player.image_pos[0] + offense_box[0],
                             player.image_pos[1] + offense_box[1],
                             offense_box[2], offense_box[3]]
              defense_box = enemy.current_sprite['defense_box']
              defense_box = [enemy.image_pos[0] + defense_box[0],
                             enemy.image_pos[1] + defense_box[1],
                             defense_box[2], defense_box[3]]        
              if offense_box[0] < defense_box[0] + defense_box[2] \
              and offense_box[0] + offense_box[2] > defense_box[0] \
              and offense_box[1] < defense_box[1] + defense_box[3] \
              and offense_box[1] + offense_box[3] > defense_box[1]:
                  sounds['player_hit'].play()
                  if player.attack_type == "normal":
                     enemy.health -= 5
                     if enemy.axis_pos[1] != 0 or enemy.health <= 0:
                        enemy.xvel = 3
                        enemy.yvel = 9
                        enemy.current_state = 'knocked_up'
                        enemy.current_animation =  enemy.animations['knocked_up']
                        if player.current_state == 'grab':
                           if enemy == player.grabbed_enemy:
                              player.current_state = 'attack'
                              player.grabbed_enemy = None
                     elif enemy.current_state == 'grabbed':
                        enemy.current_animation =  enemy.animations['grabbed_hurt']                        
                     else:
                        enemy.current_state = 'hurt'
                        enemy.current_animation =  enemy.animations['hurt']
                  elif player.attack_type == "strong":
                     enemy.health -= 10
                     enemy.xvel = 3
                     enemy.yvel = 9
                     enemy.current_state = 'knocked_up'
                     enemy.current_animation =  enemy.animations['knocked_up']
                     if enemy == player.grabbed_enemy:
                        player.grabbed_enemy = None
                  if enemy.health <= 0:
                     sounds['enemy_die'].play()                     
                  enemy.anim_time = 0
                  enemy.animation_frame = 0
                  enemy.hit_freeze_time = 2
                  player.hit_freeze_time = 2
                  player.enemy_draw_health_bar = enemy.draw_health_bar
                  player.enemy_health_bar_timer = 80
                  player.attack_chain_time = 12
                  hit_connect = True
                  hit_spark.active = True
                  hit_spark.hit_freeze_time = 2
                  hit_spark.anim_time = 0
                  hit_spark.animation_frame = 0
                  if player.axis_pos[0] - enemy.axis_pos[0] < 0:
                     enemy.sprites =  enemy.right_side_sprites
                     hit_spark.sprites =  hit_spark.left_side_sprites
                     x_offset = offense_box[2]
                  else:
                     enemy.sprites =  enemy.left_side_sprites
                     enemy.xvel = -enemy.xvel
                     hit_spark.sprites =  hit_spark.right_side_sprites
                     x_offset = 0               
                  hit_spark.current_sprite = hit_spark.sprites[hit_spark.current_animation[hit_spark.animation_frame]]
                  hit_spark.image = hit_spark.current_sprite['image']
                  hit_spark.axis_pos[0] = offense_box[0] + x_offset
                  hit_spark.axis_pos[1] = offense_box[1] + int(offense_box[3] / 2)
        elif player.current_state == 'walk':
           if abs(player.z_pos - enemy.z_pos) < 9 \
           and abs(player.axis_pos[0] - enemy.axis_pos[0]) < 15 \
           and enemy.axis_pos[1] == 0 \
           and enemy.current_state not in ('knocked_down','death'):
              if player.sprites ==  player.left_side_sprites:
                 player.direction = 1
                 enemy.direction = -1
                 if enemy.sprites == enemy.right_side_sprites:
                    player.grab_type = "front"
                    x_offset = -37 * player.direction
                 else:
                    player.grab_type = "back"
                    x_offset = -10 * player.direction               
              elif player.sprites ==  player.right_side_sprites:
                 player.direction = -1
                 enemy.direction = 1
                 if enemy.sprites == enemy.left_side_sprites:
                    player.grab_type = "front"
                    x_offset = -37 * player.direction
                 else:
                    player.grab_type = "back"
                    x_offset = -10 * player.direction              
              player.grabbed_enemy = enemy
              player.current_state = 'grab'
              player.grab_attack_couunt = 0
              if player.grab_type == "front":
                 player.change_animation('grab1')
              elif player.grab_type == "back":   
                 player.change_animation('grab2')
              player.axis_pos[0] = enemy.axis_pos[0] + x_offset
              if player.axis_pos[0] < 20:
                 player.axis_pos[0] = 20
                 enemy.axis_pos[0] = player.axis_pos[0] - x_offset
              elif player.axis_pos[0] > 300:
                 player.axis_pos[0] = 300
                 enemy.axis_pos[0] = player.axis_pos[0] - x_offset             
              player.z_pos = enemy.z_pos + 1
              player.xvel = 0
              player.zvel = 0
              player.enemy_draw_health_bar = enemy.draw_health_bar
              player.enemy_health_bar_timer = 80
              enemy.current_state = 'grabbed'
              enemy.change_animation('grabbed')
              
        if enemy.attack_type != None and not enemy.hit_connect:
           if player.current_state not in ('throwed', 'death') \
           and enemy.current_sprite['offense_box']!= [0, 0, 0, 0] \
           and player.current_sprite['defense_box']!= [0, 0, 0, 0] \
           and abs(enemy.z_pos - player.z_pos) < 9:
              offense_box = enemy.current_sprite['offense_box']
              offense_box = [enemy.image_pos[0] + offense_box[0],
                             enemy.image_pos[1] + offense_box[1],
                             offense_box[2], offense_box[3]]
              defense_box = player.current_sprite['defense_box']
              defense_box = [player.image_pos[0] + defense_box[0],
                             player.image_pos[1] + defense_box[1],
                             defense_box[2], defense_box[3]]        
              if offense_box[0] < defense_box[0] + defense_box[2] \
              and offense_box[0] + offense_box[2] > defense_box[0] \
              and offense_box[1] < defense_box[1] + defense_box[3] \
              and offense_box[1] + offense_box[3] > defense_box[1]:
                  sounds['enemy_hit'].play()
                  if enemy.attack_type == "normal":
                     player.health -= 5
                     if player.axis_pos[1] != 0 or player.health <= 0:
                        player.xvel = 3
                        player.yvel = 9
                        player.current_state = 'knocked_up'
                        player.current_animation =  player.animations['knocked_up']
                     else:
                        player.current_state = 'hurt'
                        player.current_animation =  player.animations['hurt']
                  elif enemy.attack_type == "strong":
                     player.health -= 10
                     player.xvel = 3
                     player.yvel = 9
                     player.current_state = 'knocked_up'
                     player.current_animation =  player.animations['knocked_up']
                  if player.grabbed_enemy:
                     player.grabbed_enemy.current_state = 'stand'
                     player.grabbed_enemy.change_animation('stand')
                     player.grabbed_enemy = None
                  if player.health <= 0:
                     sounds['player_die'].play()                     
                  player.anim_time = 0
                  player.animation_frame = 0
                  player.hit_freeze_time = 2
                  player.enemy_draw_health_bar = enemy.draw_health_bar
                  player.enemy_health_bar_timer = 80
                  enemy.hit_freeze_time = 2
                  enemy.hit_connect = True
                  hit_spark.active = True
                  hit_spark.hit_freeze_time = 2
                  hit_spark.anim_time = 0
                  hit_spark.animation_frame = 0
                  if enemy.axis_pos[0] - player.axis_pos[0] < 0:
                     player.sprites =  player.right_side_sprites
                     hit_spark.sprites =  hit_spark.left_side_sprites
                     x_offset = offense_box[2]
                  else:
                     player.sprites =  player.left_side_sprites
                     player.xvel = -player.xvel
                     hit_spark.sprites =  hit_spark.right_side_sprites
                     x_offset = 0               
                  hit_spark.current_sprite = hit_spark.sprites[hit_spark.current_animation[hit_spark.animation_frame]]
                  hit_spark.image = hit_spark.current_sprite['image']
                  hit_spark.axis_pos[0] = offense_box[0] + x_offset
                  hit_spark.axis_pos[1] = offense_box[1] + int(offense_box[3] / 2)
    if hit_connect:           
       player.hit_connect = True
    
def spawn_enemies(enemies_data, opponent, groups):
    for data in enemies_data:
        enemy = data[0]
        x_pos = data[1]
        z_pos = data[2]
        enemy = enemy([x_pos, 0], z_pos, 1, opponent, groups=groups)

 
class Player():
    def __init__(self, image, sprite_file, animation_file, axis_pos, z_pos, groups=[]):
        for group in groups:
            group.append(self)
        self.groups = groups       
        self.right_side_sprites = self.get_sprites(image, sprite_file)
        self.left_side_sprites = self.get_left_side_sprites(self.right_side_sprites)
        self.sprites = self.left_side_sprites
        self.animations = self.get_animations(animation_file)
        self.axis_pos = axis_pos
        self.current_animation = self.animations['stand']
        self.animation_frame = 0
        self.max_anim_time = 2
        self.current_sprite = self.sprites[self.current_animation[self.animation_frame]]
        self.image = self.current_sprite['image']
        self.image_pos=[
        self.axis_pos[0] + self.current_sprite['axis_shift'][0],
        self.axis_pos[1] + self.current_sprite['axis_shift'][1]]
        self.anim_time = 0
        self.attack_chain = ["attack1", "attack2", "attack3", "attack4", "attack5"]
        self.attack_chain_type = ["normal", "normal", "normal", "normal", "strong"]
        self.attack_chain_length = len(self.attack_chain)
        self.attack_chain_index = 0
        self.attack_chain_time = 0
        self.attack_type = None
        self.hit_connect = False
        self.throw_sequence = None
        self.grab_type = None
        self.grabbed_enemy = None
        self.special_move_type = None
        self.dead = False
        self.enemy_draw_health_bar = None
        self.enemy_health_bar_timer = 0
        self.grab_attack_couunt = 0
        self.timer = 0
        self.xvel = 0
        self.yvel = 0
        self.zvel = 0
        self.z_pos = z_pos
        self.direction = -1
        self.hit_freeze_time = 0
        self.health = 120
        self.health_bar = self.make_health_bar()
        self.current_state = 'stand'
        self.states = {'stand':self.stand, 'walk':self.walk, 'auto_walk':self.auto_walk, 'crouch':self.crouch,
                       'jump_start':self.jump_start, 'jump':self.jump, 'fall':self.fall,
                       'attack':self.attack, 'air_attack':self.air_attack, 'grab':self.grab,
                       'switch_grab':self.switch_grab, 'special_move':self.special_move,
                       'throw':self.throw, 'special_jump':self.special_jump, 'hurt':self.hurt,
                       'knocked_up':self.knocked_up, 'knocked_down':self.knocked_down, 'death':self.death}
        self.current_state = 'auto_walk'
        self.change_animation('walk')
        self.timer = 30
        
    def get_sprites(self, image, player_sprite_file):
        sprites = []
        sprites_data = load_sprite_data(player_sprite_file)
        for i in range(len(sprites_data['rect'])):
            sprites.append({'image':image.subsurface(sprites_data['rect'][i]),
                            'axis_shift':sprites_data['axis_shift'][i],
                            'offense_box':sprites_data['offense_box'][i],
                            'defense_box':sprites_data['defense_box'][i]})
        return sprites
                            
    def get_animations(self, player_animation_file):
        animations = {}            
        animations_data = load_animation_data(player_animation_file)
        animations['stand'] = animations_data[0]
        animations['walk'] = animations_data[1]
        animations['crouch'] = animations_data[18]
        animations['jump_start'] = animations_data[2]
        animations['jump'] = animations_data[3]
        animations['fall'] = animations_data[4]
        animations['attack1'] = animations_data[9]
        animations['attack2'] = animations_data[10]
        animations['attack3'] = animations_data[11]
        animations['attack4'] = animations_data[12]
        animations['attack5'] = animations_data[13]
        animations['air_attack1'] = animations_data[7]
        animations['air_attack2'] = animations_data[5]
        animations['air_attack3'] = animations_data[8]
        animations['rear_attack'] = animations_data[26]
        animations['grab1'] = animations_data[14]
        animations['grab2'] = animations_data[15]
        animations['switch_grab_part1'] = animations_data[6]
        animations['switch_grab_part2'] = animations_data[22]
        animations['grab_attack1'] = animations_data[16]
        animations['grab_attack2'] = animations_data[17]
        animations['grab_attack3'] = animations_data[18]
        animations['grab_attack4'] = animations_data[19]
        animations['throw1'] = animations_data[19]
        animations['throw2'] = animations_data[20]
        animations['special_jump'] = animations_data[21]
        animations['special_move1'] = animations_data[23]
        animations['special_move2'] = animations_data[24]
        animations['special_move3'] = animations_data[25]
        animations['hurt'] = animations_data[27]
        animations['knocked_up'] = animations_data[28]
        animations['knocked_down'] = animations_data[29]
        animations['get_up'] = animations_data[30]
        animations['death'] = animations_data[31]
        return animations
                            
    def get_left_side_sprites(self, sprites):
        left_side_sprites=[]
        for sprite in sprites:
            image_width, image_height = sprite['image'].get_size()             
            left_side_sprite={
            'image':pygame.transform.flip(sprite['image'], True, False),    
            'axis_shift':[-(image_width + sprite['axis_shift'][0]), sprite['axis_shift'][1]],
            'offense_box':sprite['offense_box'],
            'defense_box':sprite['defense_box']}
            if sprite['offense_box'] != [0,0,0,0]:
               offense_box = sprite['offense_box']
               left_side_offense_box = [image_width - (offense_box[0] + offense_box[2]),
                                        offense_box[1], offense_box[2], offense_box[3]]
               left_side_sprite['offense_box'] = left_side_offense_box
            if sprite['defense_box'] != [0,0,0,0]:
               defense_box = sprite['defense_box']
               left_side_defense_box = [image_width - (defense_box[0] + defense_box[2]),
                                        defense_box[1], defense_box[2], defense_box[3]]
               left_side_sprite['defense_box'] = left_side_defense_box
            left_side_sprites.append(left_side_sprite)            
        return left_side_sprites
    
    def update_animation(self):
        self.anim_time += 1
        if self.anim_time  >= self.max_anim_time:
           self.anim_time = 0
           self.animation_frame += 1
           if self.current_animation[self.animation_frame] == -1:
              self.animation_frame = 0
           self.current_sprite = self.sprites[self.current_animation[self.animation_frame]]
           self.image = self.current_sprite['image']
           
    def change_animation(self, animation):
        self.current_animation = self.animations[animation]
        self.anim_time = 0
        self.animation_frame = 0
        self.current_sprite = self.sprites[self.current_animation[self.animation_frame]]
        self.image = self.current_sprite['image']
        
    def end_of_animation(self):
        return self.animation_frame == 0 and self.anim_time == 0
      
    def make_health_bar(self):
        surface1 = pygame.Surface([136, 18]).convert()
        surface1.set_colorkey(BLACK)
        surface2 = pygame.Surface([122, 8]).convert()
        surface2.fill(RED)
        rect = [0, 0, 122, 8]
        pygame.draw.rect(surface2, WHITE, rect, 1)
        surface1.blit(surface2, (14, 10))
        image = self.left_side_sprites[-1]['image'].copy()
        pygame.draw.rect(image, YELLOW, image.get_rect(), 1)
        surface3 = pygame.Surface(image.get_size()).convert()
        surface3.fill((1, 1, 1))
        surface3.blit(image, (0, 0))
        surface1.blit(surface3, (0, 3))
        font = pygame.font.SysFont('Arial', 11, bold = True)
        name = font.render("Axel", True, WHITE)
        surface1.blit(name, (22, -2))
        return surface1
                     
    def scroll_background(self):
        if scroll_ok:
           if self.axis_pos[0] > CENTER_X and self.xvel > 0:
              dx = -self.xvel  #CENTER_X - self.axis_pos[0]
              background_pos[0] += dx
              if background_pos[0] > 0:
                 background_pos[0] = 0
              elif background_pos[0] < -1216:
                 background_pos[0] = -1216
              else:
                 self.axis_pos[0] += dx
                 for enemy in enemies_group:
                     enemy.axis_pos[0] += dx
                     #if enemy.axis_pos[0] < -100:
                        #enemy.kill()
        
    def stand(self):
        global attack, special, jump
        self.update_animation()
        if left:
           self.current_state = 'walk'
           self.sprites = self.right_side_sprites
           self.change_animation('walk')
           self.xvel = -walk_speed
        elif right:
           self.current_state = 'walk'
           self.sprites = self.left_side_sprites
           self.change_animation('walk')
           self.xvel = walk_speed
        if jump:
           if attack:
              attack = False
              jump = False
              self.attack_type = "strong"
              self.current_state = 'attack'
              self.change_animation('rear_attack')
           else:    
              self.yvel = jump_speed
              if left:
                 self.xvel = -2
              elif right:
                 self.xvel = 2
              self.current_state = 'jump_start'
              self.change_animation('jump_start')
        if up:
           self.current_state = 'walk'
           self.change_animation('walk')
           self.zvel = -walk_speed
        elif down:
           self.current_state = 'walk'
           self.change_animation('walk')
           self.zvel = walk_speed
        elif attack:
           attack = False
           self.current_state = 'attack'
           if self.attack_chain_time > 0:
              self.attack_chain_time = 0
              self.attack_chain_index += 1
              if self.attack_chain_index >= self.attack_chain_length:
                 self.attack_chain_index = 0
           self.attack_type = self.attack_chain_type[self.attack_chain_index]      
           animation = self.attack_chain[self.attack_chain_index]
           self.change_animation(animation)
           sounds['attack'].play()            
        elif special:
           special = False
           if self. health > 10:
              self. health -= 10
              self.current_state = 'special_move'
              self.special_move_type = "hurricane"
              self.attack_type = "strong"
              self.change_animation('special_move1')
              sounds['special_move2'].play()
           
    def walk(self):
        global attack, special
        self.axis_pos[0] += self.xvel
        self.z_pos += self.zvel
        if self.axis_pos[0] < 20 or self.axis_pos[0] > 300:
           self.axis_pos[0] -= self.xvel        
        if self.z_pos < level_z_min or self.z_pos > level_z_max:
           self.z_pos -= self.zvel
        self.scroll_background()   
        self.update_animation()
        if not (left or right or up or down):
           self.current_state = 'stand'
           self.change_animation('stand')
           self.xvel = 0
           self.zvel = 0
        if jump:
           self.yvel = jump_speed
           if left:
              self.xvel = -2
           elif right:
              self.xvel = 2
           self.current_state = 'jump_start'
           self.change_animation('jump_start')
        elif attack:
           attack = False
           self.current_state = 'attack'
           self.attack_type = 'normal'     
           self.change_animation('attack1')
           sounds['attack'].play()
        elif special:
           special = False
           if self. health > 10:
              self. health -= 10
              self.current_state = 'special_move'
              self.xvel = 0
              self.zvel = 0
              if self.sprites ==  self.left_side_sprites:
                 self.direction = 1
              else:
                 self.direction = -1
              if (right and self.direction == 1) or (left and self.direction == -1):
                 self.special_move_type = "combo"
                 self.attack_type = "normal"
                 self.change_animation('special_move2')
              elif up or down:
                 self.xvel = 9
                 self.special_move_type = "dash"
                 self.attack_type = "strong"
                 self.change_animation('special_move3')
                 sounds['special_move2'].play()

    def auto_walk(self):
        self.axis_pos[0] += 3
        self.update_animation()
        self.timer -= 1
        if self.timer <= 0:
           self.timer = 0
           self.current_state = 'stand'
           self.change_animation('stand')           
       
    def crouch(self):
        global attack, special
        pass
           
    def jump_start(self):
        self.update_animation()
        if self.end_of_animation():
           if self.yvel > 0:
              self.current_state = 'jump'
              self.change_animation('jump')
           else:
              self.current_state = 'stand'
              self.change_animation('stand')
              self.reset_buttons()
              
    def jump(self):
        global attack
        self.axis_pos[0] += self.xvel
        self.axis_pos[1] -= self.yvel
        self.yvel -= gravity
        if self.axis_pos[0] < 20 or self.axis_pos[0] > 300:
           self.axis_pos[0] -= self.xvel
        self.scroll_background()
        self.update_animation()   
        if attack:
           attack = False
           self.attack_type = "strong"
           self.current_state = 'air_attack'
           if down:
              self.change_animation('air_attack3')
           elif self.xvel != 0:
              self.change_animation('air_attack2')
           else:
              self.change_animation('air_attack1')
           sounds['special_move1'].play()   
        if self.yvel < 0:
           self.current_state = 'fall'
           self.change_animation('fall')
           
    def fall(self):
        global attack
        self.axis_pos[0] += self.xvel
        self.axis_pos[1] -= self.yvel
        self.yvel -= gravity
        if self.axis_pos[0] < 20 or self.axis_pos[0] > 300:
           self.axis_pos[0] -= self.xvel                
        self.scroll_background()
        self.update_animation()   
        if attack:
           attack = False
           self.attack_type = "strong"
           self.current_state = 'air_attack'
           if down:
              self.change_animation('air_attack3')
           elif self.xvel != 0:
              self.change_animation('air_attack2')
           else:
              self.change_animation('air_attack1')
        if self.axis_pos[1] + self.z_pos >= self.z_pos:
           self.axis_pos[1] = 0
           global jump
           jump = False
           self.xvel = 0
           self.yvel = 0
           self.current_state = 'jump_start'
           self.change_animation('jump_start')
        
    def attack(self):
        self.update_animation()
        if self.end_of_animation():
           self.hit_connect = False
           global attack
           if attack and self.attack_chain_index < self.attack_chain_length - 1 \
           and self.attack_chain_time > 0:
              self.attack_chain_time = 0
              self.attack_chain_index += 1
              self.attack_type = self.attack_chain_type[self.attack_chain_index]
              animation = self.attack_chain[self.attack_chain_index]   
              self.change_animation(animation)
           elif attack and self.attack_chain_index == 0:
              self.attack_type = self.attack_chain_type[self.attack_chain_index] 
              animation = self.attack_chain[self.attack_chain_index]
              self.change_animation(animation)
              sounds['attack'].play()
           else:
              if self.attack_chain_time == 0:
                 self.attack_chain_index = 0
              self.attack_type = None   
              self.current_state = 'stand'
              self.change_animation('stand')
           attack = False
                      
    def air_attack(self):
        self.axis_pos[0] += self.xvel
        self.axis_pos[1] -= self.yvel
        self.yvel -= gravity
        if self.axis_pos[0] < 20 or self.axis_pos[0] > 300:
           self.axis_pos[0] -= self.xvel
        self.scroll_background()   
        self.update_animation()
        if self.end_of_animation():
           self.hit_connect = False
           self.attack_type = None           
           if self.yvel > 0:
              self.current_state = 'jump'
              self.current_animation = self.animations['jump']
           elif self.yvel < 0:
              self.current_state = 'fall'
              self.current_animation = self.animations['fall']
           self.animation_frame = len(self.current_animation) - 2
        if self.axis_pos[1] + self.z_pos >= self.z_pos:
           self.axis_pos[1] = 0
           global jump
           jump = False
           self.xvel = 0
           self.yvel = 0
           self.hit_connect = False
           self.attack_type = None
           self.current_state = 'jump_start'
           self.change_animation('jump_start')
                      
    def grab(self):
        global attack, jump, special
        self.update_animation()
        if self.end_of_animation():
           if self.grab_type == "front":
              self.change_animation('grab1')
              self.hit_connect = False
              self.attack_type = None
           if jump:
              self.current_state = 'switch_grab'
              self.change_animation('switch_grab_part1')
              self.axis_pos[0] = self.grabbed_enemy.axis_pos[0] + (-37 * self.direction)
              jump = False
           elif special:
              special = False
              if self. health > 10:
                 self. health -= 10
                 self.current_state = 'special_move'
                 self.special_move_type = "hurricane"
                 self.attack_type = "strong"
                 self.change_animation('special_move1')
                 sounds['special_move2'].play()              
        if attack and not (self.hit_connect or self.attack_type):
           if self.grab_type == "front" \
           and ((right and self.direction == 1) or (left and self.direction == -1)):
              if self.grab_attack_couunt >= 3:
                 self.grab_attack_couunt = 0
                 self.attack_type = "strong"
                 self.current_state = 'attack'
                 self.change_animation('grab_attack2')
              else:    
                 self.attack_type = "normal"
                 self.change_animation('grab_attack1')
                 self.grab_attack_couunt += 1
           elif self.grab_type == "front" \
           and ((left and self.direction == 1) or (right and self.direction == -1)):
              self.current_state = 'throw'
              self.change_animation('throw1')
              self.throw_sequence = [(-20, 0), (-20, 0), (-20, 0), (-2, -9)]
              sounds['special_move1'].play()
           elif self.grab_type == "back":
              self.current_state = 'throw'
              self.change_animation('throw2')
              self.throw_sequence = [(-23, 0), (-23, 0), (-23, 0), (10, -9), (10, -9),
                                     (10, -41), (10, -41), (29, -16), (29, -16), (36, 0)]
              self.grabbed_enemy.change_animation('throwed2')
              self.anim_time += 1
              sounds['special_move1'].play()
           else:
              self.current_state = 'attack'
              self.attack_type = "strong"
              self.change_animation('grab_attack3')
           attack = False
        elif ((left and self.direction == 1) or (right and self.direction == -1)):
           self.timer += 1
           if self.timer > 5:
              self.timer = 0
              self.current_state = 'stand'
              self.change_animation('stand')
              self.grabbed_enemy.current_state = 'stand'
              self.grabbed_enemy.change_animation('stand')
              if self.grab_type == "back":
                 self.axis_pos[0] = self.grabbed_enemy.axis_pos[0] + (16 * -self.direction)
              self.grabbed_enemy = None
        else:
           self.timer = 0
           
    def switch_grab(self):
        self.update_animation()
        if self.end_of_animation():
           if self.current_animation == self.animations['switch_grab_part2']:
              self.current_state = 'grab'
              if self.grab_type == "front":
                 self.grab_type = "back"
                 self.change_animation('grab2')
                 x_offset = -10 * self.direction
                 self.axis_pos[0] = self.grabbed_enemy.axis_pos[0] + x_offset
              elif self.grab_type == "back":
                 self.grab_type = "front"
                 self.change_animation('grab1')
                 x_offset = -37 * self.direction
                 self.axis_pos[0] = self.grabbed_enemy.axis_pos[0] + x_offset
              if self.axis_pos[0] < 20:
                 self.axis_pos[0] = 20
                 self.grabbed_enemy.axis_pos[0] = self.axis_pos[0] - x_offset
              elif self.axis_pos[0] > 300:
                 self.axis_pos[0] = 300
                 self.grabbed_enemy.axis_pos[0] = self.axis_pos[0] - x_offset  
           else:
              if self.sprites ==  self.left_side_sprites:
                 self.sprites =  self.right_side_sprites
                 self.direction = -1
                 self.grabbed_enemy.direction = 1
              else:
                 self.sprites =  self.left_side_sprites
                 self.direction = 1
                 self.grabbed_enemy.direction = -1
              self.change_animation('switch_grab_part2')
        
    def throw(self):
        self.update_animation()
        if self.end_of_animation():
           global background_shacking_object
           if self.grab_type == "front":
              self.current_state = 'stand'
              self.change_animation('stand')
           elif self.grab_type == "back":
              self.xvel = 3
              self.yvel = 5
              self.current_state = 'special_jump'
              self.change_animation('special_jump')
              self.grabbed_enemy.current_state = 'throwed'
              self.grabbed_enemy.change_animation('throwed1')
              background_shacking_object = self.grabbed_enemy
              self.grabbed_enemy = None
        if self.anim_time == 0 \
        and self.grabbed_enemy and self.grabbed_enemy.current_state == "grabbed":
           if self.animation_frame < len(self.throw_sequence):
              axis_offset = self.throw_sequence[self.animation_frame]
              self.grabbed_enemy.axis_pos[0] = self.axis_pos[0] + axis_offset[0] * self.grabbed_enemy.direction
              self.grabbed_enemy.axis_pos[1] = self.axis_pos[1] + axis_offset[1]
           else:
              throw_velocity = (4, 8)
              self.grabbed_enemy.xvel = throw_velocity[0] * self.grabbed_enemy.direction
              self.grabbed_enemy.yvel = throw_velocity[1]
              self.grabbed_enemy.axis_pos[0] += 20 * self.grabbed_enemy.direction
              self.grabbed_enemy.axis_pos[1] -= 5
              self.grabbed_enemy.current_state = 'throwed'
              self.grabbed_enemy.change_animation('throwed1')
              self.grabbed_enemy.image = pygame.transform.flip(self.grabbed_enemy.image, True, True)
              background_shacking_object = self.grabbed_enemy
              self.grabbed_enemy = None
                   
    def special_jump(self):
        self.axis_pos[0] += self.xvel * self.direction
        self.axis_pos[1] -= self.yvel
        if self.axis_pos[0] < 20 or self.axis_pos[0] > 300:
           self.axis_pos[0] -= self.xvel * self.direction
        self.scroll_background()   
        if 0 > self.yvel >= -gravity:
           self.anim_time = self.max_anim_time 
           self.update_animation()
        if self.axis_pos[1] + self.z_pos >= self.z_pos:
           if self.yvel != 0:
              self.axis_pos[1] = 0
              self.yvel = 0
              self.anim_time = self.max_anim_time 
              self.update_animation()
           self.xvel -= 1
           if self.xvel < 0:
              self.xvel = 0
              self.yvel = 0
              self.current_state = 'jump_start'
              self.anim_time = self.max_anim_time 
              self.update_animation()
        else:
           self.yvel -= gravity

    def special_move(self): 
        self.update_animation()
        if self.special_move_type == "hurricane":
           if self.anim_time == 0:
              self.hit_connect = False            
           if self.end_of_animation():
              self.hit_connect = False
              self.attack_type = None
              self.current_state = 'stand'
              self.change_animation('stand')
              self.reset_buttons()
        elif self.special_move_type == "combo":
           if self.anim_time == 0:
              self.hit_connect = False
           if self.animation_frame ==  17:
              self.attack_type = "strong"
           if self.current_animation[self.animation_frame + 1] == -1:
              self.hit_connect = False
              self.attack_type = None
              self.yvel = 9
              self.anim_time = 0
              self.animation_frame = 0           
              self.current_state = 'special_jump'
              self.current_animation = self.animations['special_jump']
        elif self.special_move_type == "dash":
           self.axis_pos[0] += self.xvel * self.direction
           if self.axis_pos[0] < 20 or self.axis_pos[0] > 300:
              self.axis_pos[0] -= self.xvel * self.direction
           self.scroll_background()   
           self.xvel -= 1
           if self.xvel < 0:
              self.xvel = 0
           if self.anim_time == 0:
              self.hit_connect = False           
           if self.end_of_animation():
              self.reset_buttons() 
              self.hit_connect = False
              self.attack_type = None              
              self.xvel = 0
              self.current_state = 'stand'
              self.change_animation('stand')
              
    def reset(self):
        for group in self.groups:
            group.append(self)
        self.sprites = self.left_side_sprites
        self.axis_pos[0] = -30
        self.axis_pos[1] = 0
        self.z_pos = 202
        self.xvel = 0
        self.yvel = 0
        self.zvel = 0
        self.dead = False
        self.health = 120
        self.enemy_health_bar_timer = 0
        self.current_state = 'auto_walk'
        self.change_animation('walk')
        self.timer = 30
        self.reset_buttons()
        
    def reset_buttons(self):
        global attack, special, jump
        attack = False
        special = False
        jump = False
        
    def hurt(self):
        self.update_animation()
        if self.end_of_animation():
           self.xvel = 0
           self.zvel = 0
           self.attack_type = None
           self.hit_connect = False
           self.current_state = 'stand'
           self.change_animation('stand')
           self.reset_buttons()
        global special
        if special:
           special = False
           if self.current_animation == self.animations['hurt']:  
              if self. health > 10:
                 self. health -= 10
                 self.current_state = 'special_move'
                 self.special_move_type = "hurricane"
                 self.attack_type = "strong"
                 self.change_animation('special_move1')
                 sounds['special_move2'].play()
                      
    def knocked_up(self):
        self.axis_pos[0] += self.xvel
        self.axis_pos[1] -= self.yvel
        self.yvel -= 1
        if self.axis_pos[0] < 20 or self.axis_pos[0] > 300:
           self.axis_pos[0] -= self.xvel
        self.scroll_background()   
        self.update_animation()
        if self.axis_pos[1] + self.z_pos >= self.z_pos:
           self.axis_pos[1] = 0
           #self.xvel = 3 
           self.yvel = 6
           self.current_state = 'knocked_down'
           self.change_animation('knocked_down')
           
    def knocked_down(self):
        self.axis_pos[0] += self.xvel
        self.axis_pos[1] -= self.yvel
        self.yvel -= 1
        if self.axis_pos[0] < 20 or self.axis_pos[0] > 300:
           self.axis_pos[0] -= self.xvel
        self.scroll_background()   
        self.update_animation()
        if self.axis_pos[1] + self.z_pos >= self.z_pos:
           self.axis_pos[1] = 0
           #self.xvel = 3
           self.yvel = 0
           if self.health <= 0:
              self.current_state = 'death'
              self.change_animation('death')
           else:  
              self.current_state = 'hurt'
              self.change_animation('get_up')
           
    def death(self):
        self.update_animation()
        if self.end_of_animation():
           self.kill()
        
    def kill(self):
        for group in self.groups:
            if self in group:
               group.remove(self)
        self.dead = True       

    def draw(self, surface):
        self.image_pos[0] = self.axis_pos[0] + self.current_sprite['axis_shift'][0]
        self.image_pos[1] = self.axis_pos[1] + self.current_sprite['axis_shift'][1] + self.z_pos
        surface.blit(self.image, self.image_pos)
        surface.blit(self.health_bar, (5, 5))
        if self.health > 0:
           pygame.draw.rect(surface, YELLOW, [20, 16, self.health, 6])
        if self.enemy_health_bar_timer > 0:
           self.enemy_health_bar_timer -= 1
           self.enemy_draw_health_bar(surface)


def main():

    pygame.init()

    #Open Pygame window
    screen = pygame.display.set_mode((640, 480),) #add RESIZABLE or FULLSCREEN
    display_surface = pygame.Surface((320, 240)).convert()
    scaled_display_surface = pygame.transform.scale(display_surface,(640,480))
    #Title
    pygame.display.set_caption("City of Rage")
    #icon
    icon = pygame.image.load('data\\axel.png')
    #icon = pygame.Surface((1, 1))
    #icon.set_alpha(0)
    pygame.display.set_icon(icon)
    #font
    font=pygame.font.SysFont('Arial', 30)
    #clock
    clock = pygame.time.Clock()

    #images
    Axel_image = pygame.image.load('data\\Genesis 32X SCD - Streets of Rage 2 - Axel.png').convert()
    hit_sparks_image = pygame.image.load('data\\hit_spark.png').convert()
    background = pygame.image.load('data\\City Street.gif').convert()
    #foreground = background.subsurface((1, 246, 1535, 240))
    background = background.subsurface((0, 0, 1536, 240))
    Axel_image.set_colorkey(Axel_image.get_at((0,0)))
    hit_sparks_image.set_colorkey(hit_sparks_image.get_at((0,0)))
    #foreground.set_colorkey(foreground.get_at((0,0)))
    #variables
    global left, right, up, down, jump, attack, special, hit_spark, level_z_min, level_z_max, background_shacking_object
    global walk_speed, jump_speed, gravity, ground_y_pos, background_pos, scroll_ok, enemies_group, sounds
    left = False
    right = False
    up = False
    down = False
    jump = False
    attack = False
    special = False
    walk_speed = 3
    jump_speed = 9
    gravity = 1
    ground_y_pos = 202
    level_z_min = 160
    level_z_max = 230
    scroll_ok = True
    objects_to_draw = []
    enemies_group = []
    sounds = load_sounds()
    player = Player(Axel_image, 'data\\Axel.spr', 'data\\Axel.anm', [-30, 0], ground_y_pos+10, groups=[objects_to_draw])
    hit_spark = animation.Animation(hit_sparks_image, 'data\\hit_spark.spr', 'data\\hit_spark.anm', [100, 100], 1/3)
    enemies.load_data()
    #enemy = enemies.Galsia([190, 0], ground_y_pos, 1, player, groups=[objects_to_draw, enemies_group])
    bosses.load_data()
    #enemy = bosses.Big_Ben([190, 0], ground_y_pos, 1, player, groups=[objects_to_draw, enemies_group])
    #background_width, background_height = background.get_size()
    background_pos = [0, 0]
    background_shacking_object = None
    background_shacke_amount = 0
    galsia = enemies.Galsia
    Big_Ben =  bosses.Big_Ben
    level_data = [{'x_pos': 0, 'scroll': True, 'enemies': ((galsia, -150, 180), (galsia, 450, 180), (galsia, 470, 200))},
                  {'x_pos': 400, 'scroll': False, 'enemies' :((galsia, -50, 180), (galsia, 380, 180), (galsia, 380, 200))},
                  {'x_pos': 1216, 'scroll': True, 'enemies' :((Big_Ben, 350, 180), (galsia, 380, 180), (galsia, -50, 200))}]
    level_data_length = len(level_data) - 1
    level_data_index = 0
    level_end = False
    x_pos = -level_data[level_data_index]['x_pos']
    title_screen(display_surface, screen)
              
    #pygame.key.set_repeat(400, 30)

    while True:
        #loop speed limitation
        #30 frames per second is enought
        pygame.time.Clock().tick(30)
        
        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            #keyboard movement commands    
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                   left = True
                   right = False
                   if player.current_state == 'walk':
                      player.sprites = player.right_side_sprites
                      player.xvel = -walk_speed
                elif event.key == K_RIGHT:
                   right = True
                   left = False                   
                   if player.current_state == 'walk':
                      player.sprites = player.left_side_sprites
                      player.xvel = walk_speed
                if event.key == K_UP:
                   up = True
                   down = False
                   if player.current_state == 'walk':
                      player.zvel = -walk_speed
                elif event.key == K_DOWN:
                   down = True
                   up = False
                   if player.current_state == 'walk':
                      player.zvel = walk_speed
                if event.key == K_h:
                   attack = True
                if event.key == K_j:
                   jump = True
                elif event.key == K_k:
                   special = True
                elif event.key == K_p:
                   pause(screen)                 
            if event.type == KEYUP:
                if event.key == K_LEFT:
                   left=False
                   if player.current_state == 'walk':
                      player.xvel = 0
                      if player.zvel == 0:
                         player.current_state = 'stand'
                         player.change_animation('stand')
                elif event.key == K_RIGHT:
                   right=False
                   if player.current_state == 'walk':
                      player.xvel = 0
                      if player.zvel == 0:
                         player.current_state = 'stand'
                         player.change_animation('stand')                      
                if event.key == K_DOWN:
                   down = False
                   if player.current_state == 'walk':
                      player.zvel = 0
                      if player.xvel == 0:
                         player.current_state = 'stand'
                         player.change_animation('stand')                      
                elif event.key == K_UP:
                   up = False
                   if player.current_state == 'walk':
                      player.zvel = 0
                      if player.xvel == 0:
                         player.current_state = 'stand'
                         player.change_animation('stand')
                         
                      
        collisions(player, enemies_group)
        
        if player.hit_freeze_time < 1:
           player.states[player.current_state]()
        else:
           player.hit_freeze_time -= 1       
        if player.attack_chain_time > 0:
           player.attack_chain_time -= 1
           if player.attack_chain_time <= 0:
              player.attack_chain_time = 0
              player.attack_chain_index = 0
              
        if not level_end:
           if background_pos[0] <= x_pos and scroll_ok:
              enemies_data = level_data[level_data_index]['enemies']
              spawn_enemies(enemies_data, player, [objects_to_draw, enemies_group])
              scroll_ok = level_data[level_data_index]['scroll']
              level_data_index += 1
              if level_data_index > level_data_length:
                 level_data_index -= 1
                 level_end = True
              x_pos = -level_data[level_data_index]['x_pos']
              #scroll_ok = False
           elif not scroll_ok:
              if len(enemies_group) == 0:
                 scroll_ok = True
        elif level_end:
           if len(enemies_group) == 0:
              end(screen, "win")
              screen_transition(screen, "exit")
              level_data_index = 0
              level_end = False
              x_pos = -level_data[level_data_index]['x_pos']
              background_pos[0] = 0
              background_pos[1] = 0
              enemies_group.clear()
              objects_to_draw.clear()
              player.reset()
              title_screen(display_surface, screen)
              
        if player.dead:
           end(screen, "lose")
           screen_transition(screen, "exit")
           level_data_index = 0
           level_end = False
           x_pos = -level_data[level_data_index]['x_pos']
           background_pos[0] = 0
           background_pos[1] = 0
           enemies_group.clear()
           objects_to_draw.clear()
           player.reset()
           title_screen(display_surface, screen)
           
        for enemy in enemies_group:
            if enemy.hit_freeze_time < 1:    
               enemy.states[enemy.current_state]()
            else:
               enemy.hit_freeze_time -= 1
               
        if background_shacking_object:
           if background_shacke_amount == 0:
              if background_shacking_object.current_state == 'knocked_down':
                 background_shacke_amount = 5
                 sounds['knocked_down'].play()
           else:
              if background_pos[1] == 0:
                 background_pos[1] = background_shacke_amount
              else:
                 background_pos[1] = 0
              background_shacke_amount -= 0.3
              if background_shacke_amount <= 0:
                 background_shacke_amount = 0
                 background_pos[1] = 0
                 background_shacking_object = None
              
        #collisions(player, enemies_group)

        objects_to_draw.sort(key = lambda obj: obj.z_pos)

        #draw everything
        display_surface.fill(BLUE)
        display_surface.blit(background, background_pos)
        #display_surface.blit(player.image, player.image_pos)
        for obj in objects_to_draw:
            obj.draw(display_surface)
        if hit_spark.active:
           if hit_spark.hit_freeze_time < 1:
              hit_spark.draw(display_surface)
              hit_spark.update()
           else:
              hit_spark.hit_freeze_time -= 1
        #display_surface.blit(foreground, background_pos)
        scaled_display_surface = pygame.transform.scale(display_surface,(640,480))
        screen.blit(scaled_display_surface, (0,0))
        pygame.display.flip()

if __name__ == "__main__":
    main()
