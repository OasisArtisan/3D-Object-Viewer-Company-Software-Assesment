"""Includes the Projector interface as well as all of its implementations"""

from abc import ABC, abstractmethod


class Projector(ABC):
    """Exposes a single function to project 3D vertices onto the screen."""

    @abstractmethod
    def project(self, vertices):
        """Takes an Nx3 matrix representing 3D vertices and projects them onto
        the 2D screen returning an Nx2 numpy matrix

        Args:
            vertices: A numpy Nx3 matrix representing 3D vertices
        Returns:
            Nx2 numpy matrix representing the 2D projection
        """
        pass


class OrthographicProjector(Projector):
    """Implements orthographic projection

    Assumes infinite focal length and infinite distance to the screen
    Read more https://en.wikipedia.org/wiki/Orthographic_projection
    """
    def project(self, vertices):
        """See base class"""

        assert len(vertices.shape) == 2
        assert vertices.shape[0] > 0
        assert vertices.shape[1] == 3

        return vertices[:, :2]


class PerspectiveProjector(Projector):
    def project(self, vertices):
        # TODO
        raise NotImplementedError()