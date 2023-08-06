
# region [Imports]

# * Standard Library Imports -->
import os
import configparser
from typing import Union, Callable, List, Set, Tuple, Iterable
from datetime import datetime, timedelta
from pprint import pprint
import re
# * Third Party Imports -->
from fuzzywuzzy import fuzz

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from gidconfig.data.enums import Get
from gidconfig.utility.functions import readit
# endregion [Imports]


# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]


class ConfigHandler(configparser.ConfigParser):
    def __init__(self, config_file=None, auto_read=True, auto_save=True, allow_no_value=True, **kwargs):
        super().__init__(**kwargs, allow_no_value=allow_no_value)
        self.config_file = '' if config_file is None else config_file
        self.auto_read = auto_read
        self.auto_save = auto_save
        self._method_select = {Get.basic: self.get, Get.boolean: self.getboolean, Get.int: self.getint, Get.list: self.getlist, Get.path: self.get_path, Get.datetime: self.get_datetime}
        self.annotation_replacements = {'[DEFAULT]': 'Options in this section are used if those options are not set in a Section'}
        if self.auto_read is True:
            self.read(self.config_file)

    def getlist(self, section, option, delimiter=',', as_set=False, casefold_items=False, fallback_option: str = None):
        _raw = self.get(section, option, fallback=self.get(section, fallback_option) if fallback_option is not None else fallback_option).strip()
        if _raw.endswith(delimiter):
            _raw = _raw.rstrip(delimiter)
        if _raw.startswith(delimiter):
            _raw = _raw.lstrip(delimiter).strip()
        _out = _raw.replace(delimiter + ' ', delimiter).split(delimiter)
        _out = list(map(lambda x: x.strip(), _out))
        if casefold_items is True:
            _out = list(map(lambda x: x.casefold(), _out))
        if as_set is True:
            _out = set(_out)
        return _out

    def list_from_keys_only(self, section, as_set=True):
        _result = self.options(section)
        _out = []
        for line in _result:
            if line != '':
                _out.append(line)
        if as_set is True:
            _out = set(_out)
        return _out

    def get_path(self, section, option, cwd_symbol='+cwd+'):
        _raw_path = self.get(section, option)
        if cwd_symbol in _raw_path:
            _out = _raw_path.replace(cwd_symbol, os.getcwd()).replace('\\', '/')
        elif '+userdata+' in _raw_path:
            _out = _raw_path.replace('+userdata+', os.getenv('APPDATA')).replace('\\', '/')
        elif _raw_path == 'notset':
            _out = None
        else:
            _out = os.path.join(_raw_path).replace('\\', '/')
        return _out

    def _best_fuzzymatch(self, in_term, in_targets: Union[list, set, frozenset, tuple, dict]):
        # Todo: replace with process.extractOne() from fuzzywuzzy!
        _rating_list = []
        for _target in in_targets:
            _rating_list.append((_target, fuzz.ratio(in_term, _target)))
        _rating_list.sort(key=lambda x: x[1], reverse=True)
        log.debug("with a fuzzymatch, the term '%s' was best matched to '%s' with and Levenstein-distance of %s", in_term, _rating_list[0][0], _rating_list[0][1])
        return _rating_list[0][0]

    def get_timedelta(self, section, option, amount_seperator=' ', delta_seperator=','):
        _raw_timedelta = self.get(section, option)
        if _raw_timedelta != 'notset':
            _raw_timedelta_list = _raw_timedelta.split(delta_seperator)
            _arg_dict = {'days': 0,
                         'seconds': 0,
                         'microseconds': 0,
                         'milliseconds': 0,
                         'minutes': 0,
                         'hours': 0,
                         'weeks': 0}
            for raw_delta_data in _raw_timedelta_list:
                _amount, _typus = raw_delta_data.strip().split(amount_seperator)
                _key = self._best_fuzzymatch(_typus, _arg_dict)
                _arg_dict[_key] = float(_amount) if '.' in _amount else int(_amount)
            return timedelta(**_arg_dict)

    def get_datetime(self, section, option, dtformat=None):
        _date_time_string = self.get(section, option)
        if _date_time_string == "notset":
            return None
        _dtformat = '%Y-%m-%d %H:%M:%S' if dtformat is None else dtformat
        return datetime.strptime(_date_time_string, _dtformat).astimezone()

    def set_datetime(self, section, option, datetime_object, dtformat=None):
        _dtformat = '%Y-%m-%d %H:%M:%S' if dtformat is None else format
        self.set(section, option, datetime_object.strftime(_dtformat))
        if self.auto_save is True:
            self.save()

    def set(self, section, option, value):
        if isinstance(value, list):
            value = ', '.join(list(map(str, value)))
        if not isinstance(value, str):
            value = str(value)
        super().set(section, option, value)
        if self.auto_save is True:
            self.save()

    def enum_get(self, section: str, option: str, typus: Get = Get.basic):
        return self._method_select.get(typus, self.get)(section, option)

    def save(self):
        with open(self.config_file, 'w') as confile:
            self.write(confile)
        self.read()

    def read(self, filename=None):
        _configfile = self.config_file if filename is None else filename
        super().read(_configfile)

    def set_annotation_replacement(self, replacements: dict):
        for key, value in replacements.items():
            self.annotation_replacements[key] = value

    def get_annotated_config(self):
        content = readit(self.config_file)
        for target, annotation in self.annotation_replacements.items():
            replacement = f";; {annotation}\n{target}"
            content = content.replace(target, replacement)
        return content

    def __contains__(self, item: object):
        return item in self.sections()

    def __str__(self):
        return os.path.splitext(os.path.basename(self.config_file))[0].upper()


class SingleAccessConfigHandler(ConfigHandler):
    bool_true_values = {'yes', '1', 'true', '+', 'y', 'on', 'enabled', 'positive'}
    bool_false_values = {'no', '0', 'false', '-', 'n', 'off', 'disabled', 'negative'}

    def __init__(self, config_file=None, auto_read=True, auto_save=True, allow_no_value=True, list_delimiter=',', comment_marker='#', top_comment: Union[str, list, tuple] = None, comment_prefixes='~', ** kwargs):
        self.section_comments = {}
        self.comment_marker = comment_marker
        self.top_comment = self._validate_top_comment(top_comment)
        self.top_comment_regex = re.compile(r"^.*?(?=\n\[)", re.DOTALL)
        self.section_header_chars = {'top': '▲', 'bottom': '▼', 'middle': '▌'}
        super().__init__(config_file=config_file, auto_read=auto_read, auto_save=auto_save, allow_no_value=allow_no_value, comment_prefixes='~', ** kwargs)
        self.list_delimiter = list_delimiter

        self.section_header_size = 150
        self.typus_table = {str: str,
                            int: int,
                            float: float,
                            list: self._as_list,
                            List: self._as_list,
                            List[str]: self._as_list,
                            List[int]: self._as_list_int,
                            List[float]: self._as_list_float,
                            set: self._as_set,
                            Set: self._as_set,
                            Set[str]: self._as_set,
                            Set[int]: self._as_set_int,
                            Set[float]: self._as_set_float,
                            tuple: self._as_tuple,
                            Tuple: self._as_tuple,
                            Tuple[str]: self._as_tuple,
                            Tuple[int]: self._as_tuple_int,
                            Tuple[float]: self._as_tuple_float,
                            bool: self._as_bool}

    def _validate_top_comment(self, top_comment):
        if isinstance(top_comment, str):
            top_comment = top_comment.splitlines()
        _out = []
        for line in top_comment:
            if not line.startswith(self.comment_marker):
                line = f"{self.comment_marker} {line.strip()}"
            _out.append(line)
        return '\n'.join(_out)

    def retrieve(self, section, option, typus=str, *, fallback_section: str = None, fallback_option: str = None, direct_fallback=None, mod_func: Callable = None):
        raw_data = self.get(section=section, option=option, fallback=None)
        if raw_data in [None, '']:
            if direct_fallback is not None:
                return direct_fallback
            if fallback_option is not None:
                fallback_section = section if fallback_section is None else fallback_section
                raw_data = self.get(fallback_section, fallback_option)
            else:
                if self.has_section(section) is False:
                    raise configparser.NoSectionError(section)
                elif self.has_option(section, option) is False:
                    raise configparser.NoOptionError(option, section)
        data = self.typus_table.get(typus)(raw_data)
        if mod_func is not None:
            if type(data) in [list, tuple, set]:
                data = type(data)(map(mod_func, data))
            else:
                data = mod_func(data)
        return data

    def _as_list(self, raw_data):
        raw_data = raw_data.strip(self.list_delimiter).strip()

        list_data = raw_data.split(self.list_delimiter)
        return list(map(lambda x: x.strip(), list_data))

    def _as_list_int(self, raw_data):
        list_data = self._as_list(raw_data)
        return list(map(int, list_data))

    def _as_list_float(self, raw_data):
        list_data = self._as_list(raw_data)
        return list(map(float, list_data))

    def _as_set(self, raw_data):
        return set(self._as_list(raw_data))

    def _as_set_int(self, raw_data):
        return set(self._as_list_int(raw_data))

    def _as_set_float(self, raw_data):
        return set(self._as_list_float(raw_data))

    def _as_tuple(self, raw_data):
        return tuple(self._as_list(raw_data))

    def _as_tuple_int(self, raw_data):
        return tuple(self._as_list_int(raw_data))

    def _as_tuple_float(self, raw_data):
        return tuple(self._as_list_float(raw_data))

    def _as_bool(self, raw_data):
        raw_data = raw_data.casefold()
        if raw_data in self.bool_true_values:
            return True
        if raw_data in self.bool_false_values:
            return False
        else:
            raise ValueError(f"'{raw_data}' can not converted to a bool value")

    def _make_section_header(self, section):
        section = f" {section.upper()} "
        top = f'{self.comment_marker} {self.section_header_chars.get("top")*self.section_header_size}'
        middle = f'{self.comment_marker} {section.center(self.section_header_size, self.section_header_chars.get("middle"))}'
        bottom = f'{self.comment_marker} {self.section_header_chars.get("bottom")*self.section_header_size}'
        return '\n'.join(['\n', top, middle, bottom, '\n'])

    def _reset_section_comments(self, filename=None):
        filename = self.config_file if filename is None else filename
        _new_content = []
        with open(filename, 'r') as f:
            old_content = f.read()
        content_lines = old_content.splitlines()
        for index, line in enumerate(content_lines):
            for key, value in self.section_comments.items():
                if line == f'[{key}]':
                    line = self._make_section_header(key) + '\n'.join(value + [f'[{key}]'])
            if not line.startswith(self.comment_marker) and line != '' and not line.startswith('\t') and not content_lines[index + 1].startswith('\t'):
                line = line + '\n'
            _new_content.append(line)
        with open(filename, 'w') as f:
            if self.top_comment is not None:
                f.write(self._make_section_header('instructions') + '\n')
                f.write(self.top_comment + '\n\n' + f'# {"-"*self.section_header_size}\n\n')
            f.write('\n'.join(_new_content))

    def write(self, filename=None):
        filename = self.config_file if filename is None else filename
        with open(filename, 'w') as f:
            super().write(f)
        self._reset_section_comments(filename)

    def read(self, filename=None):
        _configfile = [self.config_file] if filename is None else filename
        _cleaned_content = []
        _buffered_comment_lines = []
        _current_section = None
        with open(_configfile, 'r') as f:
            content_lines = f.read().splitlines()
        for line in reversed(content_lines):

            if line.startswith('['):
                _current_section = line.strip('[]')

            elif line.startswith(f"{self.comment_marker} {self.section_header_chars.get('top')}") or line.startswith(f"{self.comment_marker} {self.section_header_chars.get('middle')}") or line.startswith(f"{self.comment_marker} {self.section_header_chars.get('bottom')}"):
                line = None
            elif _current_section is not None and line.startswith(self.comment_marker):
                _buffered_comment_lines.append(line)
                line = None
            elif _current_section is not None and not line.startswith(self.comment_marker):
                self.section_comments[_current_section] = _buffered_comment_lines
                _current_section = None
                _buffered_comment_lines = []

            if line is not None:
                _cleaned_content.append(line)
        content = self.top_comment_regex.sub('', '\n'.join(reversed(_cleaned_content)))
        super().read_string(content)


if __name__ == '__main__':
    pass
