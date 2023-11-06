"""Includes the GUI abstract class"""

from abc import ABC, abstractmethod
from Object import Object
from Renderer import Renderer


class GUI(ABC):
    """Represents an abstract GUI that exposes drawing functions and allows objects to be put in.

    Attributes:
        graphics: A Graphics object that will handle 3D object drawing.
        obj: The current object being displayed on the GUI
    """

    def __init__(self, renderer: Renderer):
        self.renderer = renderer
        self.renderer.gui = self
        self.obj = None

    @abstractmethod
    def put_object(self, obj: Object) -> None:
        """Makes a deep copy of the object and displays it on the canvas

        Args:
            obj: An Object instance to be displayed
        Returns:
             None
        """
        pass

    @abstractmethod
    def wait(self) -> None:
        """Waits for the GUI to be closed

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_canvas_size(self) -> (int, int):
        """Returns the size width and height of the canvas (The GUI portion that displays the object)

        Returns:
            (int, int) representing width and height respectively.
        """
        pass

    @abstractmethod
    def draw_canvas_point(self, x, y, v_color) -> None:
        pass

    @abstractmethod
    def draw_canvas_line(self, x1, y1, x2, y2, e_color) -> None:
        pass

    @abstractmethod
    def draw_canvas_polygon(self, xy_list, e_color, f_color) -> None:
        pass

    @abstractmethod
    def clear_canvas(self) -> None:
        """Clears the current object from the canvas

        Must set self.obj to None

        Returns:
            None
        """
        pass

    def redraw_canvas(self) -> None:
        """Del"""
        obj = self.obj
        self.clear_canvas()
        self.renderer.render_object(obj)
        self.obj = obj
