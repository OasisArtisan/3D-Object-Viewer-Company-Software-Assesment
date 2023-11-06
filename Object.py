"""Includes the Object class

Typical usage example:
    obj = Object(vertices, faces)
"""

import numpy as np


class Object:
    """Represents any 3D object as a triangular mesh.

    Attributes:
        vertices: An Nx3 numpy matrix where each row represents the (x,y,z) coordinates.
        faces: a list of tuples where each tuple contains the 3 indices into the vertices list that constitute a face.
    """

    def __init__(self, vertices, faces):
        """Constructs a new 3D object given its vertices and faces.

        Args:
            vertices: a list of tuples where each tuple is in the form (x,y,z) to specifying a vertex.
            Alternatively, you can pass an Nx3 numpy matrix where each row represents the (x,y,z) coordinates.
            faces: a list of tuples where each tuple contains 3 indices into the vertices list that constitute a face.
        """
        self.vertices = np.array(vertices)
        self.faces = faces

    def normalize(self):
        """Offsets and scales the object such that all vertices are within [-1, 1]

        Returns:
            None
        """
        mx = np.max(self.vertices, axis=0)
        mn = np.min(self.vertices, axis=0)
        centroid = (mx+mn) / 2
        self.vertices -= centroid
        scale = np.max(np.abs(self.vertices))
        if scale > 0:  # Scale could be zero for a single point or repeated point.
            self.vertices /= scale

    def rotate(self, yaw, pitch, roll):
        """Rotates the object about the origin (0,0,0)

        Args:
            yaw: Rotation about the z-axis in radians.
            pitch: Rotation about the y-axis in radians.
            roll: Rotation about the x-axis in radians.

        Returns:
            None
        """
        a, b, r = yaw, pitch, roll
        cos = np.cos
        sin = np.sin
        rot_mat = np.array([
            [cos(a)*cos(b), cos(a)*sin(b)*sin(r)-sin(a)*cos(r), cos(a)*sin(b)*cos(r)+sin(a)*sin(r)],
            [sin(a)*cos(b), sin(a)*sin(b)*sin(r)+cos(a)*cos(r), sin(a)*sin(b)*cos(r)-cos(a)*sin(r)],
            [-sin(b), cos(b)*sin(r), cos(b)*cos(r)]
        ])
        self.vertices = self.vertices @ rot_mat