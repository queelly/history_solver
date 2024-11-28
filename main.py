from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
config = r'--oem 3 --psm 6'

def split_image(image_path, n, m):

    matrix = []
    
    img = Image.open(image_path)
    img_width, img_height = img.size
    
    tile_width = img_width // m
    tile_height = img_height // n
    
    cnt_ready = 0
    for i in range(n):
        temp = []
        for j in range(m):
            left = j * tile_width
            upper = i * tile_height
            right = left + tile_width
            lower = upper + tile_height
            
            tile = img.crop((left, upper, right, lower))
            
            temp.append(pytesseract.image_to_string(tile, config=config, lang='rus').strip()[0].upper())
            cnt_ready += 1
            print(f'{cnt_ready // 4}% is done!')

        matrix.append(temp)
    return matrix
    

n = 20
matrix = split_image("test.png", n, n)
result = []

for i in range(n):
    vertical = ''
    horisontal = ''
    for j in range(n):
        vertical += matrix[i][j]
        horisontal += matrix[j][i]
    
    result.append(vertical + '\n')
    result.append(vertical[::-1] + '\n')
    result.append(horisontal + '\n')
    result.append(horisontal[::-1] + '\n')

result.append('=' * 20 + '\n')

for i in range(-n + 1, n):
    d1 = ''
    d2 = ''
    for j in range(0, n):
        if 0 <= j + i < n:
            d1 += matrix[j][j + i]
            d2 += matrix[j + i][j]
    result.append(d1 + '\n')
    result.append(d1[::-1] + '\n')
    result.append(d2 + '\n')
    result.append(d2[::-1] + '\n')

with open('result.txt', 'w') as file_result:
    file_result.writelines(result)
print("WORK IS DONE!!!")
