## Synthesizer

import pygame as pg
from audio_gen import *

# Pygame Initialization

pg.init()
pg.mixer.init()

screen = pg.display.set_mode((1280,720))
font = pg.font.SysFont("Bauhaus 93", 48)
BG_COLOR = (20,20,20)
tempo = 100
octave = 3
WAVE_TYPE = 1
mouse = pg.mouse.get_pos()
delay = False


## Keys

string_wh = "zxcvbnm,./qwertyuiop["
string_blk = "sdghjl;2346790"

# {0: <rect(13, 525, 43, 175)>,... }
white_keys_dict = {}
# 
black_keys_dict = {}

white_keys_mapping_dict = {}
black_keys_mapping_dict = {}
white_keys_mapping_dict_rev = {}
white_keys_mapping_dict_rev = {}

# {0: 'C0', 1: 'C#0', 2: 'D0', 3: 'D#0'... }
keys_notes_dict = {}
white_keys_notes_dict = {}
black_keys_notes_dict = {}

#{122: 0, 120: 1, 99: 2, 118: 3, 98: 4,... }
pg_keys_dict = {}

## Importing notes

with open("notes.txt", 'r') as n:
    main = n.readlines()
count_black = 0
count_white = 0
for elem in range(len(main)):
    if elem == len(main)-1:
        white_keys_mapping_dict[count_white] = [main[elem], 0, 0,0, 0, 0]
        white_keys_notes_dict[count_white] = main[elem]
        keys_notes_dict[elem] = main[elem]
        count_white += 1
    else:
        if "#" in main[elem]:
            black_keys_mapping_dict[count_black] = [main[elem][:-1], 0, 0 ,0, 0, 0]
            black_keys_notes_dict[count_black] = main[elem][:-1]
            count_black += 1
        else:
            white_keys_notes_dict[count_white] = main[elem][:-1]
            white_keys_mapping_dict[count_white] = [main[elem][:-1], 0, 0, 0,0, 0]
            count_white += 1
        keys_notes_dict[elem] = main[elem][:-1]
n.close()

## Key controls

controllable_keys = "zxcvbnm,./qwertyuiop[]asdfghjkl;1234567890"
controllable_keys_dict = {controllable_keys[e]: e for e in range(len(controllable_keys))}
pg_keys_dict = {pg.key.key_code(k): controllable_keys_dict[k] for k in controllable_keys_dict.keys()}
controllable_keys_dict_rev = {controllable_keys_dict[ke]: ke for ke in controllable_keys_dict.keys()}


def persistent_displays(octa=octave):
    ## Background 
    screen.fill(BG_COLOR)
    screen.blit(font.render("Hi this is a synth", True, (0,255,249)), (20, 20))
    screen.blit(font.render(wave_types[WAVE_TYPE], True, (200,0,50)), (170, 100))
    
    ##screen.blit(font.render(str(mouse), True, (200,200,255)),(400,400))
   
    ##screen.blit(font.render("Apply LPF?", True, (90,90,90)), (1000,100))   
    ## Button 1
    pg.draw.rect(screen, (30,200,35), pg.Rect(100,100,60,60))
    
    ## Button 2 
    
    i = 0
    while i < 28:
        if i <= 21:
            recter = pg.Rect(13+(i*45),525,43,175)
            white_keys_dict[i] = recter            
            white_keys_mapping_dict[i+7*octa][2]=recter
            i += 1
        else:
            recter = pg.Rect(13+(i*45),525,43,175)
            white_keys_dict[i] = recter            
            i += 1
        pg.draw.rect(screen, (250,250,250), recter)
        
    k = 0
    i = 0
    while k < 27:
        if k in [2, 6, 9, 13, 16, 20, 23]:
            black_keys_dict[k] = ""
            k += 1
        else:
            if i < 14:
                recter_2 = pg.Rect(46+(k*45),525,21,100)
                black_keys_dict[k] = recter_2
                pg.draw.rect(screen, (0,0,0), recter_2)                
                black_keys_mapping_dict[i+5*octa][2] = recter_2
                i += 1
                k += 1
            else: 
                recter_2 = pg.Rect(46+(k*45),525,21,100)
                black_keys_dict[k] = recter_2
                pg.draw.rect(screen, (0,0,0), recter_2)                
                k += 1
    
    ## Update button
    pg.display.update()
    
persistent_displays()

key_map = {}
def key_mapper_white(ew, octa=octave):
    for elem in range(ew+1):
        white_keys_mapping_dict[elem+7*octave][1] = controllable_keys[elem]
        key_map[controllable_keys[elem]] = white_keys_dict[elem]         

key_mapper_white(21)

def black_key_map(s):
    i = 0
    for elem in black_keys_dict.keys():
        if black_keys_dict[elem] == "":
            i += 0
        elif i < len(s):
            black_keys_mapping_dict[i+5*octave][1] = s[i]          
            key_map[s[i]] = black_keys_dict[elem]
            i += 1
        else:
            pass
            
string_blk = "sdghjl;2346790"
black_key_map(string_blk)


# {'C0': 16.3516, 'C#0': 17.323916733725454,... }
init_f = 16.3516
freq_dict = {}
white_count = 0
blk_count = 0
def f_append(frequency, wc, bc):
    for elem in keys_notes_dict.keys():
        if keys_notes_dict[elem] in white_keys_notes_dict.values():
            white_keys_mapping_dict[wc][3] = frequency
            wc += 1
            freq_dict[keys_notes_dict[elem]] = frequency  
            frequency = frequency * 2 ** (1/12) 
        else:
            black_keys_mapping_dict[bc][3] = frequency
            bc += 1
            freq_dict[keys_notes_dict[elem]] = frequency   
            frequency = frequency * 2 ** (1/12)
f_append(init_f, white_count, blk_count)    

def sound_update(wt):
    a = []
    for elem in white_keys_mapping_dict.keys():
        a = pyg_sound(white_keys_mapping_dict[elem][3], wt, delay)
        white_keys_mapping_dict[elem][4] = a
        
    for elem in black_keys_mapping_dict.keys():
        a = pyg_sound(black_keys_mapping_dict[elem][3], wt, delay)
        black_keys_mapping_dict[elem][4] = a

sound_update(WAVE_TYPE)    

playable = {}
def playable_update():
    for elem in white_keys_mapping_dict.keys():
        if ((type(white_keys_mapping_dict[elem][1]) == str) and
            (white_keys_mapping_dict[elem][1] in string_wh)):
            playable[white_keys_mapping_dict[elem][1]] = white_keys_mapping_dict[elem][4]
            white_keys_mapping_dict[elem][5] = pg.key.key_code(white_keys_mapping_dict[elem][1])
            
    for elem in black_keys_mapping_dict.keys():
        if ((type(black_keys_mapping_dict[elem][1]) == str) and
           (black_keys_mapping_dict[elem][1] in string_blk)):
            playable[black_keys_mapping_dict[elem][1]] = black_keys_mapping_dict[elem][4]        
            black_keys_mapping_dict[elem][5] = pg.key.key_code(black_keys_mapping_dict[elem][1])    

playable_update()
runner = 1
while runner:
    for event in pg.event.get(): 
        #mouse = pg.mouse.get_pos()
        if event.type == pg.QUIT:
            runner = False
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            runner = False
        if event.type == pg.KEYDOWN:
            pass
        if ((event.type == pg.KEYDOWN) and 
            (event.key in pg_keys_dict.keys()) and 
            (controllable_keys[pg_keys_dict[event.key]] in key_map) and
            (controllable_keys_dict_rev[pg_keys_dict[event.key]] in playable.keys())):
            playable[controllable_keys_dict_rev[pg_keys_dict[event.key]]].play()
            playable[controllable_keys_dict_rev[pg_keys_dict[event.key]]].fadeout(100*duration)
            pg.draw.rect(screen, (210,240,220), key_map[controllable_keys[pg_keys_dict[event.key]]])
            pg.display.update()
        if event.type == pg.KEYUP:
            persistent_displays()
            pg.display.update()
        if event.type == pg.MOUSEBUTTONDOWN:
            ##screen.blit(font.render(str(mouse), True, (200,200,255)),(400,400))
            if (((mouse[0] - 250/2) < 5) and ((mouse[1] - 250/2) < 5)):
                WAVE_TYPE = (WAVE_TYPE+1)%len(wave_types.keys())
                f_append(init_f, white_count, blk_count)
                sound_update(WAVE_TYPE)
                playable_update()
        if event.type == pg.MOUSEBUTTONUP:
            persistent_displays()
            pg.display.update()
            

pg.mixer.quit()
pg.quit()