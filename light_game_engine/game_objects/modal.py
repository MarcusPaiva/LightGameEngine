"""
A modal box (popup) with a message and, optionally, a row of buttons
to choose from - built on top of pygame.
"""
from dataclasses import dataclass, field
from typing import Callable, List, Optional

from light_game_engine.game_objects.button import Button
from light_game_engine.bounding_box import RectBoundingBox
from light_game_engine.font import GameFont
from light_game_engine.game_artfacts_2d import Rect
from light_game_engine.inputs.game_input import Buttons, Joystick
from light_game_engine.screen import SurfaceScreen


@dataclass
class Options:
    """
    One choice shown as a button inside a :class:`Modal`.
    """
    text: str
    on_click: Callable[[], None]
    background_color: str = field(default="#cccccc")
    hover_color: str = field(default="#cccccc")


class Modal:
    """
    A box shown in the middle of the screen, with a message and an
    optional row of option buttons (see :meth:`add_options`).
    """

    def __init__(self, screen: SurfaceScreen, text: str, width_ratio: float = 0.6,
                 height_ratio: float = 0.55, margin: int = 10, font_size: int = 40, show=True):
        """
        :param screen: The screen this modal will be drawn on.
        :param text: The message shown inside the modal.
        :param width_ratio: How wide the modal is, as a share of the
            screen's width (0.6 means 60% of the screen's width).
        :param height_ratio: How tall the modal is, as a share of the
            screen's height.
        :param margin: Space, in pixels, used around the option buttons.
        :param font_size: Size of the text, in points.
        :param show: Whether the modal starts visible.
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
        self._focused_index = 0

    def set_font(self, value: str):
        """
        Use your own font file instead of the system's default font.

        :param value: Path to a ``.ttf`` font file.
        :return: This instance, for chaining.
        """
        self._font_name = value
        return self

    def __compute_bounding_box(self) -> RectBoundingBox:
        """
        Work out a box centered on the screen, sized as a share of the
        screen's current width and height.

        :return: The centered box.
        :rtype: RectBoundingBox
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
        Show or hide this modal.

        :param value: True to show it, False to hide it.
        :return: This instance, for chaining.
        """
        self._show = value
        return self

    def setup(self):
        """
        Load the font for this modal's text. Call this once before the
        first :meth:`update` call.

        :return: This instance, for chaining.
        """
        font = GameFont(self._font_size, self._text)
        if self._font_name is not None:
            font.set_font(self._font_name)
        self._main_font = font.set_color([255, 255, 255])
        return self

    def add_options(self, options: List[Options]):
        """
        Add one or more option buttons to this modal.

        :param options: The options to add.
        :return: This instance, for chaining.
        """
        self._options += options
        return self

    def update(self, joystick: Optional[Joystick] = None):
        """
        Move this modal forward by one frame: re-draw its text and its
        option buttons.

        :param joystick: Joystick used to move between and confirm
            options. When given, D-pad left/right move the focus
            between options, and the focused option's confirm button
            activates it - the same as clicking it with the mouse.
        :return: This instance, for chaining.
        """
        self._main_bounding_box = self.__compute_bounding_box()
        self.__process_button_text()
        self.__navigate_options(joystick)
        self.__process_options(joystick)
        return self

    def __navigate_options(self, joystick: Optional[Joystick]):
        """
        Move the focused option left or right on a D-pad press, and
        keep the focused option valid as options are added or removed.

        :param joystick: Joystick to read D-pad presses from, if any.
        :return: None
        """
        if not self._options:
            self._focused_index = 0
            return
        self._focused_index = max(0, min(self._focused_index, len(self._options) - 1))
        if joystick is None:
            return
        if joystick.button_just_pressed(Buttons.dpad_right):
            self._focused_index = min(self._focused_index + 1, len(self._options) - 1)
        elif joystick.button_just_pressed(Buttons.dpad_left):
            self._focused_index = max(self._focused_index - 1, 0)

    def __process_options(self, joystick: Optional[Joystick] = None):
        """
        Build and place the option buttons, side by side, with equal
        gaps between them and equal space on each side of the row - no
        matter how wide each button's text makes it.

        :param joystick: Joystick passed on to each option's update(),
            so the focused option can react to its confirm button.
        :return: None
        """
        self._options_buttons = []
        if not self._options:
            return

        x = self._main_bounding_box.x0
        y = self._main_bounding_box.y0
        end_y = y + (self._main_bounding_box.height * 0.8)
        size_x = self._main_bounding_box.width

        buttons = []
        for index, option in enumerate(self._options):
            btn = Button(self._screen, 0, end_y, option.text, margin=self._margin, on_click=option.on_click)
            btn.hover_color(option.hover_color)
            btn.background_color(option.background_color)
            btn.disable(not self._show)
            btn.focus(index == self._focused_index)
            btn.setup()
            buttons.append(btn)

        widths = [btn.content_size().width for btn in buttons]
        gap = self._margin
        total_width = sum(widths) + gap * (len(buttons) - 1)
        outer_margin = max((size_x - total_width) / 2, 0)

        current_left = x + outer_margin
        for btn, width in zip(buttons, widths):
            btn.set_position(current_left + self._margin, end_y)
            btn.update(joystick)
            self._options_buttons.append(btn)
            current_left += width + gap

    def __process_button_text(self):
        """
        Draw the modal's message and work out where to place it inside
        the modal's box.
        """
        self._button_text = self._main_font.render()
        button_text_size = self._button_text.get_size()
        text_center_x = button_text_size[0] / 2
        text_center_y = self._main_bounding_box.height * 0.35
        box = self._main_bounding_box
        self._text_position = [box.center_x - text_center_x, box.center_y - text_center_y]

    def draw(self):
        """
        Draw this modal, its message, and its option buttons onto its
        screen. Draws nothing if the modal is hidden.

        :return: This instance, for chaining.
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
