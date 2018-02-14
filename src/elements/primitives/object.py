from src.elements.primitives import *
from src.elements.primitives.handler import Handler

from src.elements.primitives.rectangle import Rectangle
from src.elements.properties.color import Color
from src.elements.properties.point import Point
from src.elements.properties.size import Size


class Object(Rectangle):
    def __init__(self):
        Rectangle.__init__(self)

        self.handler = Handler()

        self.pivot = Point()
        self.offset = Point()

        self.is_selected = False

        self.is_resizing = False
        self.direction = NONE

        self.z_index = 0

        self.fill_color = Color(0.25, 0.25, 0.25, 1.0)
        self.stroke_color = Color(1, 1, 1, 1)
        self.stroke_width = 0

        self.is_line = False

    # Define position for controls
    def initialize_controls(self):
        raise NotImplementedError

    def draw(self, context):

        if self.is_selected:
            # Cannot change handler dimension if line
            if not self.is_line:
                self.handler.set_dimensions(self.x, self.y, self.width, self.height)
            self.initialize_controls()
            self.handler.draw(context)

    # Returns True if x,y lies inside controls
    def inside_position(self, x, y):
        if not len(self.handler.controls):
            return False
        return (x >= (self.x - self.handler.controls[0].size / 2.0)) and (
            x <= (self.x + self.width + self.handler.controls[0].size / 2.0)) and (
                   y >= (self.y - self.handler.controls[0].size / 2.0)) and (
                   y <= (self.y + self.height + self.handler.controls[0].size / 2.0))

    # Returns true if current object lies inside a area
    def in_region(self, x, y, width, height):
        if width < 0:
            x += width
            width *= -1
        if height < 0:
            y += height
            height *= -1
        return (x + width) > self.x and (y + height) > self.y and x < (self.x + self.width) and y < (
            self.y + self.height)

    # checks if current object is inside a selection window
    def inside_selection(self, selection):
        return self.in_region(selection.x, selection.y, selection.width, selection.height)

    # Resize object based on new x,y
    def resize(self, new_x, new_y):

        direction = self.direction

        point = Point()
        point.x = self.x
        point.y = self.y

        size = Size()
        size.width = self.width
        size.height = self.height

        direction = get_direction(direction)

        if direction is not VERTICAL:
            size.width = new_x - self.pivot.x
            if size.width < 0:
                point.x = new_x
            else:
                point.x = self.pivot.x

        if direction is not HORIZONTAL:
            size.height = new_y - self.pivot.y
            if size.height < 0:
                point.y = new_y
            else:
                point.y = self.pivot.y

        self.set_point(point)
        self.set_size(size)
