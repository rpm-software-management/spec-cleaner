import logging
import re

from .rpmexception import NoMatchExceptionError
from .rpmrequirestoken import RpmRequiresToken

chunk_types = ('text', 'space', 'macro', 'operator', 'version')

state_types = ('start', 'name', 'operator', 'version')

re_brackets = {}
re_brackets['('] = re.compile(
    r'(' + r'\(' + r'|' + r'\)' + r'|' + r'\\(' + r'|' + r'\\)' + r'|' + r'[^\()]+' + r')'
)

re_brackets['{'] = re.compile(
    r'(' + r'\{' + r'|' + r'\}' + r'|' + r'\\{' + r'|' + r'\\}' + r'|' + r'[^\{}]+' + r')'
)

re_name = re.compile(r'[-A-Za-z0-9_~(){}@:;.+/*\[\]]+')
re_version = re.compile(r'[-A-Za-z0-9_~():.+]+')
re_spaces = re.compile(r'(\s*,\s*|\s+)')
re_macro_unbraced = re.compile('%[A-Za-z0-9_]{3,}')
re_version_operator = re.compile('(>=|<=|=>|=<|>|<|=)')

logger = logging.getLogger('DepParser')
# Switch to logging.DEBUG if needed
logger.setLevel(logging.ERROR)


def find_end_of_bracketed_macro(string, regex, opening, closing):
    """Find the end of bracketed macros."""
    # ommit the initial bracket, or %bracket
    if string.startswith('%'):
        macro = string[0:2]
        string = string[2:]
    else:
        macro = string[0:1]
        string = string[1:]
    opened = 1
    while opened and string:
        try:
            bite, string = consume_chars(regex, string)
        except NoMatchExceptionError:
            raise Exception('unexpected parser error when looking for end of macro')

        if bite == opening:
            opened += 1
        elif bite == closing:
            opened -= 1
        macro += bite

    if opened:
        raise Exception('Unexpectedly met end of string when looking for end of macro')
    return macro, string


def consume_chars(regex, string):
    """Consume regex matches of all characters of a string."""
    match = regex.match(string)
    if match:
        end = match.end()
        return string[0:end], string[end:]
    else:
        raise NoMatchExceptionError(
            'Expected match failed (string: "%s", regex: "%s" )' % (string, regex.pattern)
        )


def read_boolean(string):
    """Read boolean macros."""
    return find_end_of_bracketed_macro(string, re_brackets['('], '(', ')')


def matching_bracket(bracket):
    """Find the appropriate matching brackets."""
    if bracket == '{':
        return '}'
    elif bracket == '(':
        return ')'
    raise Exception(
        'Undefined bracket matching - add defintion of "%s" to ' 'matching_bracket()' % bracket
    )


def read_macro(string):
    """Read macro in brackets."""
    opening = string[1]
    closing = matching_bracket(opening)
    return find_end_of_bracketed_macro(string, re_brackets[opening], opening, closing)


def read_next_chunk(string):
    """Read string chunks after operators."""
    chunk = ''
    chunk_type = ''

    if not string:
        return '', '', 'text'

    if string[0:2] in ('>=', '<=', '=>', '=<'):
        chunk = string[0:2]
        chunk_type = 'operator'
        rest = string[2:]

    elif string[0:1] in ('<', '>', '='):
        chunk = string[0:1]
        chunk_type = 'operator'
        rest = string[1:]

    elif string[0].isspace() or string[0] == ',':
        chunk = ''
        chunk_type = 'space'
        rest = consume_chars(re_spaces, string)[1]

    elif string[0:2] == '%%':
        chunk = '%%'
        chunk_type = 'text'
        rest = string[2:]

    elif string[0:2] in ('%{', '%('):
        chunk, rest = read_macro(string)
        chunk_type = 'macro'

    elif string[0] == '%':
        chunk, rest = consume_chars(re_macro_unbraced, string)
        chunk_type = 'macro'

    elif string[0] == '(':
        chunk, rest = read_boolean(string)
        chunk_type = 'macro'

    else:
        chunk, rest = consume_chars(re_name, string)
        chunk_type = 'text'

    return (rest, chunk, chunk_type)


class DepParserError(Exception):
    """Exception definition for dependency parsing."""

    pass


class DependencyParser:
    """Dependency parsing class."""

    def __init__(self, line):
        """Initialize class."""
        # adding comma will cause flush in the end of line
        self.string = line + ', '
        self.parsed = []
        self.token = []
        self.state = 'start'
        self.space = False
        self.token_name = ''
        self.token_operator = None
        self.token_version = None
        self.go_on = True
        while self.go_on:
            self.string, self.next, self.next_type = read_next_chunk(self.string)
            logger.debug(
                """========
                chunk: '%s'
                chunk_type: '%s'
                rest: '%s'
                token: '%s'
                parsed: '%s'""",
                self.next,
                self.next_type,
                self.string,
                self.token,
                self.parsed,
            )
            self.state_change()

    def flat_out(self):
        """Flatten versioned definition to a single string."""
        result = []
        for name, operator, ver in self.parsed:
            result.append(RpmRequiresToken(name, operator, ver))
        return result

    def flush(self):
        """Clean token variables of the class."""
        self.parsed.append((self.token_name, self.token_operator, self.token_version))
        # cleanup state
        self.token = []
        self.token_name = ''
        self.token_operator = None
        self.token_version = None
        if not self.string:
            self.go_on = False

    def reconstitute_token(self):
        """Erase token."""
        r = ''.join(self.token)
        logger.debug("reconstituting '%s'", r)
        self.token = []
        return r

    def name_state_change(self):
        """Check name of next token."""
        if self.next_type in ['text', 'macro']:
            if self.space:
                logger.debug('text after space --> flush')
                self.token_name = self.reconstitute_token()
                self.space = False
                self.flush()
        elif self.next_type == 'space':
            self.space = True
        elif self.next_type == 'operator':
            self.token_name = self.reconstitute_token()
            self.state = 'operator'
            self.space = False

        self.token.append(self.next)

    def operator_state_change(self):
        """Check next operator token."""
        if self.next_type in ['text', 'macro']:
            self.state = 'version'
            self.token_operator = self.reconstitute_token()
            self.space = False
        elif self.next_type == 'space':
            self.space = True
        elif self.next_type == 'operator':
            if self.space:
                raise DepParserError('found operator after operator')

        self.token.append(self.next)

    def version_state_change(self):
        """Check valid token after version."""
        if self.next_type == 'text':
            pass
        elif self.next_type == 'space':
            self.token_version = self.reconstitute_token()
            self.flush()
            self.state = 'name'
            self.space = False
        elif self.next_type == 'macro':
            pass
        elif self.next_type == 'operator':
            raise DepParserError('found operator after version')

        self.token.append(self.next)

    def start_state_change(self):
        """Check next token valid for starting definition."""
        if self.next_type == 'text':
            self.state = 'name'
        elif self.next_type == 'space':
            pass
        elif self.next_type == 'macro':
            self.state = 'name'
        elif self.next_type == 'operator':
            raise DepParserError('found operator when name expected')

        self.token.append(self.next)

    def state_change(self):
        """Select which state change to check."""
        if self.state == 'name':
            self.name_state_change()
        elif self.state == 'operator':
            self.operator_state_change()
        elif self.state == 'version':
            self.version_state_change()
        elif self.state == 'start':
            self.start_state_change()
        logger.debug('new state: %s', self.state)
