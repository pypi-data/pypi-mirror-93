from django.template.loader import render_to_string
from jinja2 import Environment, PackageLoader, select_autoescape

from ..templatetags.dtt_filters import to_snake_case


class UrlGenerator(object):

    def __init__(self, model_name):
        self.model_name = model_name
        self.template = 'django_test_tools/urls.py.j2'

    def print_urls(self, filename):
        self._print(filename, 'urls')

    def print_paths(self, filename):
        self._print(filename, 'paths')

    def _print(self, filename, what_to_print):
        data = dict()
        data['model_name'] = self.model_name
        data['print_{}'.format(what_to_print)] = True
        rendered = render_to_string(self.template, data)
        with open(filename, 'w', encoding='utf-8') as url_file:
            url_file.write(rendered)


class SerializerTestGenerator(object):

    def __init__(self):
        self.env = Environment(
            loader=PackageLoader('django_test_tools', 'templates'),
            autoescape=select_autoescape(['html', 'j2'])
        )
        self.env.filters['to_snake_case'] = to_snake_case

        self.template_name = 'django_test_tools/test_serializers.py.j2'
        self.template = self.env.get_template(self.template_name)

    def print(self, serializer_info, filename):
        rendered = self.template.render(serializer_info)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(rendered)


class GenericTemplateWriter(object):

    def __init__(self, template_name, **kwargs):
        trim_blocks = kwargs.get('trim_blocks', False)
        lstrip_blocks = kwargs.get('lstrip_blocks', False)
        self.env = Environment(
            loader=PackageLoader('django_test_tools', 'templates'),
            autoescape=select_autoescape(['html', ],),
            trim_blocks=trim_blocks,
            lstrip_blocks=lstrip_blocks
        )
        self.env.filters['to_snake_case'] = to_snake_case

        self.template_name = 'django_test_tools/{}'.format(template_name)
        self.template = self.env.get_template(self.template_name)

    def write(self, template_data, filename):
        rendered = self.template.render(template_data)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(rendered)
