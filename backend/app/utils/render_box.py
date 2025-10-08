from PIL import Image, ImageDraw, ImageFont
import textwrap

def draw_text_in_box(draw, box, text, font_path, initial_font_size=30):
    x1, y1, x2, y2 = box
    font_size = initial_font_size
    font = None

    box_width = x2 - x1
    box_height = y2 - y1

    wrapped_text = ''

    while font_size > 0:
        font = ImageFont.truetype(font_path, font_size)

        lines = []
        words = text.split()
        if not words:
            break

        current_line = words[0]

        for word in words[1:]:
            # check the width of the line if we add the next word
            if font.getbbox(current_line + " " + word)[2] <= box_width:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)
        wrapped_text = "\n".join(lines)

        # Get the height and width of the text block with the current font size
        text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
        x1, y1, x2, y2 = text_bbox[0], text_bbox[1], text_bbox[2], text_bbox[3]
        
        text_width = x2 - x1
        text_height = y2 - y1

        # If it fits, break the loop
        if text_width <= box_width and text_height <= box_height:
            break

        # Decreasing the font size otherwise
        font_size -= 1

    # Draw the text on the image
    if font_size > 0:
        text_width = text_bbox[2] - text_bbox[0]

        # Calculate and get the final dimensions of the text block
        final_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
        text_width = final_bbox[2] - final_bbox[0]
        text_height = final_bbox[3] - final_bbox[1]

        # Calculated the centered position to draw the text
        text_x = box[0] + (box_width - text_width) / 2
        text_y = box[1] + (box_height - text_height) / 2
        draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill='black', align='center')