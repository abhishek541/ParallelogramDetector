from PIL import Image
import math

im = Image.open('test-images\TestImage1c.jpg')
pix = im.load()
print(im.format, im.size, im.mode)

width = im.size[0]
height = im.size[1]
im_gray = Image.new('L', im.size)

gray_val = []
for y in range(0, height):
    for x in range(0, width):
        RGB = im.getpixel((x,y))
        R,G,B = RGB
        L = 0.30*R + 0.59*G + 0.11*B
        gray_val.append(L)

im_gray.putdata(gray_val)
pix_gray = im_gray.load()
print(pix_gray[0, 129])
img_arr = []
for i in range(0, width):
    row = []
    for j in range(0, height):
        row.append(pix_gray[i,j])
    img_arr.append(row)

print(img_arr[0][129])

sobelimagex = []

for indexi, i in enumerate(img_arr):
    sobelrowx = []
    for indexj, j in enumerate(i):
        upperleft, upperright, left, right, lowerleft, lowerright = 0, 0, 0, 0, 0, 0
        if indexj > 0:  # forget the left border
            if indexi > 0:
                upperleft = img_arr[indexi - 1][indexj - 1] * 1
            left = img_arr[indexi][indexj - 1] * 2
            if indexi < width - 1:
                lowerleft = img_arr[indexi + 1][indexj - 1] * 1

        if indexj < height - 1:  # forget the right border
            if indexi > 0:
                upperright = img_arr[indexi - 1][indexj + 1] * -1
            right = img_arr[indexi][indexj + 1] * -2
            if indexi < width - 1:
                lowerright = img_arr[indexi + 1][indexj + 1] * -1
        val = upperleft + upperright + left + right + lowerleft + lowerright
        if val > 255:
            val = 255
        if val < 0:
            val = 0
        sobelrowx.append(val)
    sobelimagex.append(sobelrowx)

sobelarrx = []
for m in range(0, height):
    for l in range(0, width):
        xval = sobelimagex[l][m]
        sobelarrx.append(xval)

im_x = Image.new('L', im.size)
im_x.putdata(sobelarrx)
#im_x.show()

sobelimagey = []

for indexi, i in enumerate(img_arr):
    sobelrowy = []
    for indexj, j in enumerate(i):
        upperleft, upperright, up, low, lowerleft, lowerright = 0, 0, 0, 0, 0, 0
        if indexi > 0:  # forget the top border
            if indexj > 0:
                upperleft = img_arr[indexi - 1][indexj - 1] * 1
            up = img_arr[indexi - 1][indexj] * 2
            if indexj < height - 1:
                upperright = img_arr[indexi - 1][indexj + 1] * 1

        if indexi < width - 1:  # forget the bottom border
            if indexi < width - 1:
                lowerleft = img_arr[indexi + 1][indexj - 1] * -1
            low = img_arr[indexi + 1][indexj] * -2
            if indexj < height - 1:
                lowerright = img_arr[indexi + 1][indexj + 1] * -1
        val = upperleft + upperright + up + low + lowerleft + lowerright
        if val > 255:
            val = 255
        if val < 0:
            val = 0
        sobelrowy.append(val)
    sobelimagey.append(sobelrowy)

sobelarry = []
for m in range(0, height):
    for l in range(0, width):
        yval = sobelimagey[l][m]
        sobelarry.append(yval)

im_y = Image.new('L', im.size)
im_y.putdata(sobelarry)
#im_y.show()

im_gradarr = []
for m in range(0, height):
    for l in range(0, width):
        grad_val = math.sqrt(sobelimagex[l][m]**2 + sobelimagey[l][m]**2)
        im_gradarr.append(grad_val)

im_grad = Image.new('L', im.size)
im_grad.putdata(im_gradarr)
im_grad.show()