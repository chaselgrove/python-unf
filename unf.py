# See file COPYING distributed with unf for copyright and license.

import hashlib

class UNF:

    def __init__(self, data, digits=7):
        self.version = 6
        self.data = data
        self.digits = digits
        self.characters = 128
        if data is None:
            self._string = self._normalize_none(self.data)
        elif isinstance(data, basestring):
            self._string = self._normalize_basestring(self.data)
        else:
            raise TypeError('unsupported type for data')
        h = hashlib.sha256(self._string)
        self.hash = h.digest()
        self.unf = self.hash[:16].encode('base64').rstrip('\n')
        self.formatted = 'UNF:%d:%s' % (self.version, self.unf)
        return

    def __str__(self):
        return self.formatted

    def _normalize_none(self, data):
        return '\0\0\0'

    def _normalize_basestring(self, data):
        return data.encode('utf-8')[:self.characters] + '\n\0'

# eof
