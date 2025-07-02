
from PIL import Image
from PIL import ImageFilter


def resize_and_uncolor_image(image_path, output_path, size=(200, 200)):
    with Image.open(image_path) as img:
        img = img.resize(size)
        img = img.filter(ImageFilter.GaussianBlur(int(input("Enter blur radius (0 for no blur): "))))
        img = img.convert("L")  # Convert to grayscale
        img.save(output_path)
        print(f"Image resized and saved to {output_path}")
        


def main():
    input_image = 'imgs/img.jpg'
    output_image = 'imgs/resized_img.jpg'
    size = (200, 200)
    resize_and_uncolor_image(input_image, output_image, size)

if __name__ == "__main__":
    main()