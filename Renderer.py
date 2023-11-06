"""Includes the Renderer interface as well as all of its implementations"""

import numpy as np

from abc import ABC, abstractmethod
from Projector import Projector
from Object import Object


class Renderer(ABC):
    """Exposes one function to render 3D objects

    Attributes:
        projector: The projecter that will be used to project 3D points onto the screen.
        gui: The graphical user interface which will be used as the 2D drawing engine.
    """

    def __init__(self, projector: Projector,  gui=None):
        self.projector = projector
        self.gui = gui

    @abstractmethod
    def render_object(self, obj: Object) -> None:
        """Uses the GUI drawing functions to translate the 3D object into 2D points, lines, and polygons.

        Args:
            obj: The 3D object to render
        Returns:
            None
        """
        pass


class WireframeRenderer(Renderer):
    """Renders objects in wireframe

    Attributes (See base class for more attributes):
        vertices_color
        edges_color
    """

    def __init__(self, projector: Projector,  gui=None):
        """initializes renderer with blue colors"""
        super().__init__(projector, gui)
        self.vertices_color = "#0000FF"
        self.edges_color = "#0000FF"

    def render_object(self, obj: Object) -> None:
        """Renders objects in wireframe (See base class)

        The object is normalized, shifted and scaled such that it occupies approximately half of the canvas size.
        """
        assert self.gui is not None

        w, h = self.gui.get_canvas_size()
        vertices = obj.vertices*np.min([w, h])*0.35 + np.array([w/2, h/2, 0])

        self.gui.clear_canvas()

        vertices_2d = self.projector.project(vertices)
        for x, y in vertices_2d:
            self.gui.draw_canvas_point(x, y, v_color=self.vertices_color)

        for face in obj.faces:
            face_vertices = list()
            for v_id in face:
                face_vertices.extend(vertices_2d[v_id])

            self.gui.draw_canvas_polygon(face_vertices,
                                         e_color=self.edges_color,
                                         f_color="")
        self.gui.obj = obj


class FlatShadedRenderer(Renderer):
    """Renders flat shaded objects

    The renderer uses the simple painter's algorithm.
    Cannot render objects with intersecting faces properly.
    Can be slow since it renders all of the non-visible polygons as well. TODO: Implement back face culling

    Attributes (See base class for more attributes):
        vertices_color
        edges_color
        bright_face_color: Color of faces parallel to the screen
        dark_face_color: Color of faces orthogonal to the screen
    """
    def __init__(self, projector: Projector,  gui=None):
        """initializes renderer with blue colors"""
        super().__init__(projector, gui)
        self.vertices_color = "#0000FF"
        self.edges_color = "#0000FF"
        self.bright_face_color = "#0000FF"
        self.dark_face_color = "#00005F"

    def render_object(self, obj: Object) -> None:
        """Renders flat shaded objects (See base class)

        The object is normalized, shifted and scaled such that it occupies approximately half of the canvas size.
        """
        assert self.gui is not None

        w, h = self.gui.get_canvas_size()
        vertices = obj.vertices*np.min([w, h])*0.35 + np.array([w/2, h/2, 0])

        self._sort_obj_faces_by_depth(obj)
        self.gui.clear_canvas()

        vertices_2d = self.projector.project(vertices)
        for x, y in vertices_2d:
            self.gui.draw_canvas_point(x, y, v_color=self.vertices_color)

        for face in obj.faces:
            P1, P2, P3 = [vertices[face[i]] for i in range(3)]
            U = P2 - P1
            V = P3 - P1
            N = np.cross(U, V)
            N /= np.linalg.norm(N)
            norm_z_axis_component = np.abs(N[2])
            color_hex = self._color_fader(self.bright_face_color, self.dark_face_color, norm_z_axis_component)

            face_vertices = list()
            for v_id in face:
                face_vertices.extend(vertices_2d[v_id])

            self.gui.draw_canvas_polygon(face_vertices,
                                         e_color=self.edges_color,
                                         f_color=color_hex)

        self.gui.obj = obj

    def _sort_obj_faces_by_depth(self, obj: Object) -> None:
        """Sorts the renderer object's faces inplace based on the average z value

        This is done as a prestep before normal drawing

        Args:
            obj: The Object instance to be sorted

        Returns:
            None
        """
        depth_face_ls = list()
        for face in obj.faces:
            z_avg = 0
            for v_id in face:
                x, y, z = obj.vertices[v_id]
                z_avg += z
            z_avg /= 3
            depth_face_ls.append((z_avg, face))
        depth_face_ls = sorted(depth_face_ls, key=lambda x: x[0], reverse=True)
        obj.faces.clear()
        for z_avg, face in depth_face_ls:
            obj.faces.append(face)

    def _color_fader(self, color1, color2, alpha) -> str:
        """ Fades the color from color1 to color2 based on alpha as color1*alpha + (1-alpha)*color2

        Args:
            color1: First color as a hex string. Ex. "#0000FF"
            color2
            alpha: a value in [0, 1]

        Returns:
            the hex string of the combination of the two colors
        """
        hex2rgb = lambda c : np.array([int(c.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)])
        c1_rgb = hex2rgb(color1)
        c2_rgb = hex2rgb(color2)
        c3_rgb = c1_rgb * alpha + c2_rgb * (1-alpha)
        c3_hex = '#{:02x}{:02x}{:02x}'.format(*[int(x) for x in c3_rgb])
        return c3_hex