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

    def draw_text(self, coords, text, fill=None, font=None, **kwargs):
        """
        Convenience wrapper for 'PIL.ImageDraw.Draw'

        Arguments
        ---------
        coords : tuple of int
            (x,y) coordinates of text location
        text : str
            Text to be drawn
        fill : str, default=None
            Text color
        font : 'PIL.ImageFont' instance, default=None
            Text font
        """
        if fill is None:
            fill = self.fill
        if font is None:
            font = self.font_instance

        self.draw.text(coords, str(text), fill=fill, font=font, **kwargs)

    def update_image(self, stats, repo_name, cache_dir):
        """
        Update the provided template image with text summarizing respository and citation statistics.

        Arguments
        ---------
        stats : dict
            A dictionary entry for each issue or pull request in the history (see `Git_metrics.get_issues_PRs`)
        repo_name : str
            Name of repository on GitHub (for drawn text)
        cache_dir : str
            Name of directory in which to cache updated image

        Returns
        -------
        self.img : 'PIL.Image' instance
            The provided template image updated with text
        """
        self.draw_text(
            (70, 404),
            f"{stats['n_recent_authors']} total contributors in last {stats['age_recent_commit']} days",
        )

        self.draw_text(
            (70, 30),
            f"{len(stats['new_authors'])} new contributors in last {stats['age_recent_commit']} days:",
        )
        # case-insensitive sort
        text_authors = sorted(stats["new_authors"], key=str.lower)
        # bound text block width to fit in box
        text_authors = "\n".join(textwrap.wrap(", ".join(text_authors), width=47))
        self.draw_text((70, 100), text_authors, font=ImageFont.truetype(self.font, 46))

        self.draw_text(
            (1258, 51),
            f"last {stats['issues']['age_recent']} days: {stats['issues']['recent_close']} issues closed, {stats['issues']['recent_open']} opened\n{stats['pullRequests']['recent_close']} PRs closed, {stats['pullRequests']['recent_open']} opened",
            align="right",
        )

        self.draw_text(
            (1390, 285),
            f"papers citing {repo_name}: {stats['aggregate']['cite_month']} last month\n{stats['aggregate']['cite_year']} this year\n{stats['aggregate']['cite_all']} all-time",
            align="right",
        )

        # package name
        # self.draw_text((1158, 405), repo_name, font=ImageFont.truetype(self.font, 36), anchor='ms')

        now = datetime.now(timezone.utc).strftime("%B %d, %Y")
        self.draw_text(
            (1210, 465),
            f"Generated on {now}",
            font=ImageFont.truetype(self.font, 34),
        )

        # img.show()
        self.img.save(f"{cache_dir}/{repo_name}_user_stats_{self.color}.png")

        return self.img
