import textwrap
from datetime import datetime, timezone

from PIL import Image, ImageDraw, ImageFont


class StatsImage:
    def __init__(self, template_image, font, color="dark"):
        """
        Class for updating a template image (e.g. to be displayed in a GitHub README) with repository and citation statistics.

        Arguments
        ---------
        template_image : str
            Template image to be updated
        font : str
            Font file (.tff) to be used
        color : str
            One of ["dark", "light"]. Background color of the image.
        """

        self.img = Image.open(template_image)
        self.draw = ImageDraw.Draw(self.img)

        self.font = font
        self.font_instance = ImageFont.truetype(font, 54)

        self.color = color
        if self.color == "dark":
            self.fill = "#ffffff"
        else:
            self.fill = "#000000"

