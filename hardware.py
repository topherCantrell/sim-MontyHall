import board
import busio
import digitalio


pin_rot_door_pick =  digitalio.DigitalInOut(board.GP2)
pin_rot_door_rand = digitalio.DigitalInOut(board.GP3)
pin_rot_door_1 = digitalio.DigitalInOut(board.GP4)
pin_rot_door_2 = digitalio.DigitalInOut(board.GP5)
pin_rot_door_3 = digitalio.DigitalInOut(board.GP6)
#
pin_rot_last_pick = digitalio.DigitalInOut(board.GP7)
pin_rot_last_rand = digitalio.DigitalInOut(board.GP8)
pin_rot_stay = digitalio.DigitalInOut(board.GP9)
pin_rot_switch = digitalio.DigitalInOut(board.GP10)
#
pin_bt_1 = digitalio.DigitalInOut(board.GP11)
pin_bt_2 = digitalio.DigitalInOut(board.GP12)
pin_bt_3 = digitalio.DigitalInOut(board.GP13)
pin_bt_stay = digitalio.DigitalInOut(board.GP14)
pin_bt_switch = digitalio.DigitalInOut(board.GP15)
pin_bt_stats = digitalio.DigitalInOut(board.GP16)
pin_bt_clear = digitalio.DigitalInOut(board.GP17)
pin_bt_start = digitalio.DigitalInOut(board.GP18)
pin_bt_peek = digitalio.DigitalInOut(board.GP19)
#
pin_led_start = digitalio.DigitalInOut(board.GP20)
pin_led_stay = digitalio.DigitalInOut(board.GP21)
pin_led_switch = digitalio.DigitalInOut(board.GP22)
pin_led_door_1 = digitalio.DigitalInOut(board.GP26)
pin_led_door_2 = digitalio.DigitalInOut(board.GP27)
pin_led_door_3 = digitalio.DigitalInOut(board.GP28)

i2c = busio.I2C(scl=board.GP1, sda=board.GP0)

for pin in [pin_rot_door_1, pin_rot_door_2, pin_rot_door_3, 
            pin_rot_door_rand, pin_rot_door_pick, 
            pin_rot_last_rand, pin_rot_last_pick, pin_rot_stay, pin_rot_switch,
            pin_bt_1, pin_bt_2, pin_bt_3, pin_bt_stay, pin_bt_switch, 
            pin_bt_stats, pin_bt_clear, pin_bt_start, pin_bt_peek]:            
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP


for pin in  [pin_led_start, pin_led_stay, pin_led_switch, pin_led_door_1, pin_led_door_2, pin_led_door_3]:
    pin.direction = digitalio.Direction.OUTPUT
    pin.value = False

last_drawn_data = {}

display_addresses = [0x70, 0x72, 0x71]

for address in display_addresses:
    i2c.try_lock()
    i2c.writeto(address, bytes([0x21]))
    i2c.writeto(address, bytes([0xEF]))
    i2c.writeto(address, bytes([0x81]))
    i2c.writeto(address, bytes([0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
    i2c.unlock()

def or_image(final, other):
    for i in range(len(final)):
        final[i] = final[i] | other[i]
    return final

def get_blank_image():
    return [0]*16

def set_start_led(value):
    pin_led_start.value = value

def get_clear():
    if not pin_bt_clear.value:
        return True
    return False

def get_start():
    if not pin_bt_start.value:
        return True
    return False

def get_peek():
    if not pin_bt_peek.value:
        return True
    return False

def get_stats():
    if not pin_bt_stats.value:
        return True
    return False

def get_last():
    if not pin_bt_stay.value:
        return 1
    if not pin_bt_switch.value:
        return 2
    return 0

def set_last_leds(a,b):
    pin_led_stay.value = a
    pin_led_switch.value = b

def get_door():
    if not pin_bt_1.value:
        return 1
    if not pin_bt_2.value:
        return 2
    if not pin_bt_3.value:  
        return 3
    return 0

def set_door_leds(a,b,c):
    pin_led_door_1.value = a
    pin_led_door_2.value = b
    pin_led_door_3.value = c

def set_last_leds(a,b):
    pin_led_stay.value = a
    pin_led_switch.value = b

def show_image(num, data):
    global last_drawn_data
    i2c.try_lock()
    i2c.writeto(display_addresses[num], bytes([0] + data))
    i2c.unlock()
    last_drawn_data[num] = data

def get_selections():
    left = None
    right = None
    if not pin_rot_door_3.value:
        left = '3'
    if not pin_rot_door_2.value:
        left = '2'
    if not pin_rot_door_1.value:
        left = '1'
    if not pin_rot_door_rand.value:
        left = 'rand'
    if not pin_rot_door_pick.value:
        left = 'pick'    
    if not pin_rot_switch.value:
        right = 'switch'
    if not pin_rot_stay.value:
        right = 'stay'
    if not pin_rot_last_rand.value:
        right = 'rand'
    if not pin_rot_last_pick.value:
        right = 'pick'    
    
    return left,right

