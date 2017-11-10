from PIL import Image

im = Image.open('test-images\TestImage1c.jpg')
pix = im.load()
print(im.format, im.size, im.mode)

width = im.size[0]
height = im.size[1]
im_gray = Image.new('L', im.size)

gray_val = []
for y in range(0, height):
    row = ""
    for x in range(0, width):
        RGB = im.getpixel((x,y))
        R,G,B = RGB
        L = 0.30*R + 0.59*G + 0.11*B
        gray_val.append(L)

im_gray.putdata(gray_val)
im_gray.show()

