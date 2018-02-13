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
