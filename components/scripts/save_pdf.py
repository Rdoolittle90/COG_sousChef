import datetime
import io
from io import BytesIO

from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer
from src.bot import DiscordBot

pdfmetrics.registerFont(TTFont('impossible', f'{DiscordBot.paths["cogs"]}/sousChef/components/fonts/Imposible_fill.ttf'))
pdfmetrics.registerFont(TTFont('brazierflame', f'{DiscordBot.paths["cogs"]}/sousChef/components/fonts/BrazierFlame.ttf'))


def create_recipe_doc(recipe_info, output_file):
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles for fonts
    custom_title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontName='impossible', fontSize=40)
    custom_subtitle_style = ParagraphStyle('CustomSubtitle', parent=styles['Heading3'], fontName='brazierflame', fontSize=16)

    # Recipe name
    story.append(Paragraph(recipe_info["name"], custom_title_style))
    story.append(Spacer(1, 10))

    # Ratings
    if recipe_info["ratings"]:
        total_rating = 0
        for rating in recipe_info["ratings"].values():
            total_rating += rating
        total_rating /= len(recipe_info["ratings"])
        story.append(Paragraph("★" * int(total_rating) + "✩" * (5 - int(total_rating)) + f"<br/>{datetime.datetime.now().strftime('%Y-%m-%d')}", styles['BodyText']))

    if recipe_info["spice"] > 1:
        story.append(Paragraph(f"Spice Rating: {recipe_info['spice']}/10", custom_subtitle_style))

    story.append(Spacer(1, 10))

    # Description
    story.append(Paragraph("Description:", styles['Heading3']))
    story.append(Paragraph(recipe_info["description"], styles['BodyText']))

    if len(recipe_info["description"]) > 2000:
        story.append(PageBreak())
    else:
        story.append(Spacer(1, 20))

    # Ingredients
    story.append(Paragraph("Ingredients:", styles['Heading3']))
    ingredients_text = "<br/>".join([f"- {item}" for item in recipe_info["ingredients"]])
    story.append(Paragraph(ingredients_text, styles['BodyText']))
    story.append(Spacer(1, 20))

    # Instructions
    story.append(Paragraph("Instructions:", styles['Heading3']))
    instructions_text = "<br/>".join(recipe_info["instructions"])
    story.append(Paragraph(instructions_text, styles['BodyText']))
    story.append(Spacer(1, 20))

    doc.build(story)
    # Add a border to each page of the created document
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    width, height = letter

    # Draw the border
    border_margin = 5  # adjust this value for the desired border margin
    can.setStrokeColorRGB(0,0,0)  # black color
    can.rect(border_margin, border_margin, width - 2*border_margin, height - 2*border_margin)
    can.showPage()  # finish the current page
    can.save()

    # Move the content of the packet to the beginning so we can read it.
    packet.seek(0)
    border_pdf = PdfReader(packet)

    # Now merge this border PDF with the original using PyPDF2
    existing_pdf = PdfReader(output_file)
    pdf_writer = PdfWriter()

    # Loop through all pages and merge the border
    for page_num in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[page_num]
        page.merge_page(border_pdf.pages[0])  # merge the border onto content page
        pdf_writer.add_page(page)

    with open(output_file, "wb") as out_stream:
        pdf_writer.write(out_stream)


def stamp_image_to_pdf(input_pdf_path, output_pdf_path, logo_path):
    # Create a new PDF with Reportlab
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawInlineImage(logo_path, letter[0]-110, letter[1]-160, width=100, height=150)
    can.save()

    # Move buffer position to beginning
    packet.seek(0)
    new_pdf = PdfReader(packet)

    # Read the existing PDF
    existing_pdf = PdfReader(open(input_pdf_path, "rb"))
    output = PdfWriter()

    # Iterate over all pages and stamp the logo on each
    for idx, page in enumerate(existing_pdf.pages):
        if idx == 0:
            page.merge_page(new_pdf.pages[0])
        output.add_page(page)

    # Write the output to the final file
    with open(output_pdf_path, "wb") as output_pdf_file:
        output.write(output_pdf_file)
