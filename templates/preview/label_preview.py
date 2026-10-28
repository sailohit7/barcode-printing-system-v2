# preview/label_preview.py

class LabelPreview:

    def __init__(self, template):

        self.template = template

    def generate_layout(self):

        layout = []

        for field in self.template["fields"]:

            element = {
                "type": field["type"],
                "x": field["x"],
                "y": field["y"],
                "key": field["key"]
            }

            layout.append(element)

        return layout