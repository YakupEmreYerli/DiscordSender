from PIL import Image, ImageDraw

def create_icon():
    # Create a 256x256 image with transparent background
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw a blue circle
    draw.ellipse((20, 20, 236, 236), fill='#5865F2', outline='#FFFFFF', width=10)
    
    # Draw a simple "paper plane" triangle
    # Polygon points: (Tip, Left Wing, Center Base, Right Wing)
    draw.polygon([(128, 60), (60, 190), (128, 160), (196, 190)], fill='white')

    # Save as .ico
    img.save('app_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print("app_icon.ico created successfully.")

if __name__ == "__main__":
    create_icon()
