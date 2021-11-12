from microbit import *  # NEEDS TO BE INCLUDED IN ALL CODE WRITTEN FOR MICROBIT
import radio  # WORTH CHECKING OUT RADIO CLASS IN BBC MICRO DOCS
import utime

radio.on()  # TURNS ON USE OF ANTENNA ON MICROBIT
radio.config(length=251)
radio.config(channel=47)

# INITIALISE COMMANDS
x = 0 # roll
y = 0 # pitch
arm = 0
throttle = 0

display.off()
height = 0
s = 0
height_wanted = 40  #24 pulse in one rotation, we want 4 rotations. 96 pulses
height_error = 0

# time
d = utime.ticks_ms()

throttle_flag = 0

# function to retrieve height 
def rotary_encoder():
    global height, s 
    
    # orange = A
    a_in = pin3.read_analog()
    # green = B
    b_in = pin0.read_analog()
    
    # if signal is ON, set a or b to 1, if signal is OFF, set a or b to 0
    if a_in > 512:
        a = 1
    else:
        a = 0
        
    if b_in > 512:
        b = 1
    else:
        b = 0
    
    #print("A: ", a, " B: ", b)
    
    # Drone rising (throttle increase): B follows A
    # Drone falling (throttle decrease): A follows B
    
    # if signals not equal, pulse has occured, either up or down
    if b != a and s == 0:
        # throttle increasing
        height = height + int(a)
        # throttle decreasing 
        height = height - int(b)
        #flag high
        s = 1
    
    # condition so that same pulse isn't counted twice - both signals must go to 0 again before another pulse can be counted
    elif b == 0 and a == 0:
        s = 0
    
    #print("Height: ", height)
    
# function to retrieve the pitch and roll values
def toggle():
    global x, y
    
    pitch = pin1.read_analog()
    roll = pin2.read_analog()
   
    #print("Pitch: ", pitch, "| Roll: ", roll)
    
    	
    # convert to x and y coordinates
    # only vary the pitch and roll between -10 and 10 so drone doesn't lean too much
    if pitch < 100:
        y = 10
    elif pitch > 100 and pitch < 200:
        y = 8
    elif pitch > 200 and pitch < 300:
        y = 6
    elif pitch > 300 and pitch < 400:
        y = 4
    elif pitch > 400 and pitch < 500:
        y = 2
    elif pitch > 500 and pitch < 600:
        y = 0
    elif pitch > 600 and pitch < 700:
        y = -2
    elif pitch > 700 and pitch < 800:
        y = -4
    elif pitch > 800 and pitch < 900:
        y = -6
    elif pitch > 900 and pitch < 1000:
        y = -8
    else:
        y = -10
        
    if roll < 100:
        x = -10
    elif roll > 100 and roll <200:
        x = -8
    elif roll > 200 and roll < 300:
        x = -6
    elif roll > 300 and roll < 400:
        x = -4
    elif roll > 400 and roll < 500:
        x = -2
    elif roll > 500 and roll < 600:
        x = 0
    elif roll > 600 and roll < 700:
        x = 2
    elif roll > 700 and roll < 800:
        x = 4
    elif roll > 800 and roll < 900:
        x = 6
    elif roll > 900 and roll < 1000:
        x = 8
    else:
        x = 10
    
    print("X: ", x, " Y: ", y)

while True:
    
    # retrieve height
    rotary_encoder()
    # retrieve x and y coordinates from pitch and roll
    toggle()

	# ON
    if button_a.is_pressed():
        sleep(300)  # Without the delay, it was cycling too quickly through this 
                    # logic and turning the engines back off after turning them on
        if arm == 0:
            arm = 1
            throttle_flag = 0
            height = 0
        else:
            arm = 0
            
    
    # OFF
    if button_b.is_pressed():
        throttle_flag = 1
    
    # if the difference in ticks between d (value saved when the program is first run) and ticks that have elapsed since is greater than 50, send radio data
    # might have to change ticks_add to ticks_diff ??
    if utime.ticks_diff(utime.ticks_ms(), -d) >= 50 or utime.ticks_diff(utime.ticks_ms(), -d) < 0:
        radio.send(str(x) + "," + str(y) + "," + str(height) + "," + str(arm) + "," + str(throttle_flag))
	# reset d, so this code can execute every 50 ms
        d = utime.ticks_ms()
    
    #print(d)
    
    # sleep(50)
