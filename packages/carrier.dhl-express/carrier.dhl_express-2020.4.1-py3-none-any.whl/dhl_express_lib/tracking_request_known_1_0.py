#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Wed Apr  1 15:24:33 2020 by generateDS.py version 2.35.15.
# Python 3.8.2 (v3.8.2:7b3ab5921f, Feb 24 2020, 17:52:18)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './pydhl/tracking_request_known_1_0.py')
#
# Command line arguments:
#   /Users/daniel/Documents/Documentations/DHL/2020-03/schemas/TrackingRequestKnown-1.0.xsd
#
# Command line:
#   /Users/daniel/Workspace/Project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./pydhl/tracking_request_known_1_0.py" /Users/daniel/Documents/Documentations/DHL/2020-03/schemas/TrackingRequestKnown-1.0.xsd
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


class AccountType(Enum):
    """Account Type by method of payment ( DHL account)"""
    D='D'


class BillCode(Enum):
    """DHL billing options"""
    DSA='DSA'
    DBA='DBA'
    TCA='TCA'
    IEA='IEA'
    UAN='UAN'


class CommunicationType(Enum):
    """Communications line type (P: phone, F: fax)"""
    P='P'
    F='F'


class ConsigneeIDTypeType(Enum):
    S='S'
    E='E'
    D='D'


class CurrencyRoleTypeCode(Enum):
    """CurrencyRoleTypeCode"""
    BILLCU='BILLCU'
    PULCL='PULCL'
    INVCU='INVCU'
    BASEC='BASEC'


class DimensionUnit(Enum):
    """Dimension Unit I (inches)"""
    C='C'
    I='I'


class DlvyNotificationFlagType(Enum):
    Y='Y'
    N='N'


class DoorTo(Enum):
    """Defines the type of delivery service that applies to the shipment"""
    DD='DD'
    DA='DA'
    AA='AA'
    DC='DC'


class DutyTaxPaymentType(Enum):
    """Duty and tax charge payment type (S:Shipper, R:Recipient, T:Third
    Party/Other)"""
    S='S'
    R='R'
    T='T'


class ExportReasonCode(Enum):
    """Export reason code (P:Permanent, T:Temporary, R:Re-Export)"""
    P='P'
    T='T'
    R='R'


class IDType(Enum):
    """ID Type"""
    SSN='SSN'
    EIN='EIN'
    DUNS='DUNS'


class ImageFormat(Enum):
    """Image Format"""
    PDF='PDF'
    PNG='PNG'
    TIFF='TIFF'
    GIF='GIF'
    JPEG='JPEG'


class LabelImageFormat(Enum):
    """LabelImageFormat"""
    PDF='PDF'
    ZPL_2='ZPL2'
    EPL_2='EPL2'


class LabelTemplate(Enum):
    """LabelTemplate"""
    _8_X_4_A_4_PDF='8X4_A4_PDF'
    _8_X_4_THERMAL='8X4_thermal'
    _8_X_4_A_4_TC_PDF='8X4_A4_TC_PDF'
    _6_X_4_THERMAL='6X4_thermal'
    _6_X_4_A_4_PDF='6X4_A4_PDF'
    _8_X_4_CI_PDF='8X4_CI_PDF'
    _8_X_4_CI_THERMAL='8X4_CI_thermal'


class LevelOfDetails(Enum):
    """Checkpoint details selection flag"""
    LAST_CHECK_POINT_ONLY='LAST_CHECK_POINT_ONLY'
    ALL_CHECK_POINTS='ALL_CHECK_POINTS'


class LogoImageFormat(Enum):
    """LogoImage Format"""
    PNG='PNG'
    GIF='GIF'
    JPEG='JPEG'
    JPG='JPG'


class OutputFormat(Enum):
    """OutputFormat"""
    PDF='PDF'
    PL_2='PL2'
    ZPL_2='ZPL2'
    JPG='JPG'
    PNG='PNG'
    EPL_2='EPL2'
    EPLN='EPLN'
    ZPLN='ZPLN'


class PLTStatus(Enum):
    """PLTStatus"""
    A='A'
    D='D'
    S='S'


class PackageType(Enum):
    """Package Type (EE: DHL Express Envelope, OD:Other DHL Packaging,
    CP:Customer-provided.Ground shipments must choose CP)"""
    EE='EE'
    OD='OD'
    CP='CP'


class PaymentType(Enum):
    """payment type (S:Shipper,R:Recipient,T:Third Party)"""
    S='S'
    R='R'
    T='T'


class PiecesEnabled(Enum):
    """Pieces Enabling Flag"""
    Y='Y'
    N='N'


class PiecesEnabledType(Enum):
    """S for Only shipment Details,B for Both
    Shipment and Piece Details,P for only Piece Details"""
    S='S'
    B='B'
    P='P'


class RegionCode(Enum):
    """RegionCode"""
    AP='AP'
    EA='EA'
    AM='AM'


class ResidenceOrBusiness(Enum):
    """Identifies if a location is a business, residence, or both (B:Business,
    R:Residence, C:Business Residence)"""
    B='B'
    R='R'
    C='C'


class SEDNumber(Enum):
    FTSR='FTSR'
    XTN='XTN'
    SAS='SAS'


class SEDNumberType(Enum):
    F='F'
    X='X'
    S='S'


class ShipmentPaymentType(Enum):
    """Shipment payment type (S:Shipper, R:Recipient, T:Third party/other)"""
    S='S'
    R='R'
    T='T'


class ShipperIDTypeType(Enum):
    S='S'
    E='E'
    D='D'


class Type(Enum):
    """Image Type"""
    HWB='HWB'
    INV='INV'
    PNV='PNV'
    COO='COO'
    NAF='NAF'
    CIN='CIN'
    DCL='DCL'


class WeightUnit(Enum):
    """Unit of weight measurement (L:Pounds)"""
    K='K'
    L='L'


class WeightUnitType(Enum):
    L='L'
    K='K'
    G='G'


class YesNo(Enum):
    """Boolean flag"""
    Y='Y'
    N='N'


class KnownTrackingRequest(GeneratedsSuper):
    """Root element for known shipment tracking request"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, schemaVersion=1.0, Request=None, LanguageCode=None, AWBNumber=None, LPNumber=None, LevelOfDetails=None, PiecesEnabled=None, CountryCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.schemaVersion = _cast(float, schemaVersion)
        self.schemaVersion_nsprefix_ = None
        self.Request = Request
        self.Request_nsprefix_ = None
        self.LanguageCode = LanguageCode
        self.validate_LanguageCode(self.LanguageCode)
        self.LanguageCode_nsprefix_ = None
        if AWBNumber is None:
            self.AWBNumber = []
        else:
            self.AWBNumber = AWBNumber
        self.AWBNumber_nsprefix_ = None
        if LPNumber is None:
            self.LPNumber = []
        else:
            self.LPNumber = LPNumber
        self.LPNumber_nsprefix_ = None
        self.LevelOfDetails = LevelOfDetails
        self.validate_LevelOfDetails(self.LevelOfDetails)
        self.LevelOfDetails_nsprefix_ = None
        self.PiecesEnabled = PiecesEnabled
        self.validate_PiecesEnabledType(self.PiecesEnabled)
        self.PiecesEnabled_nsprefix_ = None
        self.CountryCode = CountryCode
        self.validate_CountryCode(self.CountryCode)
        self.CountryCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, KnownTrackingRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if KnownTrackingRequest.subclass:
            return KnownTrackingRequest.subclass(*args_, **kwargs_)
        else:
            return KnownTrackingRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Request(self):
        return self.Request
    def set_Request(self, Request):
        self.Request = Request
    def get_LanguageCode(self):
        return self.LanguageCode
    def set_LanguageCode(self, LanguageCode):
        self.LanguageCode = LanguageCode
    def get_AWBNumber(self):
        return self.AWBNumber
    def set_AWBNumber(self, AWBNumber):
        self.AWBNumber = AWBNumber
    def add_AWBNumber(self, value):
        self.AWBNumber.append(value)
    def insert_AWBNumber_at(self, index, value):
        self.AWBNumber.insert(index, value)
    def replace_AWBNumber_at(self, index, value):
        self.AWBNumber[index] = value
    def get_LPNumber(self):
        return self.LPNumber
    def set_LPNumber(self, LPNumber):
        self.LPNumber = LPNumber
    def add_LPNumber(self, value):
        self.LPNumber.append(value)
    def insert_LPNumber_at(self, index, value):
        self.LPNumber.insert(index, value)
    def replace_LPNumber_at(self, index, value):
        self.LPNumber[index] = value
    def get_LevelOfDetails(self):
        return self.LevelOfDetails
    def set_LevelOfDetails(self, LevelOfDetails):
        self.LevelOfDetails = LevelOfDetails
    def get_PiecesEnabled(self):
        return self.PiecesEnabled
    def set_PiecesEnabled(self, PiecesEnabled):
        self.PiecesEnabled = PiecesEnabled
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def get_schemaVersion(self):
        return self.schemaVersion
    def set_schemaVersion(self, schemaVersion):
        self.schemaVersion = schemaVersion
    def validate_LanguageCode(self, value):
        result = True
        # Validate type LanguageCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_AWBNumber(self, value):
        result = True
        # Validate type AWBNumber, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 11:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on AWBNumber' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_TrackingPieceID(self, value):
        result = True
        # Validate type TrackingPieceID, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on TrackingPieceID' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on TrackingPieceID' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_LevelOfDetails(self, value):
        result = True
        # Validate type LevelOfDetails, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['LAST_CHECK_POINT_ONLY', 'ALL_CHECK_POINTS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LevelOfDetails' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PiecesEnabledType(self, value):
        result = True
        # Validate type PiecesEnabledType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['S', 'B', 'P']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on PiecesEnabledType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CountryCode(self, value):
        result = True
        # Validate type CountryCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CountryCode' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Request is not None or
            self.LanguageCode is not None or
            self.AWBNumber or
            self.LPNumber or
            self.LevelOfDetails is not None or
            self.PiecesEnabled is not None or
            self.CountryCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='KnownTrackingRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('KnownTrackingRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'KnownTrackingRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='KnownTrackingRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='KnownTrackingRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='KnownTrackingRequest'):
        if self.schemaVersion is not None and 'schemaVersion' not in already_processed:
            already_processed.add('schemaVersion')
            outfile.write(' schemaVersion="%s"' % self.gds_format_decimal(self.schemaVersion, input_name='schemaVersion'))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='KnownTrackingRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Request is not None:
            namespaceprefix_ = self.Request_nsprefix_ + ':' if (UseCapturedNS_ and self.Request_nsprefix_) else ''
            self.Request.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Request', pretty_print=pretty_print)
        if self.LanguageCode is not None:
            namespaceprefix_ = self.LanguageCode_nsprefix_ + ':' if (UseCapturedNS_ and self.LanguageCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLanguageCode>%s</%sLanguageCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LanguageCode), input_name='LanguageCode')), namespaceprefix_ , eol_))
        for AWBNumber_ in self.AWBNumber:
            namespaceprefix_ = self.AWBNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.AWBNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAWBNumber>%s</%sAWBNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(AWBNumber_), input_name='AWBNumber')), namespaceprefix_ , eol_))
        for LPNumber_ in self.LPNumber:
            namespaceprefix_ = self.LPNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.LPNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLPNumber>%s</%sLPNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(LPNumber_), input_name='LPNumber')), namespaceprefix_ , eol_))
        if self.LevelOfDetails is not None:
            namespaceprefix_ = self.LevelOfDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.LevelOfDetails_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLevelOfDetails>%s</%sLevelOfDetails>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LevelOfDetails), input_name='LevelOfDetails')), namespaceprefix_ , eol_))
        if self.PiecesEnabled is not None:
            namespaceprefix_ = self.PiecesEnabled_nsprefix_ + ':' if (UseCapturedNS_ and self.PiecesEnabled_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPiecesEnabled>%s</%sPiecesEnabled>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PiecesEnabled), input_name='PiecesEnabled')), namespaceprefix_ , eol_))
        if self.CountryCode is not None:
            namespaceprefix_ = self.CountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryCode>%s</%sCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryCode), input_name='CountryCode')), namespaceprefix_ , eol_))
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
        value = find_attr_value_('schemaVersion', node)
        if value is not None and 'schemaVersion' not in already_processed:
            already_processed.add('schemaVersion')
            value = self.gds_parse_decimal(value, node, 'schemaVersion')
            self.schemaVersion = value
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Request':
            obj_ = Request.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Request = obj_
            obj_.original_tagname_ = 'Request'
        elif nodeName_ == 'LanguageCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LanguageCode')
            value_ = self.gds_validate_string(value_, node, 'LanguageCode')
            self.LanguageCode = value_
            self.LanguageCode_nsprefix_ = child_.prefix
            # validate type LanguageCode
            self.validate_LanguageCode(self.LanguageCode)
        elif nodeName_ == 'AWBNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AWBNumber')
            value_ = self.gds_validate_string(value_, node, 'AWBNumber')
            self.AWBNumber.append(value_)
            self.AWBNumber_nsprefix_ = child_.prefix
            # validate type AWBNumber
            self.validate_AWBNumber(self.AWBNumber[-1])
        elif nodeName_ == 'LPNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LPNumber')
            value_ = self.gds_validate_string(value_, node, 'LPNumber')
            self.LPNumber.append(value_)
            self.LPNumber_nsprefix_ = child_.prefix
            # validate type TrackingPieceID
            self.validate_TrackingPieceID(self.LPNumber[-1])
        elif nodeName_ == 'LevelOfDetails':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LevelOfDetails')
            value_ = self.gds_validate_string(value_, node, 'LevelOfDetails')
            self.LevelOfDetails = value_
            self.LevelOfDetails_nsprefix_ = child_.prefix
            # validate type LevelOfDetails
            self.validate_LevelOfDetails(self.LevelOfDetails)
        elif nodeName_ == 'PiecesEnabled':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PiecesEnabled')
            value_ = self.gds_validate_string(value_, node, 'PiecesEnabled')
            self.PiecesEnabled = value_
            self.PiecesEnabled_nsprefix_ = child_.prefix
            # validate type PiecesEnabledType
            self.validate_PiecesEnabledType(self.PiecesEnabled)
        elif nodeName_ == 'CountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryCode')
            value_ = self.gds_validate_string(value_, node, 'CountryCode')
            self.CountryCode = value_
            self.CountryCode_nsprefix_ = child_.prefix
            # validate type CountryCode
            self.validate_CountryCode(self.CountryCode)
# end class KnownTrackingRequest


class DataTypes(GeneratedsSuper):
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
                CurrentSubclassModule_, DataTypes)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DataTypes.subclass:
            return DataTypes.subclass(*args_, **kwargs_)
        else:
            return DataTypes(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DataTypes', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DataTypes')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DataTypes':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DataTypes')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DataTypes', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DataTypes'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DataTypes', fromsubclass_=False, pretty_print=True):
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
# end class DataTypes


class Billing(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ShipperAccountNumber=None, ShippingPaymentType=None, BillingAccountNumber=None, DutyPaymentType=None, DutyAccountNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ShipperAccountNumber = ShipperAccountNumber
        self.validate_AccountNumber(self.ShipperAccountNumber)
        self.ShipperAccountNumber_nsprefix_ = None
        self.ShippingPaymentType = ShippingPaymentType
        self.validate_PaymentType(self.ShippingPaymentType)
        self.ShippingPaymentType_nsprefix_ = None
        self.BillingAccountNumber = BillingAccountNumber
        self.validate_AccountNumber(self.BillingAccountNumber)
        self.BillingAccountNumber_nsprefix_ = None
        self.DutyPaymentType = DutyPaymentType
        self.validate_DutyTaxPaymentType(self.DutyPaymentType)
        self.DutyPaymentType_nsprefix_ = None
        self.DutyAccountNumber = DutyAccountNumber
        self.validate_AccountNumber(self.DutyAccountNumber)
        self.DutyAccountNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Billing)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Billing.subclass:
            return Billing.subclass(*args_, **kwargs_)
        else:
            return Billing(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ShipperAccountNumber(self):
        return self.ShipperAccountNumber
    def set_ShipperAccountNumber(self, ShipperAccountNumber):
        self.ShipperAccountNumber = ShipperAccountNumber
    def get_ShippingPaymentType(self):
        return self.ShippingPaymentType
    def set_ShippingPaymentType(self, ShippingPaymentType):
        self.ShippingPaymentType = ShippingPaymentType
    def get_BillingAccountNumber(self):
        return self.BillingAccountNumber
    def set_BillingAccountNumber(self, BillingAccountNumber):
        self.BillingAccountNumber = BillingAccountNumber
    def get_DutyPaymentType(self):
        return self.DutyPaymentType
    def set_DutyPaymentType(self, DutyPaymentType):
        self.DutyPaymentType = DutyPaymentType
    def get_DutyAccountNumber(self):
        return self.DutyAccountNumber
    def set_DutyAccountNumber(self, DutyAccountNumber):
        self.DutyAccountNumber = DutyAccountNumber
    def validate_AccountNumber(self, value):
        result = True
        # Validate type AccountNumber, a restriction on xsd:positiveInteger.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 100000000:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on AccountNumber' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999999999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on AccountNumber' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_PaymentType(self, value):
        result = True
        # Validate type PaymentType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['S', 'R', 'T']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on PaymentType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on PaymentType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DutyTaxPaymentType(self, value):
        result = True
        # Validate type DutyTaxPaymentType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['S', 'R', 'T']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DutyTaxPaymentType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on DutyTaxPaymentType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.ShipperAccountNumber is not None or
            self.ShippingPaymentType is not None or
            self.BillingAccountNumber is not None or
            self.DutyPaymentType is not None or
            self.DutyAccountNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Billing', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Billing')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Billing':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Billing')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Billing', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Billing'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Billing', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ShipperAccountNumber is not None:
            namespaceprefix_ = self.ShipperAccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipperAccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipperAccountNumber>%s</%sShipperAccountNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.ShipperAccountNumber, input_name='ShipperAccountNumber'), namespaceprefix_ , eol_))
        if self.ShippingPaymentType is not None:
            namespaceprefix_ = self.ShippingPaymentType_nsprefix_ + ':' if (UseCapturedNS_ and self.ShippingPaymentType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShippingPaymentType>%s</%sShippingPaymentType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShippingPaymentType), input_name='ShippingPaymentType')), namespaceprefix_ , eol_))
        if self.BillingAccountNumber is not None:
            namespaceprefix_ = self.BillingAccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.BillingAccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBillingAccountNumber>%s</%sBillingAccountNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.BillingAccountNumber, input_name='BillingAccountNumber'), namespaceprefix_ , eol_))
        if self.DutyPaymentType is not None:
            namespaceprefix_ = self.DutyPaymentType_nsprefix_ + ':' if (UseCapturedNS_ and self.DutyPaymentType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDutyPaymentType>%s</%sDutyPaymentType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DutyPaymentType), input_name='DutyPaymentType')), namespaceprefix_ , eol_))
        if self.DutyAccountNumber is not None:
            namespaceprefix_ = self.DutyAccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.DutyAccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDutyAccountNumber>%s</%sDutyAccountNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.DutyAccountNumber, input_name='DutyAccountNumber'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ShipperAccountNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'ShipperAccountNumber')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'ShipperAccountNumber')
            self.ShipperAccountNumber = ival_
            self.ShipperAccountNumber_nsprefix_ = child_.prefix
            # validate type AccountNumber
            self.validate_AccountNumber(self.ShipperAccountNumber)
        elif nodeName_ == 'ShippingPaymentType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShippingPaymentType')
            value_ = self.gds_validate_string(value_, node, 'ShippingPaymentType')
            self.ShippingPaymentType = value_
            self.ShippingPaymentType_nsprefix_ = child_.prefix
            # validate type PaymentType
            self.validate_PaymentType(self.ShippingPaymentType)
        elif nodeName_ == 'BillingAccountNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'BillingAccountNumber')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'BillingAccountNumber')
            self.BillingAccountNumber = ival_
            self.BillingAccountNumber_nsprefix_ = child_.prefix
            # validate type AccountNumber
            self.validate_AccountNumber(self.BillingAccountNumber)
        elif nodeName_ == 'DutyPaymentType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DutyPaymentType')
            value_ = self.gds_validate_string(value_, node, 'DutyPaymentType')
            self.DutyPaymentType = value_
            self.DutyPaymentType_nsprefix_ = child_.prefix
            # validate type DutyTaxPaymentType
            self.validate_DutyTaxPaymentType(self.DutyPaymentType)
        elif nodeName_ == 'DutyAccountNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'DutyAccountNumber')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'DutyAccountNumber')
            self.DutyAccountNumber = ival_
            self.DutyAccountNumber_nsprefix_ = child_.prefix
            # validate type AccountNumber
            self.validate_AccountNumber(self.DutyAccountNumber)
# end class Billing


class Commodity(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CommodityCode=None, CommodityName=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CommodityCode = CommodityCode
        self.validate_CommodityCode(self.CommodityCode)
        self.CommodityCode_nsprefix_ = None
        self.CommodityName = CommodityName
        self.validate_CommodityName(self.CommodityName)
        self.CommodityName_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Commodity)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Commodity.subclass:
            return Commodity.subclass(*args_, **kwargs_)
        else:
            return Commodity(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CommodityCode(self):
        return self.CommodityCode
    def set_CommodityCode(self, CommodityCode):
        self.CommodityCode = CommodityCode
    def get_CommodityName(self):
        return self.CommodityName
    def set_CommodityName(self, CommodityName):
        self.CommodityName = CommodityName
    def validate_CommodityCode(self, value):
        result = True
        # Validate type CommodityCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CommodityCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on CommodityCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CommodityName(self, value):
        result = True
        # Validate type CommodityName, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CommodityName' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.CommodityCode is not None or
            self.CommodityName is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Commodity', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Commodity')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Commodity':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Commodity')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Commodity', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Commodity'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Commodity', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CommodityCode is not None:
            namespaceprefix_ = self.CommodityCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CommodityCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCommodityCode>%s</%sCommodityCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CommodityCode), input_name='CommodityCode')), namespaceprefix_ , eol_))
        if self.CommodityName is not None:
            namespaceprefix_ = self.CommodityName_nsprefix_ + ':' if (UseCapturedNS_ and self.CommodityName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCommodityName>%s</%sCommodityName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CommodityName), input_name='CommodityName')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'CommodityCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CommodityCode')
            value_ = self.gds_validate_string(value_, node, 'CommodityCode')
            self.CommodityCode = value_
            self.CommodityCode_nsprefix_ = child_.prefix
            # validate type CommodityCode
            self.validate_CommodityCode(self.CommodityCode)
        elif nodeName_ == 'CommodityName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CommodityName')
            value_ = self.gds_validate_string(value_, node, 'CommodityName')
            self.CommodityName = value_
            self.CommodityName_nsprefix_ = child_.prefix
            # validate type CommodityName
            self.validate_CommodityName(self.CommodityName)
# end class Commodity


class Consignee(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CompanyName=None, AddressLine=None, City=None, Division=None, DivisionCode=None, PostalCode=None, CountryCode=None, CountryName=None, FederalTaxId=None, StateTaxId=None, Contact=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CompanyName = CompanyName
        self.validate_CompanyNameValidator(self.CompanyName)
        self.CompanyName_nsprefix_ = None
        if AddressLine is None:
            self.AddressLine = []
        else:
            self.AddressLine = AddressLine
        self.AddressLine_nsprefix_ = None
        self.City = City
        self.validate_City(self.City)
        self.City_nsprefix_ = None
        self.Division = Division
        self.validate_Division(self.Division)
        self.Division_nsprefix_ = None
        self.DivisionCode = DivisionCode
        self.validate_DivisionCodeType(self.DivisionCode)
        self.DivisionCode_nsprefix_ = None
        self.PostalCode = PostalCode
        self.validate_PostalCode(self.PostalCode)
        self.PostalCode_nsprefix_ = None
        self.CountryCode = CountryCode
        self.validate_CountryCode(self.CountryCode)
        self.CountryCode_nsprefix_ = None
        self.CountryName = CountryName
        self.validate_CountryName(self.CountryName)
        self.CountryName_nsprefix_ = None
        self.FederalTaxId = FederalTaxId
        self.validate_FederalTaxIdType(self.FederalTaxId)
        self.FederalTaxId_nsprefix_ = None
        self.StateTaxId = StateTaxId
        self.validate_StateTaxIdType(self.StateTaxId)
        self.StateTaxId_nsprefix_ = None
        self.Contact = Contact
        self.Contact_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Consignee)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Consignee.subclass:
            return Consignee.subclass(*args_, **kwargs_)
        else:
            return Consignee(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CompanyName(self):
        return self.CompanyName
    def set_CompanyName(self, CompanyName):
        self.CompanyName = CompanyName
    def get_AddressLine(self):
        return self.AddressLine
    def set_AddressLine(self, AddressLine):
        self.AddressLine = AddressLine
    def add_AddressLine(self, value):
        self.AddressLine.append(value)
    def insert_AddressLine_at(self, index, value):
        self.AddressLine.insert(index, value)
    def replace_AddressLine_at(self, index, value):
        self.AddressLine[index] = value
    def get_City(self):
        return self.City
    def set_City(self, City):
        self.City = City
    def get_Division(self):
        return self.Division
    def set_Division(self, Division):
        self.Division = Division
    def get_DivisionCode(self):
        return self.DivisionCode
    def set_DivisionCode(self, DivisionCode):
        self.DivisionCode = DivisionCode
    def get_PostalCode(self):
        return self.PostalCode
    def set_PostalCode(self, PostalCode):
        self.PostalCode = PostalCode
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def get_CountryName(self):
        return self.CountryName
    def set_CountryName(self, CountryName):
        self.CountryName = CountryName
    def get_FederalTaxId(self):
        return self.FederalTaxId
    def set_FederalTaxId(self, FederalTaxId):
        self.FederalTaxId = FederalTaxId
    def get_StateTaxId(self):
        return self.StateTaxId
    def set_StateTaxId(self, StateTaxId):
        self.StateTaxId = StateTaxId
    def get_Contact(self):
        return self.Contact
    def set_Contact(self, Contact):
        self.Contact = Contact
    def validate_CompanyNameValidator(self, value):
        result = True
        # Validate type CompanyNameValidator, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CompanyNameValidator' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_AddressLine(self, value):
        result = True
        # Validate type AddressLine, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on AddressLine' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_City(self, value):
        result = True
        # Validate type City, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on City' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_Division(self, value):
        result = True
        # Validate type Division, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on Division' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DivisionCodeType(self, value):
        result = True
        # Validate type DivisionCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on DivisionCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PostalCode(self, value):
        result = True
        # Validate type PostalCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_CountryCode(self, value):
        result = True
        # Validate type CountryCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CountryCode' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CountryName(self, value):
        result = True
        # Validate type CountryName, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CountryName' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_FederalTaxIdType(self, value):
        result = True
        # Validate type FederalTaxIdType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on FederalTaxIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on FederalTaxIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_StateTaxIdType(self, value):
        result = True
        # Validate type StateTaxIdType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on StateTaxIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on StateTaxIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.CompanyName is not None or
            self.AddressLine or
            self.City is not None or
            self.Division is not None or
            self.DivisionCode is not None or
            self.PostalCode is not None or
            self.CountryCode is not None or
            self.CountryName is not None or
            self.FederalTaxId is not None or
            self.StateTaxId is not None or
            self.Contact is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Consignee', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Consignee')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Consignee':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Consignee')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Consignee', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Consignee'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Consignee', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CompanyName is not None:
            namespaceprefix_ = self.CompanyName_nsprefix_ + ':' if (UseCapturedNS_ and self.CompanyName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCompanyName>%s</%sCompanyName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CompanyName), input_name='CompanyName')), namespaceprefix_ , eol_))
        for AddressLine_ in self.AddressLine:
            namespaceprefix_ = self.AddressLine_nsprefix_ + ':' if (UseCapturedNS_ and self.AddressLine_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAddressLine>%s</%sAddressLine>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(AddressLine_), input_name='AddressLine')), namespaceprefix_ , eol_))
        if self.City is not None:
            namespaceprefix_ = self.City_nsprefix_ + ':' if (UseCapturedNS_ and self.City_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCity>%s</%sCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.City), input_name='City')), namespaceprefix_ , eol_))
        if self.Division is not None:
            namespaceprefix_ = self.Division_nsprefix_ + ':' if (UseCapturedNS_ and self.Division_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDivision>%s</%sDivision>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Division), input_name='Division')), namespaceprefix_ , eol_))
        if self.DivisionCode is not None:
            namespaceprefix_ = self.DivisionCode_nsprefix_ + ':' if (UseCapturedNS_ and self.DivisionCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDivisionCode>%s</%sDivisionCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DivisionCode), input_name='DivisionCode')), namespaceprefix_ , eol_))
        if self.PostalCode is not None:
            namespaceprefix_ = self.PostalCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PostalCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPostalCode>%s</%sPostalCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PostalCode), input_name='PostalCode')), namespaceprefix_ , eol_))
        if self.CountryCode is not None:
            namespaceprefix_ = self.CountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryCode>%s</%sCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryCode), input_name='CountryCode')), namespaceprefix_ , eol_))
        if self.CountryName is not None:
            namespaceprefix_ = self.CountryName_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryName>%s</%sCountryName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryName), input_name='CountryName')), namespaceprefix_ , eol_))
        if self.FederalTaxId is not None:
            namespaceprefix_ = self.FederalTaxId_nsprefix_ + ':' if (UseCapturedNS_ and self.FederalTaxId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFederalTaxId>%s</%sFederalTaxId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FederalTaxId), input_name='FederalTaxId')), namespaceprefix_ , eol_))
        if self.StateTaxId is not None:
            namespaceprefix_ = self.StateTaxId_nsprefix_ + ':' if (UseCapturedNS_ and self.StateTaxId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStateTaxId>%s</%sStateTaxId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.StateTaxId), input_name='StateTaxId')), namespaceprefix_ , eol_))
        if self.Contact is not None:
            namespaceprefix_ = self.Contact_nsprefix_ + ':' if (UseCapturedNS_ and self.Contact_nsprefix_) else ''
            self.Contact.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Contact', pretty_print=pretty_print)
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
        if nodeName_ == 'CompanyName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CompanyName')
            value_ = self.gds_validate_string(value_, node, 'CompanyName')
            self.CompanyName = value_
            self.CompanyName_nsprefix_ = child_.prefix
            # validate type CompanyNameValidator
            self.validate_CompanyNameValidator(self.CompanyName)
        elif nodeName_ == 'AddressLine':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AddressLine')
            value_ = self.gds_validate_string(value_, node, 'AddressLine')
            self.AddressLine.append(value_)
            self.AddressLine_nsprefix_ = child_.prefix
            # validate type AddressLine
            self.validate_AddressLine(self.AddressLine[-1])
        elif nodeName_ == 'City':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'City')
            value_ = self.gds_validate_string(value_, node, 'City')
            self.City = value_
            self.City_nsprefix_ = child_.prefix
            # validate type City
            self.validate_City(self.City)
        elif nodeName_ == 'Division':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Division')
            value_ = self.gds_validate_string(value_, node, 'Division')
            self.Division = value_
            self.Division_nsprefix_ = child_.prefix
            # validate type Division
            self.validate_Division(self.Division)
        elif nodeName_ == 'DivisionCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DivisionCode')
            value_ = self.gds_validate_string(value_, node, 'DivisionCode')
            self.DivisionCode = value_
            self.DivisionCode_nsprefix_ = child_.prefix
            # validate type DivisionCodeType
            self.validate_DivisionCodeType(self.DivisionCode)
        elif nodeName_ == 'PostalCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PostalCode')
            value_ = self.gds_validate_string(value_, node, 'PostalCode')
            self.PostalCode = value_
            self.PostalCode_nsprefix_ = child_.prefix
            # validate type PostalCode
            self.validate_PostalCode(self.PostalCode)
        elif nodeName_ == 'CountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryCode')
            value_ = self.gds_validate_string(value_, node, 'CountryCode')
            self.CountryCode = value_
            self.CountryCode_nsprefix_ = child_.prefix
            # validate type CountryCode
            self.validate_CountryCode(self.CountryCode)
        elif nodeName_ == 'CountryName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryName')
            value_ = self.gds_validate_string(value_, node, 'CountryName')
            self.CountryName = value_
            self.CountryName_nsprefix_ = child_.prefix
            # validate type CountryName
            self.validate_CountryName(self.CountryName)
        elif nodeName_ == 'FederalTaxId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FederalTaxId')
            value_ = self.gds_validate_string(value_, node, 'FederalTaxId')
            self.FederalTaxId = value_
            self.FederalTaxId_nsprefix_ = child_.prefix
            # validate type FederalTaxIdType
            self.validate_FederalTaxIdType(self.FederalTaxId)
        elif nodeName_ == 'StateTaxId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'StateTaxId')
            value_ = self.gds_validate_string(value_, node, 'StateTaxId')
            self.StateTaxId = value_
            self.StateTaxId_nsprefix_ = child_.prefix
            # validate type StateTaxIdType
            self.validate_StateTaxIdType(self.StateTaxId)
        elif nodeName_ == 'Contact':
            obj_ = Contact.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Contact = obj_
            obj_.original_tagname_ = 'Contact'
# end class Consignee


class Contact(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PersonName=None, PhoneNumber=None, PhoneExtension=None, FaxNumber=None, Telex=None, Email=None, MobilePhoneNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PersonName = PersonName
        self.validate_PersonName(self.PersonName)
        self.PersonName_nsprefix_ = None
        self.PhoneNumber = PhoneNumber
        self.validate_PhoneNumber(self.PhoneNumber)
        self.PhoneNumber_nsprefix_ = None
        self.PhoneExtension = PhoneExtension
        self.validate_PhoneExtension(self.PhoneExtension)
        self.PhoneExtension_nsprefix_ = None
        self.FaxNumber = FaxNumber
        self.validate_PhoneNumber(self.FaxNumber)
        self.FaxNumber_nsprefix_ = None
        self.Telex = Telex
        self.validate_Telex(self.Telex)
        self.Telex_nsprefix_ = None
        self.Email = Email
        self.Email_nsprefix_ = None
        self.MobilePhoneNumber = MobilePhoneNumber
        self.validate_MobilePhoneNumber(self.MobilePhoneNumber)
        self.MobilePhoneNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Contact)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Contact.subclass:
            return Contact.subclass(*args_, **kwargs_)
        else:
            return Contact(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PersonName(self):
        return self.PersonName
    def set_PersonName(self, PersonName):
        self.PersonName = PersonName
    def get_PhoneNumber(self):
        return self.PhoneNumber
    def set_PhoneNumber(self, PhoneNumber):
        self.PhoneNumber = PhoneNumber
    def get_PhoneExtension(self):
        return self.PhoneExtension
    def set_PhoneExtension(self, PhoneExtension):
        self.PhoneExtension = PhoneExtension
    def get_FaxNumber(self):
        return self.FaxNumber
    def set_FaxNumber(self, FaxNumber):
        self.FaxNumber = FaxNumber
    def get_Telex(self):
        return self.Telex
    def set_Telex(self, Telex):
        self.Telex = Telex
    def get_Email(self):
        return self.Email
    def set_Email(self, Email):
        self.Email = Email
    def get_MobilePhoneNumber(self):
        return self.MobilePhoneNumber
    def set_MobilePhoneNumber(self, MobilePhoneNumber):
        self.MobilePhoneNumber = MobilePhoneNumber
    def validate_PersonName(self, value):
        result = True
        # Validate type PersonName, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on PersonName' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PhoneNumber(self, value):
        result = True
        # Validate type PhoneNumber, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_PhoneExtension(self, value):
        result = True
        # Validate type PhoneExtension, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on PhoneExtension' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_Telex(self, value):
        result = True
        # Validate type Telex, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 25:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on Telex' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_MobilePhoneNumber(self, value):
        result = True
        # Validate type MobilePhoneNumber, a restriction on xsd:positiveInteger.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value > 9999999999999999999999999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on MobilePhoneNumber' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.PersonName is not None or
            self.PhoneNumber is not None or
            self.PhoneExtension is not None or
            self.FaxNumber is not None or
            self.Telex is not None or
            self.Email is not None or
            self.MobilePhoneNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Contact', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Contact')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Contact':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Contact')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Contact', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Contact'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Contact', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PersonName is not None:
            namespaceprefix_ = self.PersonName_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPersonName>%s</%sPersonName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PersonName), input_name='PersonName')), namespaceprefix_ , eol_))
        if self.PhoneNumber is not None:
            namespaceprefix_ = self.PhoneNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PhoneNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhoneNumber>%s</%sPhoneNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhoneNumber), input_name='PhoneNumber')), namespaceprefix_ , eol_))
        if self.PhoneExtension is not None:
            namespaceprefix_ = self.PhoneExtension_nsprefix_ + ':' if (UseCapturedNS_ and self.PhoneExtension_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhoneExtension>%s</%sPhoneExtension>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhoneExtension), input_name='PhoneExtension')), namespaceprefix_ , eol_))
        if self.FaxNumber is not None:
            namespaceprefix_ = self.FaxNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.FaxNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFaxNumber>%s</%sFaxNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FaxNumber), input_name='FaxNumber')), namespaceprefix_ , eol_))
        if self.Telex is not None:
            namespaceprefix_ = self.Telex_nsprefix_ + ':' if (UseCapturedNS_ and self.Telex_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTelex>%s</%sTelex>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Telex), input_name='Telex')), namespaceprefix_ , eol_))
        if self.Email is not None:
            namespaceprefix_ = self.Email_nsprefix_ + ':' if (UseCapturedNS_ and self.Email_nsprefix_) else ''
            self.Email.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Email', pretty_print=pretty_print)
        if self.MobilePhoneNumber is not None:
            namespaceprefix_ = self.MobilePhoneNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.MobilePhoneNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMobilePhoneNumber>%s</%sMobilePhoneNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.MobilePhoneNumber, input_name='MobilePhoneNumber'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'PersonName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PersonName')
            value_ = self.gds_validate_string(value_, node, 'PersonName')
            self.PersonName = value_
            self.PersonName_nsprefix_ = child_.prefix
            # validate type PersonName
            self.validate_PersonName(self.PersonName)
        elif nodeName_ == 'PhoneNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhoneNumber')
            value_ = self.gds_validate_string(value_, node, 'PhoneNumber')
            self.PhoneNumber = value_
            self.PhoneNumber_nsprefix_ = child_.prefix
            # validate type PhoneNumber
            self.validate_PhoneNumber(self.PhoneNumber)
        elif nodeName_ == 'PhoneExtension':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhoneExtension')
            value_ = self.gds_validate_string(value_, node, 'PhoneExtension')
            self.PhoneExtension = value_
            self.PhoneExtension_nsprefix_ = child_.prefix
            # validate type PhoneExtension
            self.validate_PhoneExtension(self.PhoneExtension)
        elif nodeName_ == 'FaxNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FaxNumber')
            value_ = self.gds_validate_string(value_, node, 'FaxNumber')
            self.FaxNumber = value_
            self.FaxNumber_nsprefix_ = child_.prefix
            # validate type PhoneNumber
            self.validate_PhoneNumber(self.FaxNumber)
        elif nodeName_ == 'Telex':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Telex')
            value_ = self.gds_validate_string(value_, node, 'Telex')
            self.Telex = value_
            self.Telex_nsprefix_ = child_.prefix
            # validate type Telex
            self.validate_Telex(self.Telex)
        elif nodeName_ == 'Email':
            obj_ = Email.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Email = obj_
            obj_.original_tagname_ = 'Email'
        elif nodeName_ == 'MobilePhoneNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'MobilePhoneNumber')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'MobilePhoneNumber')
            self.MobilePhoneNumber = ival_
            self.MobilePhoneNumber_nsprefix_ = child_.prefix
            # validate type MobilePhoneNumber
            self.validate_MobilePhoneNumber(self.MobilePhoneNumber)
# end class Contact


class Dutiable(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DeclaredValue=None, DeclaredCurrency=None, ScheduleB=None, ExportLicense=None, ShipperEIN=None, ShipperIDType=None, ConsigneeIDType=None, ImportLicense=None, ConsigneeEIN=None, TermsOfTrade=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DeclaredValue = DeclaredValue
        self.validate_Money(self.DeclaredValue)
        self.DeclaredValue_nsprefix_ = None
        self.DeclaredCurrency = DeclaredCurrency
        self.validate_CurrencyCode(self.DeclaredCurrency)
        self.DeclaredCurrency_nsprefix_ = None
        self.ScheduleB = ScheduleB
        self.validate_ScheduleB(self.ScheduleB)
        self.ScheduleB_nsprefix_ = None
        self.ExportLicense = ExportLicense
        self.ExportLicense_nsprefix_ = None
        self.ShipperEIN = ShipperEIN
        self.validate_ShipperEINType(self.ShipperEIN)
        self.ShipperEIN_nsprefix_ = None
        self.ShipperIDType = ShipperIDType
        self.validate_ShipperIDTypeType(self.ShipperIDType)
        self.ShipperIDType_nsprefix_ = None
        self.ConsigneeIDType = ConsigneeIDType
        self.validate_ConsigneeIDTypeType(self.ConsigneeIDType)
        self.ConsigneeIDType_nsprefix_ = None
        self.ImportLicense = ImportLicense
        self.ImportLicense_nsprefix_ = None
        self.ConsigneeEIN = ConsigneeEIN
        self.validate_ConsigneeEINType(self.ConsigneeEIN)
        self.ConsigneeEIN_nsprefix_ = None
        self.TermsOfTrade = TermsOfTrade
        self.TermsOfTrade_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Dutiable)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Dutiable.subclass:
            return Dutiable.subclass(*args_, **kwargs_)
        else:
            return Dutiable(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DeclaredValue(self):
        return self.DeclaredValue
    def set_DeclaredValue(self, DeclaredValue):
        self.DeclaredValue = DeclaredValue
    def get_DeclaredCurrency(self):
        return self.DeclaredCurrency
    def set_DeclaredCurrency(self, DeclaredCurrency):
        self.DeclaredCurrency = DeclaredCurrency
    def get_ScheduleB(self):
        return self.ScheduleB
    def set_ScheduleB(self, ScheduleB):
        self.ScheduleB = ScheduleB
    def get_ExportLicense(self):
        return self.ExportLicense
    def set_ExportLicense(self, ExportLicense):
        self.ExportLicense = ExportLicense
    def get_ShipperEIN(self):
        return self.ShipperEIN
    def set_ShipperEIN(self, ShipperEIN):
        self.ShipperEIN = ShipperEIN
    def get_ShipperIDType(self):
        return self.ShipperIDType
    def set_ShipperIDType(self, ShipperIDType):
        self.ShipperIDType = ShipperIDType
    def get_ConsigneeIDType(self):
        return self.ConsigneeIDType
    def set_ConsigneeIDType(self, ConsigneeIDType):
        self.ConsigneeIDType = ConsigneeIDType
    def get_ImportLicense(self):
        return self.ImportLicense
    def set_ImportLicense(self, ImportLicense):
        self.ImportLicense = ImportLicense
    def get_ConsigneeEIN(self):
        return self.ConsigneeEIN
    def set_ConsigneeEIN(self, ConsigneeEIN):
        self.ConsigneeEIN = ConsigneeEIN
    def get_TermsOfTrade(self):
        return self.TermsOfTrade
    def set_TermsOfTrade(self, TermsOfTrade):
        self.TermsOfTrade = TermsOfTrade
    def validate_Money(self, value):
        result = True
        # Validate type Money, a restriction on xsd:float.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, float):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (float)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0.00:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on Money' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999999999.99:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on Money' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_CurrencyCode(self, value):
        result = True
        # Validate type CurrencyCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CurrencyCode' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ScheduleB(self, value):
        result = True
        # Validate type ScheduleB, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 15:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ScheduleB' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ShipperEINType(self, value):
        result = True
        # Validate type ShipperEINType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ShipperEINType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ShipperIDTypeType(self, value):
        result = True
        # Validate type ShipperIDTypeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['S', 'E', 'D']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ShipperIDTypeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ConsigneeIDTypeType(self, value):
        result = True
        # Validate type ConsigneeIDTypeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['S', 'E', 'D']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ConsigneeIDTypeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on ConsigneeIDTypeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ConsigneeEINType(self, value):
        result = True
        # Validate type ConsigneeEINType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ConsigneeEINType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.DeclaredValue is not None or
            self.DeclaredCurrency is not None or
            self.ScheduleB is not None or
            self.ExportLicense is not None or
            self.ShipperEIN is not None or
            self.ShipperIDType is not None or
            self.ConsigneeIDType is not None or
            self.ImportLicense is not None or
            self.ConsigneeEIN is not None or
            self.TermsOfTrade is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Dutiable', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Dutiable')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Dutiable':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Dutiable')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Dutiable', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Dutiable'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Dutiable', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DeclaredValue is not None:
            namespaceprefix_ = self.DeclaredValue_nsprefix_ + ':' if (UseCapturedNS_ and self.DeclaredValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeclaredValue>%s</%sDeclaredValue>%s' % (namespaceprefix_ , self.gds_format_float(self.DeclaredValue, input_name='DeclaredValue'), namespaceprefix_ , eol_))
        if self.DeclaredCurrency is not None:
            namespaceprefix_ = self.DeclaredCurrency_nsprefix_ + ':' if (UseCapturedNS_ and self.DeclaredCurrency_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeclaredCurrency>%s</%sDeclaredCurrency>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DeclaredCurrency), input_name='DeclaredCurrency')), namespaceprefix_ , eol_))
        if self.ScheduleB is not None:
            namespaceprefix_ = self.ScheduleB_nsprefix_ + ':' if (UseCapturedNS_ and self.ScheduleB_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sScheduleB>%s</%sScheduleB>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ScheduleB), input_name='ScheduleB')), namespaceprefix_ , eol_))
        if self.ExportLicense is not None:
            namespaceprefix_ = self.ExportLicense_nsprefix_ + ':' if (UseCapturedNS_ and self.ExportLicense_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExportLicense>%s</%sExportLicense>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ExportLicense), input_name='ExportLicense')), namespaceprefix_ , eol_))
        if self.ShipperEIN is not None:
            namespaceprefix_ = self.ShipperEIN_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipperEIN_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipperEIN>%s</%sShipperEIN>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShipperEIN), input_name='ShipperEIN')), namespaceprefix_ , eol_))
        if self.ShipperIDType is not None:
            namespaceprefix_ = self.ShipperIDType_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipperIDType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipperIDType>%s</%sShipperIDType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShipperIDType), input_name='ShipperIDType')), namespaceprefix_ , eol_))
        if self.ConsigneeIDType is not None:
            namespaceprefix_ = self.ConsigneeIDType_nsprefix_ + ':' if (UseCapturedNS_ and self.ConsigneeIDType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sConsigneeIDType>%s</%sConsigneeIDType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ConsigneeIDType), input_name='ConsigneeIDType')), namespaceprefix_ , eol_))
        if self.ImportLicense is not None:
            namespaceprefix_ = self.ImportLicense_nsprefix_ + ':' if (UseCapturedNS_ and self.ImportLicense_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImportLicense>%s</%sImportLicense>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ImportLicense), input_name='ImportLicense')), namespaceprefix_ , eol_))
        if self.ConsigneeEIN is not None:
            namespaceprefix_ = self.ConsigneeEIN_nsprefix_ + ':' if (UseCapturedNS_ and self.ConsigneeEIN_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sConsigneeEIN>%s</%sConsigneeEIN>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ConsigneeEIN), input_name='ConsigneeEIN')), namespaceprefix_ , eol_))
        if self.TermsOfTrade is not None:
            namespaceprefix_ = self.TermsOfTrade_nsprefix_ + ':' if (UseCapturedNS_ and self.TermsOfTrade_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTermsOfTrade>%s</%sTermsOfTrade>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TermsOfTrade), input_name='TermsOfTrade')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'DeclaredValue' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'DeclaredValue')
            fval_ = self.gds_validate_float(fval_, node, 'DeclaredValue')
            self.DeclaredValue = fval_
            self.DeclaredValue_nsprefix_ = child_.prefix
            # validate type Money
            self.validate_Money(self.DeclaredValue)
        elif nodeName_ == 'DeclaredCurrency':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DeclaredCurrency')
            value_ = self.gds_validate_string(value_, node, 'DeclaredCurrency')
            self.DeclaredCurrency = value_
            self.DeclaredCurrency_nsprefix_ = child_.prefix
            # validate type CurrencyCode
            self.validate_CurrencyCode(self.DeclaredCurrency)
        elif nodeName_ == 'ScheduleB':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ScheduleB')
            value_ = self.gds_validate_string(value_, node, 'ScheduleB')
            self.ScheduleB = value_
            self.ScheduleB_nsprefix_ = child_.prefix
            # validate type ScheduleB
            self.validate_ScheduleB(self.ScheduleB)
        elif nodeName_ == 'ExportLicense':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ExportLicense')
            value_ = self.gds_validate_string(value_, node, 'ExportLicense')
            self.ExportLicense = value_
            self.ExportLicense_nsprefix_ = child_.prefix
        elif nodeName_ == 'ShipperEIN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipperEIN')
            value_ = self.gds_validate_string(value_, node, 'ShipperEIN')
            self.ShipperEIN = value_
            self.ShipperEIN_nsprefix_ = child_.prefix
            # validate type ShipperEINType
            self.validate_ShipperEINType(self.ShipperEIN)
        elif nodeName_ == 'ShipperIDType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipperIDType')
            value_ = self.gds_validate_string(value_, node, 'ShipperIDType')
            self.ShipperIDType = value_
            self.ShipperIDType_nsprefix_ = child_.prefix
            # validate type ShipperIDTypeType
            self.validate_ShipperIDTypeType(self.ShipperIDType)
        elif nodeName_ == 'ConsigneeIDType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ConsigneeIDType')
            value_ = self.gds_validate_string(value_, node, 'ConsigneeIDType')
            self.ConsigneeIDType = value_
            self.ConsigneeIDType_nsprefix_ = child_.prefix
            # validate type ConsigneeIDTypeType
            self.validate_ConsigneeIDTypeType(self.ConsigneeIDType)
        elif nodeName_ == 'ImportLicense':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ImportLicense')
            value_ = self.gds_validate_string(value_, node, 'ImportLicense')
            self.ImportLicense = value_
            self.ImportLicense_nsprefix_ = child_.prefix
        elif nodeName_ == 'ConsigneeEIN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ConsigneeEIN')
            value_ = self.gds_validate_string(value_, node, 'ConsigneeEIN')
            self.ConsigneeEIN = value_
            self.ConsigneeEIN_nsprefix_ = child_.prefix
            # validate type ConsigneeEINType
            self.validate_ConsigneeEINType(self.ConsigneeEIN)
        elif nodeName_ == 'TermsOfTrade':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TermsOfTrade')
            value_ = self.gds_validate_string(value_, node, 'TermsOfTrade')
            self.TermsOfTrade = value_
            self.TermsOfTrade_nsprefix_ = child_.prefix
# end class Dutiable


class ExportLicense(GeneratedsSuper):
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
                CurrentSubclassModule_, ExportLicense)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ExportLicense.subclass:
            return ExportLicense.subclass(*args_, **kwargs_)
        else:
            return ExportLicense(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ExportLicense', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ExportLicense')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ExportLicense':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ExportLicense')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ExportLicense', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ExportLicense'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ExportLicense', fromsubclass_=False, pretty_print=True):
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
# end class ExportLicense


class ImportLicense(GeneratedsSuper):
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
                CurrentSubclassModule_, ImportLicense)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ImportLicense.subclass:
            return ImportLicense.subclass(*args_, **kwargs_)
        else:
            return ImportLicense(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ImportLicense', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ImportLicense')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ImportLicense':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ImportLicense')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ImportLicense', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ImportLicense'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ImportLicense', fromsubclass_=False, pretty_print=True):
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
# end class ImportLicense


class TermsOfTrade(GeneratedsSuper):
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
                CurrentSubclassModule_, TermsOfTrade)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TermsOfTrade.subclass:
            return TermsOfTrade.subclass(*args_, **kwargs_)
        else:
            return TermsOfTrade(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TermsOfTrade', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TermsOfTrade')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TermsOfTrade':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TermsOfTrade')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TermsOfTrade', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TermsOfTrade'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TermsOfTrade', fromsubclass_=False, pretty_print=True):
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
# end class TermsOfTrade


class Email(GeneratedsSuper):
    """Email message"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, From=None, To=None, cc=None, Subject=None, ReplyTo=None, Body=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.From = From
        self.validate_EmailAddress(self.From)
        self.From_nsprefix_ = None
        self.To = To
        self.validate_EmailAddress(self.To)
        self.To_nsprefix_ = None
        if cc is None:
            self.cc = []
        else:
            self.cc = cc
        self.cc_nsprefix_ = None
        self.Subject = Subject
        self.Subject_nsprefix_ = None
        self.ReplyTo = ReplyTo
        self.validate_EmailAddress(self.ReplyTo)
        self.ReplyTo_nsprefix_ = None
        self.Body = Body
        self.validate_EmailBody(self.Body)
        self.Body_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Email)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Email.subclass:
            return Email.subclass(*args_, **kwargs_)
        else:
            return Email(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_From(self):
        return self.From
    def set_From(self, From):
        self.From = From
    def get_To(self):
        return self.To
    def set_To(self, To):
        self.To = To
    def get_cc(self):
        return self.cc
    def set_cc(self, cc):
        self.cc = cc
    def add_cc(self, value):
        self.cc.append(value)
    def insert_cc_at(self, index, value):
        self.cc.insert(index, value)
    def replace_cc_at(self, index, value):
        self.cc[index] = value
    def get_Subject(self):
        return self.Subject
    def set_Subject(self, Subject):
        self.Subject = Subject
    def get_ReplyTo(self):
        return self.ReplyTo
    def set_ReplyTo(self, ReplyTo):
        self.ReplyTo = ReplyTo
    def get_Body(self):
        return self.Body
    def set_Body(self, Body):
        self.Body = Body
    def validate_EmailAddress(self, value):
        result = True
        # Validate type EmailAddress, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_EmailBody(self, value):
        result = True
        # Validate type EmailBody, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 255:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on EmailBody' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.From is not None or
            self.To is not None or
            self.cc or
            self.Subject is not None or
            self.ReplyTo is not None or
            self.Body is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Email', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Email')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Email':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Email')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Email', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Email'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Email', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.From is not None:
            namespaceprefix_ = self.From_nsprefix_ + ':' if (UseCapturedNS_ and self.From_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFrom>%s</%sFrom>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.From), input_name='From')), namespaceprefix_ , eol_))
        if self.To is not None:
            namespaceprefix_ = self.To_nsprefix_ + ':' if (UseCapturedNS_ and self.To_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTo>%s</%sTo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.To), input_name='To')), namespaceprefix_ , eol_))
        for cc_ in self.cc:
            namespaceprefix_ = self.cc_nsprefix_ + ':' if (UseCapturedNS_ and self.cc_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scc>%s</%scc>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(cc_), input_name='cc')), namespaceprefix_ , eol_))
        if self.Subject is not None:
            namespaceprefix_ = self.Subject_nsprefix_ + ':' if (UseCapturedNS_ and self.Subject_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSubject>%s</%sSubject>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Subject), input_name='Subject')), namespaceprefix_ , eol_))
        if self.ReplyTo is not None:
            namespaceprefix_ = self.ReplyTo_nsprefix_ + ':' if (UseCapturedNS_ and self.ReplyTo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReplyTo>%s</%sReplyTo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ReplyTo), input_name='ReplyTo')), namespaceprefix_ , eol_))
        if self.Body is not None:
            namespaceprefix_ = self.Body_nsprefix_ + ':' if (UseCapturedNS_ and self.Body_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBody>%s</%sBody>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Body), input_name='Body')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'From':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'From')
            value_ = self.gds_validate_string(value_, node, 'From')
            self.From = value_
            self.From_nsprefix_ = child_.prefix
            # validate type EmailAddress
            self.validate_EmailAddress(self.From)
        elif nodeName_ == 'To':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'To')
            value_ = self.gds_validate_string(value_, node, 'To')
            self.To = value_
            self.To_nsprefix_ = child_.prefix
            # validate type EmailAddress
            self.validate_EmailAddress(self.To)
        elif nodeName_ == 'cc':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'cc')
            value_ = self.gds_validate_string(value_, node, 'cc')
            self.cc.append(value_)
            self.cc_nsprefix_ = child_.prefix
            # validate type EmailAddress
            self.validate_EmailAddress(self.cc[-1])
        elif nodeName_ == 'Subject':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Subject')
            value_ = self.gds_validate_string(value_, node, 'Subject')
            self.Subject = value_
            self.Subject_nsprefix_ = child_.prefix
        elif nodeName_ == 'ReplyTo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReplyTo')
            value_ = self.gds_validate_string(value_, node, 'ReplyTo')
            self.ReplyTo = value_
            self.ReplyTo_nsprefix_ = child_.prefix
            # validate type EmailAddress
            self.validate_EmailAddress(self.ReplyTo)
        elif nodeName_ == 'Body':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Body')
            value_ = self.gds_validate_string(value_, node, 'Body')
            self.Body = value_
            self.Body_nsprefix_ = child_.prefix
            # validate type EmailBody
            self.validate_EmailBody(self.Body)
# end class Email


class ExportDeclaration(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, InterConsignee=None, IsPartiesRelation=None, ECCN=None, SignatureName=None, SignatureTitle=None, ExportReason=None, ExportReasonCode=None, SedNumber=None, SedNumberType=None, MxStateCode=None, ExportLineItem=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.InterConsignee = InterConsignee
        self.validate_InterConsigneeType(self.InterConsignee)
        self.InterConsignee_nsprefix_ = None
        self.IsPartiesRelation = IsPartiesRelation
        self.validate_YesNo(self.IsPartiesRelation)
        self.IsPartiesRelation_nsprefix_ = None
        self.ECCN = ECCN
        self.validate_ECCNType(self.ECCN)
        self.ECCN_nsprefix_ = None
        self.SignatureName = SignatureName
        self.validate_SignatureName(self.SignatureName)
        self.SignatureName_nsprefix_ = None
        self.SignatureTitle = SignatureTitle
        self.validate_SignatureTitle(self.SignatureTitle)
        self.SignatureTitle_nsprefix_ = None
        self.ExportReason = ExportReason
        self.validate_ExportReason(self.ExportReason)
        self.ExportReason_nsprefix_ = None
        self.ExportReasonCode = ExportReasonCode
        self.validate_ExportReasonCode(self.ExportReasonCode)
        self.ExportReasonCode_nsprefix_ = None
        self.SedNumber = SedNumber
        self.validate_SEDNumber(self.SedNumber)
        self.SedNumber_nsprefix_ = None
        self.SedNumberType = SedNumberType
        self.validate_SEDNumberType(self.SedNumberType)
        self.SedNumberType_nsprefix_ = None
        self.MxStateCode = MxStateCode
        self.validate_MxStateCodeType(self.MxStateCode)
        self.MxStateCode_nsprefix_ = None
        if ExportLineItem is None:
            self.ExportLineItem = []
        else:
            self.ExportLineItem = ExportLineItem
        self.ExportLineItem_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ExportDeclaration)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ExportDeclaration.subclass:
            return ExportDeclaration.subclass(*args_, **kwargs_)
        else:
            return ExportDeclaration(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_InterConsignee(self):
        return self.InterConsignee
    def set_InterConsignee(self, InterConsignee):
        self.InterConsignee = InterConsignee
    def get_IsPartiesRelation(self):
        return self.IsPartiesRelation
    def set_IsPartiesRelation(self, IsPartiesRelation):
        self.IsPartiesRelation = IsPartiesRelation
    def get_ECCN(self):
        return self.ECCN
    def set_ECCN(self, ECCN):
        self.ECCN = ECCN
    def get_SignatureName(self):
        return self.SignatureName
    def set_SignatureName(self, SignatureName):
        self.SignatureName = SignatureName
    def get_SignatureTitle(self):
        return self.SignatureTitle
    def set_SignatureTitle(self, SignatureTitle):
        self.SignatureTitle = SignatureTitle
    def get_ExportReason(self):
        return self.ExportReason
    def set_ExportReason(self, ExportReason):
        self.ExportReason = ExportReason
    def get_ExportReasonCode(self):
        return self.ExportReasonCode
    def set_ExportReasonCode(self, ExportReasonCode):
        self.ExportReasonCode = ExportReasonCode
    def get_SedNumber(self):
        return self.SedNumber
    def set_SedNumber(self, SedNumber):
        self.SedNumber = SedNumber
    def get_SedNumberType(self):
        return self.SedNumberType
    def set_SedNumberType(self, SedNumberType):
        self.SedNumberType = SedNumberType
    def get_MxStateCode(self):
        return self.MxStateCode
    def set_MxStateCode(self, MxStateCode):
        self.MxStateCode = MxStateCode
    def get_ExportLineItem(self):
        return self.ExportLineItem
    def set_ExportLineItem(self, ExportLineItem):
        self.ExportLineItem = ExportLineItem
    def add_ExportLineItem(self, value):
        self.ExportLineItem.append(value)
    def insert_ExportLineItem_at(self, index, value):
        self.ExportLineItem.insert(index, value)
    def replace_ExportLineItem_at(self, index, value):
        self.ExportLineItem[index] = value
    def validate_InterConsigneeType(self, value):
        result = True
        # Validate type InterConsigneeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 70:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on InterConsigneeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on InterConsigneeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_YesNo(self, value):
        result = True
        # Validate type YesNo, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['Y', 'N']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on YesNo' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on YesNo' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ECCNType(self, value):
        result = True
        # Validate type ECCNType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 11:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ECCNType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ECCNType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_SignatureName(self, value):
        result = True
        # Validate type SignatureName, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on SignatureName' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_SignatureTitle(self, value):
        result = True
        # Validate type SignatureTitle, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on SignatureTitle' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ExportReason(self, value):
        result = True
        # Validate type ExportReason, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on ExportReason' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ExportReasonCode(self, value):
        result = True
        # Validate type ExportReasonCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['P', 'T', 'R']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ExportReasonCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on ExportReasonCode' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_SEDNumber(self, value):
        result = True
        # Validate type SEDNumber, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FTSR', 'XTN', 'SAS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on SEDNumber' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_SEDNumberType(self, value):
        result = True
        # Validate type SEDNumberType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['F', 'X', 'S']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on SEDNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on SEDNumberType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_MxStateCodeType(self, value):
        result = True
        # Validate type MxStateCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on MxStateCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on MxStateCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.InterConsignee is not None or
            self.IsPartiesRelation is not None or
            self.ECCN is not None or
            self.SignatureName is not None or
            self.SignatureTitle is not None or
            self.ExportReason is not None or
            self.ExportReasonCode is not None or
            self.SedNumber is not None or
            self.SedNumberType is not None or
            self.MxStateCode is not None or
            self.ExportLineItem
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ExportDeclaration', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ExportDeclaration')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ExportDeclaration':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ExportDeclaration')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ExportDeclaration', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ExportDeclaration'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ExportDeclaration', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.InterConsignee is not None:
            namespaceprefix_ = self.InterConsignee_nsprefix_ + ':' if (UseCapturedNS_ and self.InterConsignee_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInterConsignee>%s</%sInterConsignee>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.InterConsignee), input_name='InterConsignee')), namespaceprefix_ , eol_))
        if self.IsPartiesRelation is not None:
            namespaceprefix_ = self.IsPartiesRelation_nsprefix_ + ':' if (UseCapturedNS_ and self.IsPartiesRelation_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIsPartiesRelation>%s</%sIsPartiesRelation>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IsPartiesRelation), input_name='IsPartiesRelation')), namespaceprefix_ , eol_))
        if self.ECCN is not None:
            namespaceprefix_ = self.ECCN_nsprefix_ + ':' if (UseCapturedNS_ and self.ECCN_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sECCN>%s</%sECCN>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ECCN), input_name='ECCN')), namespaceprefix_ , eol_))
        if self.SignatureName is not None:
            namespaceprefix_ = self.SignatureName_nsprefix_ + ':' if (UseCapturedNS_ and self.SignatureName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSignatureName>%s</%sSignatureName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SignatureName), input_name='SignatureName')), namespaceprefix_ , eol_))
        if self.SignatureTitle is not None:
            namespaceprefix_ = self.SignatureTitle_nsprefix_ + ':' if (UseCapturedNS_ and self.SignatureTitle_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSignatureTitle>%s</%sSignatureTitle>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SignatureTitle), input_name='SignatureTitle')), namespaceprefix_ , eol_))
        if self.ExportReason is not None:
            namespaceprefix_ = self.ExportReason_nsprefix_ + ':' if (UseCapturedNS_ and self.ExportReason_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExportReason>%s</%sExportReason>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ExportReason), input_name='ExportReason')), namespaceprefix_ , eol_))
        if self.ExportReasonCode is not None:
            namespaceprefix_ = self.ExportReasonCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ExportReasonCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExportReasonCode>%s</%sExportReasonCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ExportReasonCode), input_name='ExportReasonCode')), namespaceprefix_ , eol_))
        if self.SedNumber is not None:
            namespaceprefix_ = self.SedNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.SedNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSedNumber>%s</%sSedNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SedNumber), input_name='SedNumber')), namespaceprefix_ , eol_))
        if self.SedNumberType is not None:
            namespaceprefix_ = self.SedNumberType_nsprefix_ + ':' if (UseCapturedNS_ and self.SedNumberType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSedNumberType>%s</%sSedNumberType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SedNumberType), input_name='SedNumberType')), namespaceprefix_ , eol_))
        if self.MxStateCode is not None:
            namespaceprefix_ = self.MxStateCode_nsprefix_ + ':' if (UseCapturedNS_ and self.MxStateCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMxStateCode>%s</%sMxStateCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MxStateCode), input_name='MxStateCode')), namespaceprefix_ , eol_))
        for ExportLineItem_ in self.ExportLineItem:
            namespaceprefix_ = self.ExportLineItem_nsprefix_ + ':' if (UseCapturedNS_ and self.ExportLineItem_nsprefix_) else ''
            ExportLineItem_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ExportLineItem', pretty_print=pretty_print)
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
        if nodeName_ == 'InterConsignee':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'InterConsignee')
            value_ = self.gds_validate_string(value_, node, 'InterConsignee')
            self.InterConsignee = value_
            self.InterConsignee_nsprefix_ = child_.prefix
            # validate type InterConsigneeType
            self.validate_InterConsigneeType(self.InterConsignee)
        elif nodeName_ == 'IsPartiesRelation':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IsPartiesRelation')
            value_ = self.gds_validate_string(value_, node, 'IsPartiesRelation')
            self.IsPartiesRelation = value_
            self.IsPartiesRelation_nsprefix_ = child_.prefix
            # validate type YesNo
            self.validate_YesNo(self.IsPartiesRelation)
        elif nodeName_ == 'ECCN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ECCN')
            value_ = self.gds_validate_string(value_, node, 'ECCN')
            self.ECCN = value_
            self.ECCN_nsprefix_ = child_.prefix
            # validate type ECCNType
            self.validate_ECCNType(self.ECCN)
        elif nodeName_ == 'SignatureName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SignatureName')
            value_ = self.gds_validate_string(value_, node, 'SignatureName')
            self.SignatureName = value_
            self.SignatureName_nsprefix_ = child_.prefix
            # validate type SignatureName
            self.validate_SignatureName(self.SignatureName)
        elif nodeName_ == 'SignatureTitle':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SignatureTitle')
            value_ = self.gds_validate_string(value_, node, 'SignatureTitle')
            self.SignatureTitle = value_
            self.SignatureTitle_nsprefix_ = child_.prefix
            # validate type SignatureTitle
            self.validate_SignatureTitle(self.SignatureTitle)
        elif nodeName_ == 'ExportReason':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ExportReason')
            value_ = self.gds_validate_string(value_, node, 'ExportReason')
            self.ExportReason = value_
            self.ExportReason_nsprefix_ = child_.prefix
            # validate type ExportReason
            self.validate_ExportReason(self.ExportReason)
        elif nodeName_ == 'ExportReasonCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ExportReasonCode')
            value_ = self.gds_validate_string(value_, node, 'ExportReasonCode')
            self.ExportReasonCode = value_
            self.ExportReasonCode_nsprefix_ = child_.prefix
            # validate type ExportReasonCode
            self.validate_ExportReasonCode(self.ExportReasonCode)
        elif nodeName_ == 'SedNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SedNumber')
            value_ = self.gds_validate_string(value_, node, 'SedNumber')
            self.SedNumber = value_
            self.SedNumber_nsprefix_ = child_.prefix
            # validate type SEDNumber
            self.validate_SEDNumber(self.SedNumber)
        elif nodeName_ == 'SedNumberType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SedNumberType')
            value_ = self.gds_validate_string(value_, node, 'SedNumberType')
            self.SedNumberType = value_
            self.SedNumberType_nsprefix_ = child_.prefix
            # validate type SEDNumberType
            self.validate_SEDNumberType(self.SedNumberType)
        elif nodeName_ == 'MxStateCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MxStateCode')
            value_ = self.gds_validate_string(value_, node, 'MxStateCode')
            self.MxStateCode = value_
            self.MxStateCode_nsprefix_ = child_.prefix
            # validate type MxStateCodeType
            self.validate_MxStateCodeType(self.MxStateCode)
        elif nodeName_ == 'ExportLineItem':
            obj_ = ExportLineItem.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ExportLineItem.append(obj_)
            obj_.original_tagname_ = 'ExportLineItem'
# end class ExportDeclaration


class ExportLineItem(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, LineNumber=None, Quantity=None, QuantityUnit=None, Description=None, Value=None, IsDomestic=None, CommodityCode=None, ScheduleB=None, ECCN=None, Weight=None, License=None, LicenseSymbol=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.LineNumber = LineNumber
        self.validate_LineNumber(self.LineNumber)
        self.LineNumber_nsprefix_ = None
        self.Quantity = Quantity
        self.validate_Quantity(self.Quantity)
        self.Quantity_nsprefix_ = None
        self.QuantityUnit = QuantityUnit
        self.validate_QuantityUnit(self.QuantityUnit)
        self.QuantityUnit_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
        self.Value = Value
        self.validate_Money(self.Value)
        self.Value_nsprefix_ = None
        self.IsDomestic = IsDomestic
        self.validate_YesNo(self.IsDomestic)
        self.IsDomestic_nsprefix_ = None
        self.CommodityCode = CommodityCode
        self.validate_CommodityCode(self.CommodityCode)
        self.CommodityCode_nsprefix_ = None
        self.ScheduleB = ScheduleB
        self.validate_ScheduleB(self.ScheduleB)
        self.ScheduleB_nsprefix_ = None
        self.ECCN = ECCN
        self.ECCN_nsprefix_ = None
        self.Weight = Weight
        self.Weight_nsprefix_ = None
        self.License = License
        self.License_nsprefix_ = None
        self.LicenseSymbol = LicenseSymbol
        self.validate_LicenseNumber(self.LicenseSymbol)
        self.LicenseSymbol_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ExportLineItem)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ExportLineItem.subclass:
            return ExportLineItem.subclass(*args_, **kwargs_)
        else:
            return ExportLineItem(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_LineNumber(self):
        return self.LineNumber
    def set_LineNumber(self, LineNumber):
        self.LineNumber = LineNumber
    def get_Quantity(self):
        return self.Quantity
    def set_Quantity(self, Quantity):
        self.Quantity = Quantity
    def get_QuantityUnit(self):
        return self.QuantityUnit
    def set_QuantityUnit(self, QuantityUnit):
        self.QuantityUnit = QuantityUnit
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def get_IsDomestic(self):
        return self.IsDomestic
    def set_IsDomestic(self, IsDomestic):
        self.IsDomestic = IsDomestic
    def get_CommodityCode(self):
        return self.CommodityCode
    def set_CommodityCode(self, CommodityCode):
        self.CommodityCode = CommodityCode
    def get_ScheduleB(self):
        return self.ScheduleB
    def set_ScheduleB(self, ScheduleB):
        self.ScheduleB = ScheduleB
    def get_ECCN(self):
        return self.ECCN
    def set_ECCN(self, ECCN):
        self.ECCN = ECCN
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def get_License(self):
        return self.License
    def set_License(self, License):
        self.License = License
    def get_LicenseSymbol(self):
        return self.LicenseSymbol
    def set_LicenseSymbol(self, LicenseSymbol):
        self.LicenseSymbol = LicenseSymbol
    def validate_LineNumber(self, value):
        result = True
        # Validate type LineNumber, a restriction on xsd:positiveInteger.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on LineNumber' % {"value": value, "lineno": lineno} )
                result = False
            if value > 200:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on LineNumber' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_Quantity(self, value):
        result = True
        # Validate type Quantity, a restriction on xsd:positiveInteger.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value > 32000:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on Quantity' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_QuantityUnit(self, value):
        result = True
        # Validate type QuantityUnit, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on QuantityUnit' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_Money(self, value):
        result = True
        # Validate type Money, a restriction on xsd:float.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, float):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (float)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0.00:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on Money' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999999999.99:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on Money' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_YesNo(self, value):
        result = True
        # Validate type YesNo, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['Y', 'N']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on YesNo' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on YesNo' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CommodityCode(self, value):
        result = True
        # Validate type CommodityCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CommodityCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on CommodityCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ScheduleB(self, value):
        result = True
        # Validate type ScheduleB, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 15:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ScheduleB' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_LicenseNumber(self, value):
        result = True
        # Validate type LicenseNumber, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 16:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on LicenseNumber' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.LineNumber is not None or
            self.Quantity is not None or
            self.QuantityUnit is not None or
            self.Description is not None or
            self.Value is not None or
            self.IsDomestic is not None or
            self.CommodityCode is not None or
            self.ScheduleB is not None or
            self.ECCN is not None or
            self.Weight is not None or
            self.License is not None or
            self.LicenseSymbol is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ExportLineItem', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ExportLineItem')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ExportLineItem':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ExportLineItem')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ExportLineItem', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ExportLineItem'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ExportLineItem', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.LineNumber is not None:
            namespaceprefix_ = self.LineNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.LineNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLineNumber>%s</%sLineNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.LineNumber, input_name='LineNumber'), namespaceprefix_ , eol_))
        if self.Quantity is not None:
            namespaceprefix_ = self.Quantity_nsprefix_ + ':' if (UseCapturedNS_ and self.Quantity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sQuantity>%s</%sQuantity>%s' % (namespaceprefix_ , self.gds_format_integer(self.Quantity, input_name='Quantity'), namespaceprefix_ , eol_))
        if self.QuantityUnit is not None:
            namespaceprefix_ = self.QuantityUnit_nsprefix_ + ':' if (UseCapturedNS_ and self.QuantityUnit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sQuantityUnit>%s</%sQuantityUnit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.QuantityUnit), input_name='QuantityUnit')), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
        if self.Value is not None:
            namespaceprefix_ = self.Value_nsprefix_ + ':' if (UseCapturedNS_ and self.Value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sValue>%s</%sValue>%s' % (namespaceprefix_ , self.gds_format_float(self.Value, input_name='Value'), namespaceprefix_ , eol_))
        if self.IsDomestic is not None:
            namespaceprefix_ = self.IsDomestic_nsprefix_ + ':' if (UseCapturedNS_ and self.IsDomestic_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIsDomestic>%s</%sIsDomestic>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IsDomestic), input_name='IsDomestic')), namespaceprefix_ , eol_))
        if self.CommodityCode is not None:
            namespaceprefix_ = self.CommodityCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CommodityCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCommodityCode>%s</%sCommodityCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CommodityCode), input_name='CommodityCode')), namespaceprefix_ , eol_))
        if self.ScheduleB is not None:
            namespaceprefix_ = self.ScheduleB_nsprefix_ + ':' if (UseCapturedNS_ and self.ScheduleB_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sScheduleB>%s</%sScheduleB>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ScheduleB), input_name='ScheduleB')), namespaceprefix_ , eol_))
        if self.ECCN is not None:
            namespaceprefix_ = self.ECCN_nsprefix_ + ':' if (UseCapturedNS_ and self.ECCN_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sECCN>%s</%sECCN>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ECCN), input_name='ECCN')), namespaceprefix_ , eol_))
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            self.Weight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Weight', pretty_print=pretty_print)
        if self.License is not None:
            namespaceprefix_ = self.License_nsprefix_ + ':' if (UseCapturedNS_ and self.License_nsprefix_) else ''
            self.License.export(outfile, level, namespaceprefix_, namespacedef_='', name_='License', pretty_print=pretty_print)
        if self.LicenseSymbol is not None:
            namespaceprefix_ = self.LicenseSymbol_nsprefix_ + ':' if (UseCapturedNS_ and self.LicenseSymbol_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLicenseSymbol>%s</%sLicenseSymbol>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LicenseSymbol), input_name='LicenseSymbol')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'LineNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'LineNumber')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'LineNumber')
            self.LineNumber = ival_
            self.LineNumber_nsprefix_ = child_.prefix
            # validate type LineNumber
            self.validate_LineNumber(self.LineNumber)
        elif nodeName_ == 'Quantity' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Quantity')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'Quantity')
            self.Quantity = ival_
            self.Quantity_nsprefix_ = child_.prefix
            # validate type Quantity
            self.validate_Quantity(self.Quantity)
        elif nodeName_ == 'QuantityUnit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'QuantityUnit')
            value_ = self.gds_validate_string(value_, node, 'QuantityUnit')
            self.QuantityUnit = value_
            self.QuantityUnit_nsprefix_ = child_.prefix
            # validate type QuantityUnit
            self.validate_QuantityUnit(self.QuantityUnit)
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
        elif nodeName_ == 'Value' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'Value')
            fval_ = self.gds_validate_float(fval_, node, 'Value')
            self.Value = fval_
            self.Value_nsprefix_ = child_.prefix
            # validate type Money
            self.validate_Money(self.Value)
        elif nodeName_ == 'IsDomestic':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IsDomestic')
            value_ = self.gds_validate_string(value_, node, 'IsDomestic')
            self.IsDomestic = value_
            self.IsDomestic_nsprefix_ = child_.prefix
            # validate type YesNo
            self.validate_YesNo(self.IsDomestic)
        elif nodeName_ == 'CommodityCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CommodityCode')
            value_ = self.gds_validate_string(value_, node, 'CommodityCode')
            self.CommodityCode = value_
            self.CommodityCode_nsprefix_ = child_.prefix
            # validate type CommodityCode
            self.validate_CommodityCode(self.CommodityCode)
        elif nodeName_ == 'ScheduleB':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ScheduleB')
            value_ = self.gds_validate_string(value_, node, 'ScheduleB')
            self.ScheduleB = value_
            self.ScheduleB_nsprefix_ = child_.prefix
            # validate type ScheduleB
            self.validate_ScheduleB(self.ScheduleB)
        elif nodeName_ == 'ECCN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ECCN')
            value_ = self.gds_validate_string(value_, node, 'ECCN')
            self.ECCN = value_
            self.ECCN_nsprefix_ = child_.prefix
        elif nodeName_ == 'Weight':
            obj_ = WeightType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Weight = obj_
            obj_.original_tagname_ = 'Weight'
        elif nodeName_ == 'License':
            obj_ = LicenseType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.License = obj_
            obj_.original_tagname_ = 'License'
        elif nodeName_ == 'LicenseSymbol':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LicenseSymbol')
            value_ = self.gds_validate_string(value_, node, 'LicenseSymbol')
            self.LicenseSymbol = value_
            self.LicenseSymbol_nsprefix_ = child_.prefix
            # validate type LicenseNumber
            self.validate_LicenseNumber(self.LicenseSymbol)
# end class ExportLineItem


class Piece(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PieceID=None, PackageType=None, Weight=None, DimWeight=None, Width=None, Height=None, Depth=None, PieceContents=None, PieceReference=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PieceID = PieceID
        self.validate_PieceID(self.PieceID)
        self.PieceID_nsprefix_ = None
        self.PackageType = PackageType
        self.validate_PackageType(self.PackageType)
        self.PackageType_nsprefix_ = None
        self.Weight = Weight
        self.validate_Weight(self.Weight)
        self.Weight_nsprefix_ = None
        self.DimWeight = DimWeight
        self.validate_Weight(self.DimWeight)
        self.DimWeight_nsprefix_ = None
        self.Width = Width
        self.Width_nsprefix_ = None
        self.Height = Height
        self.Height_nsprefix_ = None
        self.Depth = Depth
        self.Depth_nsprefix_ = None
        self.PieceContents = PieceContents
        self.PieceContents_nsprefix_ = None
        if PieceReference is None:
            self.PieceReference = []
        else:
            self.PieceReference = PieceReference
        self.PieceReference_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Piece)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Piece.subclass:
            return Piece.subclass(*args_, **kwargs_)
        else:
            return Piece(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PieceID(self):
        return self.PieceID
    def set_PieceID(self, PieceID):
        self.PieceID = PieceID
    def get_PackageType(self):
        return self.PackageType
    def set_PackageType(self, PackageType):
        self.PackageType = PackageType
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def get_DimWeight(self):
        return self.DimWeight
    def set_DimWeight(self, DimWeight):
        self.DimWeight = DimWeight
    def get_Width(self):
        return self.Width
    def set_Width(self, Width):
        self.Width = Width
    def get_Height(self):
        return self.Height
    def set_Height(self, Height):
        self.Height = Height
    def get_Depth(self):
        return self.Depth
    def set_Depth(self, Depth):
        self.Depth = Depth
    def get_PieceContents(self):
        return self.PieceContents
    def set_PieceContents(self, PieceContents):
        self.PieceContents = PieceContents
    def get_PieceReference(self):
        return self.PieceReference
    def set_PieceReference(self, PieceReference):
        self.PieceReference = PieceReference
    def add_PieceReference(self, value):
        self.PieceReference.append(value)
    def insert_PieceReference_at(self, index, value):
        self.PieceReference.insert(index, value)
    def replace_PieceReference_at(self, index, value):
        self.PieceReference[index] = value
    def validate_PieceID(self, value):
        result = True
        # Validate type PieceID, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on PieceID' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PackageType(self, value):
        result = True
        # Validate type PackageType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['EE', 'OD', 'CP']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on PackageType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on PackageType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_Weight(self, value):
        result = True
        # Validate type Weight, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if value > 999999.9:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on Weight' % {"value": value, "lineno": lineno} )
                result = False
            if len(str(value)) >= 7:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on Weight' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.PieceID is not None or
            self.PackageType is not None or
            self.Weight is not None or
            self.DimWeight is not None or
            self.Width is not None or
            self.Height is not None or
            self.Depth is not None or
            self.PieceContents is not None or
            self.PieceReference
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Piece', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Piece')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Piece':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Piece')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Piece', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Piece'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Piece', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PieceID is not None:
            namespaceprefix_ = self.PieceID_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPieceID>%s</%sPieceID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PieceID), input_name='PieceID')), namespaceprefix_ , eol_))
        if self.PackageType is not None:
            namespaceprefix_ = self.PackageType_nsprefix_ + ':' if (UseCapturedNS_ and self.PackageType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPackageType>%s</%sPackageType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PackageType), input_name='PackageType')), namespaceprefix_ , eol_))
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeight>%s</%sWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Weight, input_name='Weight'), namespaceprefix_ , eol_))
        if self.DimWeight is not None:
            namespaceprefix_ = self.DimWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.DimWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDimWeight>%s</%sDimWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.DimWeight, input_name='DimWeight'), namespaceprefix_ , eol_))
        if self.Width is not None:
            namespaceprefix_ = self.Width_nsprefix_ + ':' if (UseCapturedNS_ and self.Width_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWidth>%s</%sWidth>%s' % (namespaceprefix_ , self.gds_format_integer(self.Width, input_name='Width'), namespaceprefix_ , eol_))
        if self.Height is not None:
            namespaceprefix_ = self.Height_nsprefix_ + ':' if (UseCapturedNS_ and self.Height_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHeight>%s</%sHeight>%s' % (namespaceprefix_ , self.gds_format_integer(self.Height, input_name='Height'), namespaceprefix_ , eol_))
        if self.Depth is not None:
            namespaceprefix_ = self.Depth_nsprefix_ + ':' if (UseCapturedNS_ and self.Depth_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDepth>%s</%sDepth>%s' % (namespaceprefix_ , self.gds_format_integer(self.Depth, input_name='Depth'), namespaceprefix_ , eol_))
        if self.PieceContents is not None:
            namespaceprefix_ = self.PieceContents_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceContents_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPieceContents>%s</%sPieceContents>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PieceContents), input_name='PieceContents')), namespaceprefix_ , eol_))
        for PieceReference_ in self.PieceReference:
            namespaceprefix_ = self.PieceReference_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceReference_nsprefix_) else ''
            PieceReference_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PieceReference', pretty_print=pretty_print)
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
            # validate type PieceID
            self.validate_PieceID(self.PieceID)
        elif nodeName_ == 'PackageType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PackageType')
            value_ = self.gds_validate_string(value_, node, 'PackageType')
            self.PackageType = value_
            self.PackageType_nsprefix_ = child_.prefix
            # validate type PackageType
            self.validate_PackageType(self.PackageType)
        elif nodeName_ == 'Weight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Weight')
            fval_ = self.gds_validate_decimal(fval_, node, 'Weight')
            self.Weight = fval_
            self.Weight_nsprefix_ = child_.prefix
            # validate type Weight
            self.validate_Weight(self.Weight)
        elif nodeName_ == 'DimWeight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'DimWeight')
            fval_ = self.gds_validate_decimal(fval_, node, 'DimWeight')
            self.DimWeight = fval_
            self.DimWeight_nsprefix_ = child_.prefix
            # validate type Weight
            self.validate_Weight(self.DimWeight)
        elif nodeName_ == 'Width' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Width')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'Width')
            self.Width = ival_
            self.Width_nsprefix_ = child_.prefix
        elif nodeName_ == 'Height' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Height')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'Height')
            self.Height = ival_
            self.Height_nsprefix_ = child_.prefix
        elif nodeName_ == 'Depth' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Depth')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'Depth')
            self.Depth = ival_
            self.Depth_nsprefix_ = child_.prefix
        elif nodeName_ == 'PieceContents':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PieceContents')
            value_ = self.gds_validate_string(value_, node, 'PieceContents')
            self.PieceContents = value_
            self.PieceContents_nsprefix_ = child_.prefix
        elif nodeName_ == 'PieceReference':
            obj_ = Reference.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PieceReference.append(obj_)
            obj_.original_tagname_ = 'PieceReference'
# end class Piece


class Pieces(GeneratedsSuper):
    """Element encapsulating peices information"""
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
                CurrentSubclassModule_, Pieces)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Pieces.subclass:
            return Pieces.subclass(*args_, **kwargs_)
        else:
            return Pieces(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Pieces', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Pieces')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Pieces':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Pieces')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Pieces', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Pieces'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Pieces', fromsubclass_=False, pretty_print=True):
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
            obj_ = Piece.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Piece.append(obj_)
            obj_.original_tagname_ = 'Piece'
# end class Pieces


class ShipValResponsePiece(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PieceNumber=None, Depth=None, Width=None, Height=None, Weight=None, PackageType=None, DimWeight=None, PieceContents=None, PieceReference=None, DataIdentifier=None, LicensePlate=None, LicensePlateBarCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PieceNumber = PieceNumber
        self.validate_PieceNumber(self.PieceNumber)
        self.PieceNumber_nsprefix_ = None
        self.Depth = Depth
        self.Depth_nsprefix_ = None
        self.Width = Width
        self.Width_nsprefix_ = None
        self.Height = Height
        self.Height_nsprefix_ = None
        self.Weight = Weight
        self.validate_Weight(self.Weight)
        self.Weight_nsprefix_ = None
        self.PackageType = PackageType
        self.validate_PackageType(self.PackageType)
        self.PackageType_nsprefix_ = None
        self.DimWeight = DimWeight
        self.validate_Weight(self.DimWeight)
        self.DimWeight_nsprefix_ = None
        self.PieceContents = PieceContents
        self.validate_PieceContents(self.PieceContents)
        self.PieceContents_nsprefix_ = None
        if PieceReference is None:
            self.PieceReference = []
        else:
            self.PieceReference = PieceReference
        self.PieceReference_nsprefix_ = None
        self.DataIdentifier = DataIdentifier
        self.DataIdentifier_nsprefix_ = None
        self.LicensePlate = LicensePlate
        self.validate_PieceID(self.LicensePlate)
        self.LicensePlate_nsprefix_ = None
        self.LicensePlateBarCode = LicensePlateBarCode
        self.validate_BarCode(self.LicensePlateBarCode)
        self.LicensePlateBarCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipValResponsePiece)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipValResponsePiece.subclass:
            return ShipValResponsePiece.subclass(*args_, **kwargs_)
        else:
            return ShipValResponsePiece(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PieceNumber(self):
        return self.PieceNumber
    def set_PieceNumber(self, PieceNumber):
        self.PieceNumber = PieceNumber
    def get_Depth(self):
        return self.Depth
    def set_Depth(self, Depth):
        self.Depth = Depth
    def get_Width(self):
        return self.Width
    def set_Width(self, Width):
        self.Width = Width
    def get_Height(self):
        return self.Height
    def set_Height(self, Height):
        self.Height = Height
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def get_PackageType(self):
        return self.PackageType
    def set_PackageType(self, PackageType):
        self.PackageType = PackageType
    def get_DimWeight(self):
        return self.DimWeight
    def set_DimWeight(self, DimWeight):
        self.DimWeight = DimWeight
    def get_PieceContents(self):
        return self.PieceContents
    def set_PieceContents(self, PieceContents):
        self.PieceContents = PieceContents
    def get_PieceReference(self):
        return self.PieceReference
    def set_PieceReference(self, PieceReference):
        self.PieceReference = PieceReference
    def add_PieceReference(self, value):
        self.PieceReference.append(value)
    def insert_PieceReference_at(self, index, value):
        self.PieceReference.insert(index, value)
    def replace_PieceReference_at(self, index, value):
        self.PieceReference[index] = value
    def get_DataIdentifier(self):
        return self.DataIdentifier
    def set_DataIdentifier(self, DataIdentifier):
        self.DataIdentifier = DataIdentifier
    def get_LicensePlate(self):
        return self.LicensePlate
    def set_LicensePlate(self, LicensePlate):
        self.LicensePlate = LicensePlate
    def get_LicensePlateBarCode(self):
        return self.LicensePlateBarCode
    def set_LicensePlateBarCode(self, LicensePlateBarCode):
        self.LicensePlateBarCode = LicensePlateBarCode
    def validate_PieceNumber(self, value):
        result = True
        # Validate type PieceNumber, a restriction on xsd:positiveInteger.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_Weight(self, value):
        result = True
        # Validate type Weight, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if value > 999999.9:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on Weight' % {"value": value, "lineno": lineno} )
                result = False
            if len(str(value)) >= 7:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on Weight' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_PackageType(self, value):
        result = True
        # Validate type PackageType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['EE', 'OD', 'CP']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on PackageType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on PackageType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PieceContents(self, value):
        result = True
        # Validate type PieceContents, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 90:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on PieceContents' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PieceID(self, value):
        result = True
        # Validate type PieceID, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on PieceID' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_BarCode(self, value):
        result = True
        # Validate type BarCode, a restriction on xsd:base64Binary.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def hasContent_(self):
        if (
            self.PieceNumber is not None or
            self.Depth is not None or
            self.Width is not None or
            self.Height is not None or
            self.Weight is not None or
            self.PackageType is not None or
            self.DimWeight is not None or
            self.PieceContents is not None or
            self.PieceReference or
            self.DataIdentifier is not None or
            self.LicensePlate is not None or
            self.LicensePlateBarCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipValResponsePiece', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipValResponsePiece')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipValResponsePiece':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipValResponsePiece')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipValResponsePiece', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipValResponsePiece'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipValResponsePiece', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PieceNumber is not None:
            namespaceprefix_ = self.PieceNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPieceNumber>%s</%sPieceNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.PieceNumber, input_name='PieceNumber'), namespaceprefix_ , eol_))
        if self.Depth is not None:
            namespaceprefix_ = self.Depth_nsprefix_ + ':' if (UseCapturedNS_ and self.Depth_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDepth>%s</%sDepth>%s' % (namespaceprefix_ , self.gds_format_integer(self.Depth, input_name='Depth'), namespaceprefix_ , eol_))
        if self.Width is not None:
            namespaceprefix_ = self.Width_nsprefix_ + ':' if (UseCapturedNS_ and self.Width_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWidth>%s</%sWidth>%s' % (namespaceprefix_ , self.gds_format_integer(self.Width, input_name='Width'), namespaceprefix_ , eol_))
        if self.Height is not None:
            namespaceprefix_ = self.Height_nsprefix_ + ':' if (UseCapturedNS_ and self.Height_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHeight>%s</%sHeight>%s' % (namespaceprefix_ , self.gds_format_integer(self.Height, input_name='Height'), namespaceprefix_ , eol_))
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeight>%s</%sWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Weight, input_name='Weight'), namespaceprefix_ , eol_))
        if self.PackageType is not None:
            namespaceprefix_ = self.PackageType_nsprefix_ + ':' if (UseCapturedNS_ and self.PackageType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPackageType>%s</%sPackageType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PackageType), input_name='PackageType')), namespaceprefix_ , eol_))
        if self.DimWeight is not None:
            namespaceprefix_ = self.DimWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.DimWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDimWeight>%s</%sDimWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.DimWeight, input_name='DimWeight'), namespaceprefix_ , eol_))
        if self.PieceContents is not None:
            namespaceprefix_ = self.PieceContents_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceContents_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPieceContents>%s</%sPieceContents>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PieceContents), input_name='PieceContents')), namespaceprefix_ , eol_))
        for PieceReference_ in self.PieceReference:
            namespaceprefix_ = self.PieceReference_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceReference_nsprefix_) else ''
            PieceReference_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PieceReference', pretty_print=pretty_print)
        if self.DataIdentifier is not None:
            namespaceprefix_ = self.DataIdentifier_nsprefix_ + ':' if (UseCapturedNS_ and self.DataIdentifier_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDataIdentifier>%s</%sDataIdentifier>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DataIdentifier), input_name='DataIdentifier')), namespaceprefix_ , eol_))
        if self.LicensePlate is not None:
            namespaceprefix_ = self.LicensePlate_nsprefix_ + ':' if (UseCapturedNS_ and self.LicensePlate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLicensePlate>%s</%sLicensePlate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LicensePlate), input_name='LicensePlate')), namespaceprefix_ , eol_))
        if self.LicensePlateBarCode is not None:
            namespaceprefix_ = self.LicensePlateBarCode_nsprefix_ + ':' if (UseCapturedNS_ and self.LicensePlateBarCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLicensePlateBarCode>%s</%sLicensePlateBarCode>%s' % (namespaceprefix_ , self.gds_format_base64(self.LicensePlateBarCode, input_name='LicensePlateBarCode'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'PieceNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'PieceNumber')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'PieceNumber')
            self.PieceNumber = ival_
            self.PieceNumber_nsprefix_ = child_.prefix
            # validate type PieceNumber
            self.validate_PieceNumber(self.PieceNumber)
        elif nodeName_ == 'Depth' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Depth')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'Depth')
            self.Depth = ival_
            self.Depth_nsprefix_ = child_.prefix
        elif nodeName_ == 'Width' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Width')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'Width')
            self.Width = ival_
            self.Width_nsprefix_ = child_.prefix
        elif nodeName_ == 'Height' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Height')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'Height')
            self.Height = ival_
            self.Height_nsprefix_ = child_.prefix
        elif nodeName_ == 'Weight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Weight')
            fval_ = self.gds_validate_decimal(fval_, node, 'Weight')
            self.Weight = fval_
            self.Weight_nsprefix_ = child_.prefix
            # validate type Weight
            self.validate_Weight(self.Weight)
        elif nodeName_ == 'PackageType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PackageType')
            value_ = self.gds_validate_string(value_, node, 'PackageType')
            self.PackageType = value_
            self.PackageType_nsprefix_ = child_.prefix
            # validate type PackageType
            self.validate_PackageType(self.PackageType)
        elif nodeName_ == 'DimWeight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'DimWeight')
            fval_ = self.gds_validate_decimal(fval_, node, 'DimWeight')
            self.DimWeight = fval_
            self.DimWeight_nsprefix_ = child_.prefix
            # validate type Weight
            self.validate_Weight(self.DimWeight)
        elif nodeName_ == 'PieceContents':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PieceContents')
            value_ = self.gds_validate_string(value_, node, 'PieceContents')
            self.PieceContents = value_
            self.PieceContents_nsprefix_ = child_.prefix
            # validate type PieceContents
            self.validate_PieceContents(self.PieceContents)
        elif nodeName_ == 'PieceReference':
            obj_ = Reference.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PieceReference.append(obj_)
            obj_.original_tagname_ = 'PieceReference'
        elif nodeName_ == 'DataIdentifier':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DataIdentifier')
            value_ = self.gds_validate_string(value_, node, 'DataIdentifier')
            self.DataIdentifier = value_
            self.DataIdentifier_nsprefix_ = child_.prefix
        elif nodeName_ == 'LicensePlate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LicensePlate')
            value_ = self.gds_validate_string(value_, node, 'LicensePlate')
            self.LicensePlate = value_
            self.LicensePlate_nsprefix_ = child_.prefix
            # validate type PieceID
            self.validate_PieceID(self.LicensePlate)
        elif nodeName_ == 'LicensePlateBarCode':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'LicensePlateBarCode')
            else:
                bval_ = None
            self.LicensePlateBarCode = bval_
            self.LicensePlateBarCode_nsprefix_ = child_.prefix
            # validate type BarCode
            self.validate_BarCode(self.LicensePlateBarCode)
# end class ShipValResponsePiece


class ShipValResponsePieces(GeneratedsSuper):
    """Element encapsulating pieces information"""
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
                CurrentSubclassModule_, ShipValResponsePieces)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipValResponsePieces.subclass:
            return ShipValResponsePieces.subclass(*args_, **kwargs_)
        else:
            return ShipValResponsePieces(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipValResponsePieces', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipValResponsePieces')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipValResponsePieces':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipValResponsePieces')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipValResponsePieces', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipValResponsePieces'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipValResponsePieces', fromsubclass_=False, pretty_print=True):
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
            obj_ = ShipValResponsePiece.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Piece.append(obj_)
            obj_.original_tagname_ = 'Piece'
# end class ShipValResponsePieces


class Place(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ResidenceOrBusiness=None, CompanyName=None, AddressLine=None, City=None, CountryCode=None, DivisionCode=None, Division=None, PostalCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ResidenceOrBusiness = ResidenceOrBusiness
        self.validate_ResidenceOrBusiness(self.ResidenceOrBusiness)
        self.ResidenceOrBusiness_nsprefix_ = None
        self.CompanyName = CompanyName
        self.validate_CompanyNameValidator(self.CompanyName)
        self.CompanyName_nsprefix_ = None
        if AddressLine is None:
            self.AddressLine = []
        else:
            self.AddressLine = AddressLine
        self.AddressLine_nsprefix_ = None
        self.City = City
        self.validate_City(self.City)
        self.City_nsprefix_ = None
        self.CountryCode = CountryCode
        self.validate_CountryCode(self.CountryCode)
        self.CountryCode_nsprefix_ = None
        self.DivisionCode = DivisionCode
        self.validate_StateCode(self.DivisionCode)
        self.DivisionCode_nsprefix_ = None
        self.Division = Division
        self.validate_State(self.Division)
        self.Division_nsprefix_ = None
        self.PostalCode = PostalCode
        self.validate_PostalCode(self.PostalCode)
        self.PostalCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Place)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Place.subclass:
            return Place.subclass(*args_, **kwargs_)
        else:
            return Place(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ResidenceOrBusiness(self):
        return self.ResidenceOrBusiness
    def set_ResidenceOrBusiness(self, ResidenceOrBusiness):
        self.ResidenceOrBusiness = ResidenceOrBusiness
    def get_CompanyName(self):
        return self.CompanyName
    def set_CompanyName(self, CompanyName):
        self.CompanyName = CompanyName
    def get_AddressLine(self):
        return self.AddressLine
    def set_AddressLine(self, AddressLine):
        self.AddressLine = AddressLine
    def add_AddressLine(self, value):
        self.AddressLine.append(value)
    def insert_AddressLine_at(self, index, value):
        self.AddressLine.insert(index, value)
    def replace_AddressLine_at(self, index, value):
        self.AddressLine[index] = value
    def get_City(self):
        return self.City
    def set_City(self, City):
        self.City = City
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def get_DivisionCode(self):
        return self.DivisionCode
    def set_DivisionCode(self, DivisionCode):
        self.DivisionCode = DivisionCode
    def get_Division(self):
        return self.Division
    def set_Division(self, Division):
        self.Division = Division
    def get_PostalCode(self):
        return self.PostalCode
    def set_PostalCode(self, PostalCode):
        self.PostalCode = PostalCode
    def validate_ResidenceOrBusiness(self, value):
        result = True
        # Validate type ResidenceOrBusiness, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['B', 'R', 'C']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ResidenceOrBusiness' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on ResidenceOrBusiness' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CompanyNameValidator(self, value):
        result = True
        # Validate type CompanyNameValidator, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CompanyNameValidator' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_AddressLine(self, value):
        result = True
        # Validate type AddressLine, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on AddressLine' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_City(self, value):
        result = True
        # Validate type City, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on City' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CountryCode(self, value):
        result = True
        # Validate type CountryCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CountryCode' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_StateCode(self, value):
        result = True
        # Validate type StateCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on StateCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on StateCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_State(self, value):
        result = True
        # Validate type State, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on State' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PostalCode(self, value):
        result = True
        # Validate type PostalCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def hasContent_(self):
        if (
            self.ResidenceOrBusiness is not None or
            self.CompanyName is not None or
            self.AddressLine or
            self.City is not None or
            self.CountryCode is not None or
            self.DivisionCode is not None or
            self.Division is not None or
            self.PostalCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Place', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Place')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Place':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Place')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Place', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Place'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Place', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ResidenceOrBusiness is not None:
            namespaceprefix_ = self.ResidenceOrBusiness_nsprefix_ + ':' if (UseCapturedNS_ and self.ResidenceOrBusiness_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sResidenceOrBusiness>%s</%sResidenceOrBusiness>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ResidenceOrBusiness), input_name='ResidenceOrBusiness')), namespaceprefix_ , eol_))
        if self.CompanyName is not None:
            namespaceprefix_ = self.CompanyName_nsprefix_ + ':' if (UseCapturedNS_ and self.CompanyName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCompanyName>%s</%sCompanyName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CompanyName), input_name='CompanyName')), namespaceprefix_ , eol_))
        for AddressLine_ in self.AddressLine:
            namespaceprefix_ = self.AddressLine_nsprefix_ + ':' if (UseCapturedNS_ and self.AddressLine_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAddressLine>%s</%sAddressLine>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(AddressLine_), input_name='AddressLine')), namespaceprefix_ , eol_))
        if self.City is not None:
            namespaceprefix_ = self.City_nsprefix_ + ':' if (UseCapturedNS_ and self.City_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCity>%s</%sCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.City), input_name='City')), namespaceprefix_ , eol_))
        if self.CountryCode is not None:
            namespaceprefix_ = self.CountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryCode>%s</%sCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryCode), input_name='CountryCode')), namespaceprefix_ , eol_))
        if self.DivisionCode is not None:
            namespaceprefix_ = self.DivisionCode_nsprefix_ + ':' if (UseCapturedNS_ and self.DivisionCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDivisionCode>%s</%sDivisionCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DivisionCode), input_name='DivisionCode')), namespaceprefix_ , eol_))
        if self.Division is not None:
            namespaceprefix_ = self.Division_nsprefix_ + ':' if (UseCapturedNS_ and self.Division_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDivision>%s</%sDivision>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Division), input_name='Division')), namespaceprefix_ , eol_))
        if self.PostalCode is not None:
            namespaceprefix_ = self.PostalCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PostalCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPostalCode>%s</%sPostalCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PostalCode), input_name='PostalCode')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ResidenceOrBusiness':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ResidenceOrBusiness')
            value_ = self.gds_validate_string(value_, node, 'ResidenceOrBusiness')
            self.ResidenceOrBusiness = value_
            self.ResidenceOrBusiness_nsprefix_ = child_.prefix
            # validate type ResidenceOrBusiness
            self.validate_ResidenceOrBusiness(self.ResidenceOrBusiness)
        elif nodeName_ == 'CompanyName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CompanyName')
            value_ = self.gds_validate_string(value_, node, 'CompanyName')
            self.CompanyName = value_
            self.CompanyName_nsprefix_ = child_.prefix
            # validate type CompanyNameValidator
            self.validate_CompanyNameValidator(self.CompanyName)
        elif nodeName_ == 'AddressLine':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AddressLine')
            value_ = self.gds_validate_string(value_, node, 'AddressLine')
            self.AddressLine.append(value_)
            self.AddressLine_nsprefix_ = child_.prefix
            # validate type AddressLine
            self.validate_AddressLine(self.AddressLine[-1])
        elif nodeName_ == 'City':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'City')
            value_ = self.gds_validate_string(value_, node, 'City')
            self.City = value_
            self.City_nsprefix_ = child_.prefix
            # validate type City
            self.validate_City(self.City)
        elif nodeName_ == 'CountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryCode')
            value_ = self.gds_validate_string(value_, node, 'CountryCode')
            self.CountryCode = value_
            self.CountryCode_nsprefix_ = child_.prefix
            # validate type CountryCode
            self.validate_CountryCode(self.CountryCode)
        elif nodeName_ == 'DivisionCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DivisionCode')
            value_ = self.gds_validate_string(value_, node, 'DivisionCode')
            self.DivisionCode = value_
            self.DivisionCode_nsprefix_ = child_.prefix
            # validate type StateCode
            self.validate_StateCode(self.DivisionCode)
        elif nodeName_ == 'Division':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Division')
            value_ = self.gds_validate_string(value_, node, 'Division')
            self.Division = value_
            self.Division_nsprefix_ = child_.prefix
            # validate type State
            self.validate_State(self.Division)
        elif nodeName_ == 'PostalCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PostalCode')
            value_ = self.gds_validate_string(value_, node, 'PostalCode')
            self.PostalCode = value_
            self.PostalCode_nsprefix_ = child_.prefix
            # validate type PostalCode
            self.validate_PostalCode(self.PostalCode)
# end class Place


class Reference(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ReferenceID=None, ReferenceType=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ReferenceID = ReferenceID
        self.validate_ReferenceID(self.ReferenceID)
        self.ReferenceID_nsprefix_ = None
        self.ReferenceType = ReferenceType
        self.validate_ReferenceType(self.ReferenceType)
        self.ReferenceType_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Reference)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Reference.subclass:
            return Reference.subclass(*args_, **kwargs_)
        else:
            return Reference(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ReferenceID(self):
        return self.ReferenceID
    def set_ReferenceID(self, ReferenceID):
        self.ReferenceID = ReferenceID
    def get_ReferenceType(self):
        return self.ReferenceType
    def set_ReferenceType(self, ReferenceType):
        self.ReferenceType = ReferenceType
    def validate_ReferenceID(self, value):
        result = True
        # Validate type ReferenceID, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ReferenceID' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ReferenceType(self, value):
        result = True
        # Validate type ReferenceType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ReferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ReferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.ReferenceID is not None or
            self.ReferenceType is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Reference', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Reference')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Reference':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Reference')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Reference', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Reference'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Reference', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ReferenceID is not None:
            namespaceprefix_ = self.ReferenceID_nsprefix_ + ':' if (UseCapturedNS_ and self.ReferenceID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReferenceID>%s</%sReferenceID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ReferenceID), input_name='ReferenceID')), namespaceprefix_ , eol_))
        if self.ReferenceType is not None:
            namespaceprefix_ = self.ReferenceType_nsprefix_ + ':' if (UseCapturedNS_ and self.ReferenceType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReferenceType>%s</%sReferenceType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ReferenceType), input_name='ReferenceType')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ReferenceID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReferenceID')
            value_ = self.gds_validate_string(value_, node, 'ReferenceID')
            self.ReferenceID = value_
            self.ReferenceID_nsprefix_ = child_.prefix
            # validate type ReferenceID
            self.validate_ReferenceID(self.ReferenceID)
        elif nodeName_ == 'ReferenceType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReferenceType')
            value_ = self.gds_validate_string(value_, node, 'ReferenceType')
            self.ReferenceType = value_
            self.ReferenceType_nsprefix_ = child_.prefix
            # validate type ReferenceType
            self.validate_ReferenceType(self.ReferenceType)
# end class Reference


class ShipmentDetails(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, NumberOfPieces=None, Pieces=None, Weight=None, WeightUnit=None, ProductCode=None, GlobalProductCode=None, LocalProductCode=None, Date=None, Contents=None, DoorTo=None, DimensionUnit=None, InsuredAmount=None, PackageType=None, IsDutiable=None, CurrencyCode=None, CustData=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.NumberOfPieces = NumberOfPieces
        self.NumberOfPieces_nsprefix_ = None
        self.Pieces = Pieces
        self.Pieces_nsprefix_ = None
        self.Weight = Weight
        self.validate_Weight(self.Weight)
        self.Weight_nsprefix_ = None
        self.WeightUnit = WeightUnit
        self.validate_WeightUnit(self.WeightUnit)
        self.WeightUnit_nsprefix_ = None
        self.ProductCode = ProductCode
        self.validate_ProductCode(self.ProductCode)
        self.ProductCode_nsprefix_ = None
        self.GlobalProductCode = GlobalProductCode
        self.validate_ProductCode(self.GlobalProductCode)
        self.GlobalProductCode_nsprefix_ = None
        self.LocalProductCode = LocalProductCode
        self.validate_LocalProductCode(self.LocalProductCode)
        self.LocalProductCode_nsprefix_ = None
        if isinstance(Date, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Date, '%Y-%m-%d').date()
        else:
            initvalue_ = Date
        self.Date = initvalue_
        self.Date_nsprefix_ = None
        self.Contents = Contents
        self.validate_ShipmentContents(self.Contents)
        self.Contents_nsprefix_ = None
        self.DoorTo = DoorTo
        self.validate_DoorTo(self.DoorTo)
        self.DoorTo_nsprefix_ = None
        self.DimensionUnit = DimensionUnit
        self.validate_DimensionUnit(self.DimensionUnit)
        self.DimensionUnit_nsprefix_ = None
        self.InsuredAmount = InsuredAmount
        self.validate_Money(self.InsuredAmount)
        self.InsuredAmount_nsprefix_ = None
        self.PackageType = PackageType
        self.validate_PackageType(self.PackageType)
        self.PackageType_nsprefix_ = None
        self.IsDutiable = IsDutiable
        self.validate_YesNo(self.IsDutiable)
        self.IsDutiable_nsprefix_ = None
        self.CurrencyCode = CurrencyCode
        self.validate_CurrencyCode(self.CurrencyCode)
        self.CurrencyCode_nsprefix_ = None
        self.CustData = CustData
        self.validate_CustData(self.CustData)
        self.CustData_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentDetails)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentDetails.subclass:
            return ShipmentDetails.subclass(*args_, **kwargs_)
        else:
            return ShipmentDetails(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_NumberOfPieces(self):
        return self.NumberOfPieces
    def set_NumberOfPieces(self, NumberOfPieces):
        self.NumberOfPieces = NumberOfPieces
    def get_Pieces(self):
        return self.Pieces
    def set_Pieces(self, Pieces):
        self.Pieces = Pieces
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def get_WeightUnit(self):
        return self.WeightUnit
    def set_WeightUnit(self, WeightUnit):
        self.WeightUnit = WeightUnit
    def get_ProductCode(self):
        return self.ProductCode
    def set_ProductCode(self, ProductCode):
        self.ProductCode = ProductCode
    def get_GlobalProductCode(self):
        return self.GlobalProductCode
    def set_GlobalProductCode(self, GlobalProductCode):
        self.GlobalProductCode = GlobalProductCode
    def get_LocalProductCode(self):
        return self.LocalProductCode
    def set_LocalProductCode(self, LocalProductCode):
        self.LocalProductCode = LocalProductCode
    def get_Date(self):
        return self.Date
    def set_Date(self, Date):
        self.Date = Date
    def get_Contents(self):
        return self.Contents
    def set_Contents(self, Contents):
        self.Contents = Contents
    def get_DoorTo(self):
        return self.DoorTo
    def set_DoorTo(self, DoorTo):
        self.DoorTo = DoorTo
    def get_DimensionUnit(self):
        return self.DimensionUnit
    def set_DimensionUnit(self, DimensionUnit):
        self.DimensionUnit = DimensionUnit
    def get_InsuredAmount(self):
        return self.InsuredAmount
    def set_InsuredAmount(self, InsuredAmount):
        self.InsuredAmount = InsuredAmount
    def get_PackageType(self):
        return self.PackageType
    def set_PackageType(self, PackageType):
        self.PackageType = PackageType
    def get_IsDutiable(self):
        return self.IsDutiable
    def set_IsDutiable(self, IsDutiable):
        self.IsDutiable = IsDutiable
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_CustData(self):
        return self.CustData
    def set_CustData(self, CustData):
        self.CustData = CustData
    def validate_Weight(self, value):
        result = True
        # Validate type Weight, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if value > 999999.9:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on Weight' % {"value": value, "lineno": lineno} )
                result = False
            if len(str(value)) >= 7:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on Weight' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_WeightUnit(self, value):
        result = True
        # Validate type WeightUnit, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['K', 'L']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on WeightUnit' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on WeightUnit' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ProductCode(self, value):
        result = True
        # Validate type ProductCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ProductCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ProductCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_ProductCode_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_ProductCode_patterns_, ))
                result = False
        return result
    validate_ProductCode_patterns_ = [['^(([A-Z0-9])*)$']]
    def validate_LocalProductCode(self, value):
        result = True
        # Validate type LocalProductCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on LocalProductCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on LocalProductCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_Date(self, value):
        result = True
        # Validate type Date, a restriction on xsd:date.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.date):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.date)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_ShipmentContents(self, value):
        result = True
        # Validate type ShipmentContents, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 90:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ShipmentContents' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DoorTo(self, value):
        result = True
        # Validate type DoorTo, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['DD', 'DA', 'AA', 'DC']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DoorTo' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on DoorTo' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DimensionUnit(self, value):
        result = True
        # Validate type DimensionUnit, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['C', 'I']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DimensionUnit' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on DimensionUnit' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_Money(self, value):
        result = True
        # Validate type Money, a restriction on xsd:float.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, float):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (float)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0.00:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on Money' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999999999.99:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on Money' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_PackageType(self, value):
        result = True
        # Validate type PackageType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['EE', 'OD', 'CP']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on PackageType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on PackageType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_YesNo(self, value):
        result = True
        # Validate type YesNo, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['Y', 'N']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on YesNo' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on YesNo' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CurrencyCode(self, value):
        result = True
        # Validate type CurrencyCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CurrencyCode' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CustData(self, value):
        result = True
        # Validate type CustData, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 100:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CustData' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on CustData' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.NumberOfPieces is not None or
            self.Pieces is not None or
            self.Weight is not None or
            self.WeightUnit is not None or
            self.ProductCode is not None or
            self.GlobalProductCode is not None or
            self.LocalProductCode is not None or
            self.Date is not None or
            self.Contents is not None or
            self.DoorTo is not None or
            self.DimensionUnit is not None or
            self.InsuredAmount is not None or
            self.PackageType is not None or
            self.IsDutiable is not None or
            self.CurrencyCode is not None or
            self.CustData is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDetails', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentDetails')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentDetails':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentDetails')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentDetails', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentDetails'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDetails', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.NumberOfPieces is not None:
            namespaceprefix_ = self.NumberOfPieces_nsprefix_ + ':' if (UseCapturedNS_ and self.NumberOfPieces_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumberOfPieces>%s</%sNumberOfPieces>%s' % (namespaceprefix_ , self.gds_format_integer(self.NumberOfPieces, input_name='NumberOfPieces'), namespaceprefix_ , eol_))
        if self.Pieces is not None:
            namespaceprefix_ = self.Pieces_nsprefix_ + ':' if (UseCapturedNS_ and self.Pieces_nsprefix_) else ''
            self.Pieces.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Pieces', pretty_print=pretty_print)
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeight>%s</%sWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Weight, input_name='Weight'), namespaceprefix_ , eol_))
        if self.WeightUnit is not None:
            namespaceprefix_ = self.WeightUnit_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightUnit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeightUnit>%s</%sWeightUnit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WeightUnit), input_name='WeightUnit')), namespaceprefix_ , eol_))
        if self.ProductCode is not None:
            namespaceprefix_ = self.ProductCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ProductCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProductCode>%s</%sProductCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProductCode), input_name='ProductCode')), namespaceprefix_ , eol_))
        if self.GlobalProductCode is not None:
            namespaceprefix_ = self.GlobalProductCode_nsprefix_ + ':' if (UseCapturedNS_ and self.GlobalProductCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGlobalProductCode>%s</%sGlobalProductCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GlobalProductCode), input_name='GlobalProductCode')), namespaceprefix_ , eol_))
        if self.LocalProductCode is not None:
            namespaceprefix_ = self.LocalProductCode_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalProductCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalProductCode>%s</%sLocalProductCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalProductCode), input_name='LocalProductCode')), namespaceprefix_ , eol_))
        if self.Date is not None:
            namespaceprefix_ = self.Date_nsprefix_ + ':' if (UseCapturedNS_ and self.Date_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDate>%s</%sDate>%s' % (namespaceprefix_ , self.gds_format_date(self.Date, input_name='Date'), namespaceprefix_ , eol_))
        if self.Contents is not None:
            namespaceprefix_ = self.Contents_nsprefix_ + ':' if (UseCapturedNS_ and self.Contents_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sContents>%s</%sContents>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Contents), input_name='Contents')), namespaceprefix_ , eol_))
        if self.DoorTo is not None:
            namespaceprefix_ = self.DoorTo_nsprefix_ + ':' if (UseCapturedNS_ and self.DoorTo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDoorTo>%s</%sDoorTo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DoorTo), input_name='DoorTo')), namespaceprefix_ , eol_))
        if self.DimensionUnit is not None:
            namespaceprefix_ = self.DimensionUnit_nsprefix_ + ':' if (UseCapturedNS_ and self.DimensionUnit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDimensionUnit>%s</%sDimensionUnit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DimensionUnit), input_name='DimensionUnit')), namespaceprefix_ , eol_))
        if self.InsuredAmount is not None:
            namespaceprefix_ = self.InsuredAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.InsuredAmount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInsuredAmount>%s</%sInsuredAmount>%s' % (namespaceprefix_ , self.gds_format_float(self.InsuredAmount, input_name='InsuredAmount'), namespaceprefix_ , eol_))
        if self.PackageType is not None:
            namespaceprefix_ = self.PackageType_nsprefix_ + ':' if (UseCapturedNS_ and self.PackageType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPackageType>%s</%sPackageType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PackageType), input_name='PackageType')), namespaceprefix_ , eol_))
        if self.IsDutiable is not None:
            namespaceprefix_ = self.IsDutiable_nsprefix_ + ':' if (UseCapturedNS_ and self.IsDutiable_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIsDutiable>%s</%sIsDutiable>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IsDutiable), input_name='IsDutiable')), namespaceprefix_ , eol_))
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.CustData is not None:
            namespaceprefix_ = self.CustData_nsprefix_ + ':' if (UseCapturedNS_ and self.CustData_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustData>%s</%sCustData>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CustData), input_name='CustData')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'NumberOfPieces' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'NumberOfPieces')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'NumberOfPieces')
            self.NumberOfPieces = ival_
            self.NumberOfPieces_nsprefix_ = child_.prefix
        elif nodeName_ == 'Pieces':
            obj_ = Pieces.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Pieces = obj_
            obj_.original_tagname_ = 'Pieces'
        elif nodeName_ == 'Weight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Weight')
            fval_ = self.gds_validate_decimal(fval_, node, 'Weight')
            self.Weight = fval_
            self.Weight_nsprefix_ = child_.prefix
            # validate type Weight
            self.validate_Weight(self.Weight)
        elif nodeName_ == 'WeightUnit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WeightUnit')
            value_ = self.gds_validate_string(value_, node, 'WeightUnit')
            self.WeightUnit = value_
            self.WeightUnit_nsprefix_ = child_.prefix
            # validate type WeightUnit
            self.validate_WeightUnit(self.WeightUnit)
        elif nodeName_ == 'ProductCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ProductCode')
            value_ = self.gds_validate_string(value_, node, 'ProductCode')
            self.ProductCode = value_
            self.ProductCode_nsprefix_ = child_.prefix
            # validate type ProductCode
            self.validate_ProductCode(self.ProductCode)
        elif nodeName_ == 'GlobalProductCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GlobalProductCode')
            value_ = self.gds_validate_string(value_, node, 'GlobalProductCode')
            self.GlobalProductCode = value_
            self.GlobalProductCode_nsprefix_ = child_.prefix
            # validate type ProductCode
            self.validate_ProductCode(self.GlobalProductCode)
        elif nodeName_ == 'LocalProductCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalProductCode')
            value_ = self.gds_validate_string(value_, node, 'LocalProductCode')
            self.LocalProductCode = value_
            self.LocalProductCode_nsprefix_ = child_.prefix
            # validate type LocalProductCode
            self.validate_LocalProductCode(self.LocalProductCode)
        elif nodeName_ == 'Date':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.Date = dval_
            self.Date_nsprefix_ = child_.prefix
            # validate type Date
            self.validate_Date(self.Date)
        elif nodeName_ == 'Contents':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Contents')
            value_ = self.gds_validate_string(value_, node, 'Contents')
            self.Contents = value_
            self.Contents_nsprefix_ = child_.prefix
            # validate type ShipmentContents
            self.validate_ShipmentContents(self.Contents)
        elif nodeName_ == 'DoorTo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DoorTo')
            value_ = self.gds_validate_string(value_, node, 'DoorTo')
            self.DoorTo = value_
            self.DoorTo_nsprefix_ = child_.prefix
            # validate type DoorTo
            self.validate_DoorTo(self.DoorTo)
        elif nodeName_ == 'DimensionUnit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DimensionUnit')
            value_ = self.gds_validate_string(value_, node, 'DimensionUnit')
            self.DimensionUnit = value_
            self.DimensionUnit_nsprefix_ = child_.prefix
            # validate type DimensionUnit
            self.validate_DimensionUnit(self.DimensionUnit)
        elif nodeName_ == 'InsuredAmount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'InsuredAmount')
            fval_ = self.gds_validate_float(fval_, node, 'InsuredAmount')
            self.InsuredAmount = fval_
            self.InsuredAmount_nsprefix_ = child_.prefix
            # validate type Money
            self.validate_Money(self.InsuredAmount)
        elif nodeName_ == 'PackageType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PackageType')
            value_ = self.gds_validate_string(value_, node, 'PackageType')
            self.PackageType = value_
            self.PackageType_nsprefix_ = child_.prefix
            # validate type PackageType
            self.validate_PackageType(self.PackageType)
        elif nodeName_ == 'IsDutiable':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IsDutiable')
            value_ = self.gds_validate_string(value_, node, 'IsDutiable')
            self.IsDutiable = value_
            self.IsDutiable_nsprefix_ = child_.prefix
            # validate type YesNo
            self.validate_YesNo(self.IsDutiable)
        elif nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
            # validate type CurrencyCode
            self.validate_CurrencyCode(self.CurrencyCode)
        elif nodeName_ == 'CustData':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustData')
            value_ = self.gds_validate_string(value_, node, 'CustData')
            self.CustData = value_
            self.CustData_nsprefix_ = child_.prefix
            # validate type CustData
            self.validate_CustData(self.CustData)
# end class ShipmentDetails


class Shipment(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Weight=None, WeightUnit=None, Pieces=None, DoorTo=None, AirwarBillNumber=None, AccountType=None, ProductType=None, GlobalProductType=None, LocalProductType=None, Commodity=None, DeclaredValue=None, DeclaredCurrency=None, InsuredValue=None, InsuredCurrency=None, DimensionalUnit=None, DimensionalWeight=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Weight = Weight
        self.validate_Weight(self.Weight)
        self.Weight_nsprefix_ = None
        self.WeightUnit = WeightUnit
        self.validate_WeightUnit(self.WeightUnit)
        self.WeightUnit_nsprefix_ = None
        self.Pieces = Pieces
        self.Pieces_nsprefix_ = None
        self.DoorTo = DoorTo
        self.validate_DoorTo(self.DoorTo)
        self.DoorTo_nsprefix_ = None
        self.AirwarBillNumber = AirwarBillNumber
        self.validate_AWBNumber(self.AirwarBillNumber)
        self.AirwarBillNumber_nsprefix_ = None
        self.AccountType = AccountType
        self.validate_AccountType(self.AccountType)
        self.AccountType_nsprefix_ = None
        self.ProductType = ProductType
        self.ProductType_nsprefix_ = None
        self.GlobalProductType = GlobalProductType
        self.GlobalProductType_nsprefix_ = None
        self.LocalProductType = LocalProductType
        self.LocalProductType_nsprefix_ = None
        self.Commodity = Commodity
        self.Commodity_nsprefix_ = None
        self.DeclaredValue = DeclaredValue
        self.validate_Money(self.DeclaredValue)
        self.DeclaredValue_nsprefix_ = None
        self.DeclaredCurrency = DeclaredCurrency
        self.validate_CurrencyCode(self.DeclaredCurrency)
        self.DeclaredCurrency_nsprefix_ = None
        self.InsuredValue = InsuredValue
        self.validate_Money(self.InsuredValue)
        self.InsuredValue_nsprefix_ = None
        self.InsuredCurrency = InsuredCurrency
        self.validate_CurrencyCode(self.InsuredCurrency)
        self.InsuredCurrency_nsprefix_ = None
        self.DimensionalUnit = DimensionalUnit
        self.validate_WeightUnit(self.DimensionalUnit)
        self.DimensionalUnit_nsprefix_ = None
        self.DimensionalWeight = DimensionalWeight
        self.validate_Weight(self.DimensionalWeight)
        self.DimensionalWeight_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Shipment)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Shipment.subclass:
            return Shipment.subclass(*args_, **kwargs_)
        else:
            return Shipment(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def get_WeightUnit(self):
        return self.WeightUnit
    def set_WeightUnit(self, WeightUnit):
        self.WeightUnit = WeightUnit
    def get_Pieces(self):
        return self.Pieces
    def set_Pieces(self, Pieces):
        self.Pieces = Pieces
    def get_DoorTo(self):
        return self.DoorTo
    def set_DoorTo(self, DoorTo):
        self.DoorTo = DoorTo
    def get_AirwarBillNumber(self):
        return self.AirwarBillNumber
    def set_AirwarBillNumber(self, AirwarBillNumber):
        self.AirwarBillNumber = AirwarBillNumber
    def get_AccountType(self):
        return self.AccountType
    def set_AccountType(self, AccountType):
        self.AccountType = AccountType
    def get_ProductType(self):
        return self.ProductType
    def set_ProductType(self, ProductType):
        self.ProductType = ProductType
    def get_GlobalProductType(self):
        return self.GlobalProductType
    def set_GlobalProductType(self, GlobalProductType):
        self.GlobalProductType = GlobalProductType
    def get_LocalProductType(self):
        return self.LocalProductType
    def set_LocalProductType(self, LocalProductType):
        self.LocalProductType = LocalProductType
    def get_Commodity(self):
        return self.Commodity
    def set_Commodity(self, Commodity):
        self.Commodity = Commodity
    def get_DeclaredValue(self):
        return self.DeclaredValue
    def set_DeclaredValue(self, DeclaredValue):
        self.DeclaredValue = DeclaredValue
    def get_DeclaredCurrency(self):
        return self.DeclaredCurrency
    def set_DeclaredCurrency(self, DeclaredCurrency):
        self.DeclaredCurrency = DeclaredCurrency
    def get_InsuredValue(self):
        return self.InsuredValue
    def set_InsuredValue(self, InsuredValue):
        self.InsuredValue = InsuredValue
    def get_InsuredCurrency(self):
        return self.InsuredCurrency
    def set_InsuredCurrency(self, InsuredCurrency):
        self.InsuredCurrency = InsuredCurrency
    def get_DimensionalUnit(self):
        return self.DimensionalUnit
    def set_DimensionalUnit(self, DimensionalUnit):
        self.DimensionalUnit = DimensionalUnit
    def get_DimensionalWeight(self):
        return self.DimensionalWeight
    def set_DimensionalWeight(self, DimensionalWeight):
        self.DimensionalWeight = DimensionalWeight
    def validate_Weight(self, value):
        result = True
        # Validate type Weight, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if value > 999999.9:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on Weight' % {"value": value, "lineno": lineno} )
                result = False
            if len(str(value)) >= 7:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on Weight' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_WeightUnit(self, value):
        result = True
        # Validate type WeightUnit, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['K', 'L']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on WeightUnit' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on WeightUnit' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DoorTo(self, value):
        result = True
        # Validate type DoorTo, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['DD', 'DA', 'AA', 'DC']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DoorTo' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on DoorTo' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_AWBNumber(self, value):
        result = True
        # Validate type AWBNumber, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 11:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on AWBNumber' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_AccountType(self, value):
        result = True
        # Validate type AccountType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['D']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on AccountType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_Money(self, value):
        result = True
        # Validate type Money, a restriction on xsd:float.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, float):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (float)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0.00:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on Money' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999999999.99:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on Money' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_CurrencyCode(self, value):
        result = True
        # Validate type CurrencyCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CurrencyCode' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Weight is not None or
            self.WeightUnit is not None or
            self.Pieces is not None or
            self.DoorTo is not None or
            self.AirwarBillNumber is not None or
            self.AccountType is not None or
            self.ProductType is not None or
            self.GlobalProductType is not None or
            self.LocalProductType is not None or
            self.Commodity is not None or
            self.DeclaredValue is not None or
            self.DeclaredCurrency is not None or
            self.InsuredValue is not None or
            self.InsuredCurrency is not None or
            self.DimensionalUnit is not None or
            self.DimensionalWeight is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Shipment', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Shipment')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Shipment':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Shipment')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Shipment', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Shipment'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Shipment', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeight>%s</%sWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Weight, input_name='Weight'), namespaceprefix_ , eol_))
        if self.WeightUnit is not None:
            namespaceprefix_ = self.WeightUnit_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightUnit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeightUnit>%s</%sWeightUnit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WeightUnit), input_name='WeightUnit')), namespaceprefix_ , eol_))
        if self.Pieces is not None:
            namespaceprefix_ = self.Pieces_nsprefix_ + ':' if (UseCapturedNS_ and self.Pieces_nsprefix_) else ''
            self.Pieces.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Pieces', pretty_print=pretty_print)
        if self.DoorTo is not None:
            namespaceprefix_ = self.DoorTo_nsprefix_ + ':' if (UseCapturedNS_ and self.DoorTo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDoorTo>%s</%sDoorTo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DoorTo), input_name='DoorTo')), namespaceprefix_ , eol_))
        if self.AirwarBillNumber is not None:
            namespaceprefix_ = self.AirwarBillNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.AirwarBillNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAirwarBillNumber>%s</%sAirwarBillNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AirwarBillNumber), input_name='AirwarBillNumber')), namespaceprefix_ , eol_))
        if self.AccountType is not None:
            namespaceprefix_ = self.AccountType_nsprefix_ + ':' if (UseCapturedNS_ and self.AccountType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccountType>%s</%sAccountType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccountType), input_name='AccountType')), namespaceprefix_ , eol_))
        if self.ProductType is not None:
            namespaceprefix_ = self.ProductType_nsprefix_ + ':' if (UseCapturedNS_ and self.ProductType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProductType>%s</%sProductType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProductType), input_name='ProductType')), namespaceprefix_ , eol_))
        if self.GlobalProductType is not None:
            namespaceprefix_ = self.GlobalProductType_nsprefix_ + ':' if (UseCapturedNS_ and self.GlobalProductType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGlobalProductType>%s</%sGlobalProductType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GlobalProductType), input_name='GlobalProductType')), namespaceprefix_ , eol_))
        if self.LocalProductType is not None:
            namespaceprefix_ = self.LocalProductType_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalProductType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalProductType>%s</%sLocalProductType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalProductType), input_name='LocalProductType')), namespaceprefix_ , eol_))
        if self.Commodity is not None:
            namespaceprefix_ = self.Commodity_nsprefix_ + ':' if (UseCapturedNS_ and self.Commodity_nsprefix_) else ''
            self.Commodity.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Commodity', pretty_print=pretty_print)
        if self.DeclaredValue is not None:
            namespaceprefix_ = self.DeclaredValue_nsprefix_ + ':' if (UseCapturedNS_ and self.DeclaredValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeclaredValue>%s</%sDeclaredValue>%s' % (namespaceprefix_ , self.gds_format_float(self.DeclaredValue, input_name='DeclaredValue'), namespaceprefix_ , eol_))
        if self.DeclaredCurrency is not None:
            namespaceprefix_ = self.DeclaredCurrency_nsprefix_ + ':' if (UseCapturedNS_ and self.DeclaredCurrency_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeclaredCurrency>%s</%sDeclaredCurrency>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DeclaredCurrency), input_name='DeclaredCurrency')), namespaceprefix_ , eol_))
        if self.InsuredValue is not None:
            namespaceprefix_ = self.InsuredValue_nsprefix_ + ':' if (UseCapturedNS_ and self.InsuredValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInsuredValue>%s</%sInsuredValue>%s' % (namespaceprefix_ , self.gds_format_float(self.InsuredValue, input_name='InsuredValue'), namespaceprefix_ , eol_))
        if self.InsuredCurrency is not None:
            namespaceprefix_ = self.InsuredCurrency_nsprefix_ + ':' if (UseCapturedNS_ and self.InsuredCurrency_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInsuredCurrency>%s</%sInsuredCurrency>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.InsuredCurrency), input_name='InsuredCurrency')), namespaceprefix_ , eol_))
        if self.DimensionalUnit is not None:
            namespaceprefix_ = self.DimensionalUnit_nsprefix_ + ':' if (UseCapturedNS_ and self.DimensionalUnit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDimensionalUnit>%s</%sDimensionalUnit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DimensionalUnit), input_name='DimensionalUnit')), namespaceprefix_ , eol_))
        if self.DimensionalWeight is not None:
            namespaceprefix_ = self.DimensionalWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.DimensionalWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDimensionalWeight>%s</%sDimensionalWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.DimensionalWeight, input_name='DimensionalWeight'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Weight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Weight')
            fval_ = self.gds_validate_decimal(fval_, node, 'Weight')
            self.Weight = fval_
            self.Weight_nsprefix_ = child_.prefix
            # validate type Weight
            self.validate_Weight(self.Weight)
        elif nodeName_ == 'WeightUnit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WeightUnit')
            value_ = self.gds_validate_string(value_, node, 'WeightUnit')
            self.WeightUnit = value_
            self.WeightUnit_nsprefix_ = child_.prefix
            # validate type WeightUnit
            self.validate_WeightUnit(self.WeightUnit)
        elif nodeName_ == 'Pieces':
            obj_ = Pieces.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Pieces = obj_
            obj_.original_tagname_ = 'Pieces'
        elif nodeName_ == 'DoorTo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DoorTo')
            value_ = self.gds_validate_string(value_, node, 'DoorTo')
            self.DoorTo = value_
            self.DoorTo_nsprefix_ = child_.prefix
            # validate type DoorTo
            self.validate_DoorTo(self.DoorTo)
        elif nodeName_ == 'AirwarBillNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AirwarBillNumber')
            value_ = self.gds_validate_string(value_, node, 'AirwarBillNumber')
            self.AirwarBillNumber = value_
            self.AirwarBillNumber_nsprefix_ = child_.prefix
            # validate type AWBNumber
            self.validate_AWBNumber(self.AirwarBillNumber)
        elif nodeName_ == 'AccountType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccountType')
            value_ = self.gds_validate_string(value_, node, 'AccountType')
            self.AccountType = value_
            self.AccountType_nsprefix_ = child_.prefix
            # validate type AccountType
            self.validate_AccountType(self.AccountType)
        elif nodeName_ == 'ProductType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ProductType')
            value_ = self.gds_validate_string(value_, node, 'ProductType')
            self.ProductType = value_
            self.ProductType_nsprefix_ = child_.prefix
        elif nodeName_ == 'GlobalProductType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GlobalProductType')
            value_ = self.gds_validate_string(value_, node, 'GlobalProductType')
            self.GlobalProductType = value_
            self.GlobalProductType_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocalProductType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalProductType')
            value_ = self.gds_validate_string(value_, node, 'LocalProductType')
            self.LocalProductType = value_
            self.LocalProductType_nsprefix_ = child_.prefix
        elif nodeName_ == 'Commodity':
            obj_ = Commodity.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Commodity = obj_
            obj_.original_tagname_ = 'Commodity'
        elif nodeName_ == 'DeclaredValue' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'DeclaredValue')
            fval_ = self.gds_validate_float(fval_, node, 'DeclaredValue')
            self.DeclaredValue = fval_
            self.DeclaredValue_nsprefix_ = child_.prefix
            # validate type Money
            self.validate_Money(self.DeclaredValue)
        elif nodeName_ == 'DeclaredCurrency':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DeclaredCurrency')
            value_ = self.gds_validate_string(value_, node, 'DeclaredCurrency')
            self.DeclaredCurrency = value_
            self.DeclaredCurrency_nsprefix_ = child_.prefix
            # validate type CurrencyCode
            self.validate_CurrencyCode(self.DeclaredCurrency)
        elif nodeName_ == 'InsuredValue' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'InsuredValue')
            fval_ = self.gds_validate_float(fval_, node, 'InsuredValue')
            self.InsuredValue = fval_
            self.InsuredValue_nsprefix_ = child_.prefix
            # validate type Money
            self.validate_Money(self.InsuredValue)
        elif nodeName_ == 'InsuredCurrency':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'InsuredCurrency')
            value_ = self.gds_validate_string(value_, node, 'InsuredCurrency')
            self.InsuredCurrency = value_
            self.InsuredCurrency_nsprefix_ = child_.prefix
            # validate type CurrencyCode
            self.validate_CurrencyCode(self.InsuredCurrency)
        elif nodeName_ == 'DimensionalUnit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DimensionalUnit')
            value_ = self.gds_validate_string(value_, node, 'DimensionalUnit')
            self.DimensionalUnit = value_
            self.DimensionalUnit_nsprefix_ = child_.prefix
            # validate type WeightUnit
            self.validate_WeightUnit(self.DimensionalUnit)
        elif nodeName_ == 'DimensionalWeight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'DimensionalWeight')
            fval_ = self.gds_validate_decimal(fval_, node, 'DimensionalWeight')
            self.DimensionalWeight = fval_
            self.DimensionalWeight_nsprefix_ = child_.prefix
            # validate type Weight
            self.validate_Weight(self.DimensionalWeight)
# end class Shipment


class Shipper(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ShipperID=None, CompanyName=None, RegisteredAccount=None, AddressLine=None, City=None, Division=None, DivisionCode=None, PostalCode=None, OriginServiceAreaCode=None, OriginFacilityCode=None, CountryCode=None, CountryName=None, FederalTaxId=None, StateTaxId=None, Contact=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ShipperID = ShipperID
        self.validate_ShipperID(self.ShipperID)
        self.ShipperID_nsprefix_ = None
        self.CompanyName = CompanyName
        self.validate_CompanyNameValidator(self.CompanyName)
        self.CompanyName_nsprefix_ = None
        self.RegisteredAccount = RegisteredAccount
        self.validate_AccountNumber(self.RegisteredAccount)
        self.RegisteredAccount_nsprefix_ = None
        if AddressLine is None:
            self.AddressLine = []
        else:
            self.AddressLine = AddressLine
        self.AddressLine_nsprefix_ = None
        self.City = City
        self.validate_City(self.City)
        self.City_nsprefix_ = None
        self.Division = Division
        self.validate_Division(self.Division)
        self.Division_nsprefix_ = None
        self.DivisionCode = DivisionCode
        self.validate_DivisionCodeType1(self.DivisionCode)
        self.DivisionCode_nsprefix_ = None
        self.PostalCode = PostalCode
        self.validate_PostalCode(self.PostalCode)
        self.PostalCode_nsprefix_ = None
        self.OriginServiceAreaCode = OriginServiceAreaCode
        self.validate_OriginServiceAreaCode(self.OriginServiceAreaCode)
        self.OriginServiceAreaCode_nsprefix_ = None
        self.OriginFacilityCode = OriginFacilityCode
        self.validate_OriginFacilityCode(self.OriginFacilityCode)
        self.OriginFacilityCode_nsprefix_ = None
        self.CountryCode = CountryCode
        self.validate_CountryCode(self.CountryCode)
        self.CountryCode_nsprefix_ = None
        self.CountryName = CountryName
        self.validate_CountryName(self.CountryName)
        self.CountryName_nsprefix_ = None
        self.FederalTaxId = FederalTaxId
        self.validate_FederalTaxIdType2(self.FederalTaxId)
        self.FederalTaxId_nsprefix_ = None
        self.StateTaxId = StateTaxId
        self.validate_StateTaxIdType3(self.StateTaxId)
        self.StateTaxId_nsprefix_ = None
        self.Contact = Contact
        self.Contact_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Shipper)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Shipper.subclass:
            return Shipper.subclass(*args_, **kwargs_)
        else:
            return Shipper(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ShipperID(self):
        return self.ShipperID
    def set_ShipperID(self, ShipperID):
        self.ShipperID = ShipperID
    def get_CompanyName(self):
        return self.CompanyName
    def set_CompanyName(self, CompanyName):
        self.CompanyName = CompanyName
    def get_RegisteredAccount(self):
        return self.RegisteredAccount
    def set_RegisteredAccount(self, RegisteredAccount):
        self.RegisteredAccount = RegisteredAccount
    def get_AddressLine(self):
        return self.AddressLine
    def set_AddressLine(self, AddressLine):
        self.AddressLine = AddressLine
    def add_AddressLine(self, value):
        self.AddressLine.append(value)
    def insert_AddressLine_at(self, index, value):
        self.AddressLine.insert(index, value)
    def replace_AddressLine_at(self, index, value):
        self.AddressLine[index] = value
    def get_City(self):
        return self.City
    def set_City(self, City):
        self.City = City
    def get_Division(self):
        return self.Division
    def set_Division(self, Division):
        self.Division = Division
    def get_DivisionCode(self):
        return self.DivisionCode
    def set_DivisionCode(self, DivisionCode):
        self.DivisionCode = DivisionCode
    def get_PostalCode(self):
        return self.PostalCode
    def set_PostalCode(self, PostalCode):
        self.PostalCode = PostalCode
    def get_OriginServiceAreaCode(self):
        return self.OriginServiceAreaCode
    def set_OriginServiceAreaCode(self, OriginServiceAreaCode):
        self.OriginServiceAreaCode = OriginServiceAreaCode
    def get_OriginFacilityCode(self):
        return self.OriginFacilityCode
    def set_OriginFacilityCode(self, OriginFacilityCode):
        self.OriginFacilityCode = OriginFacilityCode
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def get_CountryName(self):
        return self.CountryName
    def set_CountryName(self, CountryName):
        self.CountryName = CountryName
    def get_FederalTaxId(self):
        return self.FederalTaxId
    def set_FederalTaxId(self, FederalTaxId):
        self.FederalTaxId = FederalTaxId
    def get_StateTaxId(self):
        return self.StateTaxId
    def set_StateTaxId(self, StateTaxId):
        self.StateTaxId = StateTaxId
    def get_Contact(self):
        return self.Contact
    def set_Contact(self, Contact):
        self.Contact = Contact
    def validate_ShipperID(self, value):
        result = True
        # Validate type ShipperID, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 30:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ShipperID' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CompanyNameValidator(self, value):
        result = True
        # Validate type CompanyNameValidator, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CompanyNameValidator' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_AccountNumber(self, value):
        result = True
        # Validate type AccountNumber, a restriction on xsd:positiveInteger.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 100000000:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on AccountNumber' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999999999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on AccountNumber' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_AddressLine(self, value):
        result = True
        # Validate type AddressLine, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on AddressLine' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_City(self, value):
        result = True
        # Validate type City, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on City' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_Division(self, value):
        result = True
        # Validate type Division, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on Division' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DivisionCodeType1(self, value):
        result = True
        # Validate type DivisionCodeType1, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on DivisionCodeType1' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PostalCode(self, value):
        result = True
        # Validate type PostalCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_OriginServiceAreaCode(self, value):
        result = True
        # Validate type OriginServiceAreaCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on OriginServiceAreaCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_OriginFacilityCode(self, value):
        result = True
        # Validate type OriginFacilityCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on OriginFacilityCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CountryCode(self, value):
        result = True
        # Validate type CountryCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CountryCode' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CountryName(self, value):
        result = True
        # Validate type CountryName, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CountryName' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_FederalTaxIdType2(self, value):
        result = True
        # Validate type FederalTaxIdType2, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on FederalTaxIdType2' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on FederalTaxIdType2' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_StateTaxIdType3(self, value):
        result = True
        # Validate type StateTaxIdType3, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on StateTaxIdType3' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on StateTaxIdType3' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.ShipperID is not None or
            self.CompanyName is not None or
            self.RegisteredAccount is not None or
            self.AddressLine or
            self.City is not None or
            self.Division is not None or
            self.DivisionCode is not None or
            self.PostalCode is not None or
            self.OriginServiceAreaCode is not None or
            self.OriginFacilityCode is not None or
            self.CountryCode is not None or
            self.CountryName is not None or
            self.FederalTaxId is not None or
            self.StateTaxId is not None or
            self.Contact is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Shipper', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Shipper')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Shipper':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Shipper')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Shipper', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Shipper'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Shipper', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ShipperID is not None:
            namespaceprefix_ = self.ShipperID_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipperID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipperID>%s</%sShipperID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShipperID), input_name='ShipperID')), namespaceprefix_ , eol_))
        if self.CompanyName is not None:
            namespaceprefix_ = self.CompanyName_nsprefix_ + ':' if (UseCapturedNS_ and self.CompanyName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCompanyName>%s</%sCompanyName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CompanyName), input_name='CompanyName')), namespaceprefix_ , eol_))
        if self.RegisteredAccount is not None:
            namespaceprefix_ = self.RegisteredAccount_nsprefix_ + ':' if (UseCapturedNS_ and self.RegisteredAccount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRegisteredAccount>%s</%sRegisteredAccount>%s' % (namespaceprefix_ , self.gds_format_integer(self.RegisteredAccount, input_name='RegisteredAccount'), namespaceprefix_ , eol_))
        for AddressLine_ in self.AddressLine:
            namespaceprefix_ = self.AddressLine_nsprefix_ + ':' if (UseCapturedNS_ and self.AddressLine_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAddressLine>%s</%sAddressLine>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(AddressLine_), input_name='AddressLine')), namespaceprefix_ , eol_))
        if self.City is not None:
            namespaceprefix_ = self.City_nsprefix_ + ':' if (UseCapturedNS_ and self.City_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCity>%s</%sCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.City), input_name='City')), namespaceprefix_ , eol_))
        if self.Division is not None:
            namespaceprefix_ = self.Division_nsprefix_ + ':' if (UseCapturedNS_ and self.Division_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDivision>%s</%sDivision>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Division), input_name='Division')), namespaceprefix_ , eol_))
        if self.DivisionCode is not None:
            namespaceprefix_ = self.DivisionCode_nsprefix_ + ':' if (UseCapturedNS_ and self.DivisionCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDivisionCode>%s</%sDivisionCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DivisionCode), input_name='DivisionCode')), namespaceprefix_ , eol_))
        if self.PostalCode is not None:
            namespaceprefix_ = self.PostalCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PostalCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPostalCode>%s</%sPostalCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PostalCode), input_name='PostalCode')), namespaceprefix_ , eol_))
        if self.OriginServiceAreaCode is not None:
            namespaceprefix_ = self.OriginServiceAreaCode_nsprefix_ + ':' if (UseCapturedNS_ and self.OriginServiceAreaCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOriginServiceAreaCode>%s</%sOriginServiceAreaCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OriginServiceAreaCode), input_name='OriginServiceAreaCode')), namespaceprefix_ , eol_))
        if self.OriginFacilityCode is not None:
            namespaceprefix_ = self.OriginFacilityCode_nsprefix_ + ':' if (UseCapturedNS_ and self.OriginFacilityCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOriginFacilityCode>%s</%sOriginFacilityCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OriginFacilityCode), input_name='OriginFacilityCode')), namespaceprefix_ , eol_))
        if self.CountryCode is not None:
            namespaceprefix_ = self.CountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryCode>%s</%sCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryCode), input_name='CountryCode')), namespaceprefix_ , eol_))
        if self.CountryName is not None:
            namespaceprefix_ = self.CountryName_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryName>%s</%sCountryName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryName), input_name='CountryName')), namespaceprefix_ , eol_))
        if self.FederalTaxId is not None:
            namespaceprefix_ = self.FederalTaxId_nsprefix_ + ':' if (UseCapturedNS_ and self.FederalTaxId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFederalTaxId>%s</%sFederalTaxId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FederalTaxId), input_name='FederalTaxId')), namespaceprefix_ , eol_))
        if self.StateTaxId is not None:
            namespaceprefix_ = self.StateTaxId_nsprefix_ + ':' if (UseCapturedNS_ and self.StateTaxId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStateTaxId>%s</%sStateTaxId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.StateTaxId), input_name='StateTaxId')), namespaceprefix_ , eol_))
        if self.Contact is not None:
            namespaceprefix_ = self.Contact_nsprefix_ + ':' if (UseCapturedNS_ and self.Contact_nsprefix_) else ''
            self.Contact.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Contact', pretty_print=pretty_print)
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
        if nodeName_ == 'ShipperID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipperID')
            value_ = self.gds_validate_string(value_, node, 'ShipperID')
            self.ShipperID = value_
            self.ShipperID_nsprefix_ = child_.prefix
            # validate type ShipperID
            self.validate_ShipperID(self.ShipperID)
        elif nodeName_ == 'CompanyName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CompanyName')
            value_ = self.gds_validate_string(value_, node, 'CompanyName')
            self.CompanyName = value_
            self.CompanyName_nsprefix_ = child_.prefix
            # validate type CompanyNameValidator
            self.validate_CompanyNameValidator(self.CompanyName)
        elif nodeName_ == 'RegisteredAccount' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'RegisteredAccount')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'RegisteredAccount')
            self.RegisteredAccount = ival_
            self.RegisteredAccount_nsprefix_ = child_.prefix
            # validate type AccountNumber
            self.validate_AccountNumber(self.RegisteredAccount)
        elif nodeName_ == 'AddressLine':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AddressLine')
            value_ = self.gds_validate_string(value_, node, 'AddressLine')
            self.AddressLine.append(value_)
            self.AddressLine_nsprefix_ = child_.prefix
            # validate type AddressLine
            self.validate_AddressLine(self.AddressLine[-1])
        elif nodeName_ == 'City':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'City')
            value_ = self.gds_validate_string(value_, node, 'City')
            self.City = value_
            self.City_nsprefix_ = child_.prefix
            # validate type City
            self.validate_City(self.City)
        elif nodeName_ == 'Division':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Division')
            value_ = self.gds_validate_string(value_, node, 'Division')
            self.Division = value_
            self.Division_nsprefix_ = child_.prefix
            # validate type Division
            self.validate_Division(self.Division)
        elif nodeName_ == 'DivisionCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DivisionCode')
            value_ = self.gds_validate_string(value_, node, 'DivisionCode')
            self.DivisionCode = value_
            self.DivisionCode_nsprefix_ = child_.prefix
            # validate type DivisionCodeType1
            self.validate_DivisionCodeType1(self.DivisionCode)
        elif nodeName_ == 'PostalCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PostalCode')
            value_ = self.gds_validate_string(value_, node, 'PostalCode')
            self.PostalCode = value_
            self.PostalCode_nsprefix_ = child_.prefix
            # validate type PostalCode
            self.validate_PostalCode(self.PostalCode)
        elif nodeName_ == 'OriginServiceAreaCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OriginServiceAreaCode')
            value_ = self.gds_validate_string(value_, node, 'OriginServiceAreaCode')
            self.OriginServiceAreaCode = value_
            self.OriginServiceAreaCode_nsprefix_ = child_.prefix
            # validate type OriginServiceAreaCode
            self.validate_OriginServiceAreaCode(self.OriginServiceAreaCode)
        elif nodeName_ == 'OriginFacilityCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OriginFacilityCode')
            value_ = self.gds_validate_string(value_, node, 'OriginFacilityCode')
            self.OriginFacilityCode = value_
            self.OriginFacilityCode_nsprefix_ = child_.prefix
            # validate type OriginFacilityCode
            self.validate_OriginFacilityCode(self.OriginFacilityCode)
        elif nodeName_ == 'CountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryCode')
            value_ = self.gds_validate_string(value_, node, 'CountryCode')
            self.CountryCode = value_
            self.CountryCode_nsprefix_ = child_.prefix
            # validate type CountryCode
            self.validate_CountryCode(self.CountryCode)
        elif nodeName_ == 'CountryName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryName')
            value_ = self.gds_validate_string(value_, node, 'CountryName')
            self.CountryName = value_
            self.CountryName_nsprefix_ = child_.prefix
            # validate type CountryName
            self.validate_CountryName(self.CountryName)
        elif nodeName_ == 'FederalTaxId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FederalTaxId')
            value_ = self.gds_validate_string(value_, node, 'FederalTaxId')
            self.FederalTaxId = value_
            self.FederalTaxId_nsprefix_ = child_.prefix
            # validate type FederalTaxIdType2
            self.validate_FederalTaxIdType2(self.FederalTaxId)
        elif nodeName_ == 'StateTaxId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'StateTaxId')
            value_ = self.gds_validate_string(value_, node, 'StateTaxId')
            self.StateTaxId = value_
            self.StateTaxId_nsprefix_ = child_.prefix
            # validate type StateTaxIdType3
            self.validate_StateTaxIdType3(self.StateTaxId)
        elif nodeName_ == 'Contact':
            obj_ = Contact.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Contact = obj_
            obj_.original_tagname_ = 'Contact'
# end class Shipper


class SpecialService(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, SpecialServiceType=None, CommunicationAddress=None, CommunicationType=None, ChargeValue=None, CurrencyCode=None, IsWaived=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.SpecialServiceType = SpecialServiceType
        self.validate_SpecialServiceType(self.SpecialServiceType)
        self.SpecialServiceType_nsprefix_ = None
        self.CommunicationAddress = CommunicationAddress
        self.validate_CommunicationAddress(self.CommunicationAddress)
        self.CommunicationAddress_nsprefix_ = None
        self.CommunicationType = CommunicationType
        self.validate_CommunicationType(self.CommunicationType)
        self.CommunicationType_nsprefix_ = None
        self.ChargeValue = ChargeValue
        self.validate_Money(self.ChargeValue)
        self.ChargeValue_nsprefix_ = None
        self.CurrencyCode = CurrencyCode
        self.validate_CurrencyCode(self.CurrencyCode)
        self.CurrencyCode_nsprefix_ = None
        self.IsWaived = IsWaived
        self.validate_YesNo(self.IsWaived)
        self.IsWaived_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SpecialService)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SpecialService.subclass:
            return SpecialService.subclass(*args_, **kwargs_)
        else:
            return SpecialService(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_SpecialServiceType(self):
        return self.SpecialServiceType
    def set_SpecialServiceType(self, SpecialServiceType):
        self.SpecialServiceType = SpecialServiceType
    def get_CommunicationAddress(self):
        return self.CommunicationAddress
    def set_CommunicationAddress(self, CommunicationAddress):
        self.CommunicationAddress = CommunicationAddress
    def get_CommunicationType(self):
        return self.CommunicationType
    def set_CommunicationType(self, CommunicationType):
        self.CommunicationType = CommunicationType
    def get_ChargeValue(self):
        return self.ChargeValue
    def set_ChargeValue(self, ChargeValue):
        self.ChargeValue = ChargeValue
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_IsWaived(self):
        return self.IsWaived
    def set_IsWaived(self, IsWaived):
        self.IsWaived = IsWaived
    def validate_SpecialServiceType(self, value):
        result = True
        # Validate type SpecialServiceType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on SpecialServiceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CommunicationAddress(self, value):
        result = True
        # Validate type CommunicationAddress, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CommunicationAddress' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CommunicationType(self, value):
        result = True
        # Validate type CommunicationType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['P', 'F']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CommunicationType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CommunicationType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_Money(self, value):
        result = True
        # Validate type Money, a restriction on xsd:float.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, float):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (float)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0.00:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on Money' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999999999.99:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on Money' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_CurrencyCode(self, value):
        result = True
        # Validate type CurrencyCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CurrencyCode' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_YesNo(self, value):
        result = True
        # Validate type YesNo, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['Y', 'N']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on YesNo' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on YesNo' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.SpecialServiceType is not None or
            self.CommunicationAddress is not None or
            self.CommunicationType is not None or
            self.ChargeValue is not None or
            self.CurrencyCode is not None or
            self.IsWaived is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SpecialService', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SpecialService')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SpecialService':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SpecialService')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SpecialService', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SpecialService'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SpecialService', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.SpecialServiceType is not None:
            namespaceprefix_ = self.SpecialServiceType_nsprefix_ + ':' if (UseCapturedNS_ and self.SpecialServiceType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSpecialServiceType>%s</%sSpecialServiceType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SpecialServiceType), input_name='SpecialServiceType')), namespaceprefix_ , eol_))
        if self.CommunicationAddress is not None:
            namespaceprefix_ = self.CommunicationAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.CommunicationAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCommunicationAddress>%s</%sCommunicationAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CommunicationAddress), input_name='CommunicationAddress')), namespaceprefix_ , eol_))
        if self.CommunicationType is not None:
            namespaceprefix_ = self.CommunicationType_nsprefix_ + ':' if (UseCapturedNS_ and self.CommunicationType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCommunicationType>%s</%sCommunicationType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CommunicationType), input_name='CommunicationType')), namespaceprefix_ , eol_))
        if self.ChargeValue is not None:
            namespaceprefix_ = self.ChargeValue_nsprefix_ + ':' if (UseCapturedNS_ and self.ChargeValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChargeValue>%s</%sChargeValue>%s' % (namespaceprefix_ , self.gds_format_float(self.ChargeValue, input_name='ChargeValue'), namespaceprefix_ , eol_))
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.IsWaived is not None:
            namespaceprefix_ = self.IsWaived_nsprefix_ + ':' if (UseCapturedNS_ and self.IsWaived_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIsWaived>%s</%sIsWaived>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IsWaived), input_name='IsWaived')), namespaceprefix_ , eol_))
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
            # validate type SpecialServiceType
            self.validate_SpecialServiceType(self.SpecialServiceType)
        elif nodeName_ == 'CommunicationAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CommunicationAddress')
            value_ = self.gds_validate_string(value_, node, 'CommunicationAddress')
            self.CommunicationAddress = value_
            self.CommunicationAddress_nsprefix_ = child_.prefix
            # validate type CommunicationAddress
            self.validate_CommunicationAddress(self.CommunicationAddress)
        elif nodeName_ == 'CommunicationType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CommunicationType')
            value_ = self.gds_validate_string(value_, node, 'CommunicationType')
            self.CommunicationType = value_
            self.CommunicationType_nsprefix_ = child_.prefix
            # validate type CommunicationType
            self.validate_CommunicationType(self.CommunicationType)
        elif nodeName_ == 'ChargeValue' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'ChargeValue')
            fval_ = self.gds_validate_float(fval_, node, 'ChargeValue')
            self.ChargeValue = fval_
            self.ChargeValue_nsprefix_ = child_.prefix
            # validate type Money
            self.validate_Money(self.ChargeValue)
        elif nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
            # validate type CurrencyCode
            self.validate_CurrencyCode(self.CurrencyCode)
        elif nodeName_ == 'IsWaived':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IsWaived')
            value_ = self.gds_validate_string(value_, node, 'IsWaived')
            self.IsWaived = value_
            self.IsWaived_nsprefix_ = child_.prefix
            # validate type YesNo
            self.validate_YesNo(self.IsWaived)
# end class SpecialService


class WeightSeg(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Weight=None, WeightUnit=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Weight = Weight
        self.validate_Weight(self.Weight)
        self.Weight_nsprefix_ = None
        self.WeightUnit = WeightUnit
        self.validate_WeightUnit(self.WeightUnit)
        self.WeightUnit_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, WeightSeg)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if WeightSeg.subclass:
            return WeightSeg.subclass(*args_, **kwargs_)
        else:
            return WeightSeg(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def get_WeightUnit(self):
        return self.WeightUnit
    def set_WeightUnit(self, WeightUnit):
        self.WeightUnit = WeightUnit
    def validate_Weight(self, value):
        result = True
        # Validate type Weight, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if value > 999999.9:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on Weight' % {"value": value, "lineno": lineno} )
                result = False
            if len(str(value)) >= 7:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on Weight' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_WeightUnit(self, value):
        result = True
        # Validate type WeightUnit, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['K', 'L']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on WeightUnit' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on WeightUnit' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Weight is not None or
            self.WeightUnit is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WeightSeg', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('WeightSeg')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'WeightSeg':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='WeightSeg')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='WeightSeg', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='WeightSeg'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WeightSeg', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeight>%s</%sWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Weight, input_name='Weight'), namespaceprefix_ , eol_))
        if self.WeightUnit is not None:
            namespaceprefix_ = self.WeightUnit_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightUnit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeightUnit>%s</%sWeightUnit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WeightUnit), input_name='WeightUnit')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Weight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Weight')
            fval_ = self.gds_validate_decimal(fval_, node, 'Weight')
            self.Weight = fval_
            self.Weight_nsprefix_ = child_.prefix
            # validate type Weight
            self.validate_Weight(self.Weight)
        elif nodeName_ == 'WeightUnit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WeightUnit')
            value_ = self.gds_validate_string(value_, node, 'WeightUnit')
            self.WeightUnit = value_
            self.WeightUnit_nsprefix_ = child_.prefix
            # validate type WeightUnit
            self.validate_WeightUnit(self.WeightUnit)
# end class WeightSeg


class Request(GeneratedsSuper):
    """Generic request header"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ServiceHeader=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ServiceHeader = ServiceHeader
        self.ServiceHeader_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Request)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Request.subclass:
            return Request.subclass(*args_, **kwargs_)
        else:
            return Request(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ServiceHeader(self):
        return self.ServiceHeader
    def set_ServiceHeader(self, ServiceHeader):
        self.ServiceHeader = ServiceHeader
    def hasContent_(self):
        if (
            self.ServiceHeader is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Request', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Request')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Request':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Request')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Request', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Request'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Request', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ServiceHeader is not None:
            namespaceprefix_ = self.ServiceHeader_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceHeader_nsprefix_) else ''
            self.ServiceHeader.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ServiceHeader', pretty_print=pretty_print)
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
        if nodeName_ == 'ServiceHeader':
            obj_ = ServiceHeader.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ServiceHeader = obj_
            obj_.original_tagname_ = 'ServiceHeader'
# end class Request


class ServiceHeader(GeneratedsSuper):
    """Standard routing header"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, MessageTime=None, MessageReference=None, SiteID=None, Password=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if isinstance(MessageTime, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(MessageTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = MessageTime
        self.MessageTime = initvalue_
        self.MessageTime_nsprefix_ = None
        self.MessageReference = MessageReference
        self.validate_MessageReference(self.MessageReference)
        self.MessageReference_nsprefix_ = None
        self.SiteID = SiteID
        self.validate_SiteID(self.SiteID)
        self.SiteID_nsprefix_ = None
        self.Password = Password
        self.validate_Password(self.Password)
        self.Password_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ServiceHeader)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ServiceHeader.subclass:
            return ServiceHeader.subclass(*args_, **kwargs_)
        else:
            return ServiceHeader(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_MessageTime(self):
        return self.MessageTime
    def set_MessageTime(self, MessageTime):
        self.MessageTime = MessageTime
    def get_MessageReference(self):
        return self.MessageReference
    def set_MessageReference(self, MessageReference):
        self.MessageReference = MessageReference
    def get_SiteID(self):
        return self.SiteID
    def set_SiteID(self, SiteID):
        self.SiteID = SiteID
    def get_Password(self):
        return self.Password
    def set_Password(self, Password):
        self.Password = Password
    def validate_MessageReference(self, value):
        result = True
        # Validate type MessageReference, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 32:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on MessageReference' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 28:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on MessageReference' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_SiteID(self, value):
        result = True
        # Validate type SiteID, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on SiteID' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on SiteID' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_Password(self, value):
        result = True
        # Validate type Password, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on Password' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on Password' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.MessageTime is not None or
            self.MessageReference is not None or
            self.SiteID is not None or
            self.Password is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ServiceHeader', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ServiceHeader')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ServiceHeader':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ServiceHeader')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ServiceHeader', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ServiceHeader'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ServiceHeader', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.MessageTime is not None:
            namespaceprefix_ = self.MessageTime_nsprefix_ + ':' if (UseCapturedNS_ and self.MessageTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMessageTime>%s</%sMessageTime>%s' % (namespaceprefix_ , self.gds_format_datetime(self.MessageTime, input_name='MessageTime'), namespaceprefix_ , eol_))
        if self.MessageReference is not None:
            namespaceprefix_ = self.MessageReference_nsprefix_ + ':' if (UseCapturedNS_ and self.MessageReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMessageReference>%s</%sMessageReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MessageReference), input_name='MessageReference')), namespaceprefix_ , eol_))
        if self.SiteID is not None:
            namespaceprefix_ = self.SiteID_nsprefix_ + ':' if (UseCapturedNS_ and self.SiteID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSiteID>%s</%sSiteID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SiteID), input_name='SiteID')), namespaceprefix_ , eol_))
        if self.Password is not None:
            namespaceprefix_ = self.Password_nsprefix_ + ':' if (UseCapturedNS_ and self.Password_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPassword>%s</%sPassword>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Password), input_name='Password')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'MessageTime':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.MessageTime = dval_
            self.MessageTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'MessageReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MessageReference')
            value_ = self.gds_validate_string(value_, node, 'MessageReference')
            self.MessageReference = value_
            self.MessageReference_nsprefix_ = child_.prefix
            # validate type MessageReference
            self.validate_MessageReference(self.MessageReference)
        elif nodeName_ == 'SiteID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SiteID')
            value_ = self.gds_validate_string(value_, node, 'SiteID')
            self.SiteID = value_
            self.SiteID_nsprefix_ = child_.prefix
            # validate type SiteID
            self.validate_SiteID(self.SiteID)
        elif nodeName_ == 'Password':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Password')
            value_ = self.gds_validate_string(value_, node, 'Password')
            self.Password = value_
            self.Password_nsprefix_ = child_.prefix
            # validate type Password
            self.validate_Password(self.Password)
# end class ServiceHeader


class Response(GeneratedsSuper):
    """Generic response header"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ServiceHeader=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ServiceHeader = ServiceHeader
        self.ServiceHeader_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Response)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Response.subclass:
            return Response.subclass(*args_, **kwargs_)
        else:
            return Response(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ServiceHeader(self):
        return self.ServiceHeader
    def set_ServiceHeader(self, ServiceHeader):
        self.ServiceHeader = ServiceHeader
    def hasContent_(self):
        if (
            self.ServiceHeader is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Response', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Response')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Response':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Response')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Response', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Response'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Response', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ServiceHeader is not None:
            namespaceprefix_ = self.ServiceHeader_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceHeader_nsprefix_) else ''
            self.ServiceHeader.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ServiceHeader', pretty_print=pretty_print)
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
        if nodeName_ == 'ServiceHeader':
            obj_ = ResponseServiceHeader.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ServiceHeader = obj_
            obj_.original_tagname_ = 'ServiceHeader'
# end class Response


class ResponseServiceHeader(GeneratedsSuper):
    """Standard routing header"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, MessageTime=None, MessageReference=None, SiteID=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if isinstance(MessageTime, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(MessageTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = MessageTime
        self.MessageTime = initvalue_
        self.MessageTime_nsprefix_ = None
        self.MessageReference = MessageReference
        self.validate_MessageReference(self.MessageReference)
        self.MessageReference_nsprefix_ = None
        self.SiteID = SiteID
        self.validate_SiteID(self.SiteID)
        self.SiteID_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ResponseServiceHeader)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ResponseServiceHeader.subclass:
            return ResponseServiceHeader.subclass(*args_, **kwargs_)
        else:
            return ResponseServiceHeader(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_MessageTime(self):
        return self.MessageTime
    def set_MessageTime(self, MessageTime):
        self.MessageTime = MessageTime
    def get_MessageReference(self):
        return self.MessageReference
    def set_MessageReference(self, MessageReference):
        self.MessageReference = MessageReference
    def get_SiteID(self):
        return self.SiteID
    def set_SiteID(self, SiteID):
        self.SiteID = SiteID
    def validate_MessageReference(self, value):
        result = True
        # Validate type MessageReference, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 32:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on MessageReference' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 28:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on MessageReference' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_SiteID(self, value):
        result = True
        # Validate type SiteID, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on SiteID' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on SiteID' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.MessageTime is not None or
            self.MessageReference is not None or
            self.SiteID is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ResponseServiceHeader', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ResponseServiceHeader')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ResponseServiceHeader':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ResponseServiceHeader')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ResponseServiceHeader', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ResponseServiceHeader'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ResponseServiceHeader', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.MessageTime is not None:
            namespaceprefix_ = self.MessageTime_nsprefix_ + ':' if (UseCapturedNS_ and self.MessageTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMessageTime>%s</%sMessageTime>%s' % (namespaceprefix_ , self.gds_format_datetime(self.MessageTime, input_name='MessageTime'), namespaceprefix_ , eol_))
        if self.MessageReference is not None:
            namespaceprefix_ = self.MessageReference_nsprefix_ + ':' if (UseCapturedNS_ and self.MessageReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMessageReference>%s</%sMessageReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MessageReference), input_name='MessageReference')), namespaceprefix_ , eol_))
        if self.SiteID is not None:
            namespaceprefix_ = self.SiteID_nsprefix_ + ':' if (UseCapturedNS_ and self.SiteID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSiteID>%s</%sSiteID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SiteID), input_name='SiteID')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'MessageTime':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.MessageTime = dval_
            self.MessageTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'MessageReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MessageReference')
            value_ = self.gds_validate_string(value_, node, 'MessageReference')
            self.MessageReference = value_
            self.MessageReference_nsprefix_ = child_.prefix
            # validate type MessageReference
            self.validate_MessageReference(self.MessageReference)
        elif nodeName_ == 'SiteID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SiteID')
            value_ = self.gds_validate_string(value_, node, 'SiteID')
            self.SiteID = value_
            self.SiteID_nsprefix_ = child_.prefix
            # validate type SiteID
            self.validate_SiteID(self.SiteID)
# end class ResponseServiceHeader


class Status(GeneratedsSuper):
    """Status/Exception signal element"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ActionStatus=None, Condition=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ActionStatus = ActionStatus
        self.ActionStatus_nsprefix_ = None
        if Condition is None:
            self.Condition = []
        else:
            self.Condition = Condition
        self.Condition_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Status)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Status.subclass:
            return Status.subclass(*args_, **kwargs_)
        else:
            return Status(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ActionStatus(self):
        return self.ActionStatus
    def set_ActionStatus(self, ActionStatus):
        self.ActionStatus = ActionStatus
    def get_Condition(self):
        return self.Condition
    def set_Condition(self, Condition):
        self.Condition = Condition
    def add_Condition(self, value):
        self.Condition.append(value)
    def insert_Condition_at(self, index, value):
        self.Condition.insert(index, value)
    def replace_Condition_at(self, index, value):
        self.Condition[index] = value
    def hasContent_(self):
        if (
            self.ActionStatus is not None or
            self.Condition
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Status', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Status')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Status':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Status')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Status', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Status'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Status', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ActionStatus is not None:
            namespaceprefix_ = self.ActionStatus_nsprefix_ + ':' if (UseCapturedNS_ and self.ActionStatus_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sActionStatus>%s</%sActionStatus>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ActionStatus), input_name='ActionStatus')), namespaceprefix_ , eol_))
        for Condition_ in self.Condition:
            namespaceprefix_ = self.Condition_nsprefix_ + ':' if (UseCapturedNS_ and self.Condition_nsprefix_) else ''
            Condition_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Condition', pretty_print=pretty_print)
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
        if nodeName_ == 'ActionStatus':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ActionStatus')
            value_ = self.gds_validate_string(value_, node, 'ActionStatus')
            self.ActionStatus = value_
            self.ActionStatus_nsprefix_ = child_.prefix
        elif nodeName_ == 'Condition':
            obj_ = Condition.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Condition.append(obj_)
            obj_.original_tagname_ = 'Condition'
# end class Status


class Note(GeneratedsSuper):
    """Note/Warning"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ActionNote=None, Condition=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ActionNote = ActionNote
        self.ActionNote_nsprefix_ = None
        if Condition is None:
            self.Condition = []
        else:
            self.Condition = Condition
        self.Condition_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Note)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Note.subclass:
            return Note.subclass(*args_, **kwargs_)
        else:
            return Note(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ActionNote(self):
        return self.ActionNote
    def set_ActionNote(self, ActionNote):
        self.ActionNote = ActionNote
    def get_Condition(self):
        return self.Condition
    def set_Condition(self, Condition):
        self.Condition = Condition
    def add_Condition(self, value):
        self.Condition.append(value)
    def insert_Condition_at(self, index, value):
        self.Condition.insert(index, value)
    def replace_Condition_at(self, index, value):
        self.Condition[index] = value
    def hasContent_(self):
        if (
            self.ActionNote is not None or
            self.Condition
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Note', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Note')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Note':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Note')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Note', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Note'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Note', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ActionNote is not None:
            namespaceprefix_ = self.ActionNote_nsprefix_ + ':' if (UseCapturedNS_ and self.ActionNote_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sActionNote>%s</%sActionNote>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ActionNote), input_name='ActionNote')), namespaceprefix_ , eol_))
        for Condition_ in self.Condition:
            namespaceprefix_ = self.Condition_nsprefix_ + ':' if (UseCapturedNS_ and self.Condition_nsprefix_) else ''
            Condition_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Condition', pretty_print=pretty_print)
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
        if nodeName_ == 'ActionNote':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ActionNote')
            value_ = self.gds_validate_string(value_, node, 'ActionNote')
            self.ActionNote = value_
            self.ActionNote_nsprefix_ = child_.prefix
        elif nodeName_ == 'Condition':
            obj_ = Condition.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Condition.append(obj_)
            obj_.original_tagname_ = 'Condition'
# end class Note


class Condition(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ConditionCode=None, ConditionData=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ConditionCode = ConditionCode
        self.ConditionCode_nsprefix_ = None
        self.ConditionData = ConditionData
        self.ConditionData_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Condition)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Condition.subclass:
            return Condition.subclass(*args_, **kwargs_)
        else:
            return Condition(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ConditionCode(self):
        return self.ConditionCode
    def set_ConditionCode(self, ConditionCode):
        self.ConditionCode = ConditionCode
    def get_ConditionData(self):
        return self.ConditionData
    def set_ConditionData(self, ConditionData):
        self.ConditionData = ConditionData
    def hasContent_(self):
        if (
            self.ConditionCode is not None or
            self.ConditionData is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Condition', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Condition')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Condition':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Condition')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Condition', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Condition'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Condition', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ConditionCode is not None:
            namespaceprefix_ = self.ConditionCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ConditionCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sConditionCode>%s</%sConditionCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ConditionCode), input_name='ConditionCode')), namespaceprefix_ , eol_))
        if self.ConditionData is not None:
            namespaceprefix_ = self.ConditionData_nsprefix_ + ':' if (UseCapturedNS_ and self.ConditionData_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sConditionData>%s</%sConditionData>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ConditionData), input_name='ConditionData')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ConditionCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ConditionCode')
            value_ = self.gds_validate_string(value_, node, 'ConditionCode')
            self.ConditionCode = value_
            self.ConditionCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'ConditionData':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ConditionData')
            value_ = self.gds_validate_string(value_, node, 'ConditionData')
            self.ConditionData = value_
            self.ConditionData_nsprefix_ = child_.prefix
# end class Condition


class Customer(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CustomerID=None, Name=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CustomerID = CustomerID
        self.CustomerID_nsprefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Customer)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Customer.subclass:
            return Customer.subclass(*args_, **kwargs_)
        else:
            return Customer(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CustomerID(self):
        return self.CustomerID
    def set_CustomerID(self, CustomerID):
        self.CustomerID = CustomerID
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def hasContent_(self):
        if (
            self.CustomerID is not None or
            self.Name is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Customer', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Customer')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Customer':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Customer')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Customer', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Customer'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Customer', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CustomerID is not None:
            namespaceprefix_ = self.CustomerID_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomerID>%s</%sCustomerID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CustomerID), input_name='CustomerID')), namespaceprefix_ , eol_))
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'CustomerID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustomerID')
            value_ = self.gds_validate_string(value_, node, 'CustomerID')
            self.CustomerID = value_
            self.CustomerID_nsprefix_ = child_.prefix
        elif nodeName_ == 'Name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Name')
            value_ = self.gds_validate_string(value_, node, 'Name')
            self.Name = value_
            self.Name_nsprefix_ = child_.prefix
# end class Customer


class BarCodes(GeneratedsSuper):
    """Element containing BarCode data"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, BarCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if BarCode is None:
            self.BarCode = []
        else:
            self.BarCode = BarCode
        self.BarCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BarCodes)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BarCodes.subclass:
            return BarCodes.subclass(*args_, **kwargs_)
        else:
            return BarCodes(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_BarCode(self):
        return self.BarCode
    def set_BarCode(self, BarCode):
        self.BarCode = BarCode
    def add_BarCode(self, value):
        self.BarCode.append(value)
    def insert_BarCode_at(self, index, value):
        self.BarCode.insert(index, value)
    def replace_BarCode_at(self, index, value):
        self.BarCode[index] = value
    def validate_BarCode(self, value):
        result = True
        # Validate type BarCode, a restriction on xsd:base64Binary.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def hasContent_(self):
        if (
            self.BarCode
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BarCodes', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BarCodes')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BarCodes':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BarCodes')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='BarCodes', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BarCodes'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BarCodes', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for BarCode_ in self.BarCode:
            namespaceprefix_ = self.BarCode_nsprefix_ + ':' if (UseCapturedNS_ and self.BarCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBarCode>%s</%sBarCode>%s' % (namespaceprefix_ , self.gds_format_base64(BarCode_, input_name='BarCode'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'BarCode':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'BarCode')
            else:
                bval_ = None
            self.BarCode.append(bval_)
            self.BarCode_nsprefix_ = child_.prefix
            # validate type BarCode
            self.validate_BarCode(self.BarCode[-1])
# end class BarCodes


class DestinationServiceArea(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ServiceAreaCode=None, Description=None, FacilityCode=None, InboundSortCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ServiceAreaCode = ServiceAreaCode
        self.validate_ServiceAreaCode(self.ServiceAreaCode)
        self.ServiceAreaCode_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
        self.FacilityCode = FacilityCode
        self.validate_FacilityCode(self.FacilityCode)
        self.FacilityCode_nsprefix_ = None
        self.InboundSortCode = InboundSortCode
        self.validate_InboundSortCode(self.InboundSortCode)
        self.InboundSortCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DestinationServiceArea)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DestinationServiceArea.subclass:
            return DestinationServiceArea.subclass(*args_, **kwargs_)
        else:
            return DestinationServiceArea(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ServiceAreaCode(self):
        return self.ServiceAreaCode
    def set_ServiceAreaCode(self, ServiceAreaCode):
        self.ServiceAreaCode = ServiceAreaCode
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def get_FacilityCode(self):
        return self.FacilityCode
    def set_FacilityCode(self, FacilityCode):
        self.FacilityCode = FacilityCode
    def get_InboundSortCode(self):
        return self.InboundSortCode
    def set_InboundSortCode(self, InboundSortCode):
        self.InboundSortCode = InboundSortCode
    def validate_ServiceAreaCode(self, value):
        result = True
        # Validate type ServiceAreaCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on ServiceAreaCode' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_FacilityCode(self, value):
        result = True
        # Validate type FacilityCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on FacilityCode' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_InboundSortCode(self, value):
        result = True
        # Validate type InboundSortCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on InboundSortCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on InboundSortCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.ServiceAreaCode is not None or
            self.Description is not None or
            self.FacilityCode is not None or
            self.InboundSortCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DestinationServiceArea', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DestinationServiceArea')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DestinationServiceArea':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DestinationServiceArea')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DestinationServiceArea', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DestinationServiceArea'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DestinationServiceArea', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ServiceAreaCode is not None:
            namespaceprefix_ = self.ServiceAreaCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceAreaCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceAreaCode>%s</%sServiceAreaCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceAreaCode), input_name='ServiceAreaCode')), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
        if self.FacilityCode is not None:
            namespaceprefix_ = self.FacilityCode_nsprefix_ + ':' if (UseCapturedNS_ and self.FacilityCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFacilityCode>%s</%sFacilityCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FacilityCode), input_name='FacilityCode')), namespaceprefix_ , eol_))
        if self.InboundSortCode is not None:
            namespaceprefix_ = self.InboundSortCode_nsprefix_ + ':' if (UseCapturedNS_ and self.InboundSortCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInboundSortCode>%s</%sInboundSortCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.InboundSortCode), input_name='InboundSortCode')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ServiceAreaCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceAreaCode')
            value_ = self.gds_validate_string(value_, node, 'ServiceAreaCode')
            self.ServiceAreaCode = value_
            self.ServiceAreaCode_nsprefix_ = child_.prefix
            # validate type ServiceAreaCode
            self.validate_ServiceAreaCode(self.ServiceAreaCode)
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
        elif nodeName_ == 'FacilityCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FacilityCode')
            value_ = self.gds_validate_string(value_, node, 'FacilityCode')
            self.FacilityCode = value_
            self.FacilityCode_nsprefix_ = child_.prefix
            # validate type FacilityCode
            self.validate_FacilityCode(self.FacilityCode)
        elif nodeName_ == 'InboundSortCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'InboundSortCode')
            value_ = self.gds_validate_string(value_, node, 'InboundSortCode')
            self.InboundSortCode = value_
            self.InboundSortCode_nsprefix_ = child_.prefix
            # validate type InboundSortCode
            self.validate_InboundSortCode(self.InboundSortCode)
# end class DestinationServiceArea


class OriginServiceArea(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ServiceAreaCode=None, Description=None, OutboundSortCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ServiceAreaCode = ServiceAreaCode
        self.validate_ServiceAreaCode(self.ServiceAreaCode)
        self.ServiceAreaCode_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
        self.OutboundSortCode = OutboundSortCode
        self.validate_OutboundSortCode(self.OutboundSortCode)
        self.OutboundSortCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, OriginServiceArea)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OriginServiceArea.subclass:
            return OriginServiceArea.subclass(*args_, **kwargs_)
        else:
            return OriginServiceArea(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ServiceAreaCode(self):
        return self.ServiceAreaCode
    def set_ServiceAreaCode(self, ServiceAreaCode):
        self.ServiceAreaCode = ServiceAreaCode
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def get_OutboundSortCode(self):
        return self.OutboundSortCode
    def set_OutboundSortCode(self, OutboundSortCode):
        self.OutboundSortCode = OutboundSortCode
    def validate_ServiceAreaCode(self, value):
        result = True
        # Validate type ServiceAreaCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on ServiceAreaCode' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_OutboundSortCode(self, value):
        result = True
        # Validate type OutboundSortCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on OutboundSortCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on OutboundSortCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.ServiceAreaCode is not None or
            self.Description is not None or
            self.OutboundSortCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OriginServiceArea', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OriginServiceArea')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OriginServiceArea':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OriginServiceArea')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='OriginServiceArea', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OriginServiceArea'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OriginServiceArea', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ServiceAreaCode is not None:
            namespaceprefix_ = self.ServiceAreaCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceAreaCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceAreaCode>%s</%sServiceAreaCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceAreaCode), input_name='ServiceAreaCode')), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
        if self.OutboundSortCode is not None:
            namespaceprefix_ = self.OutboundSortCode_nsprefix_ + ':' if (UseCapturedNS_ and self.OutboundSortCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOutboundSortCode>%s</%sOutboundSortCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OutboundSortCode), input_name='OutboundSortCode')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ServiceAreaCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceAreaCode')
            value_ = self.gds_validate_string(value_, node, 'ServiceAreaCode')
            self.ServiceAreaCode = value_
            self.ServiceAreaCode_nsprefix_ = child_.prefix
            # validate type ServiceAreaCode
            self.validate_ServiceAreaCode(self.ServiceAreaCode)
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
        elif nodeName_ == 'OutboundSortCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OutboundSortCode')
            value_ = self.gds_validate_string(value_, node, 'OutboundSortCode')
            self.OutboundSortCode = value_
            self.OutboundSortCode_nsprefix_ = child_.prefix
            # validate type OutboundSortCode
            self.validate_OutboundSortCode(self.OutboundSortCode)
# end class OriginServiceArea


class ServiceArea(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ServiceAreaCode=None, Description=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ServiceAreaCode = ServiceAreaCode
        self.validate_ServiceAreaCode(self.ServiceAreaCode)
        self.ServiceAreaCode_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ServiceArea)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ServiceArea.subclass:
            return ServiceArea.subclass(*args_, **kwargs_)
        else:
            return ServiceArea(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ServiceAreaCode(self):
        return self.ServiceAreaCode
    def set_ServiceAreaCode(self, ServiceAreaCode):
        self.ServiceAreaCode = ServiceAreaCode
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def validate_ServiceAreaCode(self, value):
        result = True
        # Validate type ServiceAreaCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on ServiceAreaCode' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.ServiceAreaCode is not None or
            self.Description is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ServiceArea', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ServiceArea')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ServiceArea':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ServiceArea')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ServiceArea', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ServiceArea'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ServiceArea', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ServiceAreaCode is not None:
            namespaceprefix_ = self.ServiceAreaCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceAreaCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceAreaCode>%s</%sServiceAreaCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceAreaCode), input_name='ServiceAreaCode')), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ServiceAreaCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceAreaCode')
            value_ = self.gds_validate_string(value_, node, 'ServiceAreaCode')
            self.ServiceAreaCode = value_
            self.ServiceAreaCode_nsprefix_ = child_.prefix
            # validate type ServiceAreaCode
            self.validate_ServiceAreaCode(self.ServiceAreaCode)
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
# end class ServiceArea


class ServiceEvent(GeneratedsSuper):
    """Complex type to describe a service event. Eg Pickup, Delivery"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, EventCode=None, Description=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.EventCode = EventCode
        self.validate_EventCodeType(self.EventCode)
        self.EventCode_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ServiceEvent)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ServiceEvent.subclass:
            return ServiceEvent.subclass(*args_, **kwargs_)
        else:
            return ServiceEvent(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_EventCode(self):
        return self.EventCode
    def set_EventCode(self, EventCode):
        self.EventCode = EventCode
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def validate_EventCodeType(self, value):
        result = True
        # Validate type EventCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on EventCodeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.EventCode is not None or
            self.Description is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ServiceEvent', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ServiceEvent')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ServiceEvent':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ServiceEvent')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ServiceEvent', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ServiceEvent'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ServiceEvent', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.EventCode is not None:
            namespaceprefix_ = self.EventCode_nsprefix_ + ':' if (UseCapturedNS_ and self.EventCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEventCode>%s</%sEventCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EventCode), input_name='EventCode')), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'EventCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EventCode')
            value_ = self.gds_validate_string(value_, node, 'EventCode')
            self.EventCode = value_
            self.EventCode_nsprefix_ = child_.prefix
            # validate type EventCodeType
            self.validate_EventCodeType(self.EventCode)
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
# end class ServiceEvent


class ShipmentDate(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ShipmentDateFrom=None, ShipmentDateTo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if isinstance(ShipmentDateFrom, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ShipmentDateFrom, '%Y-%m-%d').date()
        else:
            initvalue_ = ShipmentDateFrom
        self.ShipmentDateFrom = initvalue_
        self.ShipmentDateFrom_nsprefix_ = None
        if isinstance(ShipmentDateTo, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ShipmentDateTo, '%Y-%m-%d').date()
        else:
            initvalue_ = ShipmentDateTo
        self.ShipmentDateTo = initvalue_
        self.ShipmentDateTo_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentDate)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentDate.subclass:
            return ShipmentDate.subclass(*args_, **kwargs_)
        else:
            return ShipmentDate(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ShipmentDateFrom(self):
        return self.ShipmentDateFrom
    def set_ShipmentDateFrom(self, ShipmentDateFrom):
        self.ShipmentDateFrom = ShipmentDateFrom
    def get_ShipmentDateTo(self):
        return self.ShipmentDateTo
    def set_ShipmentDateTo(self, ShipmentDateTo):
        self.ShipmentDateTo = ShipmentDateTo
    def validate_Date(self, value):
        result = True
        # Validate type Date, a restriction on xsd:date.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.date):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.date)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def hasContent_(self):
        if (
            self.ShipmentDateFrom is not None or
            self.ShipmentDateTo is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDate', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentDate')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentDate':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentDate')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentDate', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentDate'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDate', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ShipmentDateFrom is not None:
            namespaceprefix_ = self.ShipmentDateFrom_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentDateFrom_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipmentDateFrom>%s</%sShipmentDateFrom>%s' % (namespaceprefix_ , self.gds_format_date(self.ShipmentDateFrom, input_name='ShipmentDateFrom'), namespaceprefix_ , eol_))
        if self.ShipmentDateTo is not None:
            namespaceprefix_ = self.ShipmentDateTo_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentDateTo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipmentDateTo>%s</%sShipmentDateTo>%s' % (namespaceprefix_ , self.gds_format_date(self.ShipmentDateTo, input_name='ShipmentDateTo'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ShipmentDateFrom':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.ShipmentDateFrom = dval_
            self.ShipmentDateFrom_nsprefix_ = child_.prefix
            # validate type Date
            self.validate_Date(self.ShipmentDateFrom)
        elif nodeName_ == 'ShipmentDateTo':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.ShipmentDateTo = dval_
            self.ShipmentDateTo_nsprefix_ = child_.prefix
            # validate type Date
            self.validate_Date(self.ShipmentDateTo)
# end class ShipmentDate


class AWBInfo(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AWBNumber=None, TrackedBy=None, Status=None, ShipmentInfo=None, Pieces=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.AWBNumber = AWBNumber
        self.validate_AWBNumber(self.AWBNumber)
        self.AWBNumber_nsprefix_ = None
        self.TrackedBy = TrackedBy
        self.TrackedBy_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
        self.ShipmentInfo = ShipmentInfo
        self.ShipmentInfo_nsprefix_ = None
        self.Pieces = Pieces
        self.Pieces_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AWBInfo)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AWBInfo.subclass:
            return AWBInfo.subclass(*args_, **kwargs_)
        else:
            return AWBInfo(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AWBNumber(self):
        return self.AWBNumber
    def set_AWBNumber(self, AWBNumber):
        self.AWBNumber = AWBNumber
    def get_TrackedBy(self):
        return self.TrackedBy
    def set_TrackedBy(self, TrackedBy):
        self.TrackedBy = TrackedBy
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def get_ShipmentInfo(self):
        return self.ShipmentInfo
    def set_ShipmentInfo(self, ShipmentInfo):
        self.ShipmentInfo = ShipmentInfo
    def get_Pieces(self):
        return self.Pieces
    def set_Pieces(self, Pieces):
        self.Pieces = Pieces
    def validate_AWBNumber(self, value):
        result = True
        # Validate type AWBNumber, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 11:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on AWBNumber' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.AWBNumber is not None or
            self.TrackedBy is not None or
            self.Status is not None or
            self.ShipmentInfo is not None or
            self.Pieces is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AWBInfo', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AWBInfo')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AWBInfo':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AWBInfo')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AWBInfo', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AWBInfo'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AWBInfo', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.AWBNumber is not None:
            namespaceprefix_ = self.AWBNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.AWBNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAWBNumber>%s</%sAWBNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AWBNumber), input_name='AWBNumber')), namespaceprefix_ , eol_))
        if self.TrackedBy is not None:
            namespaceprefix_ = self.TrackedBy_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackedBy_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTrackedBy>%s</%sTrackedBy>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TrackedBy), input_name='TrackedBy')), namespaceprefix_ , eol_))
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
        if self.ShipmentInfo is not None:
            namespaceprefix_ = self.ShipmentInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentInfo_nsprefix_) else ''
            self.ShipmentInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentInfo', pretty_print=pretty_print)
        if self.Pieces is not None:
            namespaceprefix_ = self.Pieces_nsprefix_ + ':' if (UseCapturedNS_ and self.Pieces_nsprefix_) else ''
            self.Pieces.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Pieces', pretty_print=pretty_print)
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
        if nodeName_ == 'AWBNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AWBNumber')
            value_ = self.gds_validate_string(value_, node, 'AWBNumber')
            self.AWBNumber = value_
            self.AWBNumber_nsprefix_ = child_.prefix
            # validate type AWBNumber
            self.validate_AWBNumber(self.AWBNumber)
        elif nodeName_ == 'TrackedBy':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TrackedBy')
            value_ = self.gds_validate_string(value_, node, 'TrackedBy')
            self.TrackedBy = value_
            self.TrackedBy_nsprefix_ = child_.prefix
        elif nodeName_ == 'Status':
            obj_ = Status.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
        elif nodeName_ == 'ShipmentInfo':
            obj_ = ShipmentInfo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentInfo = obj_
            obj_.original_tagname_ = 'ShipmentInfo'
        elif nodeName_ == 'Pieces':
            obj_ = TrackingPieces.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Pieces = obj_
            obj_.original_tagname_ = 'Pieces'
# end class AWBInfo


class TrackedBy(GeneratedsSuper):
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
                CurrentSubclassModule_, TrackedBy)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TrackedBy.subclass:
            return TrackedBy.subclass(*args_, **kwargs_)
        else:
            return TrackedBy(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackedBy', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TrackedBy')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TrackedBy':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TrackedBy')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TrackedBy', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TrackedBy'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackedBy', fromsubclass_=False, pretty_print=True):
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
# end class TrackedBy


class ShipmentInfo(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, OriginServiceArea=None, DestinationServiceArea=None, ShipperName=None, ShipperAccountNumber=None, ConsigneeName=None, ShipmentDate=None, Pieces=None, Weight=None, WeightUnit=None, EstDlvyDate=None, EstDlvyDateUTC=None, GlobalProductCode=None, ShipmentDesc=None, DlvyNotificationFlag=None, Shipper=None, Consignee=None, ShipmentEvent=None, ShipperReference=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.OriginServiceArea = OriginServiceArea
        self.OriginServiceArea_nsprefix_ = None
        self.DestinationServiceArea = DestinationServiceArea
        self.DestinationServiceArea_nsprefix_ = None
        self.ShipperName = ShipperName
        self.validate_TrackRespPersonName(self.ShipperName)
        self.ShipperName_nsprefix_ = None
        self.ShipperAccountNumber = ShipperAccountNumber
        self.validate_AccountNumber(self.ShipperAccountNumber)
        self.ShipperAccountNumber_nsprefix_ = None
        self.ConsigneeName = ConsigneeName
        self.validate_TrackRespPersonName(self.ConsigneeName)
        self.ConsigneeName_nsprefix_ = None
        if isinstance(ShipmentDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ShipmentDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = ShipmentDate
        self.ShipmentDate = initvalue_
        self.ShipmentDate_nsprefix_ = None
        self.Pieces = Pieces
        self.Pieces_nsprefix_ = None
        self.Weight = Weight
        self.Weight_nsprefix_ = None
        self.WeightUnit = WeightUnit
        self.validate_WeightUnitType(self.WeightUnit)
        self.WeightUnit_nsprefix_ = None
        if isinstance(EstDlvyDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(EstDlvyDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = EstDlvyDate
        self.EstDlvyDate = initvalue_
        self.EstDlvyDate_nsprefix_ = None
        if isinstance(EstDlvyDateUTC, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(EstDlvyDateUTC, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = EstDlvyDateUTC
        self.EstDlvyDateUTC = initvalue_
        self.EstDlvyDateUTC_nsprefix_ = None
        self.GlobalProductCode = GlobalProductCode
        self.validate_GlobalProductCode(self.GlobalProductCode)
        self.GlobalProductCode_nsprefix_ = None
        self.ShipmentDesc = ShipmentDesc
        self.ShipmentDesc_nsprefix_ = None
        self.DlvyNotificationFlag = DlvyNotificationFlag
        self.validate_DlvyNotificationFlagType(self.DlvyNotificationFlag)
        self.DlvyNotificationFlag_nsprefix_ = None
        self.Shipper = Shipper
        self.Shipper_nsprefix_ = None
        self.Consignee = Consignee
        self.Consignee_nsprefix_ = None
        if ShipmentEvent is None:
            self.ShipmentEvent = []
        else:
            self.ShipmentEvent = ShipmentEvent
        self.ShipmentEvent_nsprefix_ = None
        self.ShipperReference = ShipperReference
        self.ShipperReference_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentInfo)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentInfo.subclass:
            return ShipmentInfo.subclass(*args_, **kwargs_)
        else:
            return ShipmentInfo(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_OriginServiceArea(self):
        return self.OriginServiceArea
    def set_OriginServiceArea(self, OriginServiceArea):
        self.OriginServiceArea = OriginServiceArea
    def get_DestinationServiceArea(self):
        return self.DestinationServiceArea
    def set_DestinationServiceArea(self, DestinationServiceArea):
        self.DestinationServiceArea = DestinationServiceArea
    def get_ShipperName(self):
        return self.ShipperName
    def set_ShipperName(self, ShipperName):
        self.ShipperName = ShipperName
    def get_ShipperAccountNumber(self):
        return self.ShipperAccountNumber
    def set_ShipperAccountNumber(self, ShipperAccountNumber):
        self.ShipperAccountNumber = ShipperAccountNumber
    def get_ConsigneeName(self):
        return self.ConsigneeName
    def set_ConsigneeName(self, ConsigneeName):
        self.ConsigneeName = ConsigneeName
    def get_ShipmentDate(self):
        return self.ShipmentDate
    def set_ShipmentDate(self, ShipmentDate):
        self.ShipmentDate = ShipmentDate
    def get_Pieces(self):
        return self.Pieces
    def set_Pieces(self, Pieces):
        self.Pieces = Pieces
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def get_WeightUnit(self):
        return self.WeightUnit
    def set_WeightUnit(self, WeightUnit):
        self.WeightUnit = WeightUnit
    def get_EstDlvyDate(self):
        return self.EstDlvyDate
    def set_EstDlvyDate(self, EstDlvyDate):
        self.EstDlvyDate = EstDlvyDate
    def get_EstDlvyDateUTC(self):
        return self.EstDlvyDateUTC
    def set_EstDlvyDateUTC(self, EstDlvyDateUTC):
        self.EstDlvyDateUTC = EstDlvyDateUTC
    def get_GlobalProductCode(self):
        return self.GlobalProductCode
    def set_GlobalProductCode(self, GlobalProductCode):
        self.GlobalProductCode = GlobalProductCode
    def get_ShipmentDesc(self):
        return self.ShipmentDesc
    def set_ShipmentDesc(self, ShipmentDesc):
        self.ShipmentDesc = ShipmentDesc
    def get_DlvyNotificationFlag(self):
        return self.DlvyNotificationFlag
    def set_DlvyNotificationFlag(self, DlvyNotificationFlag):
        self.DlvyNotificationFlag = DlvyNotificationFlag
    def get_Shipper(self):
        return self.Shipper
    def set_Shipper(self, Shipper):
        self.Shipper = Shipper
    def get_Consignee(self):
        return self.Consignee
    def set_Consignee(self, Consignee):
        self.Consignee = Consignee
    def get_ShipmentEvent(self):
        return self.ShipmentEvent
    def set_ShipmentEvent(self, ShipmentEvent):
        self.ShipmentEvent = ShipmentEvent
    def add_ShipmentEvent(self, value):
        self.ShipmentEvent.append(value)
    def insert_ShipmentEvent_at(self, index, value):
        self.ShipmentEvent.insert(index, value)
    def replace_ShipmentEvent_at(self, index, value):
        self.ShipmentEvent[index] = value
    def get_ShipperReference(self):
        return self.ShipperReference
    def set_ShipperReference(self, ShipperReference):
        self.ShipperReference = ShipperReference
    def validate_TrackRespPersonName(self, value):
        result = True
        # Validate type TrackRespPersonName, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 45:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on TrackRespPersonName' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_AccountNumber(self, value):
        result = True
        # Validate type AccountNumber, a restriction on xsd:positiveInteger.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 100000000:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on AccountNumber' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999999999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on AccountNumber' % {"value": value, "lineno": lineno} )
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
            enumerations = ['L', 'K', 'G']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on WeightUnitType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_GlobalProductCode(self, value):
        result = True
        # Validate type GlobalProductCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on GlobalProductCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on GlobalProductCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DlvyNotificationFlagType(self, value):
        result = True
        # Validate type DlvyNotificationFlagType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['Y', 'N']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DlvyNotificationFlagType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on DlvyNotificationFlagType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.OriginServiceArea is not None or
            self.DestinationServiceArea is not None or
            self.ShipperName is not None or
            self.ShipperAccountNumber is not None or
            self.ConsigneeName is not None or
            self.ShipmentDate is not None or
            self.Pieces is not None or
            self.Weight is not None or
            self.WeightUnit is not None or
            self.EstDlvyDate is not None or
            self.EstDlvyDateUTC is not None or
            self.GlobalProductCode is not None or
            self.ShipmentDesc is not None or
            self.DlvyNotificationFlag is not None or
            self.Shipper is not None or
            self.Consignee is not None or
            self.ShipmentEvent or
            self.ShipperReference is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentInfo', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentInfo')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentInfo':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentInfo')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentInfo', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentInfo'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentInfo', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.OriginServiceArea is not None:
            namespaceprefix_ = self.OriginServiceArea_nsprefix_ + ':' if (UseCapturedNS_ and self.OriginServiceArea_nsprefix_) else ''
            self.OriginServiceArea.export(outfile, level, namespaceprefix_, namespacedef_='', name_='OriginServiceArea', pretty_print=pretty_print)
        if self.DestinationServiceArea is not None:
            namespaceprefix_ = self.DestinationServiceArea_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationServiceArea_nsprefix_) else ''
            self.DestinationServiceArea.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DestinationServiceArea', pretty_print=pretty_print)
        if self.ShipperName is not None:
            namespaceprefix_ = self.ShipperName_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipperName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipperName>%s</%sShipperName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShipperName), input_name='ShipperName')), namespaceprefix_ , eol_))
        if self.ShipperAccountNumber is not None:
            namespaceprefix_ = self.ShipperAccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipperAccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipperAccountNumber>%s</%sShipperAccountNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.ShipperAccountNumber, input_name='ShipperAccountNumber'), namespaceprefix_ , eol_))
        if self.ConsigneeName is not None:
            namespaceprefix_ = self.ConsigneeName_nsprefix_ + ':' if (UseCapturedNS_ and self.ConsigneeName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sConsigneeName>%s</%sConsigneeName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ConsigneeName), input_name='ConsigneeName')), namespaceprefix_ , eol_))
        if self.ShipmentDate is not None:
            namespaceprefix_ = self.ShipmentDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipmentDate>%s</%sShipmentDate>%s' % (namespaceprefix_ , self.gds_format_datetime(self.ShipmentDate, input_name='ShipmentDate'), namespaceprefix_ , eol_))
        if self.Pieces is not None:
            namespaceprefix_ = self.Pieces_nsprefix_ + ':' if (UseCapturedNS_ and self.Pieces_nsprefix_) else ''
            self.Pieces.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Pieces', pretty_print=pretty_print)
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeight>%s</%sWeight>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Weight), input_name='Weight')), namespaceprefix_ , eol_))
        if self.WeightUnit is not None:
            namespaceprefix_ = self.WeightUnit_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightUnit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeightUnit>%s</%sWeightUnit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WeightUnit), input_name='WeightUnit')), namespaceprefix_ , eol_))
        if self.EstDlvyDate is not None:
            namespaceprefix_ = self.EstDlvyDate_nsprefix_ + ':' if (UseCapturedNS_ and self.EstDlvyDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEstDlvyDate>%s</%sEstDlvyDate>%s' % (namespaceprefix_ , self.gds_format_datetime(self.EstDlvyDate, input_name='EstDlvyDate'), namespaceprefix_ , eol_))
        if self.EstDlvyDateUTC is not None:
            namespaceprefix_ = self.EstDlvyDateUTC_nsprefix_ + ':' if (UseCapturedNS_ and self.EstDlvyDateUTC_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEstDlvyDateUTC>%s</%sEstDlvyDateUTC>%s' % (namespaceprefix_ , self.gds_format_datetime(self.EstDlvyDateUTC, input_name='EstDlvyDateUTC'), namespaceprefix_ , eol_))
        if self.GlobalProductCode is not None:
            namespaceprefix_ = self.GlobalProductCode_nsprefix_ + ':' if (UseCapturedNS_ and self.GlobalProductCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGlobalProductCode>%s</%sGlobalProductCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GlobalProductCode), input_name='GlobalProductCode')), namespaceprefix_ , eol_))
        if self.ShipmentDesc is not None:
            namespaceprefix_ = self.ShipmentDesc_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentDesc_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipmentDesc>%s</%sShipmentDesc>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShipmentDesc), input_name='ShipmentDesc')), namespaceprefix_ , eol_))
        if self.DlvyNotificationFlag is not None:
            namespaceprefix_ = self.DlvyNotificationFlag_nsprefix_ + ':' if (UseCapturedNS_ and self.DlvyNotificationFlag_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDlvyNotificationFlag>%s</%sDlvyNotificationFlag>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DlvyNotificationFlag), input_name='DlvyNotificationFlag')), namespaceprefix_ , eol_))
        if self.Shipper is not None:
            namespaceprefix_ = self.Shipper_nsprefix_ + ':' if (UseCapturedNS_ and self.Shipper_nsprefix_) else ''
            self.Shipper.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Shipper', pretty_print=pretty_print)
        if self.Consignee is not None:
            namespaceprefix_ = self.Consignee_nsprefix_ + ':' if (UseCapturedNS_ and self.Consignee_nsprefix_) else ''
            self.Consignee.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Consignee', pretty_print=pretty_print)
        for ShipmentEvent_ in self.ShipmentEvent:
            namespaceprefix_ = self.ShipmentEvent_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentEvent_nsprefix_) else ''
            ShipmentEvent_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentEvent', pretty_print=pretty_print)
        if self.ShipperReference is not None:
            namespaceprefix_ = self.ShipperReference_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipperReference_nsprefix_) else ''
            self.ShipperReference.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipperReference', pretty_print=pretty_print)
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
        if nodeName_ == 'OriginServiceArea':
            obj_ = OriginServiceArea.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.OriginServiceArea = obj_
            obj_.original_tagname_ = 'OriginServiceArea'
        elif nodeName_ == 'DestinationServiceArea':
            obj_ = DestinationServiceArea.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DestinationServiceArea = obj_
            obj_.original_tagname_ = 'DestinationServiceArea'
        elif nodeName_ == 'ShipperName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipperName')
            value_ = self.gds_validate_string(value_, node, 'ShipperName')
            self.ShipperName = value_
            self.ShipperName_nsprefix_ = child_.prefix
            # validate type TrackRespPersonName
            self.validate_TrackRespPersonName(self.ShipperName)
        elif nodeName_ == 'ShipperAccountNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'ShipperAccountNumber')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'ShipperAccountNumber')
            self.ShipperAccountNumber = ival_
            self.ShipperAccountNumber_nsprefix_ = child_.prefix
            # validate type AccountNumber
            self.validate_AccountNumber(self.ShipperAccountNumber)
        elif nodeName_ == 'ConsigneeName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ConsigneeName')
            value_ = self.gds_validate_string(value_, node, 'ConsigneeName')
            self.ConsigneeName = value_
            self.ConsigneeName_nsprefix_ = child_.prefix
            # validate type TrackRespPersonName
            self.validate_TrackRespPersonName(self.ConsigneeName)
        elif nodeName_ == 'ShipmentDate':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.ShipmentDate = dval_
            self.ShipmentDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'Pieces':
            obj_ = Pieces.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Pieces = obj_
            obj_.original_tagname_ = 'Pieces'
        elif nodeName_ == 'Weight':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Weight')
            value_ = self.gds_validate_string(value_, node, 'Weight')
            self.Weight = value_
            self.Weight_nsprefix_ = child_.prefix
        elif nodeName_ == 'WeightUnit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WeightUnit')
            value_ = self.gds_validate_string(value_, node, 'WeightUnit')
            self.WeightUnit = value_
            self.WeightUnit_nsprefix_ = child_.prefix
            # validate type WeightUnitType
            self.validate_WeightUnitType(self.WeightUnit)
        elif nodeName_ == 'EstDlvyDate':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.EstDlvyDate = dval_
            self.EstDlvyDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'EstDlvyDateUTC':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.EstDlvyDateUTC = dval_
            self.EstDlvyDateUTC_nsprefix_ = child_.prefix
        elif nodeName_ == 'GlobalProductCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GlobalProductCode')
            value_ = self.gds_validate_string(value_, node, 'GlobalProductCode')
            self.GlobalProductCode = value_
            self.GlobalProductCode_nsprefix_ = child_.prefix
            # validate type GlobalProductCode
            self.validate_GlobalProductCode(self.GlobalProductCode)
        elif nodeName_ == 'ShipmentDesc':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipmentDesc')
            value_ = self.gds_validate_string(value_, node, 'ShipmentDesc')
            self.ShipmentDesc = value_
            self.ShipmentDesc_nsprefix_ = child_.prefix
        elif nodeName_ == 'DlvyNotificationFlag':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DlvyNotificationFlag')
            value_ = self.gds_validate_string(value_, node, 'DlvyNotificationFlag')
            self.DlvyNotificationFlag = value_
            self.DlvyNotificationFlag_nsprefix_ = child_.prefix
            # validate type DlvyNotificationFlagType
            self.validate_DlvyNotificationFlagType(self.DlvyNotificationFlag)
        elif nodeName_ == 'Shipper':
            obj_ = Shipper.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Shipper = obj_
            obj_.original_tagname_ = 'Shipper'
        elif nodeName_ == 'Consignee':
            obj_ = Consignee.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Consignee = obj_
            obj_.original_tagname_ = 'Consignee'
        elif nodeName_ == 'ShipmentEvent':
            obj_ = ShipmentEvent.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentEvent.append(obj_)
            obj_.original_tagname_ = 'ShipmentEvent'
        elif nodeName_ == 'ShipperReference':
            obj_ = Reference.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipperReference = obj_
            obj_.original_tagname_ = 'ShipperReference'
# end class ShipmentInfo


class ErrorResponse(GeneratedsSuper):
    """Generic response header"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ServiceHeader=None, Status=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ServiceHeader = ServiceHeader
        self.ServiceHeader_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ErrorResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ErrorResponse.subclass:
            return ErrorResponse.subclass(*args_, **kwargs_)
        else:
            return ErrorResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ServiceHeader(self):
        return self.ServiceHeader
    def set_ServiceHeader(self, ServiceHeader):
        self.ServiceHeader = ServiceHeader
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def hasContent_(self):
        if (
            self.ServiceHeader is not None or
            self.Status is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ErrorResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ErrorResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ErrorResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ErrorResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ErrorResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ErrorResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ErrorResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ServiceHeader is not None:
            namespaceprefix_ = self.ServiceHeader_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceHeader_nsprefix_) else ''
            self.ServiceHeader.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ServiceHeader', pretty_print=pretty_print)
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
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
        if nodeName_ == 'ServiceHeader':
            obj_ = ServiceHeader.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ServiceHeader = obj_
            obj_.original_tagname_ = 'ServiceHeader'
        elif nodeName_ == 'Status':
            obj_ = Status.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
# end class ErrorResponse


class ShipmentEvent(GeneratedsSuper):
    """Describes the checkpoint information"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Date=None, Time=None, ServiceEvent=None, Signatory=None, EventRemarks=None, ServiceArea=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if isinstance(Date, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Date, '%Y-%m-%d').date()
        else:
            initvalue_ = Date
        self.Date = initvalue_
        self.Date_nsprefix_ = None
        if isinstance(Time, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Time, '%H:%M:%S').time()
        else:
            initvalue_ = Time
        self.Time = initvalue_
        self.Time_nsprefix_ = None
        self.ServiceEvent = ServiceEvent
        self.ServiceEvent_nsprefix_ = None
        self.Signatory = Signatory
        self.validate_SignatoryType(self.Signatory)
        self.Signatory_nsprefix_ = None
        self.EventRemarks = EventRemarks
        self.EventRemarks_nsprefix_ = None
        self.ServiceArea = ServiceArea
        self.ServiceArea_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentEvent)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentEvent.subclass:
            return ShipmentEvent.subclass(*args_, **kwargs_)
        else:
            return ShipmentEvent(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Date(self):
        return self.Date
    def set_Date(self, Date):
        self.Date = Date
    def get_Time(self):
        return self.Time
    def set_Time(self, Time):
        self.Time = Time
    def get_ServiceEvent(self):
        return self.ServiceEvent
    def set_ServiceEvent(self, ServiceEvent):
        self.ServiceEvent = ServiceEvent
    def get_Signatory(self):
        return self.Signatory
    def set_Signatory(self, Signatory):
        self.Signatory = Signatory
    def get_EventRemarks(self):
        return self.EventRemarks
    def set_EventRemarks(self, EventRemarks):
        self.EventRemarks = EventRemarks
    def get_ServiceArea(self):
        return self.ServiceArea
    def set_ServiceArea(self, ServiceArea):
        self.ServiceArea = ServiceArea
    def validate_SignatoryType(self, value):
        result = True
        # Validate type SignatoryType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def hasContent_(self):
        if (
            self.Date is not None or
            self.Time is not None or
            self.ServiceEvent is not None or
            self.Signatory is not None or
            self.EventRemarks is not None or
            self.ServiceArea is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentEvent', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentEvent')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentEvent':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentEvent')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentEvent', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentEvent'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentEvent', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Date is not None:
            namespaceprefix_ = self.Date_nsprefix_ + ':' if (UseCapturedNS_ and self.Date_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDate>%s</%sDate>%s' % (namespaceprefix_ , self.gds_format_date(self.Date, input_name='Date'), namespaceprefix_ , eol_))
        if self.Time is not None:
            namespaceprefix_ = self.Time_nsprefix_ + ':' if (UseCapturedNS_ and self.Time_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTime>%s</%sTime>%s' % (namespaceprefix_ , self.gds_format_time(self.Time, input_name='Time'), namespaceprefix_ , eol_))
        if self.ServiceEvent is not None:
            namespaceprefix_ = self.ServiceEvent_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceEvent_nsprefix_) else ''
            self.ServiceEvent.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ServiceEvent', pretty_print=pretty_print)
        if self.Signatory is not None:
            namespaceprefix_ = self.Signatory_nsprefix_ + ':' if (UseCapturedNS_ and self.Signatory_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSignatory>%s</%sSignatory>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Signatory), input_name='Signatory')), namespaceprefix_ , eol_))
        if self.EventRemarks is not None:
            namespaceprefix_ = self.EventRemarks_nsprefix_ + ':' if (UseCapturedNS_ and self.EventRemarks_nsprefix_) else ''
            self.EventRemarks.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EventRemarks', pretty_print=pretty_print)
        if self.ServiceArea is not None:
            namespaceprefix_ = self.ServiceArea_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceArea_nsprefix_) else ''
            self.ServiceArea.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ServiceArea', pretty_print=pretty_print)
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
        if nodeName_ == 'Date':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.Date = dval_
            self.Date_nsprefix_ = child_.prefix
        elif nodeName_ == 'Time':
            sval_ = child_.text
            dval_ = self.gds_parse_time(sval_)
            self.Time = dval_
            self.Time_nsprefix_ = child_.prefix
        elif nodeName_ == 'ServiceEvent':
            obj_ = ServiceEvent.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ServiceEvent = obj_
            obj_.original_tagname_ = 'ServiceEvent'
        elif nodeName_ == 'Signatory':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Signatory')
            value_ = self.gds_validate_string(value_, node, 'Signatory')
            self.Signatory = value_
            self.Signatory_nsprefix_ = child_.prefix
            # validate type SignatoryType
            self.validate_SignatoryType(self.Signatory)
        elif nodeName_ == 'EventRemarks':
            obj_ = EventRemarks.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EventRemarks = obj_
            obj_.original_tagname_ = 'EventRemarks'
        elif nodeName_ == 'ServiceArea':
            obj_ = ServiceArea.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ServiceArea = obj_
            obj_.original_tagname_ = 'ServiceArea'
# end class ShipmentEvent


class PieceInfo(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PieceDetails=None, PieceEvent=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PieceDetails = PieceDetails
        self.PieceDetails_nsprefix_ = None
        if PieceEvent is None:
            self.PieceEvent = []
        else:
            self.PieceEvent = PieceEvent
        self.PieceEvent_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PieceInfo)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PieceInfo.subclass:
            return PieceInfo.subclass(*args_, **kwargs_)
        else:
            return PieceInfo(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PieceDetails(self):
        return self.PieceDetails
    def set_PieceDetails(self, PieceDetails):
        self.PieceDetails = PieceDetails
    def get_PieceEvent(self):
        return self.PieceEvent
    def set_PieceEvent(self, PieceEvent):
        self.PieceEvent = PieceEvent
    def add_PieceEvent(self, value):
        self.PieceEvent.append(value)
    def insert_PieceEvent_at(self, index, value):
        self.PieceEvent.insert(index, value)
    def replace_PieceEvent_at(self, index, value):
        self.PieceEvent[index] = value
    def hasContent_(self):
        if (
            self.PieceDetails is not None or
            self.PieceEvent
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PieceInfo', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PieceInfo')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PieceInfo':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PieceInfo')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PieceInfo', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PieceInfo'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PieceInfo', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PieceDetails is not None:
            namespaceprefix_ = self.PieceDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceDetails_nsprefix_) else ''
            self.PieceDetails.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PieceDetails', pretty_print=pretty_print)
        for PieceEvent_ in self.PieceEvent:
            namespaceprefix_ = self.PieceEvent_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceEvent_nsprefix_) else ''
            PieceEvent_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PieceEvent', pretty_print=pretty_print)
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
        if nodeName_ == 'PieceDetails':
            obj_ = PieceDetails.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PieceDetails = obj_
            obj_.original_tagname_ = 'PieceDetails'
        elif nodeName_ == 'PieceEvent':
            obj_ = PieceEvent.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PieceEvent.append(obj_)
            obj_.original_tagname_ = 'PieceEvent'
# end class PieceInfo


class PieceEvent(GeneratedsSuper):
    """Describes the checkpoint information"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Date=None, Time=None, ServiceEvent=None, Signatory=None, ServiceArea=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if isinstance(Date, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Date, '%Y-%m-%d').date()
        else:
            initvalue_ = Date
        self.Date = initvalue_
        self.Date_nsprefix_ = None
        if isinstance(Time, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Time, '%H:%M:%S').time()
        else:
            initvalue_ = Time
        self.Time = initvalue_
        self.Time_nsprefix_ = None
        self.ServiceEvent = ServiceEvent
        self.ServiceEvent_nsprefix_ = None
        self.Signatory = Signatory
        self.validate_SignatoryType4(self.Signatory)
        self.Signatory_nsprefix_ = None
        self.ServiceArea = ServiceArea
        self.ServiceArea_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PieceEvent)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PieceEvent.subclass:
            return PieceEvent.subclass(*args_, **kwargs_)
        else:
            return PieceEvent(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Date(self):
        return self.Date
    def set_Date(self, Date):
        self.Date = Date
    def get_Time(self):
        return self.Time
    def set_Time(self, Time):
        self.Time = Time
    def get_ServiceEvent(self):
        return self.ServiceEvent
    def set_ServiceEvent(self, ServiceEvent):
        self.ServiceEvent = ServiceEvent
    def get_Signatory(self):
        return self.Signatory
    def set_Signatory(self, Signatory):
        self.Signatory = Signatory
    def get_ServiceArea(self):
        return self.ServiceArea
    def set_ServiceArea(self, ServiceArea):
        self.ServiceArea = ServiceArea
    def validate_SignatoryType4(self, value):
        result = True
        # Validate type SignatoryType4, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def hasContent_(self):
        if (
            self.Date is not None or
            self.Time is not None or
            self.ServiceEvent is not None or
            self.Signatory is not None or
            self.ServiceArea is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PieceEvent', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PieceEvent')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PieceEvent':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PieceEvent')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PieceEvent', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PieceEvent'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PieceEvent', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Date is not None:
            namespaceprefix_ = self.Date_nsprefix_ + ':' if (UseCapturedNS_ and self.Date_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDate>%s</%sDate>%s' % (namespaceprefix_ , self.gds_format_date(self.Date, input_name='Date'), namespaceprefix_ , eol_))
        if self.Time is not None:
            namespaceprefix_ = self.Time_nsprefix_ + ':' if (UseCapturedNS_ and self.Time_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTime>%s</%sTime>%s' % (namespaceprefix_ , self.gds_format_time(self.Time, input_name='Time'), namespaceprefix_ , eol_))
        if self.ServiceEvent is not None:
            namespaceprefix_ = self.ServiceEvent_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceEvent_nsprefix_) else ''
            self.ServiceEvent.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ServiceEvent', pretty_print=pretty_print)
        if self.Signatory is not None:
            namespaceprefix_ = self.Signatory_nsprefix_ + ':' if (UseCapturedNS_ and self.Signatory_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSignatory>%s</%sSignatory>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Signatory), input_name='Signatory')), namespaceprefix_ , eol_))
        if self.ServiceArea is not None:
            namespaceprefix_ = self.ServiceArea_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceArea_nsprefix_) else ''
            self.ServiceArea.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ServiceArea', pretty_print=pretty_print)
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
        if nodeName_ == 'Date':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.Date = dval_
            self.Date_nsprefix_ = child_.prefix
        elif nodeName_ == 'Time':
            sval_ = child_.text
            dval_ = self.gds_parse_time(sval_)
            self.Time = dval_
            self.Time_nsprefix_ = child_.prefix
        elif nodeName_ == 'ServiceEvent':
            obj_ = ServiceEvent.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ServiceEvent = obj_
            obj_.original_tagname_ = 'ServiceEvent'
        elif nodeName_ == 'Signatory':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Signatory')
            value_ = self.gds_validate_string(value_, node, 'Signatory')
            self.Signatory = value_
            self.Signatory_nsprefix_ = child_.prefix
            # validate type SignatoryType4
            self.validate_SignatoryType4(self.Signatory)
        elif nodeName_ == 'ServiceArea':
            obj_ = ServiceArea.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ServiceArea = obj_
            obj_.original_tagname_ = 'ServiceArea'
# end class PieceEvent


class PieceDetails(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AWBNumber=None, LicensePlate=None, PieceNumber=None, ActualDepth=None, ActualWidth=None, ActualHeight=None, ActualWeight=None, Depth=None, Width=None, Height=None, Weight=None, PackageType=None, DimWeight=None, WeightUnit=None, PieceContents=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.AWBNumber = AWBNumber
        self.AWBNumber_nsprefix_ = None
        self.LicensePlate = LicensePlate
        self.validate_TrackingPieceID(self.LicensePlate)
        self.LicensePlate_nsprefix_ = None
        self.PieceNumber = PieceNumber
        self.PieceNumber_nsprefix_ = None
        self.ActualDepth = ActualDepth
        self.ActualDepth_nsprefix_ = None
        self.ActualWidth = ActualWidth
        self.ActualWidth_nsprefix_ = None
        self.ActualHeight = ActualHeight
        self.ActualHeight_nsprefix_ = None
        self.ActualWeight = ActualWeight
        self.ActualWeight_nsprefix_ = None
        self.Depth = Depth
        self.Depth_nsprefix_ = None
        self.Width = Width
        self.Width_nsprefix_ = None
        self.Height = Height
        self.Height_nsprefix_ = None
        self.Weight = Weight
        self.Weight_nsprefix_ = None
        self.PackageType = PackageType
        self.validate_TrackingPackageType(self.PackageType)
        self.PackageType_nsprefix_ = None
        self.DimWeight = DimWeight
        self.DimWeight_nsprefix_ = None
        self.WeightUnit = WeightUnit
        self.validate_PieceWeightUnit(self.WeightUnit)
        self.WeightUnit_nsprefix_ = None
        self.PieceContents = PieceContents
        self.PieceContents_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PieceDetails)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PieceDetails.subclass:
            return PieceDetails.subclass(*args_, **kwargs_)
        else:
            return PieceDetails(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AWBNumber(self):
        return self.AWBNumber
    def set_AWBNumber(self, AWBNumber):
        self.AWBNumber = AWBNumber
    def get_LicensePlate(self):
        return self.LicensePlate
    def set_LicensePlate(self, LicensePlate):
        self.LicensePlate = LicensePlate
    def get_PieceNumber(self):
        return self.PieceNumber
    def set_PieceNumber(self, PieceNumber):
        self.PieceNumber = PieceNumber
    def get_ActualDepth(self):
        return self.ActualDepth
    def set_ActualDepth(self, ActualDepth):
        self.ActualDepth = ActualDepth
    def get_ActualWidth(self):
        return self.ActualWidth
    def set_ActualWidth(self, ActualWidth):
        self.ActualWidth = ActualWidth
    def get_ActualHeight(self):
        return self.ActualHeight
    def set_ActualHeight(self, ActualHeight):
        self.ActualHeight = ActualHeight
    def get_ActualWeight(self):
        return self.ActualWeight
    def set_ActualWeight(self, ActualWeight):
        self.ActualWeight = ActualWeight
    def get_Depth(self):
        return self.Depth
    def set_Depth(self, Depth):
        self.Depth = Depth
    def get_Width(self):
        return self.Width
    def set_Width(self, Width):
        self.Width = Width
    def get_Height(self):
        return self.Height
    def set_Height(self, Height):
        self.Height = Height
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def get_PackageType(self):
        return self.PackageType
    def set_PackageType(self, PackageType):
        self.PackageType = PackageType
    def get_DimWeight(self):
        return self.DimWeight
    def set_DimWeight(self, DimWeight):
        self.DimWeight = DimWeight
    def get_WeightUnit(self):
        return self.WeightUnit
    def set_WeightUnit(self, WeightUnit):
        self.WeightUnit = WeightUnit
    def get_PieceContents(self):
        return self.PieceContents
    def set_PieceContents(self, PieceContents):
        self.PieceContents = PieceContents
    def validate_TrackingPieceID(self, value):
        result = True
        # Validate type TrackingPieceID, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on TrackingPieceID' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on TrackingPieceID' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_TrackingPackageType(self, value):
        result = True
        # Validate type TrackingPackageType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on TrackingPackageType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PieceWeightUnit(self, value):
        result = True
        # Validate type PieceWeightUnit, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on PieceWeightUnit' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.AWBNumber is not None or
            self.LicensePlate is not None or
            self.PieceNumber is not None or
            self.ActualDepth is not None or
            self.ActualWidth is not None or
            self.ActualHeight is not None or
            self.ActualWeight is not None or
            self.Depth is not None or
            self.Width is not None or
            self.Height is not None or
            self.Weight is not None or
            self.PackageType is not None or
            self.DimWeight is not None or
            self.WeightUnit is not None or
            self.PieceContents is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PieceDetails', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PieceDetails')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PieceDetails':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PieceDetails')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PieceDetails', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PieceDetails'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PieceDetails', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.AWBNumber is not None:
            namespaceprefix_ = self.AWBNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.AWBNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAWBNumber>%s</%sAWBNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AWBNumber), input_name='AWBNumber')), namespaceprefix_ , eol_))
        if self.LicensePlate is not None:
            namespaceprefix_ = self.LicensePlate_nsprefix_ + ':' if (UseCapturedNS_ and self.LicensePlate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLicensePlate>%s</%sLicensePlate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LicensePlate), input_name='LicensePlate')), namespaceprefix_ , eol_))
        if self.PieceNumber is not None:
            namespaceprefix_ = self.PieceNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPieceNumber>%s</%sPieceNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PieceNumber), input_name='PieceNumber')), namespaceprefix_ , eol_))
        if self.ActualDepth is not None:
            namespaceprefix_ = self.ActualDepth_nsprefix_ + ':' if (UseCapturedNS_ and self.ActualDepth_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sActualDepth>%s</%sActualDepth>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ActualDepth), input_name='ActualDepth')), namespaceprefix_ , eol_))
        if self.ActualWidth is not None:
            namespaceprefix_ = self.ActualWidth_nsprefix_ + ':' if (UseCapturedNS_ and self.ActualWidth_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sActualWidth>%s</%sActualWidth>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ActualWidth), input_name='ActualWidth')), namespaceprefix_ , eol_))
        if self.ActualHeight is not None:
            namespaceprefix_ = self.ActualHeight_nsprefix_ + ':' if (UseCapturedNS_ and self.ActualHeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sActualHeight>%s</%sActualHeight>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ActualHeight), input_name='ActualHeight')), namespaceprefix_ , eol_))
        if self.ActualWeight is not None:
            namespaceprefix_ = self.ActualWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.ActualWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sActualWeight>%s</%sActualWeight>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ActualWeight), input_name='ActualWeight')), namespaceprefix_ , eol_))
        if self.Depth is not None:
            namespaceprefix_ = self.Depth_nsprefix_ + ':' if (UseCapturedNS_ and self.Depth_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDepth>%s</%sDepth>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Depth), input_name='Depth')), namespaceprefix_ , eol_))
        if self.Width is not None:
            namespaceprefix_ = self.Width_nsprefix_ + ':' if (UseCapturedNS_ and self.Width_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWidth>%s</%sWidth>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Width), input_name='Width')), namespaceprefix_ , eol_))
        if self.Height is not None:
            namespaceprefix_ = self.Height_nsprefix_ + ':' if (UseCapturedNS_ and self.Height_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHeight>%s</%sHeight>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Height), input_name='Height')), namespaceprefix_ , eol_))
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeight>%s</%sWeight>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Weight), input_name='Weight')), namespaceprefix_ , eol_))
        if self.PackageType is not None:
            namespaceprefix_ = self.PackageType_nsprefix_ + ':' if (UseCapturedNS_ and self.PackageType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPackageType>%s</%sPackageType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PackageType), input_name='PackageType')), namespaceprefix_ , eol_))
        if self.DimWeight is not None:
            namespaceprefix_ = self.DimWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.DimWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDimWeight>%s</%sDimWeight>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DimWeight), input_name='DimWeight')), namespaceprefix_ , eol_))
        if self.WeightUnit is not None:
            namespaceprefix_ = self.WeightUnit_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightUnit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeightUnit>%s</%sWeightUnit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WeightUnit), input_name='WeightUnit')), namespaceprefix_ , eol_))
        if self.PieceContents is not None:
            namespaceprefix_ = self.PieceContents_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceContents_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPieceContents>%s</%sPieceContents>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PieceContents), input_name='PieceContents')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'AWBNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AWBNumber')
            value_ = self.gds_validate_string(value_, node, 'AWBNumber')
            self.AWBNumber = value_
            self.AWBNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'LicensePlate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LicensePlate')
            value_ = self.gds_validate_string(value_, node, 'LicensePlate')
            self.LicensePlate = value_
            self.LicensePlate_nsprefix_ = child_.prefix
            # validate type TrackingPieceID
            self.validate_TrackingPieceID(self.LicensePlate)
        elif nodeName_ == 'PieceNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PieceNumber')
            value_ = self.gds_validate_string(value_, node, 'PieceNumber')
            self.PieceNumber = value_
            self.PieceNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'ActualDepth':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ActualDepth')
            value_ = self.gds_validate_string(value_, node, 'ActualDepth')
            self.ActualDepth = value_
            self.ActualDepth_nsprefix_ = child_.prefix
        elif nodeName_ == 'ActualWidth':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ActualWidth')
            value_ = self.gds_validate_string(value_, node, 'ActualWidth')
            self.ActualWidth = value_
            self.ActualWidth_nsprefix_ = child_.prefix
        elif nodeName_ == 'ActualHeight':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ActualHeight')
            value_ = self.gds_validate_string(value_, node, 'ActualHeight')
            self.ActualHeight = value_
            self.ActualHeight_nsprefix_ = child_.prefix
        elif nodeName_ == 'ActualWeight':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ActualWeight')
            value_ = self.gds_validate_string(value_, node, 'ActualWeight')
            self.ActualWeight = value_
            self.ActualWeight_nsprefix_ = child_.prefix
        elif nodeName_ == 'Depth':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Depth')
            value_ = self.gds_validate_string(value_, node, 'Depth')
            self.Depth = value_
            self.Depth_nsprefix_ = child_.prefix
        elif nodeName_ == 'Width':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Width')
            value_ = self.gds_validate_string(value_, node, 'Width')
            self.Width = value_
            self.Width_nsprefix_ = child_.prefix
        elif nodeName_ == 'Height':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Height')
            value_ = self.gds_validate_string(value_, node, 'Height')
            self.Height = value_
            self.Height_nsprefix_ = child_.prefix
        elif nodeName_ == 'Weight':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Weight')
            value_ = self.gds_validate_string(value_, node, 'Weight')
            self.Weight = value_
            self.Weight_nsprefix_ = child_.prefix
        elif nodeName_ == 'PackageType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PackageType')
            value_ = self.gds_validate_string(value_, node, 'PackageType')
            self.PackageType = value_
            self.PackageType_nsprefix_ = child_.prefix
            # validate type TrackingPackageType
            self.validate_TrackingPackageType(self.PackageType)
        elif nodeName_ == 'DimWeight':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DimWeight')
            value_ = self.gds_validate_string(value_, node, 'DimWeight')
            self.DimWeight = value_
            self.DimWeight_nsprefix_ = child_.prefix
        elif nodeName_ == 'WeightUnit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WeightUnit')
            value_ = self.gds_validate_string(value_, node, 'WeightUnit')
            self.WeightUnit = value_
            self.WeightUnit_nsprefix_ = child_.prefix
            # validate type PieceWeightUnit
            self.validate_PieceWeightUnit(self.WeightUnit)
        elif nodeName_ == 'PieceContents':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PieceContents')
            value_ = self.gds_validate_string(value_, node, 'PieceContents')
            self.PieceContents = value_
            self.PieceContents_nsprefix_ = child_.prefix
# end class PieceDetails


class TrackingPieces(GeneratedsSuper):
    """Piece Info"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PieceInfo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if PieceInfo is None:
            self.PieceInfo = []
        else:
            self.PieceInfo = PieceInfo
        self.PieceInfo_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TrackingPieces)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TrackingPieces.subclass:
            return TrackingPieces.subclass(*args_, **kwargs_)
        else:
            return TrackingPieces(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PieceInfo(self):
        return self.PieceInfo
    def set_PieceInfo(self, PieceInfo):
        self.PieceInfo = PieceInfo
    def add_PieceInfo(self, value):
        self.PieceInfo.append(value)
    def insert_PieceInfo_at(self, index, value):
        self.PieceInfo.insert(index, value)
    def replace_PieceInfo_at(self, index, value):
        self.PieceInfo[index] = value
    def hasContent_(self):
        if (
            self.PieceInfo
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackingPieces', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TrackingPieces')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TrackingPieces':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TrackingPieces')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TrackingPieces', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TrackingPieces'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackingPieces', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for PieceInfo_ in self.PieceInfo:
            namespaceprefix_ = self.PieceInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceInfo_nsprefix_) else ''
            PieceInfo_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PieceInfo', pretty_print=pretty_print)
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
        if nodeName_ == 'PieceInfo':
            obj_ = PieceInfo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PieceInfo.append(obj_)
            obj_.original_tagname_ = 'PieceInfo'
# end class TrackingPieces


class Fault(GeneratedsSuper):
    """Piece Fault"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PieceFault=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if PieceFault is None:
            self.PieceFault = []
        else:
            self.PieceFault = PieceFault
        self.PieceFault_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Fault)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Fault.subclass:
            return Fault.subclass(*args_, **kwargs_)
        else:
            return Fault(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PieceFault(self):
        return self.PieceFault
    def set_PieceFault(self, PieceFault):
        self.PieceFault = PieceFault
    def add_PieceFault(self, value):
        self.PieceFault.append(value)
    def insert_PieceFault_at(self, index, value):
        self.PieceFault.insert(index, value)
    def replace_PieceFault_at(self, index, value):
        self.PieceFault[index] = value
    def hasContent_(self):
        if (
            self.PieceFault
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Fault', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Fault')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Fault':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Fault')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Fault', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Fault'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Fault', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for PieceFault_ in self.PieceFault:
            namespaceprefix_ = self.PieceFault_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceFault_nsprefix_) else ''
            PieceFault_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PieceFault', pretty_print=pretty_print)
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
        if nodeName_ == 'PieceFault':
            obj_ = PieceFault.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PieceFault.append(obj_)
            obj_.original_tagname_ = 'PieceFault'
# end class Fault


class PieceFault(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PieceID=None, ConditionCode=None, ConditionData=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PieceID = PieceID
        self.validate_TrackingPieceID(self.PieceID)
        self.PieceID_nsprefix_ = None
        self.ConditionCode = ConditionCode
        self.ConditionCode_nsprefix_ = None
        self.ConditionData = ConditionData
        self.ConditionData_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PieceFault)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PieceFault.subclass:
            return PieceFault.subclass(*args_, **kwargs_)
        else:
            return PieceFault(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PieceID(self):
        return self.PieceID
    def set_PieceID(self, PieceID):
        self.PieceID = PieceID
    def get_ConditionCode(self):
        return self.ConditionCode
    def set_ConditionCode(self, ConditionCode):
        self.ConditionCode = ConditionCode
    def get_ConditionData(self):
        return self.ConditionData
    def set_ConditionData(self, ConditionData):
        self.ConditionData = ConditionData
    def validate_TrackingPieceID(self, value):
        result = True
        # Validate type TrackingPieceID, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on TrackingPieceID' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on TrackingPieceID' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.PieceID is not None or
            self.ConditionCode is not None or
            self.ConditionData is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PieceFault', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PieceFault')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PieceFault':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PieceFault')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PieceFault', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PieceFault'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PieceFault', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PieceID is not None:
            namespaceprefix_ = self.PieceID_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPieceID>%s</%sPieceID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PieceID), input_name='PieceID')), namespaceprefix_ , eol_))
        if self.ConditionCode is not None:
            namespaceprefix_ = self.ConditionCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ConditionCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sConditionCode>%s</%sConditionCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ConditionCode), input_name='ConditionCode')), namespaceprefix_ , eol_))
        if self.ConditionData is not None:
            namespaceprefix_ = self.ConditionData_nsprefix_ + ':' if (UseCapturedNS_ and self.ConditionData_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sConditionData>%s</%sConditionData>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ConditionData), input_name='ConditionData')), namespaceprefix_ , eol_))
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
            # validate type TrackingPieceID
            self.validate_TrackingPieceID(self.PieceID)
        elif nodeName_ == 'ConditionCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ConditionCode')
            value_ = self.gds_validate_string(value_, node, 'ConditionCode')
            self.ConditionCode = value_
            self.ConditionCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'ConditionData':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ConditionData')
            value_ = self.gds_validate_string(value_, node, 'ConditionData')
            self.ConditionData = value_
            self.ConditionData_nsprefix_ = child_.prefix
# end class PieceFault


class QtdSInAdCur(GeneratedsSuper):
    """QtdSInAdCur"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CurrencyCode=None, CurrencyRoleTypeCode=None, PackageCharge=None, ShippingCharge=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CurrencyCode = CurrencyCode
        self.validate_CurrencyCode(self.CurrencyCode)
        self.CurrencyCode_nsprefix_ = None
        self.CurrencyRoleTypeCode = CurrencyRoleTypeCode
        self.validate_CurrencyRoleTypeCode(self.CurrencyRoleTypeCode)
        self.CurrencyRoleTypeCode_nsprefix_ = None
        self.PackageCharge = PackageCharge
        self.validate_PackageCharge(self.PackageCharge)
        self.PackageCharge_nsprefix_ = None
        self.ShippingCharge = ShippingCharge
        self.validate_ShippingCharge(self.ShippingCharge)
        self.ShippingCharge_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, QtdSInAdCur)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if QtdSInAdCur.subclass:
            return QtdSInAdCur.subclass(*args_, **kwargs_)
        else:
            return QtdSInAdCur(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_CurrencyRoleTypeCode(self):
        return self.CurrencyRoleTypeCode
    def set_CurrencyRoleTypeCode(self, CurrencyRoleTypeCode):
        self.CurrencyRoleTypeCode = CurrencyRoleTypeCode
    def get_PackageCharge(self):
        return self.PackageCharge
    def set_PackageCharge(self, PackageCharge):
        self.PackageCharge = PackageCharge
    def get_ShippingCharge(self):
        return self.ShippingCharge
    def set_ShippingCharge(self, ShippingCharge):
        self.ShippingCharge = ShippingCharge
    def validate_CurrencyCode(self, value):
        result = True
        # Validate type CurrencyCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CurrencyCode' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CurrencyRoleTypeCode(self, value):
        result = True
        # Validate type CurrencyRoleTypeCode, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['BILLCU', 'PULCL', 'INVCU', 'BASEC']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CurrencyRoleTypeCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) > 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CurrencyRoleTypeCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PackageCharge(self, value):
        result = True
        # Validate type PackageCharge, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on PackageCharge' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_ShippingCharge(self, value):
        result = True
        # Validate type ShippingCharge, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on ShippingCharge' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.CurrencyCode is not None or
            self.CurrencyRoleTypeCode is not None or
            self.PackageCharge is not None or
            self.ShippingCharge is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='QtdSInAdCur', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('QtdSInAdCur')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'QtdSInAdCur':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='QtdSInAdCur')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='QtdSInAdCur', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='QtdSInAdCur'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='QtdSInAdCur', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.CurrencyRoleTypeCode is not None:
            namespaceprefix_ = self.CurrencyRoleTypeCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyRoleTypeCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyRoleTypeCode>%s</%sCurrencyRoleTypeCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyRoleTypeCode), input_name='CurrencyRoleTypeCode')), namespaceprefix_ , eol_))
        if self.PackageCharge is not None:
            namespaceprefix_ = self.PackageCharge_nsprefix_ + ':' if (UseCapturedNS_ and self.PackageCharge_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPackageCharge>%s</%sPackageCharge>%s' % (namespaceprefix_ , self.gds_format_decimal(self.PackageCharge, input_name='PackageCharge'), namespaceprefix_ , eol_))
        if self.ShippingCharge is not None:
            namespaceprefix_ = self.ShippingCharge_nsprefix_ + ':' if (UseCapturedNS_ and self.ShippingCharge_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShippingCharge>%s</%sShippingCharge>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ShippingCharge, input_name='ShippingCharge'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
            # validate type CurrencyCode
            self.validate_CurrencyCode(self.CurrencyCode)
        elif nodeName_ == 'CurrencyRoleTypeCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyRoleTypeCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyRoleTypeCode')
            self.CurrencyRoleTypeCode = value_
            self.CurrencyRoleTypeCode_nsprefix_ = child_.prefix
            # validate type CurrencyRoleTypeCode
            self.validate_CurrencyRoleTypeCode(self.CurrencyRoleTypeCode)
        elif nodeName_ == 'PackageCharge' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'PackageCharge')
            fval_ = self.gds_validate_decimal(fval_, node, 'PackageCharge')
            self.PackageCharge = fval_
            self.PackageCharge_nsprefix_ = child_.prefix
            # validate type PackageCharge
            self.validate_PackageCharge(self.PackageCharge)
        elif nodeName_ == 'ShippingCharge' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ShippingCharge')
            fval_ = self.gds_validate_decimal(fval_, node, 'ShippingCharge')
            self.ShippingCharge = fval_
            self.ShippingCharge_nsprefix_ = child_.prefix
            # validate type ShippingCharge
            self.validate_ShippingCharge(self.ShippingCharge)
# end class QtdSInAdCur


class LabelImage(GeneratedsSuper):
    """LabelImage"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, OutputFormat=None, OutputImage=None, OutputImageNPC=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.OutputFormat = OutputFormat
        self.validate_OutputFormat(self.OutputFormat)
        self.OutputFormat_nsprefix_ = None
        self.OutputImage = OutputImage
        self.validate_OutputImage(self.OutputImage)
        self.OutputImage_nsprefix_ = None
        self.OutputImageNPC = OutputImageNPC
        self.OutputImageNPC_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LabelImage)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LabelImage.subclass:
            return LabelImage.subclass(*args_, **kwargs_)
        else:
            return LabelImage(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_OutputFormat(self):
        return self.OutputFormat
    def set_OutputFormat(self, OutputFormat):
        self.OutputFormat = OutputFormat
    def get_OutputImage(self):
        return self.OutputImage
    def set_OutputImage(self, OutputImage):
        self.OutputImage = OutputImage
    def get_OutputImageNPC(self):
        return self.OutputImageNPC
    def set_OutputImageNPC(self, OutputImageNPC):
        self.OutputImageNPC = OutputImageNPC
    def validate_OutputFormat(self, value):
        result = True
        # Validate type OutputFormat, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['PDF', 'PL2', 'ZPL2', 'JPG', 'PNG', 'EPL2', 'EPLN', 'ZPLN']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on OutputFormat' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_OutputImage(self, value):
        result = True
        # Validate type OutputImage, a restriction on xsd:base64Binary.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def hasContent_(self):
        if (
            self.OutputFormat is not None or
            self.OutputImage is not None or
            self.OutputImageNPC is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LabelImage', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LabelImage')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LabelImage':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LabelImage')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LabelImage', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LabelImage'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LabelImage', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.OutputFormat is not None:
            namespaceprefix_ = self.OutputFormat_nsprefix_ + ':' if (UseCapturedNS_ and self.OutputFormat_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOutputFormat>%s</%sOutputFormat>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OutputFormat), input_name='OutputFormat')), namespaceprefix_ , eol_))
        if self.OutputImage is not None:
            namespaceprefix_ = self.OutputImage_nsprefix_ + ':' if (UseCapturedNS_ and self.OutputImage_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOutputImage>%s</%sOutputImage>%s' % (namespaceprefix_ , self.gds_format_base64(self.OutputImage, input_name='OutputImage'), namespaceprefix_ , eol_))
        if self.OutputImageNPC is not None:
            namespaceprefix_ = self.OutputImageNPC_nsprefix_ + ':' if (UseCapturedNS_ and self.OutputImageNPC_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOutputImageNPC>%s</%sOutputImageNPC>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OutputImageNPC), input_name='OutputImageNPC')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'OutputFormat':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OutputFormat')
            value_ = self.gds_validate_string(value_, node, 'OutputFormat')
            self.OutputFormat = value_
            self.OutputFormat_nsprefix_ = child_.prefix
            # validate type OutputFormat
            self.validate_OutputFormat(self.OutputFormat)
        elif nodeName_ == 'OutputImage':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'OutputImage')
            else:
                bval_ = None
            self.OutputImage = bval_
            self.OutputImage_nsprefix_ = child_.prefix
            # validate type OutputImage
            self.validate_OutputImage(self.OutputImage)
        elif nodeName_ == 'OutputImageNPC':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OutputImageNPC')
            value_ = self.gds_validate_string(value_, node, 'OutputImageNPC')
            self.OutputImageNPC = value_
            self.OutputImageNPC_nsprefix_ = child_.prefix
# end class LabelImage


class DocImages(GeneratedsSuper):
    """DocImages"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DocImage=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if DocImage is None:
            self.DocImage = []
        else:
            self.DocImage = DocImage
        self.DocImage_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DocImages)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DocImages.subclass:
            return DocImages.subclass(*args_, **kwargs_)
        else:
            return DocImages(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DocImage(self):
        return self.DocImage
    def set_DocImage(self, DocImage):
        self.DocImage = DocImage
    def add_DocImage(self, value):
        self.DocImage.append(value)
    def insert_DocImage_at(self, index, value):
        self.DocImage.insert(index, value)
    def replace_DocImage_at(self, index, value):
        self.DocImage[index] = value
    def hasContent_(self):
        if (
            self.DocImage
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DocImages', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DocImages')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DocImages':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DocImages')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DocImages', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DocImages'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DocImages', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for DocImage_ in self.DocImage:
            namespaceprefix_ = self.DocImage_nsprefix_ + ':' if (UseCapturedNS_ and self.DocImage_nsprefix_) else ''
            DocImage_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DocImage', pretty_print=pretty_print)
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
        if nodeName_ == 'DocImage':
            obj_ = DocImage.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DocImage.append(obj_)
            obj_.original_tagname_ = 'DocImage'
# end class DocImages


class DocImage(GeneratedsSuper):
    """DocImage"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Type=None, Image=None, ImageFormat=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Type = Type
        self.validate_Type(self.Type)
        self.Type_nsprefix_ = None
        self.Image = Image
        self.validate_Image(self.Image)
        self.Image_nsprefix_ = None
        self.ImageFormat = ImageFormat
        self.validate_ImageFormat(self.ImageFormat)
        self.ImageFormat_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DocImage)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DocImage.subclass:
            return DocImage.subclass(*args_, **kwargs_)
        else:
            return DocImage(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_Image(self):
        return self.Image
    def set_Image(self, Image):
        self.Image = Image
    def get_ImageFormat(self):
        return self.ImageFormat
    def set_ImageFormat(self, ImageFormat):
        self.ImageFormat = ImageFormat
    def validate_Type(self, value):
        result = True
        # Validate type Type, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['HWB', 'INV', 'PNV', 'COO', 'NAF', 'CIN', 'DCL']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on Type' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on Type' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_Image(self, value):
        result = True
        # Validate type Image, a restriction on xsd:base64Binary.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def validate_ImageFormat(self, value):
        result = True
        # Validate type ImageFormat, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['PDF', 'PNG', 'TIFF', 'GIF', 'JPEG']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ImageFormat' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) > 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ImageFormat' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Type is not None or
            self.Image is not None or
            self.ImageFormat is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DocImage', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DocImage')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DocImage':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DocImage')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DocImage', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DocImage'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DocImage', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Type), input_name='Type')), namespaceprefix_ , eol_))
        if self.Image is not None:
            namespaceprefix_ = self.Image_nsprefix_ + ':' if (UseCapturedNS_ and self.Image_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImage>%s</%sImage>%s' % (namespaceprefix_ , self.gds_format_base64(self.Image, input_name='Image'), namespaceprefix_ , eol_))
        if self.ImageFormat is not None:
            namespaceprefix_ = self.ImageFormat_nsprefix_ + ':' if (UseCapturedNS_ and self.ImageFormat_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImageFormat>%s</%sImageFormat>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ImageFormat), input_name='ImageFormat')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Type':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Type')
            value_ = self.gds_validate_string(value_, node, 'Type')
            self.Type = value_
            self.Type_nsprefix_ = child_.prefix
            # validate type Type
            self.validate_Type(self.Type)
        elif nodeName_ == 'Image':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'Image')
            else:
                bval_ = None
            self.Image = bval_
            self.Image_nsprefix_ = child_.prefix
            # validate type Image
            self.validate_Image(self.Image)
        elif nodeName_ == 'ImageFormat':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ImageFormat')
            value_ = self.gds_validate_string(value_, node, 'ImageFormat')
            self.ImageFormat = value_
            self.ImageFormat_nsprefix_ = child_.prefix
            # validate type ImageFormat
            self.validate_ImageFormat(self.ImageFormat)
# end class DocImage


class Label(GeneratedsSuper):
    """Label"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, LabelTemplate=None, Logo=None, CustomerLogo=None, Resolution=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.LabelTemplate = LabelTemplate
        self.validate_LabelTemplate(self.LabelTemplate)
        self.LabelTemplate_nsprefix_ = None
        self.Logo = Logo
        self.validate_YesNo(self.Logo)
        self.Logo_nsprefix_ = None
        self.CustomerLogo = CustomerLogo
        self.CustomerLogo_nsprefix_ = None
        self.Resolution = Resolution
        self.validate_Resolution(self.Resolution)
        self.Resolution_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Label)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Label.subclass:
            return Label.subclass(*args_, **kwargs_)
        else:
            return Label(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_LabelTemplate(self):
        return self.LabelTemplate
    def set_LabelTemplate(self, LabelTemplate):
        self.LabelTemplate = LabelTemplate
    def get_Logo(self):
        return self.Logo
    def set_Logo(self, Logo):
        self.Logo = Logo
    def get_CustomerLogo(self):
        return self.CustomerLogo
    def set_CustomerLogo(self, CustomerLogo):
        self.CustomerLogo = CustomerLogo
    def get_Resolution(self):
        return self.Resolution
    def set_Resolution(self, Resolution):
        self.Resolution = Resolution
    def validate_LabelTemplate(self, value):
        result = True
        # Validate type LabelTemplate, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['8X4_A4_PDF', '8X4_thermal', '8X4_A4_TC_PDF', '6X4_thermal', '6X4_A4_PDF', '8X4_CI_PDF', '8X4_CI_thermal']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LabelTemplate' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_YesNo(self, value):
        result = True
        # Validate type YesNo, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['Y', 'N']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on YesNo' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on YesNo' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_Resolution(self, value):
        result = True
        # Validate type Resolution, a restriction on xsd:positiveInteger.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 200:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on Resolution' % {"value": value, "lineno": lineno} )
                result = False
            if value > 300:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on Resolution' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.LabelTemplate is not None or
            self.Logo is not None or
            self.CustomerLogo is not None or
            self.Resolution is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Label', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Label')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Label':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Label')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Label', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Label'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Label', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.LabelTemplate is not None:
            namespaceprefix_ = self.LabelTemplate_nsprefix_ + ':' if (UseCapturedNS_ and self.LabelTemplate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLabelTemplate>%s</%sLabelTemplate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LabelTemplate), input_name='LabelTemplate')), namespaceprefix_ , eol_))
        if self.Logo is not None:
            namespaceprefix_ = self.Logo_nsprefix_ + ':' if (UseCapturedNS_ and self.Logo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLogo>%s</%sLogo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Logo), input_name='Logo')), namespaceprefix_ , eol_))
        if self.CustomerLogo is not None:
            namespaceprefix_ = self.CustomerLogo_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerLogo_nsprefix_) else ''
            self.CustomerLogo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CustomerLogo', pretty_print=pretty_print)
        if self.Resolution is not None:
            namespaceprefix_ = self.Resolution_nsprefix_ + ':' if (UseCapturedNS_ and self.Resolution_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sResolution>%s</%sResolution>%s' % (namespaceprefix_ , self.gds_format_integer(self.Resolution, input_name='Resolution'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'LabelTemplate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LabelTemplate')
            value_ = self.gds_validate_string(value_, node, 'LabelTemplate')
            self.LabelTemplate = value_
            self.LabelTemplate_nsprefix_ = child_.prefix
            # validate type LabelTemplate
            self.validate_LabelTemplate(self.LabelTemplate)
        elif nodeName_ == 'Logo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Logo')
            value_ = self.gds_validate_string(value_, node, 'Logo')
            self.Logo = value_
            self.Logo_nsprefix_ = child_.prefix
            # validate type YesNo
            self.validate_YesNo(self.Logo)
        elif nodeName_ == 'CustomerLogo':
            obj_ = CustomerLogo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CustomerLogo = obj_
            obj_.original_tagname_ = 'CustomerLogo'
        elif nodeName_ == 'Resolution' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Resolution')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'Resolution')
            self.Resolution = ival_
            self.Resolution_nsprefix_ = child_.prefix
            # validate type Resolution
            self.validate_Resolution(self.Resolution)
# end class Label


class CustomerLogo(GeneratedsSuper):
    """CustomerLogo"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, LogoImage=None, LogoImageFormat=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.LogoImage = LogoImage
        self.validate_LogoImage(self.LogoImage)
        self.LogoImage_nsprefix_ = None
        self.LogoImageFormat = LogoImageFormat
        self.validate_LogoImageFormat(self.LogoImageFormat)
        self.LogoImageFormat_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CustomerLogo)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CustomerLogo.subclass:
            return CustomerLogo.subclass(*args_, **kwargs_)
        else:
            return CustomerLogo(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_LogoImage(self):
        return self.LogoImage
    def set_LogoImage(self, LogoImage):
        self.LogoImage = LogoImage
    def get_LogoImageFormat(self):
        return self.LogoImageFormat
    def set_LogoImageFormat(self, LogoImageFormat):
        self.LogoImageFormat = LogoImageFormat
    def validate_LogoImage(self, value):
        result = True
        # Validate type LogoImage, a restriction on xsd:base64Binary.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 1048576:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on LogoImage' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_LogoImageFormat(self, value):
        result = True
        # Validate type LogoImageFormat, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['PNG', 'GIF', 'JPEG', 'JPG']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LogoImageFormat' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.LogoImage is not None or
            self.LogoImageFormat is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CustomerLogo', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CustomerLogo')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CustomerLogo':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CustomerLogo')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CustomerLogo', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CustomerLogo'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CustomerLogo', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.LogoImage is not None:
            namespaceprefix_ = self.LogoImage_nsprefix_ + ':' if (UseCapturedNS_ and self.LogoImage_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLogoImage>%s</%sLogoImage>%s' % (namespaceprefix_ , self.gds_format_base64(self.LogoImage, input_name='LogoImage'), namespaceprefix_ , eol_))
        if self.LogoImageFormat is not None:
            namespaceprefix_ = self.LogoImageFormat_nsprefix_ + ':' if (UseCapturedNS_ and self.LogoImageFormat_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLogoImageFormat>%s</%sLogoImageFormat>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LogoImageFormat), input_name='LogoImageFormat')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'LogoImage':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'LogoImage')
            else:
                bval_ = None
            self.LogoImage = bval_
            self.LogoImage_nsprefix_ = child_.prefix
            # validate type LogoImage
            self.validate_LogoImage(self.LogoImage)
        elif nodeName_ == 'LogoImageFormat':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LogoImageFormat')
            value_ = self.gds_validate_string(value_, node, 'LogoImageFormat')
            self.LogoImageFormat = value_
            self.LogoImageFormat_nsprefix_ = child_.prefix
            # validate type LogoImageFormat
            self.validate_LogoImageFormat(self.LogoImageFormat)
# end class CustomerLogo


class EventRemarks(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, FurtherDetails=None, NextSteps=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.FurtherDetails = FurtherDetails
        self.validate_FurtherDetails(self.FurtherDetails)
        self.FurtherDetails_nsprefix_ = None
        self.NextSteps = NextSteps
        self.validate_NextSteps(self.NextSteps)
        self.NextSteps_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EventRemarks)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EventRemarks.subclass:
            return EventRemarks.subclass(*args_, **kwargs_)
        else:
            return EventRemarks(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_FurtherDetails(self):
        return self.FurtherDetails
    def set_FurtherDetails(self, FurtherDetails):
        self.FurtherDetails = FurtherDetails
    def get_NextSteps(self):
        return self.NextSteps
    def set_NextSteps(self, NextSteps):
        self.NextSteps = NextSteps
    def validate_FurtherDetails(self, value):
        result = True
        # Validate type FurtherDetails, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_NextSteps(self, value):
        result = True
        # Validate type NextSteps, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def hasContent_(self):
        if (
            self.FurtherDetails is not None or
            self.NextSteps is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EventRemarks', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EventRemarks')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EventRemarks':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EventRemarks')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EventRemarks', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EventRemarks'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EventRemarks', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.FurtherDetails is not None:
            namespaceprefix_ = self.FurtherDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.FurtherDetails_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFurtherDetails>%s</%sFurtherDetails>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FurtherDetails), input_name='FurtherDetails')), namespaceprefix_ , eol_))
        if self.NextSteps is not None:
            namespaceprefix_ = self.NextSteps_nsprefix_ + ':' if (UseCapturedNS_ and self.NextSteps_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNextSteps>%s</%sNextSteps>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NextSteps), input_name='NextSteps')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'FurtherDetails':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FurtherDetails')
            value_ = self.gds_validate_string(value_, node, 'FurtherDetails')
            self.FurtherDetails = value_
            self.FurtherDetails_nsprefix_ = child_.prefix
            # validate type FurtherDetails
            self.validate_FurtherDetails(self.FurtherDetails)
        elif nodeName_ == 'NextSteps':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NextSteps')
            value_ = self.gds_validate_string(value_, node, 'NextSteps')
            self.NextSteps = value_
            self.NextSteps_nsprefix_ = child_.prefix
            # validate type NextSteps
            self.validate_NextSteps(self.NextSteps)
# end class EventRemarks


class WeightType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Weight=None, WeightUnit=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Weight = Weight
        self.validate_Weight(self.Weight)
        self.Weight_nsprefix_ = None
        self.WeightUnit = WeightUnit
        self.validate_WeightUnit(self.WeightUnit)
        self.WeightUnit_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, WeightType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if WeightType.subclass:
            return WeightType.subclass(*args_, **kwargs_)
        else:
            return WeightType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def get_WeightUnit(self):
        return self.WeightUnit
    def set_WeightUnit(self, WeightUnit):
        self.WeightUnit = WeightUnit
    def validate_Weight(self, value):
        result = True
        # Validate type Weight, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if value > 999999.9:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on Weight' % {"value": value, "lineno": lineno} )
                result = False
            if len(str(value)) >= 7:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on Weight' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_WeightUnit(self, value):
        result = True
        # Validate type WeightUnit, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['K', 'L']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on WeightUnit' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on WeightUnit' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Weight is not None or
            self.WeightUnit is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WeightType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('WeightType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'WeightType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='WeightType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='WeightType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='WeightType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WeightType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeight>%s</%sWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Weight, input_name='Weight'), namespaceprefix_ , eol_))
        if self.WeightUnit is not None:
            namespaceprefix_ = self.WeightUnit_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightUnit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeightUnit>%s</%sWeightUnit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WeightUnit), input_name='WeightUnit')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Weight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Weight')
            fval_ = self.gds_validate_decimal(fval_, node, 'Weight')
            self.Weight = fval_
            self.Weight_nsprefix_ = child_.prefix
            # validate type Weight
            self.validate_Weight(self.Weight)
        elif nodeName_ == 'WeightUnit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WeightUnit')
            value_ = self.gds_validate_string(value_, node, 'WeightUnit')
            self.WeightUnit = value_
            self.WeightUnit_nsprefix_ = child_.prefix
            # validate type WeightUnit
            self.validate_WeightUnit(self.WeightUnit)
# end class WeightType


class LicenseType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, LicenseNumber=None, ExpiryDate=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.LicenseNumber = LicenseNumber
        self.validate_LicenseNumber(self.LicenseNumber)
        self.LicenseNumber_nsprefix_ = None
        if isinstance(ExpiryDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ExpiryDate, '%Y-%m-%d').date()
        else:
            initvalue_ = ExpiryDate
        self.ExpiryDate = initvalue_
        self.ExpiryDate_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LicenseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LicenseType.subclass:
            return LicenseType.subclass(*args_, **kwargs_)
        else:
            return LicenseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_LicenseNumber(self):
        return self.LicenseNumber
    def set_LicenseNumber(self, LicenseNumber):
        self.LicenseNumber = LicenseNumber
    def get_ExpiryDate(self):
        return self.ExpiryDate
    def set_ExpiryDate(self, ExpiryDate):
        self.ExpiryDate = ExpiryDate
    def validate_LicenseNumber(self, value):
        result = True
        # Validate type LicenseNumber, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 16:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on LicenseNumber' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.LicenseNumber is not None or
            self.ExpiryDate is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LicenseType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LicenseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LicenseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LicenseType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LicenseType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LicenseType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LicenseType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.LicenseNumber is not None:
            namespaceprefix_ = self.LicenseNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.LicenseNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLicenseNumber>%s</%sLicenseNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LicenseNumber), input_name='LicenseNumber')), namespaceprefix_ , eol_))
        if self.ExpiryDate is not None:
            namespaceprefix_ = self.ExpiryDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ExpiryDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExpiryDate>%s</%sExpiryDate>%s' % (namespaceprefix_ , self.gds_format_date(self.ExpiryDate, input_name='ExpiryDate'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'LicenseNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LicenseNumber')
            value_ = self.gds_validate_string(value_, node, 'LicenseNumber')
            self.LicenseNumber = value_
            self.LicenseNumber_nsprefix_ = child_.prefix
            # validate type LicenseNumber
            self.validate_LicenseNumber(self.LicenseNumber)
        elif nodeName_ == 'ExpiryDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.ExpiryDate = dval_
            self.ExpiryDate_nsprefix_ = child_.prefix
# end class LicenseType


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
        rootTag = 'KnownTrackingRequest'
        rootClass = KnownTrackingRequest
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
        rootTag = 'KnownTrackingRequest'
        rootClass = KnownTrackingRequest
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
        rootTag = 'KnownTrackingRequest'
        rootClass = KnownTrackingRequest
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
        rootTag = 'KnownTrackingRequest'
        rootClass = KnownTrackingRequest
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from tracking_request_known_1_0 import *\n\n')
        sys.stdout.write('import tracking_request_known_1_0 as model_\n\n')
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
    "AWBInfo",
    "BarCodes",
    "Billing",
    "Commodity",
    "Condition",
    "Consignee",
    "Contact",
    "Customer",
    "CustomerLogo",
    "DataTypes",
    "DestinationServiceArea",
    "DocImage",
    "DocImages",
    "Dutiable",
    "Email",
    "ErrorResponse",
    "EventRemarks",
    "ExportDeclaration",
    "ExportLineItem",
    "Fault",
    "KnownTrackingRequest",
    "Label",
    "LabelImage",
    "LicenseType",
    "Note",
    "OriginServiceArea",
    "Piece",
    "PieceDetails",
    "PieceEvent",
    "PieceFault",
    "PieceInfo",
    "Pieces",
    "Place",
    "QtdSInAdCur",
    "Reference",
    "Request",
    "Response",
    "ResponseServiceHeader",
    "ServiceArea",
    "ServiceEvent",
    "ServiceHeader",
    "ShipValResponsePiece",
    "ShipValResponsePieces",
    "Shipment",
    "ShipmentDate",
    "ShipmentDetails",
    "ShipmentEvent",
    "ShipmentInfo",
    "Shipper",
    "SpecialService",
    "Status",
    "TrackingPieces",
    "WeightSeg",
    "WeightType"
]
