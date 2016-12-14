"""RPM dependency lines parser and helpers.

Contains class DependencyParser which parses string and generates
token tree. For common manipulation is method flat_out() useful, it
just splits dependencies into list.

For future development is useful find_end_of_macro().

"""
import re
import logging

DEBUG = None

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)


def find_end_of_macro(string, opening, closing):
    if DEBUG:
        logger = logging.getLogger('DepParser')
    else:
        logger = None
    macro = string[0:2]
    # eat '%{'
    string = string[2:]

    # let's construct regexp matching one of following:
    #   one opening or closing paren
    #   escaped variants of one opening or close paren
    #   unlimited amount of anything else
    escaped_opening = '\\' + opening
    escaped_closing = '\\' + closing
    specials = [
        re.escape(opening), re.escape(closing),
        re.escape(escaped_opening), re.escape(escaped_closing),
        '[^\\' + opening + closing + ']+'
    ]
    regex = '(' + '|'.join(specials) + ')'
    opened = 1
    while opened and string:
        if logger:
            logger.debug('opened: %d string: %s', opened, string)
        try:
            bite, string = consume_chars(regex, string, logger)
        except NoMatchException:
            raise Exception('unexpected parser error when looking for end of '
                            'macro')

        if bite == opening:
            opened += 1
        elif bite == closing:
            opened -= 1
        macro += bite

    if opened:
        raise Exception('Unexpectedly met end of string when looking for end '
                        'of macro')
    return macro


def consume_chars(regex, string, logger=None):
    if logger:
        logger.debug('consume_chars: regex: "%s"', regex)
        logger.debug('consume_chars: string:"%s"', string)
    match = re.match(regex, string)
    if match:
        end = match.end()
        if logger:
            logger.debug('consume_chars: split "%s", "%s"', string[0:end], string[end:])
        return string[0:end], string[end:]
    else:
        raise NoMatchException('Expected match failed')


class NoMatchException(Exception):
    pass


class DependencyParser(object):

    RE_NAME = r'[-A-Za-z0-9_~():.+/]+'
    RE_VERSION = r'[-A-Za-z0-9_~():.+]+'
    logger = None

    def __init__(self, string):
        self.string = string.rstrip()
        self.token = []
        self.parsed = []
        self.state = ['name']
        if DEBUG:
            self.logger = logging.getLogger('DepParser')
            self.logger.setLevel(logging.DEBUG)
        self.state_change_loop()

    def dump_token(self):
        if self.logger:
            self.logger.debug('dump_token')
        self.status()
        if not self.token:
            return
        if self.token[0].isspace():
            self.token = self.token[1:]
            if not self.token:
                return
        self.parsed.append(self.token)
        self.token = []

    def state_change_loop(self):
        while self.string:
            if self.state[-1] == 'name':
                self.read_name()
            elif self.state[-1] == 'version_operator':
                self.read_version_operator()
            elif self.state[-1] == 'version':
                self.read_version()
            elif self.state[-1] == 'macro_name':
                self.read_macro_name()
            elif self.state[-1] == 'macro_shell':
                self.read_macro_shell()
            elif self.state[-1] == 'macro_unbraced':
                self.read_macro_unbraced()
            elif self.state[-1] == 'spaces':
                self.read_spaces()
        self.dump_token()

    def status(self):
        if self.logger:
            self.logger.debug('token: %s', self.token)
            self.logger.debug('string: "%s"', self.string)
            self.logger.debug('parsed: %s', self.parsed)
            self.logger.debug('state: %s', self.state)
            self.logger.debug('--------------------------------')

    def read_spaces(self, state_change=True):
        try:
            spaces, self.string = consume_chars(r'\s+', self.string, self.logger)
            self.token.append(spaces)
            if state_change:
                self.state.pop()  # remove 'spaces' state
                # if we were reading version, space definitely means
                # end of that
                if self.state[-1] == 'version':
                    self.state.pop()
                    self.dump_token()
            self.status()
        except NoMatchException:
            pass

    def read_unknown(self):
        '''
        Try to identify, what is to be read now.
        '''
        if self.string[0:2] in ['>=', '<=', '=>', '=<'] or \
                self.string[0:1] in ['<', '>', '=']:
            self.state.append('version')
            self.state.append('version_operator')
        elif self.string[0] == ' ':
            self.state.append('spaces')
        elif self.string[0:2] == '%{':
            self.state.append('macro_name')
        elif self.string[0:2] == '%(':
            self.state.append('macro_shell')
        elif self.string[0:2] == '%%':
            self.read_double_percent()
        elif self.string[0] == '%':
            self.state.append('macro_unbraced')
        elif self.string[0] == ',':
            self.string = self.string[1:]
            self.dump_token()
        if self.logger:
            self.logger.debug('read_unknown: states: %s string: "%s"',
                              self.state, self.string)

    def read_name(self):
        try:
            name, self.string = consume_chars(self.RE_NAME, self.string, self.logger)
            if self.token and self.token[-1].isspace():
                self.dump_token()
            self.token.append(name)
            self.status()
        except NoMatchException:
            self.read_unknown()

    def read_double_percent(self):
        self.token.append('%%')
        self.string = self.string[2:]

    def read_macro_unbraced(self):
        try:
            # 3 or more alphanumeric characters
            macro, self.string = consume_chars(
                '%[A-Za-z0-9_]{3,}', self.string, self.logger)
            # add braces to macro
#            macro = '%{' + macro[1:] + '}'
            self.token.append(macro)
            self.state.pop()  # remove 'macro_unbraced' state
            self.status()
        except NoMatchException:
            self.read_unknown()

    def read_version_operator(self):
        try:
            operator, self.string = consume_chars(
                '(>=|<=|=>|=<|>|<|=)', self.string, self.logger)
            self.token.append(operator)
            # Note: this part is a bit tricky, I need to read possible
            # spaces or tabs now so I won't get to [ ..., 'version',
            # 'spaces' ] state before the end
            self.read_spaces(state_change=False)
            self.state.pop()  # get rid of 'version_operator'
            self.status()
        except NoMatchException:
            self.read_unknown()

    def read_version(self):
        try:
            version, self.string = consume_chars(
                self.RE_VERSION, self.string, self.logger)
            self.token.append(version)
            self.status()
        except NoMatchException:
            self.read_unknown()

    def read_macro_name(self):
        macro = find_end_of_macro(self.string, '{', '}')
        # remove macro from string
        self.string = self.string[len(macro):]
        self.token.append(macro)
        # now we expect previous state
        self.state.pop()
        self.status()

    def read_macro_shell(self):
        if self.logger:
            self.logger.debug('read_macro_shell')
        macro = find_end_of_macro(self.string, '(', ')')
        self.string = self.string[len(macro):]
        self.token.append(macro)
        # now we expect previous state
        self.state.pop()
        self.status()

    def flat_out(self):
        result = []
        for token in self.parsed:
            if isinstance(token, list):
                if token and token[-1].isspace():
                    token = token[:-1]
                result.append(''.join(token))
            else:
                if not token.isspace():
                    result.append(token)
        return result
