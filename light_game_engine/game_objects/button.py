"""
A clickable button UI element, built on top of pygame.
"""
from logging import disable
from typing import Optional

from light_game_engine.bounding_box import CircleBoundingBox, RectBoundingBox
from light_game_engine.font import GameFont
from light_game_engine.game_artfacts_2d import Rect
from light_game_engine.game_collision import circle_rect_collision_detection
from light_game_engine.inputs.game_input import Buttons, Joystick, mouse_click_detection, mouse_position
from light_game_engine.screen import SurfaceScreen


class Button:
    """
    A clickable text button. Reacts to a mouse click, and also to a
    controller confirm-button press when the button is focused (see
    :meth:`focus`).
    """

    def __init__(self, screen:SurfaceScreen, start_x:int, start_y:int, text:str, margin:int=10, on_click = None, font_size:int = 40):
        """
        :param screen: The screen this button will be drawn on.
        :param start_x: X position of the button.
        :param start_y: Y position of the button.
        :param text: The text shown on the button.
        :param margin: Space, in pixels, between the text and the
            button's edge.
        :param on_click: A function with no arguments, called when the
            button is clicked (or confirmed with a controller).
        :param font_size: Size of the text, in points.
        """
        self._screen = screen
        self._margin = margin
        self._x = start_x
        self._y = start_y
        self._main_bounding_box = RectBoundingBox(start_x, start_y, 0, 0)
        self._text = text
        self._font_size = font_size
        self._main_font = None
        self._on_click = on_click
        self._background_color = "#cccccc"
        self._hover_color = "#000000"
        self._hover = False
        self._button_text = None
        self._text_position = [0,0]
        self._disable = False
        self._font_name = None
        self._focused = False
        self._confirm_button = Buttons.a

    def disable(self, value:bool):
        """
        Turn this button on or off. A disabled button still draws, but
        ignores clicks and controller confirm presses.

        :param value: True to disable the button, False to enable it.
        """
        self._disable = value

    @property
    def margin(self) -> int:
        """
        :return: Space, in pixels, between the text and the button's
            edge.
        :rtype: int
        """
        return self._margin

    def focus(self, value: bool):
        """
        Mark this button as focused (for example, chosen by controller
        navigation). While focused, it is drawn with its hover color
        and reacts to the controller's confirm button, even if the
        mouse is not over it.

        :param value: True to focus this button, False to unfocus it.
        :return: This instance, for chaining.
        """
        self._focused = value
        return self

    @property
    def focused(self) -> bool:
        """
        :return: Whether this button is currently focused.
        :rtype: bool
        """
        return self._focused

    def set_confirm_button(self, button: Buttons):
        """
        Change which controller button activates this button while it
        is focused. The default is Buttons.a.

        :param button: The Buttons member that should trigger on_click.
        :return: This instance, for chaining.
        """
        self._confirm_button = button
        return self

    def set_font(self, value: str):
        """
        Use your own font file instead of the system's default font.

        :param value: Path to a ``.ttf`` font file.
        :return: This instance, for chaining.
        """
        self._font_name = value
        return self

    def setup(self):
        """
        Load the font for this button's text. Call this once before
        the first :meth:`update` call.
        """
        font = GameFont(self._font_size, self._text)
        if self._font_name is not None:
            font.set_font(self._font_name)
        self._main_font = font.set_color([255, 255, 255])

    def set_position(self, start_x: float, start_y: float):
        """
        Move this button to a new position, without changing its text
        or size.

        :param start_x: New x position.
        :param start_y: New y position.
        """
        self._x = start_x
        self._y = start_y

    def content_size(self) -> RectBoundingBox:
        """
        Measure this button's size (text plus margin), no matter where
        it is placed. You must call :meth:`setup` first.

        :return: A box, placed at (0, 0), whose width and height match
            this button's size.
        :rtype: RectBoundingBox
        """
        text_width, text_height = self._main_font.get_text_size()
        return RectBoundingBox(0, 0, text_width + self._margin * 2, text_height + self._margin * 2)

    def _process_button_box(self):
        """
        Work out this button's box (position and size), using its
        current position, text size, and margin.
        """
        x, y = self._main_font.get_text_size()
        width, height = (self._x + x + self._margin,
                         self._y + y + self._margin)
        self._main_bounding_box = RectBoundingBox(
            self._x - self._margin,
            self._y - self._margin,
            width,
            height
        )

    def background_color(self, color:str):
        """
        Set the color drawn when this button is not hovered or focused.

        :param color: Color as a hex string (for example "#cccccc").
        """
        self._background_color = color

    def hover_color(self, color:str):
        """
        Set the color drawn when this button is hovered by the mouse,
        or focused (see :meth:`focus`).

        :param color: Color as a hex string (for example "#000000").
        """
        self._hover_color = color

    def update(self, joystick: Optional[Joystick] = None):
        """
        Move this button forward by one frame: check for a mouse click,
        or (if this button is focused) a controller confirm-button
        press, and re-draw its text.

        :param joystick: Joystick to read a confirm-button press from.
            Only needed if this button can be focused by controller
            navigation.
        :return: None
        """
        self._process_button_box()
        mouse_click = mouse_click_detection()
        clicked_by_mouse = mouse_click is not None and self.__click_inside_button_detection(
            mouse_click[0], mouse_click[1]
        )
        clicked_by_joystick = (
            self._focused and joystick is not None and joystick.button_just_pressed(self._confirm_button)
        )
        if (clicked_by_mouse or clicked_by_joystick) and self._on_click is not None and not self._disable:
            self._on_click()
        self._hover = self.__mouse_hove_detection() or self._focused
        self.__process_button_text()


    def __process_button_text(self):
        """
        Draw the button's text and work out where to place it, centered
        inside the button's box.
        """
        self._button_text = self._main_font.render()
        button_text_size = self._button_text.get_size()
        text_center_x = button_text_size[0] / 2
        text_center_y = button_text_size[1] / 2
        box = self._main_bounding_box
        self._text_position = [box.center_x - text_center_x, box.center_y - text_center_y]

    def __mouse_hove_detection(self) -> bool:
        """
        Check if the mouse is currently over this button.

        :return: True if the mouse is inside this button's box.
        :rtype: bool
        """
        position_x, position_y = mouse_position()
        return self.__point_inside_button_detection(position_x, position_y)

    def __click_inside_button_detection(self, position_x:int, position_y:int) -> bool:
        """
        Check if a click position is inside this button.

        :param position_x: X position of the click.
        :param position_y: Y position of the click.
        :return: True if the click is inside this button's box.
        :rtype: bool
        """
        return self.__point_inside_button_detection(position_x, position_y)

    def __point_inside_button_detection(self, position_x: float, position_y: float) -> bool:
        """
        Check if a point is inside this button's box. Uses the shared
        circle_rect_collision_detection helper (treating the point as a
        circle with radius 0) instead of comparing edges by hand.

        :param position_x: X position to check.
        :param position_y: Y position to check.
        :return: True if the point is inside this button's box.
        :rtype: bool
        """
        point = CircleBoundingBox(position_x, position_y, 0)
        return circle_rect_collision_detection(point, 0, self._main_bounding_box)

    def draw(self) -> None:
        """
        Draw this button and its text onto its screen.

        :return: None
        """
        color = self._background_color
        if self._hover:
            color = self._hover_color
        box = self._main_bounding_box
        Rect(box.x0, box.y0, box.width, box.height).set_fill_color(color).render(self._screen)
        self._screen.draw(
            self._button_text,
            self._text_position
        )
