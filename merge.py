from PIL import Image, ImageDraw, ImageFont
import os
import datetime
import glob
from fpdf import FPDF

def main():
    pass
# testing

def create_card(poke_details):
    file = poke_details["file_name"]
    background = poke_details["background"]
    size = poke_details["pokemon_size"]
    y = poke_details["pokemon_y"]
    name = poke_details["base_name"]
    is_shiny = poke_details["is_shiny"]

    out = "asset/temp.PNG"
    poke = Image.open(f"asset/sprite/{file}.png", mode='r', formats=None)
    card = Image.open(f"asset/bg/{background}.PNG", mode='r', formats=None)
    star = Image.open(f"asset/star.png", mode='r', formats=None)

    poke = poke.resize((size, size))
    star = star.resize((140, 140))

    card_width, card_height = card.size
    poke_width, poke_height = poke.size
    x = (card_width - poke_width) // 2

    card.paste(poke.convert("RGBA"), (x, y), mask=poke.convert("RGBA"))

    if is_shiny:
        card.paste(star, (110, 1000), star)
        card.paste(star, (700, 1000), star)
        card.paste(star, (70, 140), star)

    card.save(out)

    if name == "Mew":
        name = "  Mew"

    return [out, name]

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

def add_text_to_image(image_path, text):
    image = Image.open(image_path)  # Open the image
    draw = ImageDraw.Draw(image)  # Create a drawing context
    font = ImageFont.truetype("asset/Pokemon Hollow.ttf", 150)  # Load a font

    draw.text((155, 1120), text, font=font, fill=(0, 0, 0))  # Draw the text on the image
    current_datetime = datetime.datetime.now()

    filename = f"asset/Temp/card_{current_datetime}.PNG"
    image.save(filename)  # Save the modified image
    return filename

def paste_pdf():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=0)

    image_files = glob.glob("asset/Temp/*.PNG")

    for image_file in image_files:
        pdf.add_page()
        page_width = pdf.w
        page_height = pdf.h

        # Calculate image dimensions and position
        image_width = page_width
        image_height = page_height

        pdf.image(image_file, 0, 0, image_width, image_height)

    current_datetime = datetime.datetime.now()
    pdf.output(f"Vault/VAULT_{current_datetime}.pdf")
    return None

if __name__ == "__main__":
    main()
