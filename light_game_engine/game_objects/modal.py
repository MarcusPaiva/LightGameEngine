from dataclasses import dataclass, field
from typing import Callable, List

from light_game_engine.game_objects.button import Button
from light_game_engine.bounding_box import RectBoundingBox
from light_game_engine.font import GameFont
from light_game_engine.game_artfacts_2d import Rect
from light_game_engine.screen import SurfaceScreen


@dataclass
class Options:
    text: str
    on_click: Callable[[], None]
    background_color: str = field(default="#cccccc")
    hover_color: str = field(default="#cccccc")


class Modal:
    def __init__(self, screen: SurfaceScreen, text: str, width_ratio: float = 0.6,
                 height_ratio: float = 0.55, margin: int = 10, font_size: int = 40, show=True):
        """
        Modal initializer.
        :param screen: Main screen instance.
        :param text: Text message inside modal to display.
        :param width_ratio: Modal width as a fraction of the screen's current width.
        :param height_ratio: Modal height as a fraction of the screen's current height.
        :param font_size: Text font size.
        """
        self._screen = screen
        self._margin = margin
        self._width_ratio = width_ratio
        self._height_ratio = height_ratio
        self._main_bounding_box = self.__compute_bounding_box()
        self._text = text
        self._font_size = font_size
        self._main_font = None
        self._background_color = "#000000"
        self._margin_color = "red"
        self._options: List[Options] = []
        self._show = show
        self._options_buttons: List[Button] = []
        self._font_name = None

    def set_font(self, value: str):
        """
        Use a custom font file instead of the system default.
        :param value: Path to a .ttf font file.
        :return: This instance, for chaining.
        """
        self._font_name = value
        return self

    def __compute_bounding_box(self) -> RectBoundingBox:
        """
        Compute a bounding box centered on the screen, sized proportionally
        to the screen's current dimensions.
        :return: Centered RectBoundingBox.
        """
        screen_width = self._screen.width()
        screen_height = self._screen.height()
        width = screen_width * self._width_ratio
        height = screen_height * self._height_ratio
        x0 = (screen_width - width) / 2
        y0 = (screen_height - height) / 2
        return RectBoundingBox(x0, y0, x0 + width, y0 + height)

    def show(self, value:bool):
        """
        Display modal.
        :param value: Visibility status.
        :return:
        """
        self._show = value
        return self

    def setup(self):
        """
        Setup event.
        """
        font = GameFont(self._font_size, self._text)
        if self._font_name is not None:
            font.set_font(self._font_name)
        self._main_font = font.set_color([255, 255, 255])
        return self

    def add_options(self, options: List[Options]):
        """
        Add options to modal.
        :param options: List of options to add in modal.
        :return:
        """
        self._options += options
        return self

    def update(self):
        """
        Update event.
        """
        self._main_bounding_box = self.__compute_bounding_box()
        self.__process_button_text()
        self.__process_options()
        return self

    def __process_options(self):
        """
        Process options buttons in modal, laid out left-to-right with equal
        gaps between them and equal outer margins to the box's edges,
        regardless of how wide each button's text makes it.
        :return:
        """
        self._options_buttons = []
        if not self._options:
            return

        x = self._main_bounding_box.x0
        y = self._main_bounding_box.y0
        end_y = y + (self._main_bounding_box.height * 0.8)
        size_x = self._main_bounding_box.width

        buttons = []
        for option in self._options:
            btn = Button(self._screen, 0, end_y, option.text, margin=self._margin, on_click=option.on_click)
            btn.hover_color(option.hover_color)
            btn.background_color(option.background_color)
            btn.disable(not self._show)
            btn.setup()
            buttons.append(btn)

        widths = [btn.content_size().width for btn in buttons]
        gap = self._margin
        total_width = sum(widths) + gap * (len(buttons) - 1)
        outer_margin = max((size_x - total_width) / 2, 0)

        current_left = x + outer_margin
        for btn, width in zip(buttons, widths):
            btn.set_position(current_left + self._margin, end_y)
            btn.update()
            self._options_buttons.append(btn)
            current_left += width + gap

    def __process_button_text(self):
        """
        Process button text.
        :return:
        """
        self._button_text = self._main_font.render()
        button_text_size = self._button_text.get_size()
        text_center_x = button_text_size[0] / 2
        text_center_y = self._main_bounding_box.height * 0.35
        box = self._main_bounding_box
        self._text_position = [box.center_x - text_center_x, box.center_y - text_center_y]

    def draw(self):
        """
        Draw event.
        """
        if self._show:
            box = self._main_bounding_box
            Rect(box.x0, box.y0, box.width, box.height).set_fill_color(self._margin_color).render(self._screen)
            Rect(box.x0, box.y0, box.width, box.height).set_fill_color(self._background_color).render(self._screen)

            self._screen.draw(
                self._button_text,
                self._text_position
            )
            for option in self._options_buttons:
                option.draw()
        return self
