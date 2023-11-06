"""Contains static methods for loading and saving Object instances

Apart from standard .obj formats, this module contains support for the neocis format described as follows:
    - The first line contains two integers. The first integer is the number of vertices that define the 3D
      object, and the second number is the number of faces that define the 3D object.

    - Starting at the second line each line will define one vertex of the 3D object and will consist of an
      integer followed by three real numbers. The integer is the ID of the vertex and the three real
      numbers define the (x,y,z) coordinates of the vertex. The number of lines in this section will be
      equal to the first integer in the file.

    - Following the vertex section will be a section defining the faces of the 3D object. The number of
      lines in this section will be equal to the second integer on the first line of the file. Each line in
      this section will consist of three integers that define a triangle that is a face of the object. The
      three integers each refer to the ID of a vertex from the second section of the file.

Typical usage example:
    obj = load_object_neo("object.txt")
"""

from Object import Object


def load_object(file_path) -> Object:
    """Determines the appropriate file loader from the extension and attempts to load the file"""
    if file_path.endswith(".txt") or file_path.endswith(".neo"):
        return load_object_neo(file_path)
    elif file_path.endswith(".obj"):
        return load_object_obj(file_path)
    else:
        raise Exception("Unrecognized file format.")


def save_object(file_path, obj: Object) -> None:
    """Saves an Object instance to disk using the format specified by the extension."""

    if file_path.endswith(".txt") or file_path.endswith(".neo"):
        save_object_neo(file_path, obj)
    elif file_path.endswith(".obj"):
        save_object_obj(file_path, obj)
    else:
        raise Exception("Unrecognized file format.")


def load_object_neo(file_path) -> Object:
    """Creates an Object instance from a file in the neocis format.

    Arguments:
        file_path: path to the file containing the 3D object information in neocis format.

    Returns:
        An Object object representing the file contents.

    Raises:
        OSError: if file_path was not reachable.
    """
    with open(file_path) as f:
        n_vertices, n_faces = [int(x) for x in f.readline().split(",")]

        vertices = [None] * n_vertices
        faces = [None] * n_faces

        for i in range(n_vertices):
            v_id, x, y, z = [float(x) for x in f.readline().split(",")]
            vertices[int(v_id) - 1] = (x, y, z)

        for j in range(n_faces):
            v_id1, v_id2, v_id3 = [int(x)-1 for x in f.readline().split(",")]
            faces[j] = (v_id1, v_id2, v_id3)

    return Object(vertices, faces)


def save_object_neo(file_path, obj: Object) -> None:
    """Saves an Object instance to disk using the neocis format.

    Args:
        file_path: the path of where to save the file
        obj: The Object instance to be saved

    Returns:
        None

    Raises:
        OSError: if file_path included non-existent directories or if the directory was not writable.
    """
    with open(file_path, "w") as f:
        f.write(f"{len(obj.vertices)},{len(obj.faces)}\n")
        for i,v in enumerate(obj.vertices):
            f.write(f"{i+1},{','.join([str(x) for x in v])}\n")
        for face in obj.faces:
            f.write(f"{','.join([str(x+1) for x in face])}\n")


def load_object_obj(file_path) -> Object:
    """Creates an Object instance from a file in the obj format.

    Arguments:
        file_path: path to the file containing the 3D object information in neocis format.

    Returns:
        An Object object representing the file contents.

    Raises:
        OSError: if file_path was not reachable.
    """
    vertices = list()
    faces = list()
    with open(file_path) as f:
        for l in f.readlines():
            tokens = l.split(" ")
            if tokens[0] == "v":
                vertices.append([float(x) for x in tokens[1:]])
            if tokens[0] == "f":
                faces.append([int(x)-1 for x in tokens[1:]])

    return Object(vertices, faces)


def save_object_obj(file_path, obj: Object) -> None:
    """Saves an Object instance to disk using the obj format.

    Args:
        file_path: the path of where to save the file
        obj: The Object instance to be saved

    Returns:
        None

    Raises:
        OSError: if file_path included non-existent directories or if the directory was not writable.
    """
    with open(file_path, "w") as f:
        for v in obj.vertices:
            f.write(f"v {' '.join([str(x) for x in v])}\n")
        for face in obj.faces:
            f.write(f"f {' '.join([str(x+1) for x in face])}\n")