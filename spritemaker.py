# INSTRUCTIONS:
# In your terminal window, type "spritemaker.py" followed by the image you want to convert,
# followed by a list of colors to use. You can type the colors in any case.
# The image's colors are sorted from darkest to lightest and matched to your list of colors, in order.
#
# The script will then create a txt file with the name of the image.
# If too few colors are used, they will be substituted with black.
# If too many are used, the extra colors will be discarded.
#
# EXAMPLE for Windows:
# python spritemaker.py image.png black red darkblue blue white


import sys
from PIL import Image
from collections import defaultdict

LIST_OF_COLORS = (
    "Black",
    "Gray",
    "White",
    "Blue",
    "Darkblue",
    "Red",
    "Darkred",
    "Green",
    "Darkgreen",
    "Brown",
    "Darkbrown",
    "Yellow"
)


def convimg(name, colorlist):
    
    print(f"===Processing {name}")
    colorArray = []
    
    for clr in colorlist: # Creates an array of colors to use
        clr = clr.title()
        if not clr in LIST_OF_COLORS:
            print(f"{clr} is not a useable color.")
            sys.exit()
        if clr[:4] == "Dark":
            clr = clr[:4] + clr[4].upper() + clr[5:]
        clr = f"TS_16b_{clr}"
        if not clr in colorArray:
            colorArray.append(clr)
        
    img = Image.open(name)
    
    w, h = img.size
    
    img = img.convert('RGB')
    pixels = img.getdata()
    colors = []
    
    for pxl in pixels: # Makes a list of colors in the provided image file.
        if not pxl in colors:
            colors.append(pxl)
    
    while len(colorArray) < len(colors): # Adds black to the list of colors, if user provided too few colors.
        colorArray.append("TS_16b_Black")
        print("Too few colors provided. Adding black to the list of colors.")
    
    print("Colors Used: " + str("colorArray"))
    
    colors = sorted(colors, key=lambda c: c[0] + c[1] + c[2]) # Sorts image colors by brightness
    
    colors_r = defaultdict(int) # Creates a dictionary with default values of 0.
    
    for i, color in enumerate(colors): # Adds colors to the Keys of the colors_r dictionary
        colors_r[color] = i
    
    pixels_g = list(map(lambda x: colors_r[x], pixels)) # Makes a list of corresponding colors to pixels of the original image
    
    convertedImage = []
    
    for pxl in pixels_g: # Creates the new image
        convertedImage.append(colorArray[pxl])

    print("Width: " + str(w) + " Height: " + str(h))
    
    name = name.rsplit('.', 1)[0] # Removes file extension from name
    
    f = open(f"{name}.txt", "w") # Write the text file
    f.write(", ".join(convertedImage))
    f.close()


convimg(sys.argv[1], sys.argv[2:]) #(imagename, colors)