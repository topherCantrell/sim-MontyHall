import hardware
import time
import random
import monty_hall_art_bin as ART

class MontyHall:

    def __init__(self):        
        self.num_games = 0
        self.num_wins = 0
        self.doors = [False, False, False]
        self.car_door = None
        self.picked_door = None
        self.door_to_show = None
        self.remaining_door = None
        self.prev_rot2 = 'pick'
        self.prev_rot1 = 'pick'

    def open_door(self, nums):    
        for i in range(9):
            for d in nums:
                base = 18*d 
                if d == self.car_door:
                    base += 9
                hardware.show_image(d, ART.door_art[base + i])        
            time.sleep(0.1)    

    def draw_door(self, num, show):
        base = 18*num + self.doors[num]*9
        if show:
            base += 8
        hardware.show_image(num, ART.door_art[base])
    
    def randomize_doors_animation(self):
        data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(32):        
            for d in range(3):
                for j in range(16):
                    data[j] = random.randint(0,255)
                if i>10 and d==0:
                    self.draw_door(0, False)
                elif i>20 and d==1:
                    self.draw_door(1, False)
                elif i>30 and d==2:
                    self.draw_door(2, False)
                else:
                    hardware.show_image(d, data)
            time.sleep(.1)

    def wait_start_button(self, ignore_rotaries=False):
        # Wait for button debounce
        while hardware.get_start():
            time.sleep(0.1)
        # Wait for start button press
        count = 0
        value = False
        while True:
            count -= 1
            if count<0:
                count = 3
                value = not value
            hardware.set_start_led(value)
            time.sleep(0.1)
            self.check_side_buttons(ignore_rotaries)
            if hardware.get_start():
                return    

    def wait_last_button(self):
        # Wait for button debounce
        while hardware.get_last():
            time.sleep(0.1)
        # Wait for door button press
        count = 0
        value = False
        while True:
            count -= 1
            if count<0:
                count = 3
                value = not value
            hardware.set_last_leds(value, value)
            time.sleep(0.1)
            self.check_side_buttons()
            ret = hardware.get_last()
            if ret:
                return ret        
            
    def wait_door_button(self):
        # Wait for door button debounce
        while hardware.get_door():
            time.sleep(0.1)
        # Wait for door button press
        count = 0
        value = False
        while True:
            count -= 1
            if count<0:
                count = 3
                value = not value
            hardware.set_door_leds(value, value, value)
            time.sleep(0.1)
            self.check_side_buttons()
            ret = hardware.get_door()
            if ret:
                return ret

    def _combine_digits(self,s):
        buffer = hardware.get_blank_image()
        for i in range(2):
            c = s[i]
            ofs = -1
            if c=='.':
                if i==0:
                    ofs = 20
                else:
                    ofs = 10 
            elif c>='0' and c<='9':
                ofs = int(c)+10*i
            if ofs>=0:
                buffer = hardware.or_image(buffer, ART.digits_art[ofs])
        return buffer

    def print_number(self,num):
        # We have 3 screens with 2 digits each. The decimal point is a digit.
        s = str(num)
        while len(s)<6:
            s = ' '+s
        for i in range(3):
            im = self._combine_digits(s[2*i:2*i+2])
            hardware.show_image(i, im)

    def get_stats_num(self):
        n = 0
        if self.num_games:
            n = 100*self.num_wins/self.num_games
        return n
        

    def check_side_buttons(self, ignore_rotaries=False):        

        # Rotary selects

        cur_left, cur_right = hardware.get_selections()
        if cur_left is None:
            cur_left = self.prev_rot1
        if cur_right is None:
            cur_right = self.prev_rot2
        if cur_left != self.prev_rot1 or cur_right != self.prev_rot2:
            self.prev_rot1 = cur_left
            self.prev_rot2 = cur_right
            if not ignore_rotaries:
                raise Exception('Rotary changed')            

        if hardware.get_clear():            
            self.num_games = 0
            self.num_wins = 0
            while hardware.get_clear():
                time.sleep(0.1)

        if hardware.get_peek():
            hold = dict(hardware.last_drawn_data)
            self.draw_door(0, True)
            self.draw_door(1, True)
            self.draw_door(2, True)
            while hardware.get_peek():
                time.sleep(0.1)
            for num,image in hold.items():
                hardware.show_image(num, image)

        if hardware.get_stats():
            hold = dict(hardware.last_drawn_data)
            self.print_number(self.get_stats_num())
            while hardware.get_stats():
                time.sleep(0.1)
            for num,image in hold.items():
                hardware.show_image(num, image)
        
    def one_game(self):
        
        hardware.set_start_led(False)
        hardware.set_last_leds(False, False)
        hardware.set_door_leds(False, False, False)

        self.check_side_buttons()

        animated_play = True
        if self.prev_rot1 != 'pick' or self.prev_rot2 != 'pick':
            animated_play = False

        # Pick one win and two lose doors
        if animated_play:
            self.randomize_doors_animation()
        else:
            self.draw_door(0, False)
            self.draw_door(1, False)
            self.draw_door(2, False)
        self.doors = [False, False, False]
        self.car_door = random.randint(0,2)
        self.doors[self.car_door] = True
        
        # Wait for the user to pick a door
        if self.prev_rot1 == 'pick':
            # User picks
            self.picked_door = self.wait_door_button() - 1
        elif self.prev_rot1 == 'rand':
            # Pick a random
            self.picked_door = random.randint(0,2)
        else:
            # Given on the selector
            self.picked_door = int(self.prev_rot1) - 1
        leds = [False, False, False]
        leds[self.picked_door] = True
        hardware.set_door_leds(*leds)

        # Open a losing door and find the remaining door
        while True:
            self.door_to_show = random.randint(0,2)
            if not self.doors[self.door_to_show] and self.door_to_show != self.picked_door:
                if animated_play:
                    self.open_door([self.door_to_show])
                else:
                    self.draw_door(self.door_to_show, True)
                break
        for d in range(3):
            if d != self.door_to_show and d != self.picked_door:
                self.remaining_door = d
                break

        # Wait for the user to stay or switch
        if self.prev_rot2 == 'pick':
            # User picks
            switch = self.wait_last_button() - 1
        elif self.prev_rot2 == 'rand':
            # Pick a random
            switch = random.randint(0,1)
        elif self.prev_rot2 == 'stay':
            switch = 0
        elif self.prev_rot2 == 'switch':
            switch = 1            
        leds = [False, False]
        leds[switch] = True
        hardware.set_last_leds(*leds)

        if switch:
            [self.picked_door, self.remaining_door] = [self.remaining_door, self.picked_door]
            leds = [False, False, False]
            leds[self.picked_door] = True
            hardware.set_door_leds(*leds)

        # Open the last two doors
        if animated_play:
            self.open_door([self.picked_door, self.remaining_door]) 
        else:
            self.draw_door(self.picked_door, True)
            self.draw_door(self.remaining_door, True)

        self.num_games+=1
        if self.picked_door == self.car_door:
            self.num_wins+=1    

        # Wait for the user to press the start button
        if self.prev_rot1=='pick' or self.prev_rot2=='pick':
            self.wait_start_button()
        
    def run(self):
        while True:
            try:            
                self.one_game()
            except Exception as e:
                # Wait for the user to press the start button
                # after rotary change     
                self.num_games = 0
                self.num_wins = 0           
                hardware.show_image(0, hardware.get_blank_image())
                hardware.show_image(1, hardware.get_blank_image())
                hardware.show_image(2, hardware.get_blank_image())
                self.wait_start_button(ignore_rotaries=True)                                

monty = MontyHall()
monty.run()

