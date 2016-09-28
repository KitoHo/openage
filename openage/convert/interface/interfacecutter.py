# Copyright 2016-2016 the openage authors. See copying.md for legal info.

""" Cutting some user interface assets into subtextures """

from ..texture import TextureImage

from .interfacehardcoded import (is_ingame_hud_background,
                                 TOP_STRIP_PATTERN_CORNERS,
                                 TOP_STRIP_PATTERN_SEARCH_AREA_CORNERS,
                                 MID_STRIP_PATTERN_CORNERS,
                                 MID_STRIP_PATTERN_SEARCH_AREA_CORNERS,
                                 KNOWN_SUBTEX_CORNER_COORDS)

from .visgrep import visgrep


class InterfaceCutter(object):
    """
    Callable object that cuts interface textures.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, filename):
        self.filename = filename

    def __call__(self, image):
        if is_ingame_hud_background(self.filename):
            pil_image = image.get_pil_image()

            yield self.cut_strip(pil_image,
                                 TOP_STRIP_PATTERN_CORNERS,
                                 TOP_STRIP_PATTERN_SEARCH_AREA_CORNERS)

            yield self.cut_strip(pil_image,
                                 MID_STRIP_PATTERN_CORNERS,
                                 MID_STRIP_PATTERN_SEARCH_AREA_CORNERS)

            for coords in KNOWN_SUBTEX_CORNER_COORDS:
                yield TextureImage(pil_image.crop(coords))
        else:
            yield image

    def cut_strip(self, pil_image, pattern_corners, search_area_corners):
        """
        Finds a horisontally tilable piece of the strip (ex. the top of the HUD).

        ||----///////////-------------///////////-------------///////////-------------///////////||
                  ^      pattern_corners     ^                    ^  where it is found last  ^
                  ^           this piece is tileable              ^

        so, cut out a subtexture:
                  ///////-------------///////////-------------////
        """

        pattern = pil_image.crop(pattern_corners)
        search_area = pil_image.crop(search_area_corners)

        matches = visgrep(search_area, pattern, 100000)

        if len(matches) < 2:
            raise Exception("visgrep failed to find repeating pattern (%s)\n" % self.filename)

        return TextureImage(pil_image.crop((
            pattern_corners[0],
            pattern_corners[1],
            search_area_corners[0] + matches[-1].point[0],
            pattern_corners[3]
        )))
