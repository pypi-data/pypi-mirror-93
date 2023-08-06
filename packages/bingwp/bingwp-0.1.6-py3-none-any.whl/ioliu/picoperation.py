from PIL import Image


# import Piexif

def modify_meta(path, intro):
    im = Image.open(path)
    info = im.info()
    for i in info:
        print(i)


def list_test():
    list = [1, 2, 3, 4, 5, 6, ]
    print(list[0:2])


def tuple_test():
    dict = {'a': 'b', 'c': 'd', 'd': 'e'}
    it = dict.__iter__()
    key = dict.keys()
    print(key)


