from src.elements.tools.paper import Paper


class Page(Paper):
    def __init__(self):
        Paper.__init__(self)

        self.children = list()

    def draw(self, context):
        # Draw paper
        Paper.draw(self, context)

        # Draw child elements in page
        for shape in sorted(self.children, key=lambda s: s.z_index):
            shape.draw(context)

    def add_child(self, child):
        self.children.append(child)

    def delete_object(self, child):
        if child.is_selected:
            self.children.remove(child)

    def get_children(self):
        return self.children
