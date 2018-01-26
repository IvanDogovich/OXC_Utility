#Given a save file on the battlescape, generates a PNG map showing live + dead units, colour coded.
#Author:grrussel

# More comments:
#This is a python script, indeed. It needs the pyaml and PIL libraries installed, too.
#It loads a battlescape save game (change the path in the script, not elegant but meh) 
# and makes a map of unit positions - showing red (xcom), white (dead), and blue (alien) as a png image.


#Fun parsing YAML! (slow on big save files)


def load():
   f = open("/Users/grrussel/Library/Application Support/OpenXcom/boom3.sav")
   import yaml
   dd = []
   for data in yaml.load_all(f): 
      dd.append(data)

   bg = dd[1]["battleGame"]
   return bg

b = load()

w = b["width"]
h = b["height"]
l = b["length"]

from PIL import Image
im = Image.new('RGB',(w,l))

tiles = b["tiles"]

units = b["units"]
for u in units:
   pos = u["position"]
   x,y = pos[0],pos[1] 
   faction = u["faction"]
   health  = u["health"]
   col = (255,0,0) if faction == 0 else (0,0,255)
   col = (255,255,255) if health == 0 else col
   
   im.putpixel((x,y), col)

im.save("xxx.png")
