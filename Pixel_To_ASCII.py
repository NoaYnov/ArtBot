def pixel_to_ascii(image):
    ascii_str = ""
    for pixel in image.getdata():
        # Convert pixel to grayscale
        gray = int((pixel[0] + pixel[1] + pixel[2]) / 3)
        # Map grayscale value to ASCII character
        ascii_str += "@" if gray < 128 else " "
    return ascii_str
def image_to_ascii(image_path, width=100):
    from PIL import Image
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return ""
    
    # Resize image to specified width while maintaining aspect ratio
    aspect_ratio = image.height / image.width
    height = int(aspect_ratio * width)
    image = image.resize((width, height))
    
    # Convert image to RGB if not already in that mode
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert pixels to ASCII
    ascii_str = pixel_to_ascii(image)
    
    # Format the ASCII string into lines
    ascii_lines = [ascii_str[i:i + width] for i in range(0, len(ascii_str), width)]
    print("\n".join(ascii_lines))
    return "\n".join(ascii_lines)

def save_ascii_to_html(ascii_str, output_path):
    try:
        with open(output_path, 'w') as f:
            f.write(f"<pre>{ascii_str}</pre>")
        print(f"ASCII art saved to {output_path}")
    except Exception as e:
        print(f"Error saving ASCII art: {e}")
        
def main():
    image_path = 'imgs/resized_img.jpg'  # Path to the resized image
    output_path = 'ascii_art.html'  # Output file for ASCII art
    width = 100  # Width of the ASCII art
    
    ascii_art = image_to_ascii(image_path, width)
    
    if ascii_art:
        save_ascii_to_html(ascii_art, output_path)
if __name__ == "__main__":
    main()