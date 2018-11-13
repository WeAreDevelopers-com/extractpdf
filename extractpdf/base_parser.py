"""This module is the base class for the Parser
"""

import six
import chardet

from . import exceptions


class BaseParser(object):
    """The :class:`.BaseParser` abstracts out some common functionality
    that is used across all document Parsers. In particular, it has
    the responsibility of handling all unicode and byte-encoding.
    """

    def extract(self, filename, method='', **kwargs):
        """This method must be overwritten by child classes to extract raw
        text from a filename. This method can return either a
        byte-encoded string or unicode.
        """
        raise NotImplementedError('must be overwritten by child classes')

    @classmethod
    def encode(cls, text, encoding):
        """Encode the ``text`` in ``encoding`` byte-encoding. This ignores
        code points that can't be encoded in byte-strings.
        """
        return text.encode(encoding, 'ignore')

    def process(self, filename, encoding, **kwargs):
        """Process ``filename`` and encode byte-string with ``encoding``. This
        method is called by :func:`pdfextract.parsers.process` and wraps
        the :meth:`.BaseParser.extract` method in `a delicious unicode
        sandwich <http://nedbatchelder.com/text/unipain.html>`_.

        """
        # make a "unicode sandwich" to handle dealing with unknown
        # input byte strings and converting them to a predictable
        # output encoding
        # http://nedbatchelder.com/text/unipain/unipain.html#35
        byte_string = self.extract(filename, **kwargs)
        unicode_string = self.decode(byte_string)
        return self.encode(unicode_string, encoding)

    @classmethod
    def decode(cls, text):
        """Decode ``text`` using the `chardet
        <https://github.com/chardet/chardet>`_ package.
        """
        # only decode byte strings into unicode if it hasn't already
        # been done by a subclass
        if isinstance(text, six.text_type):
            return text

        # empty text? nothing to decode
        if not text:
            return u''

        # use chardet to automatically detect the encoding text
        result = chardet.detect(text)
        encoding = result['encoding']
        if result['confidence'] < 0.6:
            encoding ='utf-8'
        return text.decode(encoding)

