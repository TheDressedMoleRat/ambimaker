import glob
from PIL import Image

images = glob.glob("g/*.png")
for image in images:
    print(image)
    with open(image, 'rb') as file:
        img = Image.open(file)
        img = img.resize((300, 300), Image.BICUBIC)
        name = 'g2/' + image[2:]
        img.save(name)