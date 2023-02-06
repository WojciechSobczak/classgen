from dataclasses import dataclass
import jinja2
from classgen.code_generator import CodeGenerator

@dataclass
class JinjaTemplate:
    environment: jinja2.Environment
    template: jinja2.Template

class JinjaCodeGenerator(CodeGenerator):

    def __init__(self) -> None:
        self.templates: dict[str, JinjaTemplate] = {}
        super().__init__()

    def load_template(self, name: str, path: str) -> JinjaTemplate:
        if self.templates.get(name) == None:
            with open(path, "r", encoding="UTF-8") as file:
                text_template = file.read()
            environment = jinja2.Environment()
            template = environment.from_string(text_template)
            self.setup_environment(environment)
            self.templates[name] = JinjaTemplate(environment, template)
        return self.templates[name]

    def setup_environment(self, environment: jinja2.Environment):
        pass