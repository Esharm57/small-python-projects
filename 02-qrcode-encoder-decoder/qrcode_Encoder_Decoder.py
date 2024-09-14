import qrcode
from pyzbar.pyzbar import decode
from PIL import Image



def make_Qr():
    data = input('enter data you want to save: ')

    qr = qrcode.QRCode(version = 1, box_size = 10, border= 5)

    qr.add_data(data)

    qr.make(fit=True)
    img = qr.make_image(fill_color = 'red', back_color = 'white')

    img.save('/Users/amitsharma/Documents/Python Projects/images/qrcodes/qrcode.png')

def extract_Qr():
    img = Image.open('/Users/amitsharma/Documents/Python Projects/images/qrcodes/qrcode.png')

    result = decode(img)

    print(result[0].data.decode('utf-8'))

while True:
    print('1. make QR code')
    print('2. extract QR code')
    print('3. exit')

    choice = int(input('enter your choice: '))

    if choice == 1:
        make_Qr()
    elif choice == 2:
        extract_Qr()
    elif choice == 3:
        break

