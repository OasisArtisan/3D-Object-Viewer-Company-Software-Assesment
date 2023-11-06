"""Includes the Tkinter GUI

Typical usage example:
    gui = TkinterGUI(graphics, object)
    gui.wait()
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import copy
import numpy as np

from GUI import GUI
from Object import Object
from Renderer import Renderer
from ObjectIO import load_object, save_object


class TkinterGUI(GUI):
    """An implementation of the GUI abstract class using the Tkinter library.

    Attributes (See base class for more attributes):
        root: The root tkinter window
        canvas_frame: The frame containing the canvas.
        canvas: The canvas on which the drawing will be.
    """
    def __init__(self, renderer: Renderer):
        super().__init__(renderer)
        self.root = tk.Tk(className="Neocis Software Assessment")
        self.canvas_frame = tk.Frame(master=self.root, width=200, height=200)

        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, background="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Configure>", self._redraw_handler)
        self.canvas.bind("<ButtonPress-1>", self._on_click_handler)
        self.canvas.bind("<B1-Motion>", self._on_move_handler)
        self.canvas.bind("<ButtonRelease-1>", self._on_release_handler)

        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self._new_handler)
        filemenu.add_command(label="Open", command=self._open_handler)
        filemenu.add_command(label="Save", command=self._save_handler)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

        self._dragging = False
        self._dragging_last = None

    def put_object(self, obj: Object) -> None:
        """See base class"""
        self.obj = copy.deepcopy(obj)
        self.obj.normalize()
        # Flip y-coordinates to match the tkinter coordinate scheme so that increasing y in for an object vertex
        # corresponds to an upward direction in the 2D projection.
        self.obj.vertices[:, 1] *= -1
        self.redraw_canvas()

    def wait(self) -> None:
        """See base class"""
        self.root.mainloop()

    def get_canvas_size(self) -> (int, int):
        """See base class"""
        return self.canvas.winfo_width(), self.canvas.winfo_height()

    def draw_canvas_point(self, x, y, v_color) -> None:
        """See base class"""
        self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=v_color)

    def draw_canvas_line(self, x1, y1, x2, y2, e_color) -> None:
        """See base class"""
        self.canvas.create_line(x1, y1, x2, y2, fill=e_color, width=3)

    def draw_canvas_polygon(self, xy_list, e_color, f_color) -> None:
        """See base class"""
        self.canvas.create_polygon(xy_list, outline=e_color, fill=f_color, width=2)

    def clear_canvas(self) -> None:
        """See base class"""
        self.canvas.delete("all")
        self.obj = None

    def _draw_axes(self):
        """Draws two black arrows specifying the x and y axes at the point of origin."""
        x0 = self.canvas.winfo_width()/2
        y0 = self.canvas.winfo_height()/2
        x1 = x0 + self.canvas.winfo_width()*0.2
        y1 = y0 - self.canvas.winfo_height()*0.2
        self.canvas.create_line(x0, y0, x0, y1, arrow=tk.LAST)
        self.canvas.create_line(x0, y0, x1, y0, arrow=tk.LAST)

    def _redraw_handler(self, event):
        """Handler called when the canvas is resized."""
        self.redraw_canvas()

    def _on_click_handler(self, event):
        """Handler called when a mouse clicks on the canvas"""
        self._dragging = True
        self._dragging_last = (event.x, event.y)

    def _on_move_handler(self, event):
        """Handler called when a mouse drags on the canvas

        This is where the rotation of the object in response to the dragging happens.
        """
        if self._dragging:
            x_last, y_last = self._dragging_last
            delta_x = event.x - x_last
            norm_delta_x = delta_x/self.canvas.winfo_width() * np.pi * 2
            delta_y = event.y - y_last
            norm_delta_y = delta_y/self.canvas.winfo_height() * np.pi * 2
            self._dragging_last = (event.x, event.y)

            self.obj.rotate(0, norm_delta_x, -norm_delta_y)
            self.redraw_canvas()

    def _on_release_handler(self, event):
        """Handler called when a mouse releases from the canvas"""
        self._dragging = False
        self._dragging_last = None

    def _new_handler(self):
        self.clear_canvas()

    def _save_handler(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".obj",
                                                filetypes=(("Wavefront", ".obj"), ("Neocis", ".txt"),
                                                           ("Neocis", ".neo")))
        try:
            save_object(filepath, self.obj)
        except Exception as e:
            messagebox.showerror(title="Exception",message=str(e))
            return

    def _open_handler(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
        try:
            obj = load_object(filepath)
        except Exception as e:
            messagebox.showerror(title="Exception",message=str(e))
            return
        self.put_object(obj)
