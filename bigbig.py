
# import Image as Image
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import os
import time

FILE_NAME = 'in.txt'
IMAGES_PATH = './image/'  # 正数图片集地址
IMAGE_SIZE = 36  # 每张小图片的大小
IMAGE_SAVE_PATH = './result/'  # 图片转换后的地址
IMAGE_RESIZE_SCALE = 2.5  # 放大倍率

arrOld = []


def read_file():
    # 读取文件
    with open(FILE_NAME) as f:
        for line in f.readlines():
            # 如果想修改分隔符，改这里
            arr = list(map(int, line.split(',')))
            arrOld.append(arr)


def create_image():

    # 为了蛋疼需求，把数组横过来
    # 建立一个横着的数组
    i = 0
    j = 0
    arr = [[0 for i in range(len(arrOld))] for j in range(len(arrOld[0]))]

    # 旋转数组
    for i in range(0, len(arrOld)):
        for j in range(0, len(arrOld[i])):
            arr[j][i] = arrOld[len(arrOld)-1-i][j]
        pass

    # 计算出总共需要多少格子
    colSize = 0
    for y in range(0, len(arr)):
        c = 0
        for x in range(0, len(arr[y])):
            count = getCountNumber(arr[y][x])
            colSize = max(count, colSize)
            c += count
    totolV = colSize * len(arr[0])

    # 创建一个新图
    to_image = Image.new('RGBA', (totolV * IMAGE_SIZE,
                                  len(arr) * IMAGE_SIZE))

    # 遍历方式有改动
    # 先是从Y轴往上便利
    for y in range(0, len(arr)):
        for x in range(0, len(arr[y])):
            number = arr[y][x]
            # 负数取正
            isPosi = number > 0
            if isPosi == False:
                number = -number
            c = 0  # 当前位
            while number != 0:
                num_img = number % 10
                from_image = convert2Image(num_img, c % 2 == 1, isPosi)
                if from_image != None:
                    # 这里坐标计算是试出来的，对就行，没仔细思考
                    to_image.paste(
                        from_image, (((x+1) * colSize - c - 1) * IMAGE_SIZE, y * IMAGE_SIZE))
                number = int(number / 10)
                c += 1

    # 画辅助线

    draw = ImageDraw.Draw(to_image)
    img_w, img_h = to_image.size
    for x in range(1, len(arr[0])):
        xoffset = x * colSize*IMAGE_SIZE
        draw.line((xoffset, 0, xoffset, img_h * IMAGE_SIZE), fill="blue")
    for y in range(1, len(arr)):
        draw.line((0, y*IMAGE_SIZE, img_w, y*IMAGE_SIZE), fill="blue")

    del draw

    # 如果想要图片变大，改这里
    to_image = to_image.resize((int(img_w * IMAGE_RESIZE_SCALE),
                                int(img_h * IMAGE_RESIZE_SCALE)))

    # 直接显示，不保存
    # to_image.show()
    # 生成一个本地文件
    out = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + '.png'
    to_image.save(IMAGE_SAVE_PATH+out)  # 保存新图


def getCountNumber(num):
    # 计算数字一共几位
    c = 0
    while num != 0:
        num = int(num / 10)
        c += 1
    return c


def convert2Image(num, isEven, isPositive):
    # 读取算筹数字成图片
    # 一位数字，是否是偶数
    if num == 0:
        return None

    # 是否是竖着的数字
    isVert = 'Counting_rod_v'
    if isEven:
        isVert = 'Counting_rod_h'

    # 判断正负数，读取不同图片，这里不做图片颜色处理
    path = IMAGES_PATH + isVert + str(num)
    if isPositive:
        path += 'p'
    else:
        path += 'm'

    image = Image.open(path + '.png')

    # 生成返回图片，用于居中处理
    new_im = Image.new('RGBA', (IMAGE_SIZE, IMAGE_SIZE))
    img_w, img_h = image.size
    offset = (int((IMAGE_SIZE - img_w)/2), int((IMAGE_SIZE - img_h)/2))
    new_im.paste(image, offset)
    return new_im


read_file()
create_image()  # 调用函数
