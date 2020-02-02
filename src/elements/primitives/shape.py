from src.elements.primitives.line import Line
from src.elements.primitives.rounded import Rounded


class Shape(object):
    def __init__(self):
        pass

    def get_shape(self, shape_name):
        if shape_name == "Rectangle":
            return Rounded()
        if shape_name == "Line":
            return Line()
