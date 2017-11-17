from PIL import Image
from math import sqrt, hypot, pi, cos, sin, atan2
from numpy import array, zeros

im = Image.open('test-images\TestImage.jpg')
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
im_gradang = zeros(im.size)
im_gradmag = zeros(im.size)
for m in range(0, height):
    for l in range(0, width):
        grad_val = int(sqrt(sobelimagex[l][m]**2 + sobelimagey[l][m]**2))
        ang_val = atan2(sobelimagey[l][m], sobelimagex[l][m])
        if ang_val < 0:
            ang_val = ang_val + 180
        im_gradarr.append(grad_val)
        im_gradmag[l][m] = grad_val
        im_gradang[l][m] = ang_val

im_normarr = []
for n in range(0, len(im_gradarr)):
    newVal = (im_gradarr[n] - min(im_gradarr))/(max(im_gradarr) - min(im_gradarr)) * 255
    print(str(n))
    im_normarr.append(newVal)

im_normmag = zeros(im.size)
for m in range(0, height):
    for l in range(0, width):
        normVal = (im_gradmag[l][m] - min(im_gradarr)) / (max(im_gradarr) - min(im_gradarr)) * 255
        im_normmag[l][m] = normVal

im_grad = Image.new('L', im.size)
im_grad.putdata(im_normarr)
print(str(max(im_normarr)))
im_grad.show()

im_nms = zeros(im.size)
for j in range(0, height):
    for i in range(0, width):
        if ((j+1) < height) and ((j-1) >= 0) and ((i+1) < width) and ((i-1) >= 0):
            # 0 degrees
            if (im_gradang[i][j] >= 337.5 or im_gradang[i][j] < 22.5) or (im_gradang[i][j] >= 157.5 and im_gradang[i][j] < 202.5):
                if im_normmag[i][j] >= im_normmag[i][j + 1] and im_normmag[i][j] >= im_normmag[i][j - 1]:
                    im_nms[i][j] = im_normmag[i][j]
            # 45 degrees
            if (im_gradang[i][j] >= 22.5 and im_gradang[i][j] < 67.5) or (im_gradang[i][j] >= 202.5 and im_gradang[i][j] < 247.5):
                if im_normmag[i][j] >= im_normmag[i - 1][j + 1] and im_normmag[i][j] >= im_normmag[i + 1][j - 1]:
                    im_nms[i][j] = im_normmag[i][j]
            # 90 degrees
            if (im_gradang[i][j] >= 67.5 and im_gradang[i][j] < 112.5) or (im_gradang[i][j] >= 247.5 and im_gradang[i][j] < 292.5):
                if im_normmag[i][j] >= im_normmag[i - 1][j] and im_normmag[i][j] >= im_normmag[i + 1][j]:
                    im_nms[i][j] = im_normmag[i][j]
            # 135 degrees
            if (im_gradang[i][j] >= 112.5 and im_gradang[i][j] < 157.5) or (im_gradang[i][j] >= 292.5 and im_gradang[i][j] < 337.5):
                if im_normmag[i][j] >= im_normmag[i - 1][j - 1] and im_normmag[i][j] >= im_normmag[i + 1][j + 1]:
                    im_nms[i][j] = im_normmag[i][j]

im_nmsarr = []
for m in range(0, height):
    for l in range(0, width):
        im_nmsarr.append(im_nms[l][m])

im_trarr = []
for y in range(0, height):
    for x in range(0, width):
        v = im_grad.getpixel((x,y))
        if v <= 40:
            v = 255
        else:
            v = 0
        im_trarr.append(v)

im_tr = Image.new('L', im.size)
im_tr.putdata(im_nmsarr)
im_tr.show()

# pim = im_tr.load()
# ntx, mry = 460, 360
# nimx, mimy = im_tr.size
# mry = int(mry / 2) * 2  # Make sure that this is even
# him = Image.new("L", (ntx, mry), 255)
# phim = him.load()
#
# rmax = hypot(nimx, mimy)
# dr = rmax / (mry / 2)
# dth = pi / ntx
#
# for jx in range(nimx):
#     print("in for: "+str(jx))
#     for iy in range(mimy):
#         col = pim[jx, iy]
#         if col == 255: continue
#         for jtx in range(ntx):
#             th = dth * jtx
#             r = jx * cos(th) + iy * sin(th)
#             iry = mry / 2 + int(r / dr + 0.5)
#             phim[jtx, iry] -= 1
#
# him.show()