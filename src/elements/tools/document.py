from src.elements.primitives import NONE


class Document:
    def __init__(self):
        self.pages = list()

    def draw(self, context, border, zoom):
        for i, page in enumerate(self.pages):
            page.y = i * page.height + border * (i + 1) / zoom
            page.x = border / zoom

            page.draw(context)

    def get_current_page(self):
        return self.pages[0]

    # Direction of for any child inside current point
    def get_direction_for_child_at_post(self, x, y):
        for child in self.get_current_page().children:
            if child.is_selected and child.handler.inside_position(x, y):
                direction = child.handler.get_direction(x, y)
                return direction
        return NONE

    def delete_children(self):
        for child in self.get_current_page().get_children():
            self.get_current_page().delete_object(child)

    def deselect_children(self):
        for child in self.get_current_page().get_children():
            child.is_selected = False

    def select_children(self):
        for child in self.get_current_page().get_children():
            child.is_selected = True

    def add_child(self, new_child):
        self.get_current_page().add_child(new_child)

    @staticmethod
    def draw_children(page, context):
        for child in page.get_children():
            # Deselect all child to ensure handlers and controllers does not get drawn
            child.is_selected = False
            child.draw(context)
