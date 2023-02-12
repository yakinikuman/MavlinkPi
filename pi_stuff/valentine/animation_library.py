import time
import random
import colorsys

# Some colors
COLOR_BLACK = (0,0,0)
COLOR_RED = (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_BLUE = (0,0,255)
COLOR_PINK = (255,20,147)


def randi_255():
    #random int from 0 to 255
    return random.randrange(0, 255)

def randf_1():
    # random float from 0 to 1
    return random.random()

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def rgb2hsv(r,g,b):
    return tuple(i for i in colorsys.rgb_to_hsv(r/255,g/255,b/255))

def increment_hue(current_hue,step):
    new_hue = current_hue + step
    if new_hue > 1:
        new_hue = new_hue - 1
    return new_hue

#bits: getting the 1's out of the binary representation
def bits(n):
    while n:
        b = n & (~n + 1)
        yield b
        n ^= b

def bits2(n,num_bits=64):
    return [(n >> bit) & 1 for bit in range(num_bits - 1, -1, -1)]

def is_bit_set(n,b):
    return (n & (1 << b))

class Animation:
    def __init__(self,debug=0,num_matrices=1):
        self.debug = debug
        self.brightness = 0.1 # leave low to limit current draw.  Can be 0-1
        self.num_matrices = num_matrices # total number of connected matrices
        self.num_rows = 8 # leds per matrix row.  Only 8x8 supported
        self.num_cols = 8 # leds per matrix col.  Only 8x8 supported
        self.num_leds = self.num_rows * self.num_cols # leds per matrix

        if debug:
            self.dots = [0] * self.num_leds
        else:
            import board
            import adafruit_dotstar as dotstar
            # Using a DotStar Digital LED Strip connected to hardware SPI
            total_led = self.num_leds * self.num_matrices + 1 # +1 because of adafruit_dotstar terminal LED error
            self.dots = dotstar.DotStar(board.SCK, board.MOSI, total_led, brightness=self.brightness)

    def dot_to_rc(self, i):
        # returns the coordinates (matrix,row,col) of self.dots index i
        matrix = i // self.num_leds
        remainder = i % self.num_leds
        row = remainder // self.num_rows
        col = remainder % self.num_rows
        return (matrix,row,col)

    def rc_to_dot(self,mrc):
        matrix = mrc[0]
        row = mrc[1]
        col = mrc[2]
        ix = matrix * self.num_leds + row * self.num_cols + col
        return ix

    def wait(self,t_sec):
        if self.debug:
            for n in range(self.num_matrices):
                self.debug_print(n)
                #input() #wait for key press
        time.sleep(t_sec)

    def debug_print(self,matrix_id=0):
        for i in range(self.num_leds):
            if i % 8 == 0:
                print("\n")
            if self.dots[i] == COLOR_BLACK:
                print(" ", end='')
            else:
                print("*", end='')

    def clear_all(self):
        for i in range(self.num_leds):
            self.dots[i] = COLOR_BLACK

    def falling_heart(self,num_matrices_to_use=None,heart_color=COLOR_PINK):
        print("Starting falling_heart")
        if num_matrices_to_use is None:
            num_matrices_to_use = self.num_matrices
        time_delay_sec = 0.075

        self.clear_all()

        frames = [0x0000000000000000,
                  0x0000000000000018,
                  0x000000000000183c,
                  0x0000000000183c7e,
                  0x00000000183c7eff,
                  0x000000183c7effff,
                  0x0000183c7effff66,
                  0x00183c7effff6600,
                  0x183c7effff660000,
                  0x3c7effff66000000,
                  0x7effff6600000000,
                  0xffff660000000000,
                  0xff66000000000000,
                  0x6600000000000000,
                  0x0000000000000000]
        for f in frames:
            for ix in range(self.num_leds):
                for j in range(num_matrices_to_use):
                    offset = j*self.num_leds
                    if is_bit_set(f,ix):
                        self.dots[ix+offset] = heart_color
                    else:
                        self.dots[ix+offset] = COLOR_BLACK
            self.wait(time_delay_sec)
        print("Ending falling_heart")

    def pulsing_rainbow(self,num_matrices_to_use=None):
        #this is a standalone function that indefinitely produces a rainbow effect
        # it was later the basis for the split rainbow_init / rainbow_cycle functions
        print("Starting pulsing_rainbow")
        if num_matrices_to_use is None:
            num_matrices_to_use = self.num_matrices
        time_delay_sec = 0.1
        self.clear_all()
        hue_step = 0.003

        current_hue = 0.0

        while True:
            for i in range(self.num_rows):
                current_hue = current_hue + hue_step
                if current_hue > 1:
                    current_hue = current_hue - 1
                color = hsv2rgb(current_hue,1,1)
                for m in range(num_matrices_to_use):
                    for j in range(self.num_cols):
                        mrc = (m,i,j)
                        ix = self.rc_to_dot(mrc)
                        self.dots[ix] = color
                self.wait(time_delay_sec)

    def rainbow_init(self,num_matrices_to_use=None):
        print("rainbow_init")
        if num_matrices_to_use is None:
            num_matrices_to_use = self.num_matrices
        time_delay_sec = 0.1
        self.clear_all()
        hue_step_x = randf_1() * 0.01
        hue_step_y = randf_1() * 0.005
        print("  hue_step_x = ", hue_step_x)
        print("  hue_step_y = ", hue_step_y)
        current_hue = 0.0

        for i in range(self.num_rows):
            current_hue = increment_hue(current_hue,hue_step_x)
            for m in range(num_matrices_to_use):
                for j in range(self.num_cols):
                    current_hue = increment_hue(current_hue, hue_step_y)
                    color = hsv2rgb(current_hue, 1, 1)
                    mrc = (m,i,j)
                    ix = self.rc_to_dot(mrc)
                    self.dots[ix] = color

    def rainbow_cycle(self,num_matrices_to_use=None):
        print("rainbow_cycle")
        if num_matrices_to_use is None:
            num_matrices_to_use = self.num_matrices

        hue_step = 0.03

        for i in range(self.num_rows):
            for m in range(num_matrices_to_use):
                for j in range(self.num_cols):
                    mrc = (m, i, j)
                    ix = self.rc_to_dot(mrc)
                    current_color = self.dots[ix]
                    current_hsv = rgb2hsv(current_color[0],current_color[1],current_color[2])
                    current_hue = current_hsv[0]
                    new_hue = increment_hue(current_hue,hue_step)
                    new_color = hsv2rgb(new_hue, 1, 1)
                    self.dots[ix] = new_color
        

if __name__ == '__main__':
    #print("Hello there!", end='')
    #a = Animation(1) # debug (one matrix)
    #a = Animation(0,1) # one matrix
    a = Animation(0,2) # two matrices
    #a.falling_heart()
    a.pulsing_rainbow()

    ## dot_to_rc tests
    #ix = 63
    #mrc = a.dot_to_rc(ix)
    #print(mrc)
    #new_ix = a.rc_to_dot(mrc)
    #print(new_ix)
