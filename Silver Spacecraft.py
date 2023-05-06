import math
import random
import time

import arcade
from arcade.key import END
from arcade.sprite_list.spatial_hash import check_for_collision

class Enemy(arcade.Sprite):
    def __init__(self, w, h, s):
        super().__init__(':resources:images/space_shooter/playerShip1_green.png')
        self.width = 60
        self.height = 50
        self.center_x = random.randint(0, w)
        self.center_y = h
        self.speed = s
        self.angle = 180

    def move(self):
        self.center_y -= self.speed
   
class Bullet(arcade.Sprite):
    def __init__(self, host):
        super().__init__(':resources:images/space_shooter/laserRed01.png')
        self.speed = 10
        self.center_x = host.center_x 
        self.center_y = host.center_y 
        self.angle = host.angle

    def move(self):
        angle_rad = math.radians(self.angle)
        self.center_x -= self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)

class Spacecraft(arcade.Sprite):
    def __init__(self, w, h):
        super().__init__(':resources:images/space_shooter/playerShip2_orange.png')
        self.widht = 40
        self.height = 30
        self.center_x = w // 2
        self.center_y = 50
        self.angle = 0
        self.change_angle = 0
        self.bullet_list = []
        self.speed = 7
        self.life = 3
        self.score = 0
        self.change_x = 0 
        self.change_y = 0

    def move(self):
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

    def rotate(self):
        self.angle += self.change_angle * self.speed

    def fire(self):
        self.bullet_list.append(Bullet(self))
        arcade.play_sound(arcade.sound.Sound(':resources:sounds/laser4.wav'))

class Game(arcade.Window):
    def __init__(self):
        self.w = 800
        self.h = 650
        super().__init__(width= self.w, height= self.h, title='Silver Spacecraft')
        self.background_image = arcade.load_texture(':resources:images/backgrounds/stars.png')
        self.me = Spacecraft(self.w, self.h)
        self.enemy_list = []
        self.start_time = time.time()
        self.num_enemy = 0

    def on_draw(self):
        arcade.start_render()

        if self.me.life <= 0:
            arcade.set_background_color(arcade.color.BLACK)
            arcade.draw_text('GAME OVER', 150, self.h//2, arcade.color.GREEN, 60)

        else:
            arcade.draw_lrwh_rectangle_textured(0, 0, self.w, self.h, self.background_image)

            self.me.draw()

            for bullet in self.me.bullet_list:
                bullet.draw()
            
            for enemy in self.enemy_list:
                enemy.draw()

            for life in range(self.me.life):
                life_image = arcade.load_texture('heart.png')
                arcade.draw_lrwh_rectangle_textured(5 + life * 21, 10 , 20, 20 , life_image)
            
            arcade.draw_text(f'score: {self.me.score}', 680, 20, arcade.color.PINK, 20)

    def on_update(self, delta_time):
        self.end_time = time.time()
        time_enemy = random.randrange(2, 8 ,2)
        if self.end_time - self.start_time >= time_enemy:
            self.num_enemy += 1
            self.enemy_list.append(Enemy(self.w, self.h, 3+ self.num_enemy//10)) 
            self.start_time = time.time()
        
        self.me.rotate()
        self.me.move()

        for bullet in self.me.bullet_list:
            bullet.move()
        
        for enemy in self.enemy_list:
            enemy.move()

        for enemy in self.enemy_list:
            for bullet in self.me.bullet_list:
                if check_for_collision(enemy, bullet):
                    arcade.play_sound(arcade.sound.Sound(':resources:sounds/explosion1.wav'))
                    self.enemy_list.remove(enemy)
                    self.me.bullet_list.remove(bullet)
                    self.me.score += 1     

        for enemy in self.enemy_list:
            if enemy.center_y <= 0:
                self.enemy_list.remove(enemy)
                self.me.life -= 1
        
        for bullet in self.me.bullet_list:
            if bullet.center_y >= self.h or self.w <= bullet.center_x <= 0 or bullet.center_y <= 0:
                self.me.bullet_list.remove(bullet)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.me.change_y = 1
        elif key == arcade.key.DOWN:
            self.me.change_y = -1
        elif key == arcade.key.LEFT:
            self.me.change_x = -1
        elif key == arcade.key.RIGHT:
            self.me.change_x = +1
        elif key == arcade.key.A:
            self.me.change_angle = 1
        elif key == arcade.key.S :
            self.me.change_angle = -1
        elif key == arcade.key.SPACE:
            self.me.fire()

    def on_key_release(self, key, modifiers):
        self.me.change_angle = 0
        self.me.change_x = 0
        self.me.change_y = 0

game = Game()
arcade.run()