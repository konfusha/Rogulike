from PIL import Image

img = Image.new('RGB', (200, 200), (30, 30, 30))
img.save('test_button.png')