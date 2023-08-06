#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Wed Apr  1 15:24:32 2020 by generateDS.py version 2.35.15.
# Python 3.8.2 (v3.8.2:7b3ab5921f, Feb 24 2020, 17:52:18)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './pydhl/dct_requestdatatypes_global.py')
#
# Command line arguments:
#   /Users/daniel/Documents/Documentations/DHL/2020-03/schemas/DCTRequestdatatypes_global.xsd
#
# Command line:
#   /Users/daniel/Workspace/Project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./pydhl/dct_requestdatatypes_global.py" /Users/daniel/Documents/Documentations/DHL/2020-03/schemas/DCTRequestdatatypes_global.xsd
#
# Current working directory (os.getcwd()):
#   py-dhl
#

from six.moves import zip_longest
import os
import sys
import re as re_
import base64
import datetime as datetime_
import decimal as decimal_
try:
    from lxml import etree as etree_
except ImportError:
    from xml.etree import ElementTree as etree_


Validate_simpletypes_ = True
SaveElementTreeNode = True
if sys.version_info.major == 2:
    BaseStrType_ = basestring
else:
    BaseStrType_ = str


def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

def parsexmlstring_(instring, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    element = etree_.fromstring(instring, parser=parser, **kwargs)
    return element

#
# Namespace prefix definition table (and other attributes, too)
#
# The module generatedsnamespaces, if it is importable, must contain
# a dictionary named GeneratedsNamespaceDefs.  This Python dictionary
# should map element type names (strings) to XML schema namespace prefix
# definitions.  The export method for any class for which there is
# a namespace prefix definition, will export that definition in the
# XML representation of that element.  See the export method of
# any generated element type class for an example of the use of this
# table.
# A sample table is:
#
#     # File: generatedsnamespaces.py
#
#     GenerateDSNamespaceDefs = {
#         "ElementtypeA": "http://www.xxx.com/namespaceA",
#         "ElementtypeB": "http://www.xxx.com/namespaceB",
#     }
#
# Additionally, the generatedsnamespaces module can contain a python
# dictionary named GenerateDSNamespaceTypePrefixes that associates element
# types with the namespace prefixes that are to be added to the
# "xsi:type" attribute value.  See the exportAttributes method of
# any generated element type and the generation of "xsi:type" for an
# example of the use of this table.
# An example table:
#
#     # File: generatedsnamespaces.py
#
#     GenerateDSNamespaceTypePrefixes = {
#         "ElementtypeC": "aaa:",
#         "ElementtypeD": "bbb:",
#     }
#

try:
    from generatedsnamespaces import GenerateDSNamespaceDefs as GenerateDSNamespaceDefs_
except ImportError:
    GenerateDSNamespaceDefs_ = {}
try:
    from generatedsnamespaces import GenerateDSNamespaceTypePrefixes as GenerateDSNamespaceTypePrefixes_
except ImportError:
    GenerateDSNamespaceTypePrefixes_ = {}

#
# You can replace the following class definition by defining an
# importable module named "generatedscollector" containing a class
# named "GdsCollector".  See the default class definition below for
# clues about the possible content of that class.
#
try:
    from generatedscollector import GdsCollector as GdsCollector_
except ImportError:

    class GdsCollector_(object):

        def __init__(self, messages=None):
            if messages is None:
                self.messages = []
            else:
                self.messages = messages

        def add_message(self, msg):
            self.messages.append(msg)

        def get_messages(self):
            return self.messages

        def clear_messages(self):
            self.messages = []

        def print_messages(self):
            for msg in self.messages:
                print("Warning: {}".format(msg))

        def write_messages(self, outstream):
            for msg in self.messages:
                outstream.write("Warning: {}\n".format(msg))


#
# The super-class for enum types
#

try:
    from enum import Enum
except ImportError:
    Enum = object

#
# The root super-class for element type classes
#
# Calls to the methods in these classes are generated by generateDS.py.
# You can replace these methods by re-implementing the following class
#   in a module named generatedssuper.py.

try:
    from generatedssuper import GeneratedsSuper
except ImportError as exp:
    
    class GeneratedsSuper(object):
        __hash__ = object.__hash__
        tzoff_pattern = re_.compile(r'(\+|-)((0\d|1[0-3]):[0-5]\d|14:00)$')
        class _FixedOffsetTZ(datetime_.tzinfo):
            def __init__(self, offset, name):
                self.__offset = datetime_.timedelta(minutes=offset)
                self.__name = name
            def utcoffset(self, dt):
                return self.__offset
            def tzname(self, dt):
                return self.__name
            def dst(self, dt):
                return None
        def gds_format_string(self, input_data, input_name=''):
            return input_data
        def gds_parse_string(self, input_data, node=None, input_name=''):
            return input_data
        def gds_validate_string(self, input_data, node=None, input_name=''):
            if not input_data:
                return ''
            else:
                return input_data
        def gds_format_base64(self, input_data, input_name=''):
            return base64.b64encode(input_data)
        def gds_validate_base64(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_integer(self, input_data, input_name=''):
            return '%d' % input_data
        def gds_parse_integer(self, input_data, node=None, input_name=''):
            try:
                ival = int(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires integer value: %s' % exp)
            return ival
        def gds_validate_integer(self, input_data, node=None, input_name=''):
            try:
                value = int(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires integer value')
            return value
        def gds_format_integer_list(self, input_data, input_name=''):
            return '%s' % ' '.join(input_data)
        def gds_validate_integer_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    int(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of integer valuess')
            return values
        def gds_format_float(self, input_data, input_name=''):
            return ('%.15f' % input_data).rstrip('0')
        def gds_parse_float(self, input_data, node=None, input_name=''):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires float or double value: %s' % exp)
            return fval_
        def gds_validate_float(self, input_data, node=None, input_name=''):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires float value')
            return value
        def gds_format_float_list(self, input_data, input_name=''):
            return '%s' % ' '.join(input_data)
        def gds_validate_float_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of float values')
            return values
        def gds_format_decimal(self, input_data, input_name=''):
            return ('%s' % input_data).rstrip('0')
        def gds_parse_decimal(self, input_data, node=None, input_name=''):
            try:
                decimal_value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires decimal value')
            return decimal_value
        def gds_validate_decimal(self, input_data, node=None, input_name=''):
            try:
                value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires decimal value')
            return value
        def gds_format_decimal_list(self, input_data, input_name=''):
            return '%s' % ' '.join(input_data)
        def gds_validate_decimal_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    decimal_.Decimal(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of decimal values')
            return values
        def gds_format_double(self, input_data, input_name=''):
            return '%e' % input_data
        def gds_parse_double(self, input_data, node=None, input_name=''):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires double or float value: %s' % exp)
            return fval_
        def gds_validate_double(self, input_data, node=None, input_name=''):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires double or float value')
            return value
        def gds_format_double_list(self, input_data, input_name=''):
            return '%s' % ' '.join(input_data)
        def gds_validate_double_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(
                        node, 'Requires sequence of double or float values')
            return values
        def gds_format_boolean(self, input_data, input_name=''):
            return ('%s' % input_data).lower()
        def gds_parse_boolean(self, input_data, node=None, input_name=''):
            if input_data in ('true', '1'):
                bval = True
            elif input_data in ('false', '0'):
                bval = False
            else:
                raise_parse_error(node, 'Requires boolean value')
            return bval
        def gds_validate_boolean(self, input_data, node=None, input_name=''):
            if input_data not in (True, 1, False, 0, ):
                raise_parse_error(
                    node,
                    'Requires boolean value '
                    '(one of True, 1, False, 0)')
            return input_data
        def gds_format_boolean_list(self, input_data, input_name=''):
            return '%s' % ' '.join(input_data)
        def gds_validate_boolean_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                if value not in (True, 1, False, 0, ):
                    raise_parse_error(
                        node,
                        'Requires sequence of boolean values '
                        '(one of True, 1, False, 0)')
            return values
        def gds_validate_datetime(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_datetime(self, input_data, input_name=''):
            if input_data.microsecond == 0:
                _svalue = '%04d-%02d-%02dT%02d:%02d:%02d' % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = '%04d-%02d-%02dT%02d:%02d:%02d.%s' % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ('%f' % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            return _svalue
        @classmethod
        def gds_parse_datetime(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            time_parts = input_data.split('.')
            if len(time_parts) > 1:
                micro_seconds = int(float('0.' + time_parts[1]) * 1000000)
                input_data = '%s.%s' % (
                    time_parts[0], "{}".format(micro_seconds).rjust(6, "0"), )
                dt = datetime_.datetime.strptime(
                    input_data, '%Y-%m-%dT%H:%M:%S.%f')
            else:
                dt = datetime_.datetime.strptime(
                    input_data, '%Y-%m-%dT%H:%M:%S')
            dt = dt.replace(tzinfo=tz)
            return dt
        def gds_validate_date(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_date(self, input_data, input_name=''):
            _svalue = '%04d-%02d-%02d' % (
                input_data.year,
                input_data.month,
                input_data.day,
            )
            try:
                if input_data.tzinfo is not None:
                    tzoff = input_data.tzinfo.utcoffset(input_data)
                    if tzoff is not None:
                        total_seconds = tzoff.seconds + (86400 * tzoff.days)
                        if total_seconds == 0:
                            _svalue += 'Z'
                        else:
                            if total_seconds < 0:
                                _svalue += '-'
                                total_seconds *= -1
                            else:
                                _svalue += '+'
                            hours = total_seconds // 3600
                            minutes = (total_seconds - (hours * 3600)) // 60
                            _svalue += '{0:02d}:{1:02d}'.format(
                                hours, minutes)
            except AttributeError:
                pass
            return _svalue
        @classmethod
        def gds_parse_date(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            dt = datetime_.datetime.strptime(input_data, '%Y-%m-%d')
            dt = dt.replace(tzinfo=tz)
            return dt.date()
        def gds_validate_time(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_time(self, input_data, input_name=''):
            if input_data.microsecond == 0:
                _svalue = '%02d:%02d:%02d' % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = '%02d:%02d:%02d.%s' % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ('%f' % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            return _svalue
        def gds_validate_simple_patterns(self, patterns, target):
            # pat is a list of lists of strings/patterns.
            # The target value must match at least one of the patterns
            # in order for the test to succeed.
            found1 = True
            for patterns1 in patterns:
                found2 = False
                for patterns2 in patterns1:
                    mo = re_.search(patterns2, target)
                    if mo is not None and len(mo.group(0)) == len(target):
                        found2 = True
                        break
                if not found2:
                    found1 = False
                    break
            return found1
        @classmethod
        def gds_parse_time(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            if len(input_data.split('.')) > 1:
                dt = datetime_.datetime.strptime(input_data, '%H:%M:%S.%f')
            else:
                dt = datetime_.datetime.strptime(input_data, '%H:%M:%S')
            dt = dt.replace(tzinfo=tz)
            return dt.time()
        def gds_check_cardinality_(
                self, value, input_name,
                min_occurs=0, max_occurs=1, required=None):
            if value is None:
                length = 0
            elif isinstance(value, list):
                length = len(value)
            else:
                length = 1
            if required is not None :
                if required and length < 1:
                    self.gds_collector_.add_message(
                        "Required value {}{} is missing".format(
                            input_name, self.gds_get_node_lineno_()))
            if length < min_occurs:
                self.gds_collector_.add_message(
                    "Number of values for {}{} is below "
                    "the minimum allowed, "
                    "expected at least {}, found {}".format(
                        input_name, self.gds_get_node_lineno_(),
                        min_occurs, length))
            elif length > max_occurs:
                self.gds_collector_.add_message(
                    "Number of values for {}{} is above "
                    "the maximum allowed, "
                    "expected at most {}, found {}".format(
                        input_name, self.gds_get_node_lineno_(),
                        max_occurs, length))
        def gds_validate_builtin_ST_(
                self, validator, value, input_name,
                min_occurs=None, max_occurs=None, required=None):
            if value is not None:
                try:
                    validator(value, input_name=input_name)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))
        def gds_validate_defined_ST_(
                self, validator, value, input_name,
                min_occurs=None, max_occurs=None, required=None):
            if value is not None:
                try:
                    validator(value)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))
        def gds_str_lower(self, instring):
            return instring.lower()
        def get_path_(self, node):
            path_list = []
            self.get_path_list_(node, path_list)
            path_list.reverse()
            path = '/'.join(path_list)
            return path
        Tag_strip_pattern_ = re_.compile(r'\{.*\}')
        def get_path_list_(self, node, path_list):
            if node is None:
                return
            tag = GeneratedsSuper.Tag_strip_pattern_.sub('', node.tag)
            if tag:
                path_list.append(tag)
            self.get_path_list_(node.getparent(), path_list)
        def get_class_obj_(self, node, default_class=None):
            class_obj1 = default_class
            if 'xsi' in node.nsmap:
                classname = node.get('{%s}type' % node.nsmap['xsi'])
                if classname is not None:
                    names = classname.split(':')
                    if len(names) == 2:
                        classname = names[1]
                    class_obj2 = globals().get(classname)
                    if class_obj2 is not None:
                        class_obj1 = class_obj2
            return class_obj1
        def gds_build_any(self, node, type_name=None):
            # provide default value in case option --disable-xml is used.
            content = ""
            content = etree_.tostring(node, encoding="unicode")
            return content
        @classmethod
        def gds_reverse_node_mapping(cls, mapping):
            return dict(((v, k) for k, v in mapping.items()))
        @staticmethod
        def gds_encode(instring):
            if sys.version_info.major == 2:
                if ExternalEncoding:
                    encoding = ExternalEncoding
                else:
                    encoding = 'utf-8'
                return instring.encode(encoding)
            else:
                return instring
        @staticmethod
        def convert_unicode(instring):
            if isinstance(instring, str):
                result = quote_xml(instring)
            elif sys.version_info.major == 2 and isinstance(instring, unicode):
                result = quote_xml(instring).encode('utf8')
            else:
                result = GeneratedsSuper.gds_encode(str(instring))
            return result
        def __eq__(self, other):
            def excl_select_objs_(obj):
                return (obj[0] != 'parent_object_' and
                        obj[0] != 'gds_collector_')
            if type(self) != type(other):
                return False
            return all(x == y for x, y in zip_longest(
                filter(excl_select_objs_, self.__dict__.items()),
                filter(excl_select_objs_, other.__dict__.items())))
        def __ne__(self, other):
            return not self.__eq__(other)
        # Django ETL transform hooks.
        def gds_djo_etl_transform(self):
            pass
        def gds_djo_etl_transform_db_obj(self, dbobj):
            pass
        # SQLAlchemy ETL transform hooks.
        def gds_sqa_etl_transform(self):
            return 0, None
        def gds_sqa_etl_transform_db_obj(self, dbobj):
            pass
        def gds_get_node_lineno_(self):
            if (hasattr(self, "gds_elementtree_node_") and
                    self.gds_elementtree_node_ is not None):
                return ' near line {}'.format(
                    self.gds_elementtree_node_.sourceline)
            else:
                return ""
    
    
    def getSubclassFromModule_(module, class_):
        '''Get the subclass of a class from a specific module.'''
        name = class_.__name__ + 'Sub'
        if hasattr(module, name):
            return getattr(module, name)
        else:
            return None


#
# If you have installed IPython you can uncomment and use the following.
# IPython is available from http://ipython.scipy.org/.
#

## from IPython.Shell import IPShellEmbed
## args = ''
## ipshell = IPShellEmbed(args,
##     banner = 'Dropping into IPython',
##     exit_msg = 'Leaving Interpreter, back to program.')

# Then use the following line where and when you want to drop into the
# IPython shell:
#    ipshell('<some message> -- Entering ipshell.\nHit Ctrl-D to exit')

#
# Globals
#

ExternalEncoding = ''
# Set this to false in order to deactivate during export, the use of
# name space prefixes captured from the input document.
UseCapturedNS_ = True
CapturedNsmap_ = {}
Tag_pattern_ = re_.compile(r'({.*})?(.*)')
String_cleanup_pat_ = re_.compile(r"[\n\r\s]+")
Namespace_extract_pat_ = re_.compile(r'{(.*)}(.*)')
CDATA_pattern_ = re_.compile(r"<!\[CDATA\[.*?\]\]>", re_.DOTALL)

# Change this to redirect the generated superclass module to use a
# specific subclass module.
CurrentSubclassModule_ = None

#
# Support/utility functions.
#


def showIndent(outfile, level, pretty_print=True):
    if pretty_print:
        for idx in range(level):
            outfile.write('    ')


def quote_xml(inStr):
    "Escape markup chars, but do not modify CDATA sections."
    if not inStr:
        return ''
    s1 = (isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr)
    s2 = ''
    pos = 0
    matchobjects = CDATA_pattern_.finditer(s1)
    for mo in matchobjects:
        s3 = s1[pos:mo.start()]
        s2 += quote_xml_aux(s3)
        s2 += s1[mo.start():mo.end()]
        pos = mo.end()
    s3 = s1[pos:]
    s2 += quote_xml_aux(s3)
    return s2


def quote_xml_aux(inStr):
    s1 = inStr.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1


def quote_attrib(inStr):
    s1 = (isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    if '"' in s1:
        if "'" in s1:
            s1 = '"%s"' % s1.replace('"', "&quot;")
        else:
            s1 = "'%s'" % s1
    else:
        s1 = '"%s"' % s1
    return s1


def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1


def get_all_text_(node):
    if node.text is not None:
        text = node.text
    else:
        text = ''
    for child in node:
        if child.tail is not None:
            text += child.tail
    return text


def find_attr_value_(attr_name, node):
    attrs = node.attrib
    attr_parts = attr_name.split(':')
    value = None
    if len(attr_parts) == 1:
        value = attrs.get(attr_name)
    elif len(attr_parts) == 2:
        prefix, name = attr_parts
        namespace = node.nsmap.get(prefix)
        if namespace is not None:
            value = attrs.get('{%s}%s' % (namespace, name, ))
    return value


def encode_str_2_3(instr):
    return instr


class GDSParseError(Exception):
    pass


def raise_parse_error(node, msg):
    if node is not None:
        msg = '%s (element %s/line %d)' % (msg, node.tag, node.sourceline, )
    raise GDSParseError(msg)


class MixedContainer:
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    TypeBase64 = 8
    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value
    def getCategory(self):
        return self.category
    def getContenttype(self, content_type):
        return self.content_type
    def getValue(self):
        return self.value
    def getName(self):
        return self.name
    def export(self, outfile, level, name, namespace,
               pretty_print=True):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:    # category == MixedContainer.CategoryComplex
            self.value.export(
                outfile, level, namespace, name_=name,
                pretty_print=pretty_print)
    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write('<%s>%s</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeInteger or \
                self.content_type == MixedContainer.TypeBoolean:
            outfile.write('<%s>%d</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeFloat or \
                self.content_type == MixedContainer.TypeDecimal:
            outfile.write('<%s>%f</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write('<%s>%g</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeBase64:
            outfile.write('<%s>%s</%s>' % (
                self.name,
                base64.b64encode(self.value),
                self.name))
    def to_etree(self, element):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                if len(element) > 0:
                    if element[-1].tail is None:
                        element[-1].tail = self.value
                    else:
                        element[-1].tail += self.value
                else:
                    if element.text is None:
                        element.text = self.value
                    else:
                        element.text += self.value
        elif self.category == MixedContainer.CategorySimple:
            subelement = etree_.SubElement(
                element, '%s' % self.name)
            subelement.text = self.to_etree_simple()
        else:    # category == MixedContainer.CategoryComplex
            self.value.to_etree(element)
    def to_etree_simple(self):
        if self.content_type == MixedContainer.TypeString:
            text = self.value
        elif (self.content_type == MixedContainer.TypeInteger or
                self.content_type == MixedContainer.TypeBoolean):
            text = '%d' % self.value
        elif (self.content_type == MixedContainer.TypeFloat or
                self.content_type == MixedContainer.TypeDecimal):
            text = '%f' % self.value
        elif self.content_type == MixedContainer.TypeDouble:
            text = '%g' % self.value
        elif self.content_type == MixedContainer.TypeBase64:
            text = '%s' % base64.b64encode(self.value)
        return text
    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n' % (
                    self.category, self.content_type,
                    self.name, self.value))
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n' % (
                    self.category, self.content_type,
                    self.name, self.value))
        else:    # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s",\n' % (
                    self.category, self.content_type, self.name,))
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(')\n')


class MemberSpec_(object):
    def __init__(self, name='', data_type='', container=0,
            optional=0, child_attrs=None, choice=None):
        self.name = name
        self.data_type = data_type
        self.container = container
        self.child_attrs = child_attrs
        self.choice = choice
        self.optional = optional
    def set_name(self, name): self.name = name
    def get_name(self): return self.name
    def set_data_type(self, data_type): self.data_type = data_type
    def get_data_type_chain(self): return self.data_type
    def get_data_type(self):
        if isinstance(self.data_type, list):
            if len(self.data_type) > 0:
                return self.data_type[-1]
            else:
                return 'xs:string'
        else:
            return self.data_type
    def set_container(self, container): self.container = container
    def get_container(self): return self.container
    def set_child_attrs(self, child_attrs): self.child_attrs = child_attrs
    def get_child_attrs(self): return self.child_attrs
    def set_choice(self, choice): self.choice = choice
    def get_choice(self): return self.choice
    def set_optional(self, optional): self.optional = optional
    def get_optional(self): return self.optional


def _cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)

#
# Data representation classes.
#


class CUSTAGRINDType(Enum):
    Y='Y'
    N='N'


class DimensionUnitType(Enum):
    """Dimension Unit I (inches);Centimeters (CM)"""
    IN='IN'
    CM='CM'


class FCNTWTYCDType(Enum):
    DD='DD'
    TD='TD'
    AL='AL'


class IsDutiableType(Enum):
    """Y - Dutiable/Non-Doc,
    N - Non-dutiable/Doc"""
    Y='Y'
    N='N'


class NXTPUType(Enum):
    Y='Y'
    N='N'


class NetworkTypeCodeType(Enum):
    DD='DD'
    TD='TD'
    AL='AL'


class OSINFOType(Enum):
    Y='Y'
    N='N'


class PackageTypeCodeType(Enum):
    FLY='FLY'
    COY='COY'
    NCY='NCY'
    PAL='PAL'
    DBL='DBL'
    BOX='BOX'


class PaymentTypeType(Enum):
    """Payment type - by method of payment ( DHL account)"""
    D='D'


class VLDTRT_DDType(Enum):
    Y='Y'
    N='N'


class WeightUnitType(Enum):
    """Kilogram (KG),Pounds (LB)"""
    KG='KG'
    LB='LB'


class DCTRequestDataTypes(GeneratedsSuper):
    """Comment describing your root element"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DCTRequestDataTypes)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DCTRequestDataTypes.subclass:
            return DCTRequestDataTypes.subclass(*args_, **kwargs_)
        else:
            return DCTRequestDataTypes(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def hasContent_(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DCTRequestDataTypes', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DCTRequestDataTypes')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DCTRequestDataTypes':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DCTRequestDataTypes')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DCTRequestDataTypes', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DCTRequestDataTypes'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DCTRequestDataTypes', fromsubclass_=False, pretty_print=True):
        pass
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class DCTRequestDataTypes


class DCTFrom(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CountryCode=None, Postalcode=None, City=None, Suburb=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CountryCode = CountryCode
        self.validate_CountryCodeType(self.CountryCode)
        self.CountryCode_nsprefix_ = None
        self.Postalcode = Postalcode
        self.validate_PostalcodeType(self.Postalcode)
        self.Postalcode_nsprefix_ = None
        self.City = City
        self.validate_CityType(self.City)
        self.City_nsprefix_ = None
        self.Suburb = Suburb
        self.validate_SuburbType(self.Suburb)
        self.Suburb_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DCTFrom)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DCTFrom.subclass:
            return DCTFrom.subclass(*args_, **kwargs_)
        else:
            return DCTFrom(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def get_Postalcode(self):
        return self.Postalcode
    def set_Postalcode(self, Postalcode):
        self.Postalcode = Postalcode
    def get_City(self):
        return self.City
    def set_City(self, City):
        self.City = City
    def get_Suburb(self):
        return self.Suburb
    def set_Suburb(self, Suburb):
        self.Suburb = Suburb
    def validate_CountryCodeType(self, value):
        result = True
        # Validate type CountryCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CountryCodeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PostalcodeType(self, value):
        result = True
        # Validate type PostalcodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 12:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on PostalcodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CityType(self, value):
        result = True
        # Validate type CityType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 45:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_SuburbType(self, value):
        result = True
        # Validate type SuburbType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 45:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on SuburbType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.CountryCode is not None or
            self.Postalcode is not None or
            self.City is not None or
            self.Suburb is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DCTFrom', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DCTFrom')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DCTFrom':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DCTFrom')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DCTFrom', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DCTFrom'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DCTFrom', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CountryCode is not None:
            namespaceprefix_ = self.CountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryCode>%s</%sCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryCode), input_name='CountryCode')), namespaceprefix_ , eol_))
        if self.Postalcode is not None:
            namespaceprefix_ = self.Postalcode_nsprefix_ + ':' if (UseCapturedNS_ and self.Postalcode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPostalcode>%s</%sPostalcode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Postalcode), input_name='Postalcode')), namespaceprefix_ , eol_))
        if self.City is not None:
            namespaceprefix_ = self.City_nsprefix_ + ':' if (UseCapturedNS_ and self.City_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCity>%s</%sCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.City), input_name='City')), namespaceprefix_ , eol_))
        if self.Suburb is not None:
            namespaceprefix_ = self.Suburb_nsprefix_ + ':' if (UseCapturedNS_ and self.Suburb_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSuburb>%s</%sSuburb>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Suburb), input_name='Suburb')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryCode')
            value_ = self.gds_validate_string(value_, node, 'CountryCode')
            self.CountryCode = value_
            self.CountryCode_nsprefix_ = child_.prefix
            # validate type CountryCodeType
            self.validate_CountryCodeType(self.CountryCode)
        elif nodeName_ == 'Postalcode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Postalcode')
            value_ = self.gds_validate_string(value_, node, 'Postalcode')
            self.Postalcode = value_
            self.Postalcode_nsprefix_ = child_.prefix
            # validate type PostalcodeType
            self.validate_PostalcodeType(self.Postalcode)
        elif nodeName_ == 'City':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'City')
            value_ = self.gds_validate_string(value_, node, 'City')
            self.City = value_
            self.City_nsprefix_ = child_.prefix
            # validate type CityType
            self.validate_CityType(self.City)
        elif nodeName_ == 'Suburb':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Suburb')
            value_ = self.gds_validate_string(value_, node, 'Suburb')
            self.Suburb = value_
            self.Suburb_nsprefix_ = child_.prefix
            # validate type SuburbType
            self.validate_SuburbType(self.Suburb)
# end class DCTFrom


class BkgDetailsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PaymentCountryCode=None, Date=None, ReadyTime=None, ReadyTimeGMTOffset=None, DimensionUnit=None, WeightUnit=None, NumberOfPieces=None, ShipmentWeight=None, Volume=None, MaxPieceWeight=None, MaxPieceHeight=None, MaxPieceDepth=None, MaxPieceWidth=None, Pieces=None, PaymentAccountNumber=None, IsDutiable=None, NetworkTypeCode=None, QtdShp=None, InsuredValue=None, InsuredCurrency=None, PaymentType=None, AcctPickupCloseTime=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PaymentCountryCode = PaymentCountryCode
        self.validate_PaymentCountryCodeType(self.PaymentCountryCode)
        self.PaymentCountryCode_nsprefix_ = None
        if isinstance(Date, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Date, '%Y-%m-%d').date()
        else:
            initvalue_ = Date
        self.Date = initvalue_
        self.Date_nsprefix_ = None
        self.ReadyTime = ReadyTime
        self.validate_ReadyTimeType(self.ReadyTime)
        self.ReadyTime_nsprefix_ = None
        self.ReadyTimeGMTOffset = ReadyTimeGMTOffset
        self.validate_ReadyTimeGMTOffsetType(self.ReadyTimeGMTOffset)
        self.ReadyTimeGMTOffset_nsprefix_ = None
        self.DimensionUnit = DimensionUnit
        self.validate_DimensionUnitType(self.DimensionUnit)
        self.DimensionUnit_nsprefix_ = None
        self.WeightUnit = WeightUnit
        self.validate_WeightUnitType(self.WeightUnit)
        self.WeightUnit_nsprefix_ = None
        self.NumberOfPieces = NumberOfPieces
        self.validate_NumberOfPiecesType(self.NumberOfPieces)
        self.NumberOfPieces_nsprefix_ = None
        self.ShipmentWeight = ShipmentWeight
        self.validate_ShipmentWeightType(self.ShipmentWeight)
        self.ShipmentWeight_nsprefix_ = None
        self.Volume = Volume
        self.validate_VolumeType(self.Volume)
        self.Volume_nsprefix_ = None
        self.MaxPieceWeight = MaxPieceWeight
        self.validate_MaxPieceWeightType(self.MaxPieceWeight)
        self.MaxPieceWeight_nsprefix_ = None
        self.MaxPieceHeight = MaxPieceHeight
        self.validate_MaxPieceHeightType(self.MaxPieceHeight)
        self.MaxPieceHeight_nsprefix_ = None
        self.MaxPieceDepth = MaxPieceDepth
        self.validate_MaxPieceDepthType(self.MaxPieceDepth)
        self.MaxPieceDepth_nsprefix_ = None
        self.MaxPieceWidth = MaxPieceWidth
        self.validate_MaxPieceWidthType(self.MaxPieceWidth)
        self.MaxPieceWidth_nsprefix_ = None
        self.Pieces = Pieces
        self.Pieces_nsprefix_ = None
        self.PaymentAccountNumber = PaymentAccountNumber
        self.validate_PaymentAccountNumberType(self.PaymentAccountNumber)
        self.PaymentAccountNumber_nsprefix_ = None
        self.IsDutiable = IsDutiable
        self.validate_IsDutiableType(self.IsDutiable)
        self.IsDutiable_nsprefix_ = None
        self.NetworkTypeCode = NetworkTypeCode
        self.validate_NetworkTypeCodeType(self.NetworkTypeCode)
        self.NetworkTypeCode_nsprefix_ = None
        if QtdShp is None:
            self.QtdShp = []
        else:
            self.QtdShp = QtdShp
        self.QtdShp_nsprefix_ = None
        self.InsuredValue = InsuredValue
        self.validate_InsuredValueType(self.InsuredValue)
        self.InsuredValue_nsprefix_ = None
        self.InsuredCurrency = InsuredCurrency
        self.validate_InsuredCurrencyType(self.InsuredCurrency)
        self.InsuredCurrency_nsprefix_ = None
        self.PaymentType = PaymentType
        self.validate_PaymentTypeType(self.PaymentType)
        self.PaymentType_nsprefix_ = None
        if isinstance(AcctPickupCloseTime, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(AcctPickupCloseTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = AcctPickupCloseTime
        self.AcctPickupCloseTime = initvalue_
        self.AcctPickupCloseTime_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BkgDetailsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BkgDetailsType.subclass:
            return BkgDetailsType.subclass(*args_, **kwargs_)
        else:
            return BkgDetailsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PaymentCountryCode(self):
        return self.PaymentCountryCode
    def set_PaymentCountryCode(self, PaymentCountryCode):
        self.PaymentCountryCode = PaymentCountryCode
    def get_Date(self):
        return self.Date
    def set_Date(self, Date):
        self.Date = Date
    def get_ReadyTime(self):
        return self.ReadyTime
    def set_ReadyTime(self, ReadyTime):
        self.ReadyTime = ReadyTime
    def get_ReadyTimeGMTOffset(self):
        return self.ReadyTimeGMTOffset
    def set_ReadyTimeGMTOffset(self, ReadyTimeGMTOffset):
        self.ReadyTimeGMTOffset = ReadyTimeGMTOffset
    def get_DimensionUnit(self):
        return self.DimensionUnit
    def set_DimensionUnit(self, DimensionUnit):
        self.DimensionUnit = DimensionUnit
    def get_WeightUnit(self):
        return self.WeightUnit
    def set_WeightUnit(self, WeightUnit):
        self.WeightUnit = WeightUnit
    def get_NumberOfPieces(self):
        return self.NumberOfPieces
    def set_NumberOfPieces(self, NumberOfPieces):
        self.NumberOfPieces = NumberOfPieces
    def get_ShipmentWeight(self):
        return self.ShipmentWeight
    def set_ShipmentWeight(self, ShipmentWeight):
        self.ShipmentWeight = ShipmentWeight
    def get_Volume(self):
        return self.Volume
    def set_Volume(self, Volume):
        self.Volume = Volume
    def get_MaxPieceWeight(self):
        return self.MaxPieceWeight
    def set_MaxPieceWeight(self, MaxPieceWeight):
        self.MaxPieceWeight = MaxPieceWeight
    def get_MaxPieceHeight(self):
        return self.MaxPieceHeight
    def set_MaxPieceHeight(self, MaxPieceHeight):
        self.MaxPieceHeight = MaxPieceHeight
    def get_MaxPieceDepth(self):
        return self.MaxPieceDepth
    def set_MaxPieceDepth(self, MaxPieceDepth):
        self.MaxPieceDepth = MaxPieceDepth
    def get_MaxPieceWidth(self):
        return self.MaxPieceWidth
    def set_MaxPieceWidth(self, MaxPieceWidth):
        self.MaxPieceWidth = MaxPieceWidth
    def get_Pieces(self):
        return self.Pieces
    def set_Pieces(self, Pieces):
        self.Pieces = Pieces
    def get_PaymentAccountNumber(self):
        return self.PaymentAccountNumber
    def set_PaymentAccountNumber(self, PaymentAccountNumber):
        self.PaymentAccountNumber = PaymentAccountNumber
    def get_IsDutiable(self):
        return self.IsDutiable
    def set_IsDutiable(self, IsDutiable):
        self.IsDutiable = IsDutiable
    def get_NetworkTypeCode(self):
        return self.NetworkTypeCode
    def set_NetworkTypeCode(self, NetworkTypeCode):
        self.NetworkTypeCode = NetworkTypeCode
    def get_QtdShp(self):
        return self.QtdShp
    def set_QtdShp(self, QtdShp):
        self.QtdShp = QtdShp
    def add_QtdShp(self, value):
        self.QtdShp.append(value)
    def insert_QtdShp_at(self, index, value):
        self.QtdShp.insert(index, value)
    def replace_QtdShp_at(self, index, value):
        self.QtdShp[index] = value
    def get_InsuredValue(self):
        return self.InsuredValue
    def set_InsuredValue(self, InsuredValue):
        self.InsuredValue = InsuredValue
    def get_InsuredCurrency(self):
        return self.InsuredCurrency
    def set_InsuredCurrency(self, InsuredCurrency):
        self.InsuredCurrency = InsuredCurrency
    def get_PaymentType(self):
        return self.PaymentType
    def set_PaymentType(self, PaymentType):
        self.PaymentType = PaymentType
    def get_AcctPickupCloseTime(self):
        return self.AcctPickupCloseTime
    def set_AcctPickupCloseTime(self, AcctPickupCloseTime):
        self.AcctPickupCloseTime = AcctPickupCloseTime
    def validate_PaymentCountryCodeType(self, value):
        result = True
        # Validate type PaymentCountryCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on PaymentCountryCodeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DateType(self, value):
        result = True
        # Validate type DateType, a restriction on xsd:date.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.date):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.date)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_ReadyTimeType(self, value):
        result = True
        # Validate type ReadyTimeType, a restriction on xsd:duration.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_ReadyTimeGMTOffsetType(self, value):
        result = True
        # Validate type ReadyTimeGMTOffsetType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ReadyTimeGMTOffsetType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ReadyTimeGMTOffsetType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DimensionUnitType(self, value):
        result = True
        # Validate type DimensionUnitType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['IN', 'CM']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DimensionUnitType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on DimensionUnitType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_WeightUnitType(self, value):
        result = True
        # Validate type WeightUnitType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['KG', 'LB']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on WeightUnitType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on WeightUnitType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_NumberOfPiecesType(self, value):
        result = True
        # Validate type NumberOfPiecesType, a restriction on xsd:positiveInteger.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on NumberOfPiecesType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on NumberOfPiecesType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_ShipmentWeightType(self, value):
        result = True
        # Validate type ShipmentWeightType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 15:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on ShipmentWeightType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_VolumeType(self, value):
        result = True
        # Validate type VolumeType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 15:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on VolumeType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_MaxPieceWeightType(self, value):
        result = True
        # Validate type MaxPieceWeightType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 15:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on MaxPieceWeightType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_MaxPieceHeightType(self, value):
        result = True
        # Validate type MaxPieceHeightType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on MaxPieceHeightType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_MaxPieceDepthType(self, value):
        result = True
        # Validate type MaxPieceDepthType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on MaxPieceDepthType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_MaxPieceWidthType(self, value):
        result = True
        # Validate type MaxPieceWidthType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on MaxPieceWidthType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_PaymentAccountNumberType(self, value):
        result = True
        # Validate type PaymentAccountNumberType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 12:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on PaymentAccountNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_IsDutiableType(self, value):
        result = True
        # Validate type IsDutiableType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['Y', 'N']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on IsDutiableType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on IsDutiableType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_NetworkTypeCodeType(self, value):
        result = True
        # Validate type NetworkTypeCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['DD', 'TD', 'AL']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NetworkTypeCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on NetworkTypeCodeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_InsuredValueType(self, value):
        result = True
        # Validate type InsuredValueType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on InsuredValueType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_InsuredCurrencyType(self, value):
        result = True
        # Validate type InsuredCurrencyType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on InsuredCurrencyType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PaymentTypeType(self, value):
        result = True
        # Validate type PaymentTypeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['D']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on PaymentTypeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_AcctPickupCloseTimeType(self, value):
        result = True
        # Validate type AcctPickupCloseTimeType, a restriction on xsd:dateTime.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.datetime):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.datetime)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def hasContent_(self):
        if (
            self.PaymentCountryCode is not None or
            self.Date is not None or
            self.ReadyTime is not None or
            self.ReadyTimeGMTOffset is not None or
            self.DimensionUnit is not None or
            self.WeightUnit is not None or
            self.NumberOfPieces is not None or
            self.ShipmentWeight is not None or
            self.Volume is not None or
            self.MaxPieceWeight is not None or
            self.MaxPieceHeight is not None or
            self.MaxPieceDepth is not None or
            self.MaxPieceWidth is not None or
            self.Pieces is not None or
            self.PaymentAccountNumber is not None or
            self.IsDutiable is not None or
            self.NetworkTypeCode is not None or
            self.QtdShp or
            self.InsuredValue is not None or
            self.InsuredCurrency is not None or
            self.PaymentType is not None or
            self.AcctPickupCloseTime is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BkgDetailsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BkgDetailsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BkgDetailsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BkgDetailsType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='BkgDetailsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BkgDetailsType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BkgDetailsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PaymentCountryCode is not None:
            namespaceprefix_ = self.PaymentCountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PaymentCountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPaymentCountryCode>%s</%sPaymentCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PaymentCountryCode), input_name='PaymentCountryCode')), namespaceprefix_ , eol_))
        if self.Date is not None:
            namespaceprefix_ = self.Date_nsprefix_ + ':' if (UseCapturedNS_ and self.Date_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDate>%s</%sDate>%s' % (namespaceprefix_ , self.gds_format_date(self.Date, input_name='Date'), namespaceprefix_ , eol_))
        if self.ReadyTime is not None:
            namespaceprefix_ = self.ReadyTime_nsprefix_ + ':' if (UseCapturedNS_ and self.ReadyTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReadyTime>%s</%sReadyTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ReadyTime), input_name='ReadyTime')), namespaceprefix_ , eol_))
        if self.ReadyTimeGMTOffset is not None:
            namespaceprefix_ = self.ReadyTimeGMTOffset_nsprefix_ + ':' if (UseCapturedNS_ and self.ReadyTimeGMTOffset_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReadyTimeGMTOffset>%s</%sReadyTimeGMTOffset>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ReadyTimeGMTOffset), input_name='ReadyTimeGMTOffset')), namespaceprefix_ , eol_))
        if self.DimensionUnit is not None:
            namespaceprefix_ = self.DimensionUnit_nsprefix_ + ':' if (UseCapturedNS_ and self.DimensionUnit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDimensionUnit>%s</%sDimensionUnit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DimensionUnit), input_name='DimensionUnit')), namespaceprefix_ , eol_))
        if self.WeightUnit is not None:
            namespaceprefix_ = self.WeightUnit_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightUnit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeightUnit>%s</%sWeightUnit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WeightUnit), input_name='WeightUnit')), namespaceprefix_ , eol_))
        if self.NumberOfPieces is not None:
            namespaceprefix_ = self.NumberOfPieces_nsprefix_ + ':' if (UseCapturedNS_ and self.NumberOfPieces_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumberOfPieces>%s</%sNumberOfPieces>%s' % (namespaceprefix_ , self.gds_format_integer(self.NumberOfPieces, input_name='NumberOfPieces'), namespaceprefix_ , eol_))
        if self.ShipmentWeight is not None:
            namespaceprefix_ = self.ShipmentWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipmentWeight>%s</%sShipmentWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ShipmentWeight, input_name='ShipmentWeight'), namespaceprefix_ , eol_))
        if self.Volume is not None:
            namespaceprefix_ = self.Volume_nsprefix_ + ':' if (UseCapturedNS_ and self.Volume_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVolume>%s</%sVolume>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Volume, input_name='Volume'), namespaceprefix_ , eol_))
        if self.MaxPieceWeight is not None:
            namespaceprefix_ = self.MaxPieceWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.MaxPieceWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMaxPieceWeight>%s</%sMaxPieceWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.MaxPieceWeight, input_name='MaxPieceWeight'), namespaceprefix_ , eol_))
        if self.MaxPieceHeight is not None:
            namespaceprefix_ = self.MaxPieceHeight_nsprefix_ + ':' if (UseCapturedNS_ and self.MaxPieceHeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMaxPieceHeight>%s</%sMaxPieceHeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.MaxPieceHeight, input_name='MaxPieceHeight'), namespaceprefix_ , eol_))
        if self.MaxPieceDepth is not None:
            namespaceprefix_ = self.MaxPieceDepth_nsprefix_ + ':' if (UseCapturedNS_ and self.MaxPieceDepth_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMaxPieceDepth>%s</%sMaxPieceDepth>%s' % (namespaceprefix_ , self.gds_format_decimal(self.MaxPieceDepth, input_name='MaxPieceDepth'), namespaceprefix_ , eol_))
        if self.MaxPieceWidth is not None:
            namespaceprefix_ = self.MaxPieceWidth_nsprefix_ + ':' if (UseCapturedNS_ and self.MaxPieceWidth_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMaxPieceWidth>%s</%sMaxPieceWidth>%s' % (namespaceprefix_ , self.gds_format_decimal(self.MaxPieceWidth, input_name='MaxPieceWidth'), namespaceprefix_ , eol_))
        if self.Pieces is not None:
            namespaceprefix_ = self.Pieces_nsprefix_ + ':' if (UseCapturedNS_ and self.Pieces_nsprefix_) else ''
            self.Pieces.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Pieces', pretty_print=pretty_print)
        if self.PaymentAccountNumber is not None:
            namespaceprefix_ = self.PaymentAccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PaymentAccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPaymentAccountNumber>%s</%sPaymentAccountNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PaymentAccountNumber), input_name='PaymentAccountNumber')), namespaceprefix_ , eol_))
        if self.IsDutiable is not None:
            namespaceprefix_ = self.IsDutiable_nsprefix_ + ':' if (UseCapturedNS_ and self.IsDutiable_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIsDutiable>%s</%sIsDutiable>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IsDutiable), input_name='IsDutiable')), namespaceprefix_ , eol_))
        if self.NetworkTypeCode is not None:
            namespaceprefix_ = self.NetworkTypeCode_nsprefix_ + ':' if (UseCapturedNS_ and self.NetworkTypeCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNetworkTypeCode>%s</%sNetworkTypeCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NetworkTypeCode), input_name='NetworkTypeCode')), namespaceprefix_ , eol_))
        for QtdShp_ in self.QtdShp:
            namespaceprefix_ = self.QtdShp_nsprefix_ + ':' if (UseCapturedNS_ and self.QtdShp_nsprefix_) else ''
            QtdShp_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='QtdShp', pretty_print=pretty_print)
        if self.InsuredValue is not None:
            namespaceprefix_ = self.InsuredValue_nsprefix_ + ':' if (UseCapturedNS_ and self.InsuredValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInsuredValue>%s</%sInsuredValue>%s' % (namespaceprefix_ , self.gds_format_decimal(self.InsuredValue, input_name='InsuredValue'), namespaceprefix_ , eol_))
        if self.InsuredCurrency is not None:
            namespaceprefix_ = self.InsuredCurrency_nsprefix_ + ':' if (UseCapturedNS_ and self.InsuredCurrency_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInsuredCurrency>%s</%sInsuredCurrency>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.InsuredCurrency), input_name='InsuredCurrency')), namespaceprefix_ , eol_))
        if self.PaymentType is not None:
            namespaceprefix_ = self.PaymentType_nsprefix_ + ':' if (UseCapturedNS_ and self.PaymentType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPaymentType>%s</%sPaymentType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PaymentType), input_name='PaymentType')), namespaceprefix_ , eol_))
        if self.AcctPickupCloseTime is not None:
            namespaceprefix_ = self.AcctPickupCloseTime_nsprefix_ + ':' if (UseCapturedNS_ and self.AcctPickupCloseTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAcctPickupCloseTime>%s</%sAcctPickupCloseTime>%s' % (namespaceprefix_ , self.gds_format_datetime(self.AcctPickupCloseTime, input_name='AcctPickupCloseTime'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'PaymentCountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PaymentCountryCode')
            value_ = self.gds_validate_string(value_, node, 'PaymentCountryCode')
            self.PaymentCountryCode = value_
            self.PaymentCountryCode_nsprefix_ = child_.prefix
            # validate type PaymentCountryCodeType
            self.validate_PaymentCountryCodeType(self.PaymentCountryCode)
        elif nodeName_ == 'Date':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.Date = dval_
            self.Date_nsprefix_ = child_.prefix
            # validate type DateType
            self.validate_DateType(self.Date)
        elif nodeName_ == 'ReadyTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReadyTime')
            value_ = self.gds_validate_string(value_, node, 'ReadyTime')
            self.ReadyTime = value_
            self.ReadyTime_nsprefix_ = child_.prefix
            # validate type ReadyTimeType
            self.validate_ReadyTimeType(self.ReadyTime)
        elif nodeName_ == 'ReadyTimeGMTOffset':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReadyTimeGMTOffset')
            value_ = self.gds_validate_string(value_, node, 'ReadyTimeGMTOffset')
            self.ReadyTimeGMTOffset = value_
            self.ReadyTimeGMTOffset_nsprefix_ = child_.prefix
            # validate type ReadyTimeGMTOffsetType
            self.validate_ReadyTimeGMTOffsetType(self.ReadyTimeGMTOffset)
        elif nodeName_ == 'DimensionUnit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DimensionUnit')
            value_ = self.gds_validate_string(value_, node, 'DimensionUnit')
            self.DimensionUnit = value_
            self.DimensionUnit_nsprefix_ = child_.prefix
            # validate type DimensionUnitType
            self.validate_DimensionUnitType(self.DimensionUnit)
        elif nodeName_ == 'WeightUnit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WeightUnit')
            value_ = self.gds_validate_string(value_, node, 'WeightUnit')
            self.WeightUnit = value_
            self.WeightUnit_nsprefix_ = child_.prefix
            # validate type WeightUnitType
            self.validate_WeightUnitType(self.WeightUnit)
        elif nodeName_ == 'NumberOfPieces' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'NumberOfPieces')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'NumberOfPieces')
            self.NumberOfPieces = ival_
            self.NumberOfPieces_nsprefix_ = child_.prefix
            # validate type NumberOfPiecesType
            self.validate_NumberOfPiecesType(self.NumberOfPieces)
        elif nodeName_ == 'ShipmentWeight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ShipmentWeight')
            fval_ = self.gds_validate_decimal(fval_, node, 'ShipmentWeight')
            self.ShipmentWeight = fval_
            self.ShipmentWeight_nsprefix_ = child_.prefix
            # validate type ShipmentWeightType
            self.validate_ShipmentWeightType(self.ShipmentWeight)
        elif nodeName_ == 'Volume' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Volume')
            fval_ = self.gds_validate_decimal(fval_, node, 'Volume')
            self.Volume = fval_
            self.Volume_nsprefix_ = child_.prefix
            # validate type VolumeType
            self.validate_VolumeType(self.Volume)
        elif nodeName_ == 'MaxPieceWeight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'MaxPieceWeight')
            fval_ = self.gds_validate_decimal(fval_, node, 'MaxPieceWeight')
            self.MaxPieceWeight = fval_
            self.MaxPieceWeight_nsprefix_ = child_.prefix
            # validate type MaxPieceWeightType
            self.validate_MaxPieceWeightType(self.MaxPieceWeight)
        elif nodeName_ == 'MaxPieceHeight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'MaxPieceHeight')
            fval_ = self.gds_validate_decimal(fval_, node, 'MaxPieceHeight')
            self.MaxPieceHeight = fval_
            self.MaxPieceHeight_nsprefix_ = child_.prefix
            # validate type MaxPieceHeightType
            self.validate_MaxPieceHeightType(self.MaxPieceHeight)
        elif nodeName_ == 'MaxPieceDepth' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'MaxPieceDepth')
            fval_ = self.gds_validate_decimal(fval_, node, 'MaxPieceDepth')
            self.MaxPieceDepth = fval_
            self.MaxPieceDepth_nsprefix_ = child_.prefix
            # validate type MaxPieceDepthType
            self.validate_MaxPieceDepthType(self.MaxPieceDepth)
        elif nodeName_ == 'MaxPieceWidth' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'MaxPieceWidth')
            fval_ = self.gds_validate_decimal(fval_, node, 'MaxPieceWidth')
            self.MaxPieceWidth = fval_
            self.MaxPieceWidth_nsprefix_ = child_.prefix
            # validate type MaxPieceWidthType
            self.validate_MaxPieceWidthType(self.MaxPieceWidth)
        elif nodeName_ == 'Pieces':
            obj_ = PiecesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Pieces = obj_
            obj_.original_tagname_ = 'Pieces'
        elif nodeName_ == 'PaymentAccountNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PaymentAccountNumber')
            value_ = self.gds_validate_string(value_, node, 'PaymentAccountNumber')
            self.PaymentAccountNumber = value_
            self.PaymentAccountNumber_nsprefix_ = child_.prefix
            # validate type PaymentAccountNumberType
            self.validate_PaymentAccountNumberType(self.PaymentAccountNumber)
        elif nodeName_ == 'IsDutiable':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IsDutiable')
            value_ = self.gds_validate_string(value_, node, 'IsDutiable')
            self.IsDutiable = value_
            self.IsDutiable_nsprefix_ = child_.prefix
            # validate type IsDutiableType
            self.validate_IsDutiableType(self.IsDutiable)
        elif nodeName_ == 'NetworkTypeCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NetworkTypeCode')
            value_ = self.gds_validate_string(value_, node, 'NetworkTypeCode')
            self.NetworkTypeCode = value_
            self.NetworkTypeCode_nsprefix_ = child_.prefix
            # validate type NetworkTypeCodeType
            self.validate_NetworkTypeCodeType(self.NetworkTypeCode)
        elif nodeName_ == 'QtdShp':
            obj_ = QtdShpType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.QtdShp.append(obj_)
            obj_.original_tagname_ = 'QtdShp'
        elif nodeName_ == 'InsuredValue' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'InsuredValue')
            fval_ = self.gds_validate_decimal(fval_, node, 'InsuredValue')
            self.InsuredValue = fval_
            self.InsuredValue_nsprefix_ = child_.prefix
            # validate type InsuredValueType
            self.validate_InsuredValueType(self.InsuredValue)
        elif nodeName_ == 'InsuredCurrency':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'InsuredCurrency')
            value_ = self.gds_validate_string(value_, node, 'InsuredCurrency')
            self.InsuredCurrency = value_
            self.InsuredCurrency_nsprefix_ = child_.prefix
            # validate type InsuredCurrencyType
            self.validate_InsuredCurrencyType(self.InsuredCurrency)
        elif nodeName_ == 'PaymentType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PaymentType')
            value_ = self.gds_validate_string(value_, node, 'PaymentType')
            self.PaymentType = value_
            self.PaymentType_nsprefix_ = child_.prefix
            # validate type PaymentTypeType
            self.validate_PaymentTypeType(self.PaymentType)
        elif nodeName_ == 'AcctPickupCloseTime':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.AcctPickupCloseTime = dval_
            self.AcctPickupCloseTime_nsprefix_ = child_.prefix
            # validate type AcctPickupCloseTimeType
            self.validate_AcctPickupCloseTimeType(self.AcctPickupCloseTime)
# end class BkgDetailsType


class DCTTo(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CountryCode=None, Postalcode=None, City=None, Suburb=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CountryCode = CountryCode
        self.validate_CountryCodeType1(self.CountryCode)
        self.CountryCode_nsprefix_ = None
        self.Postalcode = Postalcode
        self.validate_PostalcodeType2(self.Postalcode)
        self.Postalcode_nsprefix_ = None
        self.City = City
        self.validate_CityType3(self.City)
        self.City_nsprefix_ = None
        self.Suburb = Suburb
        self.validate_SuburbType4(self.Suburb)
        self.Suburb_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DCTTo)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DCTTo.subclass:
            return DCTTo.subclass(*args_, **kwargs_)
        else:
            return DCTTo(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def get_Postalcode(self):
        return self.Postalcode
    def set_Postalcode(self, Postalcode):
        self.Postalcode = Postalcode
    def get_City(self):
        return self.City
    def set_City(self, City):
        self.City = City
    def get_Suburb(self):
        return self.Suburb
    def set_Suburb(self, Suburb):
        self.Suburb = Suburb
    def validate_CountryCodeType1(self, value):
        result = True
        # Validate type CountryCodeType1, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CountryCodeType1' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PostalcodeType2(self, value):
        result = True
        # Validate type PostalcodeType2, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 12:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on PostalcodeType2' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CityType3(self, value):
        result = True
        # Validate type CityType3, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 45:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CityType3' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_SuburbType4(self, value):
        result = True
        # Validate type SuburbType4, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 45:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on SuburbType4' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.CountryCode is not None or
            self.Postalcode is not None or
            self.City is not None or
            self.Suburb is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DCTTo', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DCTTo')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DCTTo':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DCTTo')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DCTTo', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DCTTo'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DCTTo', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CountryCode is not None:
            namespaceprefix_ = self.CountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryCode>%s</%sCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryCode), input_name='CountryCode')), namespaceprefix_ , eol_))
        if self.Postalcode is not None:
            namespaceprefix_ = self.Postalcode_nsprefix_ + ':' if (UseCapturedNS_ and self.Postalcode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPostalcode>%s</%sPostalcode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Postalcode), input_name='Postalcode')), namespaceprefix_ , eol_))
        if self.City is not None:
            namespaceprefix_ = self.City_nsprefix_ + ':' if (UseCapturedNS_ and self.City_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCity>%s</%sCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.City), input_name='City')), namespaceprefix_ , eol_))
        if self.Suburb is not None:
            namespaceprefix_ = self.Suburb_nsprefix_ + ':' if (UseCapturedNS_ and self.Suburb_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSuburb>%s</%sSuburb>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Suburb), input_name='Suburb')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryCode')
            value_ = self.gds_validate_string(value_, node, 'CountryCode')
            self.CountryCode = value_
            self.CountryCode_nsprefix_ = child_.prefix
            # validate type CountryCodeType1
            self.validate_CountryCodeType1(self.CountryCode)
        elif nodeName_ == 'Postalcode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Postalcode')
            value_ = self.gds_validate_string(value_, node, 'Postalcode')
            self.Postalcode = value_
            self.Postalcode_nsprefix_ = child_.prefix
            # validate type PostalcodeType2
            self.validate_PostalcodeType2(self.Postalcode)
        elif nodeName_ == 'City':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'City')
            value_ = self.gds_validate_string(value_, node, 'City')
            self.City = value_
            self.City_nsprefix_ = child_.prefix
            # validate type CityType3
            self.validate_CityType3(self.City)
        elif nodeName_ == 'Suburb':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Suburb')
            value_ = self.gds_validate_string(value_, node, 'Suburb')
            self.Suburb = value_
            self.Suburb_nsprefix_ = child_.prefix
            # validate type SuburbType4
            self.validate_SuburbType4(self.Suburb)
# end class DCTTo


class DCTDutiable(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DeclaredCurrency=None, DeclaredValue=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DeclaredCurrency = DeclaredCurrency
        self.validate_DeclaredCurrencyType(self.DeclaredCurrency)
        self.DeclaredCurrency_nsprefix_ = None
        self.DeclaredValue = DeclaredValue
        self.validate_DeclaredValueType(self.DeclaredValue)
        self.DeclaredValue_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DCTDutiable)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DCTDutiable.subclass:
            return DCTDutiable.subclass(*args_, **kwargs_)
        else:
            return DCTDutiable(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DeclaredCurrency(self):
        return self.DeclaredCurrency
    def set_DeclaredCurrency(self, DeclaredCurrency):
        self.DeclaredCurrency = DeclaredCurrency
    def get_DeclaredValue(self):
        return self.DeclaredValue
    def set_DeclaredValue(self, DeclaredValue):
        self.DeclaredValue = DeclaredValue
    def validate_DeclaredCurrencyType(self, value):
        result = True
        # Validate type DeclaredCurrencyType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on DeclaredCurrencyType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DeclaredValueType(self, value):
        result = True
        # Validate type DeclaredValueType, a restriction on xsd:float.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, float):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (float)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0.000:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on DeclaredValueType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 999999999999999999.999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on DeclaredValueType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.DeclaredCurrency is not None or
            self.DeclaredValue is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DCTDutiable', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DCTDutiable')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DCTDutiable':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DCTDutiable')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DCTDutiable', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DCTDutiable'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DCTDutiable', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DeclaredCurrency is not None:
            namespaceprefix_ = self.DeclaredCurrency_nsprefix_ + ':' if (UseCapturedNS_ and self.DeclaredCurrency_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeclaredCurrency>%s</%sDeclaredCurrency>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DeclaredCurrency), input_name='DeclaredCurrency')), namespaceprefix_ , eol_))
        if self.DeclaredValue is not None:
            namespaceprefix_ = self.DeclaredValue_nsprefix_ + ':' if (UseCapturedNS_ and self.DeclaredValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeclaredValue>%s</%sDeclaredValue>%s' % (namespaceprefix_ , self.gds_format_float(self.DeclaredValue, input_name='DeclaredValue'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DeclaredCurrency':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DeclaredCurrency')
            value_ = self.gds_validate_string(value_, node, 'DeclaredCurrency')
            self.DeclaredCurrency = value_
            self.DeclaredCurrency_nsprefix_ = child_.prefix
            # validate type DeclaredCurrencyType
            self.validate_DeclaredCurrencyType(self.DeclaredCurrency)
        elif nodeName_ == 'DeclaredValue' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'DeclaredValue')
            fval_ = self.gds_validate_float(fval_, node, 'DeclaredValue')
            self.DeclaredValue = fval_
            self.DeclaredValue_nsprefix_ = child_.prefix
            # validate type DeclaredValueType
            self.validate_DeclaredValueType(self.DeclaredValue)
# end class DCTDutiable


class PieceType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PieceID=None, PackageTypeCode='BOX', Height=None, Depth=None, Width=None, Weight=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PieceID = PieceID
        self.validate_PieceIDType(self.PieceID)
        self.PieceID_nsprefix_ = None
        self.PackageTypeCode = PackageTypeCode
        self.validate_PackageTypeCodeType(self.PackageTypeCode)
        self.PackageTypeCode_nsprefix_ = None
        self.Height = Height
        self.validate_HeightType(self.Height)
        self.Height_nsprefix_ = None
        self.Depth = Depth
        self.validate_DepthType(self.Depth)
        self.Depth_nsprefix_ = None
        self.Width = Width
        self.validate_WidthType(self.Width)
        self.Width_nsprefix_ = None
        self.Weight = Weight
        self.validate_WeightType(self.Weight)
        self.Weight_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PieceType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PieceType.subclass:
            return PieceType.subclass(*args_, **kwargs_)
        else:
            return PieceType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PieceID(self):
        return self.PieceID
    def set_PieceID(self, PieceID):
        self.PieceID = PieceID
    def get_PackageTypeCode(self):
        return self.PackageTypeCode
    def set_PackageTypeCode(self, PackageTypeCode):
        self.PackageTypeCode = PackageTypeCode
    def get_Height(self):
        return self.Height
    def set_Height(self, Height):
        self.Height = Height
    def get_Depth(self):
        return self.Depth
    def set_Depth(self, Depth):
        self.Depth = Depth
    def get_Width(self):
        return self.Width
    def set_Width(self, Width):
        self.Width = Width
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def validate_PieceIDType(self, value):
        result = True
        # Validate type PieceIDType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_PieceIDType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_PieceIDType_patterns_, ))
                result = False
        return result
    validate_PieceIDType_patterns_ = [['^([0-9]+)$']]
    def validate_PackageTypeCodeType(self, value):
        result = True
        # Validate type PackageTypeCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FLY', 'COY', 'NCY', 'PAL', 'DBL', 'BOX']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on PackageTypeCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on PackageTypeCodeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_HeightType(self, value):
        result = True
        # Validate type HeightType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on HeightType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_DepthType(self, value):
        result = True
        # Validate type DepthType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on DepthType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_WidthType(self, value):
        result = True
        # Validate type WidthType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on WidthType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_WeightType(self, value):
        result = True
        # Validate type WeightType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 15:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on WeightType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.PieceID is not None or
            self.PackageTypeCode != "BOX" or
            self.Height is not None or
            self.Depth is not None or
            self.Width is not None or
            self.Weight is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PieceType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PieceType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PieceType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PieceType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PieceType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PieceType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PieceType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PieceID is not None:
            namespaceprefix_ = self.PieceID_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPieceID>%s</%sPieceID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PieceID), input_name='PieceID')), namespaceprefix_ , eol_))
        if self.PackageTypeCode != "BOX":
            namespaceprefix_ = self.PackageTypeCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PackageTypeCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPackageTypeCode>%s</%sPackageTypeCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PackageTypeCode), input_name='PackageTypeCode')), namespaceprefix_ , eol_))
        if self.Height is not None:
            namespaceprefix_ = self.Height_nsprefix_ + ':' if (UseCapturedNS_ and self.Height_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHeight>%s</%sHeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Height, input_name='Height'), namespaceprefix_ , eol_))
        if self.Depth is not None:
            namespaceprefix_ = self.Depth_nsprefix_ + ':' if (UseCapturedNS_ and self.Depth_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDepth>%s</%sDepth>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Depth, input_name='Depth'), namespaceprefix_ , eol_))
        if self.Width is not None:
            namespaceprefix_ = self.Width_nsprefix_ + ':' if (UseCapturedNS_ and self.Width_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWidth>%s</%sWidth>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Width, input_name='Width'), namespaceprefix_ , eol_))
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeight>%s</%sWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Weight, input_name='Weight'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'PieceID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PieceID')
            value_ = self.gds_validate_string(value_, node, 'PieceID')
            self.PieceID = value_
            self.PieceID_nsprefix_ = child_.prefix
            # validate type PieceIDType
            self.validate_PieceIDType(self.PieceID)
        elif nodeName_ == 'PackageTypeCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PackageTypeCode')
            value_ = self.gds_validate_string(value_, node, 'PackageTypeCode')
            self.PackageTypeCode = value_
            self.PackageTypeCode_nsprefix_ = child_.prefix
            # validate type PackageTypeCodeType
            self.validate_PackageTypeCodeType(self.PackageTypeCode)
        elif nodeName_ == 'Height' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Height')
            fval_ = self.gds_validate_decimal(fval_, node, 'Height')
            self.Height = fval_
            self.Height_nsprefix_ = child_.prefix
            # validate type HeightType
            self.validate_HeightType(self.Height)
        elif nodeName_ == 'Depth' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Depth')
            fval_ = self.gds_validate_decimal(fval_, node, 'Depth')
            self.Depth = fval_
            self.Depth_nsprefix_ = child_.prefix
            # validate type DepthType
            self.validate_DepthType(self.Depth)
        elif nodeName_ == 'Width' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Width')
            fval_ = self.gds_validate_decimal(fval_, node, 'Width')
            self.Width = fval_
            self.Width_nsprefix_ = child_.prefix
            # validate type WidthType
            self.validate_WidthType(self.Width)
        elif nodeName_ == 'Weight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Weight')
            fval_ = self.gds_validate_decimal(fval_, node, 'Weight')
            self.Weight = fval_
            self.Weight_nsprefix_ = child_.prefix
            # validate type WeightType
            self.validate_WeightType(self.Weight)
# end class PieceType


class QtdShpType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GlobalProductCode=None, LocalProductCode=None, QtdShpExChrg=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GlobalProductCode = GlobalProductCode
        self.validate_GlobalProductCodeType(self.GlobalProductCode)
        self.GlobalProductCode_nsprefix_ = None
        self.LocalProductCode = LocalProductCode
        self.validate_LocalProductCodeType(self.LocalProductCode)
        self.LocalProductCode_nsprefix_ = None
        if QtdShpExChrg is None:
            self.QtdShpExChrg = []
        else:
            self.QtdShpExChrg = QtdShpExChrg
        self.QtdShpExChrg_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, QtdShpType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if QtdShpType.subclass:
            return QtdShpType.subclass(*args_, **kwargs_)
        else:
            return QtdShpType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GlobalProductCode(self):
        return self.GlobalProductCode
    def set_GlobalProductCode(self, GlobalProductCode):
        self.GlobalProductCode = GlobalProductCode
    def get_LocalProductCode(self):
        return self.LocalProductCode
    def set_LocalProductCode(self, LocalProductCode):
        self.LocalProductCode = LocalProductCode
    def get_QtdShpExChrg(self):
        return self.QtdShpExChrg
    def set_QtdShpExChrg(self, QtdShpExChrg):
        self.QtdShpExChrg = QtdShpExChrg
    def add_QtdShpExChrg(self, value):
        self.QtdShpExChrg.append(value)
    def insert_QtdShpExChrg_at(self, index, value):
        self.QtdShpExChrg.insert(index, value)
    def replace_QtdShpExChrg_at(self, index, value):
        self.QtdShpExChrg[index] = value
    def validate_GlobalProductCodeType(self, value):
        result = True
        # Validate type GlobalProductCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on GlobalProductCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on GlobalProductCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_GlobalProductCodeType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_GlobalProductCodeType_patterns_, ))
                result = False
        return result
    validate_GlobalProductCodeType_patterns_ = [['^([A-Z0-9]+)$']]
    def validate_LocalProductCodeType(self, value):
        result = True
        # Validate type LocalProductCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on LocalProductCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on LocalProductCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.GlobalProductCode is not None or
            self.LocalProductCode is not None or
            self.QtdShpExChrg
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='QtdShpType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('QtdShpType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'QtdShpType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='QtdShpType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='QtdShpType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='QtdShpType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='QtdShpType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GlobalProductCode is not None:
            namespaceprefix_ = self.GlobalProductCode_nsprefix_ + ':' if (UseCapturedNS_ and self.GlobalProductCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGlobalProductCode>%s</%sGlobalProductCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GlobalProductCode), input_name='GlobalProductCode')), namespaceprefix_ , eol_))
        if self.LocalProductCode is not None:
            namespaceprefix_ = self.LocalProductCode_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalProductCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalProductCode>%s</%sLocalProductCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalProductCode), input_name='LocalProductCode')), namespaceprefix_ , eol_))
        for QtdShpExChrg_ in self.QtdShpExChrg:
            namespaceprefix_ = self.QtdShpExChrg_nsprefix_ + ':' if (UseCapturedNS_ and self.QtdShpExChrg_nsprefix_) else ''
            QtdShpExChrg_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='QtdShpExChrg', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'GlobalProductCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GlobalProductCode')
            value_ = self.gds_validate_string(value_, node, 'GlobalProductCode')
            self.GlobalProductCode = value_
            self.GlobalProductCode_nsprefix_ = child_.prefix
            # validate type GlobalProductCodeType
            self.validate_GlobalProductCodeType(self.GlobalProductCode)
        elif nodeName_ == 'LocalProductCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalProductCode')
            value_ = self.gds_validate_string(value_, node, 'LocalProductCode')
            self.LocalProductCode = value_
            self.LocalProductCode_nsprefix_ = child_.prefix
            # validate type LocalProductCodeType
            self.validate_LocalProductCodeType(self.LocalProductCode)
        elif nodeName_ == 'QtdShpExChrg':
            obj_ = QtdShpExChrgType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.QtdShpExChrg.append(obj_)
            obj_.original_tagname_ = 'QtdShpExChrg'
# end class QtdShpType


class QtdShpExChrgType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, SpecialServiceType=None, LocalSpecialServiceType=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.SpecialServiceType = SpecialServiceType
        self.validate_SpecialServiceTypeType(self.SpecialServiceType)
        self.SpecialServiceType_nsprefix_ = None
        self.LocalSpecialServiceType = LocalSpecialServiceType
        self.validate_LocalSpecialServiceTypeType(self.LocalSpecialServiceType)
        self.LocalSpecialServiceType_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, QtdShpExChrgType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if QtdShpExChrgType.subclass:
            return QtdShpExChrgType.subclass(*args_, **kwargs_)
        else:
            return QtdShpExChrgType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_SpecialServiceType(self):
        return self.SpecialServiceType
    def set_SpecialServiceType(self, SpecialServiceType):
        self.SpecialServiceType = SpecialServiceType
    def get_LocalSpecialServiceType(self):
        return self.LocalSpecialServiceType
    def set_LocalSpecialServiceType(self, LocalSpecialServiceType):
        self.LocalSpecialServiceType = LocalSpecialServiceType
    def validate_SpecialServiceTypeType(self, value):
        result = True
        # Validate type SpecialServiceTypeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on SpecialServiceTypeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_LocalSpecialServiceTypeType(self, value):
        result = True
        # Validate type LocalSpecialServiceTypeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on LocalSpecialServiceTypeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.SpecialServiceType is not None or
            self.LocalSpecialServiceType is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='QtdShpExChrgType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('QtdShpExChrgType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'QtdShpExChrgType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='QtdShpExChrgType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='QtdShpExChrgType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='QtdShpExChrgType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='QtdShpExChrgType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.SpecialServiceType is not None:
            namespaceprefix_ = self.SpecialServiceType_nsprefix_ + ':' if (UseCapturedNS_ and self.SpecialServiceType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSpecialServiceType>%s</%sSpecialServiceType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SpecialServiceType), input_name='SpecialServiceType')), namespaceprefix_ , eol_))
        if self.LocalSpecialServiceType is not None:
            namespaceprefix_ = self.LocalSpecialServiceType_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalSpecialServiceType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalSpecialServiceType>%s</%sLocalSpecialServiceType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalSpecialServiceType), input_name='LocalSpecialServiceType')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'SpecialServiceType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SpecialServiceType')
            value_ = self.gds_validate_string(value_, node, 'SpecialServiceType')
            self.SpecialServiceType = value_
            self.SpecialServiceType_nsprefix_ = child_.prefix
            # validate type SpecialServiceTypeType
            self.validate_SpecialServiceTypeType(self.SpecialServiceType)
        elif nodeName_ == 'LocalSpecialServiceType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalSpecialServiceType')
            value_ = self.gds_validate_string(value_, node, 'LocalSpecialServiceType')
            self.LocalSpecialServiceType = value_
            self.LocalSpecialServiceType_nsprefix_ = child_.prefix
            # validate type LocalSpecialServiceTypeType
            self.validate_LocalSpecialServiceTypeType(self.LocalSpecialServiceType)
# end class QtdShpExChrgType


class GenReq(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, OSINFO=None, NXTPU=None, FCNTWTYCD=None, CUSTAGRIND=None, VLDTRT_DD=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.OSINFO = OSINFO
        self.validate_OSINFOType(self.OSINFO)
        self.OSINFO_nsprefix_ = None
        self.NXTPU = NXTPU
        self.validate_NXTPUType(self.NXTPU)
        self.NXTPU_nsprefix_ = None
        self.FCNTWTYCD = FCNTWTYCD
        self.validate_FCNTWTYCDType(self.FCNTWTYCD)
        self.FCNTWTYCD_nsprefix_ = None
        self.CUSTAGRIND = CUSTAGRIND
        self.validate_CUSTAGRINDType(self.CUSTAGRIND)
        self.CUSTAGRIND_nsprefix_ = None
        self.VLDTRT_DD = VLDTRT_DD
        self.validate_VLDTRT_DDType(self.VLDTRT_DD)
        self.VLDTRT_DD_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GenReq)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GenReq.subclass:
            return GenReq.subclass(*args_, **kwargs_)
        else:
            return GenReq(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_OSINFO(self):
        return self.OSINFO
    def set_OSINFO(self, OSINFO):
        self.OSINFO = OSINFO
    def get_NXTPU(self):
        return self.NXTPU
    def set_NXTPU(self, NXTPU):
        self.NXTPU = NXTPU
    def get_FCNTWTYCD(self):
        return self.FCNTWTYCD
    def set_FCNTWTYCD(self, FCNTWTYCD):
        self.FCNTWTYCD = FCNTWTYCD
    def get_CUSTAGRIND(self):
        return self.CUSTAGRIND
    def set_CUSTAGRIND(self, CUSTAGRIND):
        self.CUSTAGRIND = CUSTAGRIND
    def get_VLDTRT_DD(self):
        return self.VLDTRT_DD
    def set_VLDTRT_DD(self, VLDTRT_DD):
        self.VLDTRT_DD = VLDTRT_DD
    def validate_OSINFOType(self, value):
        result = True
        # Validate type OSINFOType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['Y', 'N']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on OSINFOType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on OSINFOType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_NXTPUType(self, value):
        result = True
        # Validate type NXTPUType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['Y', 'N']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NXTPUType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on NXTPUType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_FCNTWTYCDType(self, value):
        result = True
        # Validate type FCNTWTYCDType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['DD', 'TD', 'AL']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on FCNTWTYCDType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on FCNTWTYCDType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CUSTAGRINDType(self, value):
        result = True
        # Validate type CUSTAGRINDType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['Y', 'N']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CUSTAGRINDType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CUSTAGRINDType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_VLDTRT_DDType(self, value):
        result = True
        # Validate type VLDTRT_DDType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['Y', 'N']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on VLDTRT_DDType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on VLDTRT_DDType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.OSINFO is not None or
            self.NXTPU is not None or
            self.FCNTWTYCD is not None or
            self.CUSTAGRIND is not None or
            self.VLDTRT_DD is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenReq', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GenReq')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GenReq':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GenReq')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GenReq', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GenReq'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenReq', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.OSINFO is not None:
            namespaceprefix_ = self.OSINFO_nsprefix_ + ':' if (UseCapturedNS_ and self.OSINFO_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOSINFO>%s</%sOSINFO>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OSINFO), input_name='OSINFO')), namespaceprefix_ , eol_))
        if self.NXTPU is not None:
            namespaceprefix_ = self.NXTPU_nsprefix_ + ':' if (UseCapturedNS_ and self.NXTPU_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNXTPU>%s</%sNXTPU>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NXTPU), input_name='NXTPU')), namespaceprefix_ , eol_))
        if self.FCNTWTYCD is not None:
            namespaceprefix_ = self.FCNTWTYCD_nsprefix_ + ':' if (UseCapturedNS_ and self.FCNTWTYCD_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFCNTWTYCD>%s</%sFCNTWTYCD>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FCNTWTYCD), input_name='FCNTWTYCD')), namespaceprefix_ , eol_))
        if self.CUSTAGRIND is not None:
            namespaceprefix_ = self.CUSTAGRIND_nsprefix_ + ':' if (UseCapturedNS_ and self.CUSTAGRIND_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCUSTAGRIND>%s</%sCUSTAGRIND>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CUSTAGRIND), input_name='CUSTAGRIND')), namespaceprefix_ , eol_))
        if self.VLDTRT_DD is not None:
            namespaceprefix_ = self.VLDTRT_DD_nsprefix_ + ':' if (UseCapturedNS_ and self.VLDTRT_DD_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVLDTRT_DD>%s</%sVLDTRT_DD>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.VLDTRT_DD), input_name='VLDTRT_DD')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'OSINFO':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OSINFO')
            value_ = self.gds_validate_string(value_, node, 'OSINFO')
            self.OSINFO = value_
            self.OSINFO_nsprefix_ = child_.prefix
            # validate type OSINFOType
            self.validate_OSINFOType(self.OSINFO)
        elif nodeName_ == 'NXTPU':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NXTPU')
            value_ = self.gds_validate_string(value_, node, 'NXTPU')
            self.NXTPU = value_
            self.NXTPU_nsprefix_ = child_.prefix
            # validate type NXTPUType
            self.validate_NXTPUType(self.NXTPU)
        elif nodeName_ == 'FCNTWTYCD':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FCNTWTYCD')
            value_ = self.gds_validate_string(value_, node, 'FCNTWTYCD')
            self.FCNTWTYCD = value_
            self.FCNTWTYCD_nsprefix_ = child_.prefix
            # validate type FCNTWTYCDType
            self.validate_FCNTWTYCDType(self.FCNTWTYCD)
        elif nodeName_ == 'CUSTAGRIND':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CUSTAGRIND')
            value_ = self.gds_validate_string(value_, node, 'CUSTAGRIND')
            self.CUSTAGRIND = value_
            self.CUSTAGRIND_nsprefix_ = child_.prefix
            # validate type CUSTAGRINDType
            self.validate_CUSTAGRINDType(self.CUSTAGRIND)
        elif nodeName_ == 'VLDTRT_DD':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'VLDTRT_DD')
            value_ = self.gds_validate_string(value_, node, 'VLDTRT_DD')
            self.VLDTRT_DD = value_
            self.VLDTRT_DD_nsprefix_ = child_.prefix
            # validate type VLDTRT_DDType
            self.validate_VLDTRT_DDType(self.VLDTRT_DD)
# end class GenReq


class PiecesType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Piece=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Piece is None:
            self.Piece = []
        else:
            self.Piece = Piece
        self.Piece_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PiecesType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PiecesType.subclass:
            return PiecesType.subclass(*args_, **kwargs_)
        else:
            return PiecesType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Piece(self):
        return self.Piece
    def set_Piece(self, Piece):
        self.Piece = Piece
    def add_Piece(self, value):
        self.Piece.append(value)
    def insert_Piece_at(self, index, value):
        self.Piece.insert(index, value)
    def replace_Piece_at(self, index, value):
        self.Piece[index] = value
    def hasContent_(self):
        if (
            self.Piece
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PiecesType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PiecesType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PiecesType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PiecesType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PiecesType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PiecesType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PiecesType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Piece_ in self.Piece:
            namespaceprefix_ = self.Piece_nsprefix_ + ':' if (UseCapturedNS_ and self.Piece_nsprefix_) else ''
            Piece_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Piece', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Piece':
            obj_ = PieceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Piece.append(obj_)
            obj_.original_tagname_ = 'Piece'
# end class PiecesType


GDSClassesMapping = {
}


USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = GDSClassesMapping.get(tag)
    if rootClass is None:
        rootClass = globals().get(tag)
    return tag, rootClass


def get_required_ns_prefix_defs(rootNode):
    '''Get all name space prefix definitions required in this XML doc.
    Return a dictionary of definitions and a char string of definitions.
    '''
    nsmap = {
        prefix: uri
        for node in rootNode.iter()
        for (prefix, uri) in node.nsmap.items()
        if prefix is not None
    }
    namespacedefs = ' '.join([
        'xmlns:{}="{}"'.format(prefix, uri)
        for prefix, uri in nsmap.items()
    ])
    return nsmap, namespacedefs


def parse(inFileName, silence=False, print_warnings=True):
    global CapturedNsmap_
    gds_collector = GdsCollector_()
    parser = None
    doc = parsexml_(inFileName, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DCTRequestDataTypes'
        rootClass = DCTRequestDataTypes
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    CapturedNsmap_, namespacedefs = get_required_ns_prefix_defs(rootNode)
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_=namespacedefs,
            pretty_print=True)
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseEtree(inFileName, silence=False, print_warnings=True):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DCTRequestDataTypes'
        rootClass = DCTRequestDataTypes
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(str(content))
        sys.stdout.write('\n')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False, print_warnings=True):
    '''Parse a string, create the object tree, and export it.

    Arguments:
    - inString -- A string.  This XML fragment should not start
      with an XML declaration containing an encoding.
    - silence -- A boolean.  If False, export the object.
    Returns -- The root object in the tree.
    '''
    parser = None
    rootNode= parsexmlstring_(inString, parser)
    gds_collector = GdsCollector_()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DCTRequestDataTypes'
        rootClass = DCTRequestDataTypes
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseLiteral(inFileName, silence=False, print_warnings=True):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DCTRequestDataTypes'
        rootClass = DCTRequestDataTypes
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from dct_requestdatatypes_global import *\n\n')
        sys.stdout.write('import dct_requestdatatypes_global as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        parse(args[0])
    else:
        usage()


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()

RenameMappings_ = {
}

__all__ = [
    "BkgDetailsType",
    "DCTDutiable",
    "DCTFrom",
    "DCTRequestDataTypes",
    "DCTTo",
    "GenReq",
    "PieceType",
    "PiecesType",
    "QtdShpExChrgType",
    "QtdShpType"
]
