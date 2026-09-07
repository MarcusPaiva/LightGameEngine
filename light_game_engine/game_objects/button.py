from logging import disable

from light_game_engine.bounding_box import CircleBoundingBox, RectBoundingBox
from light_game_engine.font import GameFont
from light_game_engine.game_artfacts_2d import Rect
from light_game_engine.game_collision import circle_rect_collision_detection
from light_game_engine.inputs.game_input import mouse_click_detection, mouse_position
from light_game_engine.screen import SurfaceScreen


class Button:

    def __init__(self, screen:SurfaceScreen, start_x:int, start_y:int, text:str, margin:int=10, on_click = None, font_size:int = 40):
        """
        Button initializer.
        :param screen: Main screen instance.
        :param start_x: Axis x start position.
        :param start_y: Axis y end position.
        :param text: Text display.
        :param on_click: On click event.
        :param font_size: Text font size.
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

    def disable(self, value:bool):
        self._disable = value

    @property
    def margin(self) -> int:
        return self._margin

    def set_font(self, value: str):
        """
        Use a custom font file instead of the system default.
        :param value: Path to a .ttf font file.
        :return: This instance, for chaining.
        """
        self._font_name = value
        return self

    def setup(self):
        font = GameFont(self._font_size, self._text)
        if self._font_name is not None:
            font.set_font(self._font_name)
        self._main_font = font.set_color([255, 255, 255])

    def set_position(self, start_x: float, start_y: float):
        """
        Reposition the button without changing its text/size.
        :param start_x: Axis x start position.
        :param start_y: Axis y start position.
        """
        self._x = start_x
        self._y = start_y

    def content_size(self) -> RectBoundingBox:
        """
        Measure the button's rendered size (text plus margin), independent
        of its position. Requires setup() to have been called first.
        :return: A zero-positioned RectBoundingBox whose width/height are the button's size.
        """
        text_width, text_height = self._main_font.get_text_size()
        return RectBoundingBox(0, 0, text_width + self._margin * 2, text_height + self._margin * 2)

    def _process_button_box(self):
        """Process button box"""
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
        Set background color.
        :param color: Color hex.
        """
        self._background_color = color

    def hover_color(self, color:str):
        """
        Set hover background color.
        :param color: Color hex.
        """
        self._hover_color = color

    def update(self):
        self._process_button_box()
        mouse_click = mouse_click_detection()
        if mouse_click is not None and self.__click_inside_button_detection(mouse_click[0],mouse_click[1]):
            if self._on_click is not None and not self._disable:
                self._on_click()
        self._hover = self.__mouse_hove_detection()
        self.__process_button_text()


    def __process_button_text(self):
        """
        Process button text.
        :return:
        """
        self._button_text = self._main_font.render()
        button_text_size = self._button_text.get_size()
        text_center_x = button_text_size[0] / 2
        text_center_y = button_text_size[1] / 2
        box = self._main_bounding_box
        self._text_position = [box.center_x - text_center_x, box.center_y - text_center_y]

    def __mouse_hove_detection(self) -> bool:
        """
        Mouse move inside box detection event.
        :return: Mouse inside box status.
        """
        position_x, position_y = mouse_position()
        return self.__point_inside_button_detection(position_x, position_y)

    def __click_inside_button_detection(self, position_x:int, position_y:int) -> bool:
        """
        Click inside box event.
        :param position_x: Axis x position event.
        :param position_y: Axis y position event.
        :return: Mouse click inside box status.
        """
        return self.__point_inside_button_detection(position_x, position_y)

    def __point_inside_button_detection(self, position_x: float, position_y: float) -> bool:
        """
        Point-vs-button-box collision. Delegates to the shared
        circle_rect_collision_detection helper (as a zero-radius circle)
        instead of comparing bounds by hand.
        :param position_x: Axis x position to test.
        :param position_y: Axis y position to test.
        :return: Whether the point falls inside the button's box.
        """
        point = CircleBoundingBox(position_x, position_y, 0)
        return circle_rect_collision_detection(point, 0, self._main_bounding_box)

    def draw(self) -> None:
        color = self._background_color
        if self._hover:
            color = self._hover_color
        box = self._main_bounding_box
        Rect(box.x0, box.y0, box.width, box.height).set_fill_color(color).render(self._screen)
        self._screen.draw(
            self._button_text,
            self._text_position
        )
