from django.utils import timezone

from django_test_tools import __version__ as current_version
from ..app_manager import DjangoAppManager


class FactoryBoyGenerator(object):
    """
    Currently supporting:

        - BooleanField
        - CharField
        - CountryField: from https://github.com/SmileyChris/django-countries
        - DateField:
        - DateTimeField
        - DecimalField
        - ForeignKey
        - GenericIPAddressField
        - IntegerField
        - MoneyField: from https://github.com/django-money/django-money
        - TextField

    The following fields are ignored by default 'AutoField', 'AutoCreatedField', 'AutoLastModifiedField'
    """

    def __init__(self, **kwargs):
        self.app_manager = DjangoAppManager()
        self.read_only_fields = ['AutoField', 'AutoCreatedField', 'AutoLastModifiedField']
        self.fields_to_ignore = []
        self.default_countries = kwargs.get('default_countries', ['PA', 'US', 'GB'])
        # names that if are varchar will be filled with digits
        self.numerical_identifiers = kwargs.get('numerical_identifiers', ['id', 'num', ])
        # max_length to consider an alpha numeric code is below or equal a string of letters will be used
        self.code_threshold = kwargs.get('code_threshold', 5)

    def create_template_data(self, app_name):
        app_data = self.app_manager.get_app_data(app_name)
        template_data = dict()
        template_data['models'] = dict()
        template_data['app_name'] = app_data['app_name']
        for model_key in app_data['models'].keys():
            template_data['models'][model_key] = dict()
            template_data['models'][model_key]['model_name'] = app_data['models'][model_key]['model_name']
            template_data['models'][model_key]['package_name'] = '{}.{}'.format(app_data['app_name'],
                                                                                app_data['models'][model_key][
                                                                                    'model_name'])

            template_data['models'][model_key]['fields'] = list()
            if app_data['models'][model_key].get('original_attrs'):
                if app_data['models'][model_key].get('original_attrs').get('unique_together'):
                    template_data['models'][model_key]['unique_together'] = app_data['models'][model_key].get(
                        'original_attrs').get('unique_together')

            for field in app_data['models'][model_key]['fields']:
                field_dict = dict()
                field_dict['field_name'] = field['field_name']
                field_dict['type'] = field['type']
                field_dict['is_supported'] = True
                if field['type'] in self.read_only_fields or field['type'] in self.fields_to_ignore:
                    pass
                else:
                    method_name = 'get_{}_factory'.format(field['type'].lower())
                    if hasattr(self, method_name):
                        field_dict['factory'] = getattr(self, method_name)(field, template_data['models'][model_key])
                        template_data['models'][model_key]['fields'].append(field_dict)
                    else:
                        field_dict['is_supported'] = False
                        template_data['models'][model_key]['fields'].append(field_dict)
        return template_data

    def get_booleanfield_factory(self, *args, **kwargs):
        return 'Iterator([True, False])'

    def get_countryfield_factory(self, *args, **kwargs):
        country_list_str = ''
        for country in self.default_countries:
            country_list_str += '\'{}\', '.format(country)
        template = 'Iterator([{}])'
        return template.format(country_list_str.strip())

    def get_charfield_factory(self, *args, **kwargs):
        if args[0].get('choices'):
            template = 'Iterator({choices}, getter=lambda x: x[0])'
            return template.format(**args[0])

        if self._is_number(args[0]['field_name']):
            template = 'LazyAttribute(lambda x: FuzzyText(length={max_length}, chars=string.digits).fuzz())'
            return template.format(**args[0])

        if args[0]['max_length'] > self.code_threshold:
            template = 'LazyAttribute(lambda x: faker.text(max_nb_chars={max_length}))'
            return template.format(**args[0])
        else:
            template = 'LazyAttribute(lambda x: FuzzyText(length={max_length}, chars=string.ascii_letters).fuzz())'
            return template.format(**args[0])

    def get_datefield_factory(self, *args, **kwargs):
        config = {'start_date': kwargs.get('start_date', '-1y'),
                  'end_date': kwargs.get('end_date', 'today')}
        template = 'LazyAttribute(lambda x: faker.date_between(start_date="{start_date}", ' \
                   'end_date="{end_date}", tzinfo=timezone(settings.TIME_ZONE)))'
        return template.format(**config)

    def get_datetimefield_factory(self, *args, **kwargs):
        config = {'start_date': kwargs.get('start_date', '-1y'),
                  'end_date': kwargs.get('end_date', 'now')}
        template = 'LazyAttribute(lambda x: faker.date_time_between(start_date="{start_date}", ' \
                   'end_date="{end_date}", tzinfo=timezone(settings.TIME_ZONE)))'
        return template.format(**config)

    def get_decimalfield_factory(self, *args, **kwargs):
        config = {
            'left_digits': args[0]['max_digits'] - args[0]['decimal_places'],
            'right_digits': args[0]['decimal_places'],
            'positive': kwargs.get('positive', True)
        }
        template = 'LazyAttribute(lambda x: faker.pydecimal(left_digits={left_digits}, ' \
                   'right_digits={right_digits}, positive={positive}))'
        return template.format(**config)

    def get_filefield_factory(self, *args, **kwargs):
        config = {'filename': kwargs.get('filename', args[0]['field_name']),
                  'extension': kwargs.get('extension', 'txt'), }
        template = 'FileField(filename=\'{filename}.{extension}\')'
        return template.format(**config)

    def get_foreignkey_factory(self, *args, **kwargs):
        config = {'model_name': args[0]['remote_field']}
        template = 'SubFactory({model_name}Factory)'
        return template.format(**config)

    def get_genericipaddressfield_factory(self, *args, **kwargs):
        config = {'network': False}
        template = 'LazyAttribute(lambda o: faker.ipv4(network={network}))'
        return template.format(**config)

    def get_integerfield_factory(self, *args, **kwargs):
        config = {'min_value': kwargs.get('min_value', 3),
                  'max_value': kwargs.get('max_value', 3), }
        template = 'LazyAttribute(lambda o: randint({min_value}, {max_value}))'
        return template.format(**config)

    def get_moneyfield_factory(self, *args, **kwargs):
        factory = self.get_decimalfield_factory(*args, **kwargs)
        return factory

    def get_textfield_factory(self, *args, **kwargs):
        config = {'sentences': kwargs.get('sentences', 3)}
        template = 'LazyAttribute(lambda x: faker.paragraph(nb_sentences={sentences}, variable_nb_sentences=True))'
        return template.format(**config)

    def _is_number(self, field_name):
        for nv in self.numerical_identifiers:
            if nv in field_name.lower():
                return True
        return False


class ModelSerializerGenerator(object):

    def __init__(self, **kwargs):
        self.app_manager = DjangoAppManager()
        self.field_types_to_ignore = kwargs.get('field_types_to_ignore', [])

    def create_template_data(self, app_name):
        app_data = self.app_manager.get_app_data(app_name)
        template_data = dict()
        template_data['template_data'] = dict()
        template_data['template_data']['version'] = current_version
        template_data['template_data']['generation_date'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        template_data['template_data']['tz'] = str(timezone.now().tzinfo)

        template_data['models'] = dict()
        template_data['app_name'] = app_data['app_name']
        for model_key in app_data['models'].keys():
            template_data['models'][model_key] = dict()
            template_data['models'][model_key]['model_name'] = app_data['models'][model_key]['model_name']
            template_data['models'][model_key]['package'] = app_data['app_name']
            template_data['models'][model_key]['qualified_name'] = '{}.{}'.format(app_data['app_name'],
                                                                                  app_data['models'][model_key][
                                                                                      'model_name'])
            template_data['models'][model_key]['has_ignored_fields'] = False
            template_data['models'][model_key]['has_foreign_keys'] = False
            template_data['models'][model_key]['fields'] = list()

            for field in app_data['models'][model_key]['fields']:
                field_dict = dict()
                field_dict['field_name'] = field['field_name']
                field_dict['type'] = field['type']
                field_dict['is_included'] = True
                if field.get('remote_field'):
                    field_dict['foreign_key'] = field.get('remote_field')
                    template_data['models'][model_key]['has_foreign_keys'] = True
                if field['type'] in self.field_types_to_ignore:
                    field_dict['is_included'] = False
                    field_dict['is_ignored'] = True
                    template_data['models'][model_key]['has_ignored_fields'] = True

                template_data['models'][model_key]['fields'].append(field_dict)

                # else:
                #     method_name = 'get_{}_factory'.format(field['type'].lower())
                #     if hasattr(self, method_name):
                #         field_dict['factory'] = getattr(self, method_name)(field, template_data['models'][model_key])
                #         template_data['models'][model_key]['fields'].append(field_dict)
                #     else:
                #         field_dict['is_supported'] = False
                #         template_data['models'][model_key]['fields'].append(field_dict)
        return template_data
