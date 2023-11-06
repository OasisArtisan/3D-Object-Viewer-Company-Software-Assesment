import argparse

from ObjectIO import load_object
from TkinterGUI import TkinterGUI
from Projector import OrthographicProjector
from Renderer import WireframeRenderer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='[Redacted] Software Assessment')
    parser.add_argument("-f", "--filepath", type=str, default="sample_objects/object.txt",
                        help="Specify the 3D object file to open. Otherwise the default object.txt is opened")
    args = parser.parse_args()

    projector = OrthographicProjector()
    renderer = WireframeRenderer(projector)
    gui = TkinterGUI(renderer)
    obj = load_object(args.filepath)
    gui.put_object(obj)
    gui.wait()
