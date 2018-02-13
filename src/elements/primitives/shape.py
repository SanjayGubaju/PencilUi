from src.elements.primitives.rounded import Rounded


class Shape(object):
    def __init__(self):
        pass

    def get_shape(self, shape_name):
        if shape_name == "Rect":
            return Rounded()
