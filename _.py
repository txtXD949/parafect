from PIL import Image

img = Image.open('png.png')
pixs = img.load()
width, height = img.size

with open('assets/txts/map(map_board).txt', 'w', encoding='utf-8') as f:
    for x in range(height):
        for y in range(width):
            r = pixs[y, x][0]

            if r == 0:
                print('#', end='', file=f)
            else:
                print(' ', end='', file=f)
        print(file=f)

