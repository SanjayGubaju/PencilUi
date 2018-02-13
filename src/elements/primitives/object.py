from src.elements.primitives import *

from src.elements.primitives.rectangle import Rectangle
from src.elements.properties.color import Color
from src.elements.properties.point import Point
from src.elements.properties.position import Position
from src.elements.properties.size import Size


class Object(Rectangle):
    def __init__(self):
        Rectangle.__init__(self)

        self.pivot = Point()

        self.is_selected = False

        self.is_resizing = False
        self.direction = NONE

        self.z_index = 0

        self.fill_color = Color(0.25, 0.25, 0.25, 1.0)
        self.stroke_color = Color(1, 1, 1, 1)
        self.stroke_width = 0

    def draw(self, context):
        pass

    def inside_position(self, x, y):
        return self.x <= x <= (self.x + self.width) and self.y <= y <= (self.y + self.height)

    def in_region(self, x, y, width, height):
        if width < 0:
            x += width
            width *= -1
        if height < 0:
            y += height
            height *= -1
        return (x + width) > self.x and (y + height) > self.y and \
               x < (self.x + self.width) and y < (self.y + self.height)

    def inside_selection(self, selection):
        return self.in_region(selection.x, selection.y, selection.width, selection.height)

    def resize(self, new_x, new_y):

        direction = self.direction

        position = Position()
        position.x = self.x
        position.y = self.y

        size = Size()
        size.x = self.x
        size.y = self.y

        direction = get_direction(direction)

        if direction is not VERTICAL:
            size.width = new_x - self.pivot.x
            if size.width < 0:
                position.x = new_x
            else:
                position.x = self.pivot.x

        if direction is not HORIZONTAL:
            size.height = new_y - self.pivot.y
            if size.height < 0:
                position.y = new_y
            else:
                position.y = self.pivot.y

        self.set_position(position)
        self.set_size(size)
