#### This link contains built in sprite images for arcade https://api.arcade.academy/en/latest/resources.html or kenny.nl assets ###
import arcade
import random
import os
import math

##Declare Constants##
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Dzejna's Balkan Cafe"
IMAGE_ROTATION = 90
CUSTOMER_COUNT = 4

#path to png files
PATH = r"C:\Users\13173\ProgrammingProjects\DzejnaGame\Assets"

SPRITE_SCALING_DZEJNA = 0.4
SPRITE_SCALING_CUSTOMERS = 0.7
SPRITE_SCALING_FURNATURE = 1.5
#Add more scalers as more sprites added

class Customer(arcade.Sprite):
    def __init__(self):
        super().__init__(os.path.join(PATH, "robot.png"), SPRITE_SCALING_CUSTOMERS)

        self._customer_order = []
    
#creating a list for customer's order
    @property
    def customer_order(self):
        return self._customer_order
    
    @customer_order.setter
    def customer_order(self, customer_order):
        self.customer_order = customer_order

class Player(arcade.Sprite):
    """
    Sprite that turns and moves
    """
    def __init__(self):
        super().__init__(os.path.join(PATH, "avatar.png"), SPRITE_SCALING_DZEJNA)
# Destination point is where we are going
        self._destination_point = None

        # Max speed
        self.speed = 5

        # Max speed we can rotate
        self.rot_speed = 5

    @property
    def destination_point(self):
        return self._destination_point

    @destination_point.setter
    def destination_point(self, destination_point):
        self._destination_point = destination_point

    def on_update(self, delta_time: float = 1 / 60):
        """ Update the player """

        # If we have no destination, don't go anywhere.
        if not self._destination_point:
            self.change_x = 0
            self.change_y = 0
            return

        # Position the start at our current location
        start_x = self.center_x
        start_y = self.center_y

        # Get the destination location
        dest_x = self._destination_point[0]
        dest_y = self._destination_point[1]

        # Do math to calculate how to get the sprite to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the player will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        target_angle_radians = math.atan2(y_diff, x_diff)
        if target_angle_radians < 0:
            target_angle_radians += 2 * math.pi

        # What angle are we at now in radians?
        actual_angle_radians = math.radians(self.angle - IMAGE_ROTATION)

        # How fast can we rotate?
        rot_speed_radians = math.radians(self.rot_speed)

        # What is the difference between what we want, and where we are?
        angle_diff_radians = target_angle_radians - actual_angle_radians

        # Figure out if we rotate clockwise or counter-clockwise
        if abs(angle_diff_radians) <= rot_speed_radians:
            # Close enough, let's set our angle to the target
            actual_angle_radians = target_angle_radians
            clockwise = None
        elif angle_diff_radians > 0 and abs(angle_diff_radians) < math.pi:
            clockwise = False
        elif angle_diff_radians > 0 and abs(angle_diff_radians) >= math.pi:
            clockwise = True
        elif angle_diff_radians < 0 and abs(angle_diff_radians) < math.pi:
            clockwise = True
        else:
            clockwise = False

        # Rotate the proper direction if needed
        if actual_angle_radians != target_angle_radians and clockwise:
            actual_angle_radians -= rot_speed_radians
        elif actual_angle_radians != target_angle_radians:
            actual_angle_radians += rot_speed_radians

        # Keep in a range of 0 to 2pi
        if actual_angle_radians > 2 * math.pi:
            actual_angle_radians -= 2 * math.pi
        elif actual_angle_radians < 0:
            actual_angle_radians += 2 * math.pi

        # Convert back to degrees
        self.angle = math.degrees(actual_angle_radians) + IMAGE_ROTATION

        # Are we close to the correct angle? If so, move forward.
        if abs(angle_diff_radians) < math.pi / 4:
            self.change_x = math.cos(actual_angle_radians) * self.speed
            self.change_y = math.sin(actual_angle_radians) * self.speed

        # Fine-tune our change_x/change_y if we are really close to destination
        # point and just need to set to that location.
        traveling = False
        if abs(self.center_x - dest_x) < abs(self.change_x):
            self.center_x = dest_x
        else:
            self.center_x += self.change_x
            traveling = True

        if abs(self.center_y - dest_y) < abs(self.change_y):
            self.center_y = dest_y
        else:
            self.center_y += self.change_y
            traveling = True

        # If we have arrived, then cancel our destination point
        if not traveling:
            self._destination_point = None

class DzejnasCafe(arcade.Window):
    def __init__(self):
        #calls parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        ##Variables that hold sprites
        #Stores player sprite
        self.dzejna_list = None 
        self.customer_list = None
        self.furnature_list = None

        #Holds simple physics engine
        self.physics_engine_walls = None
       
        ##Setup Dzejna Character information
        #Moveable player sprite
        self.dzejna_sprite = None
        #setup robot sprite
        self.robot_sprite = None
        #setup table sprite
        self.table_sprite = None
        #setup counter sprite
        self.counter_sprite = None
        #Stores money from customers to dzejna
        self.dzejna_wallet = 0 

        ##Sets store background color
        arcade.set_background_color(arcade.color.EUCALYPTUS)

    def setup(self):
        #Sets up the game and initialize variables

        #Creates instance of list using spritelist
        self.dzejna_list = arcade.SpriteList()
        self.customer_list = arcade.SpriteList()
        self.furnature_list = arcade.SpriteList()

        #Sets wallet == 0  
        self.dzejna_wallet = 0

        #Setup player
        #sets path to avatar.png
        self.dzejna_sprite = arcade.Sprite(os.path.join(PATH, "avatar.png"), SPRITE_SCALING_DZEJNA)
        self.dzejna_sprite = Player()
        self.dzejna_sprite.center_x = 500
        self.dzejna_sprite.center_y = 500
        self.dzejna_list.append(self.dzejna_sprite) 

        #Setup Customer
        #sets path to robot.png
        for i in range (CUSTOMER_COUNT):
            self.robot_sprite = arcade.Sprite(os.path.join(PATH, "robot.png"), SPRITE_SCALING_CUSTOMERS)
            self.robot_sprite.center_x = random.randrange(SCREEN_WIDTH - 15)
            self.robot_sprite.center_y = random.randrange(100, SCREEN_HEIGHT - 50)
            #self.robot_sprite = Customer()
            self.customer_list.append(self.robot_sprite)


        #Setup Table and path to table
        self.table_sprite = arcade.Sprite(os.path.join(PATH, "tablenchairs.png"), SPRITE_SCALING_FURNATURE)
        self.table_sprite.center_x = 400
        self.table_sprite.center_y = 200
        self.furnature_list.append(self.table_sprite) 

        self.table_sprite = arcade.Sprite(os.path.join(PATH, "tablenchairs.png"), SPRITE_SCALING_FURNATURE)
        self.table_sprite.center_x = 800
        self.table_sprite.center_y = 200
        self.furnature_list.append(self.table_sprite) 

        self.table_sprite = arcade.Sprite(os.path.join(PATH, "tablenchairs.png"), SPRITE_SCALING_FURNATURE)
        self.table_sprite.center_x = 1200
        self.table_sprite.center_y = 200
        self.furnature_list.append(self.table_sprite) 

        self.table_sprite = arcade.Sprite(os.path.join(PATH, "tablenchairs.png"), SPRITE_SCALING_FURNATURE)
        self.table_sprite.center_x = 1200
        self.table_sprite.center_y = 400
        self.furnature_list.append(self.table_sprite) 

        ##Setup counter and path to counter
        self.counter_sprite = arcade.Sprite(os.path.join(PATH, "counter.png"), SPRITE_SCALING_FURNATURE / 4)
        self.counter_sprite.center_x = 600
        self.counter_sprite.center_y = 700
        self.furnature_list.append(self.counter_sprite) 
        self.counter_sprite = arcade.Sprite(os.path.join(PATH, "counter.png"), SPRITE_SCALING_FURNATURE / 4)
        self.counter_sprite.center_x = 900
        self.counter_sprite.center_y = 700
        self.furnature_list.append(self.counter_sprite) 


        ###Setups physics engine###
        ##ID's player and a list of sprites the player cant pass through
        self.physics_engine_walls = arcade.PhysicsEngineSimple(self.dzejna_sprite, self.furnature_list)


    def on_draw(self):
        #Method to draw sprites on program

        ##Starts rendering game
        arcade.start_render()

        self.clear()

        #Draw Dzejna Sprite
        self.dzejna_list.draw()

        ##Draw furnature
        self.furnature_list.draw()

        #Draw customers
        self.customer_list.draw()

        #Draw the money count
        output = f'Profit: {self.dzejna_wallet}'
        #draws rectangle at 10,20 with width and heigh of 20px, color baby blue
        arcade.draw_rectangle_filled(45, 
                                     30,
                                     75.0,
                                     40.0, 
                                     arcade.color.BABY_BLUE)
        #draws text of output at 10,20, color white, font size 14
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    
    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.dzejna_sprite.destination_point = x, y
            ##Left mouse button press to move dzejna around screen

        if button == arcade.MOUSE_BUTTON_RIGHT:
            clicked = arcade.get_sprites_at_point((x, y), self.furnature_list)
            if clicked in self.furnature_list:
                self.dzejna_wallet += 50


    def on_update(self, delta_time):
        self.dzejna_list.on_update(delta_time)
        self.physics_engine_walls.update()
        self.furnature_list.update()
        self.customer_list.update()


def main():
    ##Main Method##
    game = DzejnasCafe()
    game.center_window
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
