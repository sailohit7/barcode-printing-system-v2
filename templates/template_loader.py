import json

from validators.template_validator import TemplateValidator


validator = TemplateValidator()


def load_template(template_path):

    with open(template_path, "r") as f:

        template = json.load(f)

    validator.validate(template)

    return template