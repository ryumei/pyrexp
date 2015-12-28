# -*- coding:utf-8 -*-

import re

class PyRExp(object):
    u"""regex wrapper like Perl"""

    def __init__(self, caching=True):
        u"""Argument:
* cache: Disable/Enable pattern caching"""
        self.caching = caching
        if caching:
            self.patterns = {}
        
    def _key(self, pattern_str, option_flag):
        return u'%s()%d' % (pattern_str, option_flag)

    def _retrieve_pattern(self, pattern_str, option_flag):
        k = self._key(pattern_str, option_flag)
        if self.caching and (k in self.patterns):
            pat = self.patterns[k]
        else:
            pat = re.compile(pattern_str, option_flag)
            if self.caching:
                self.patterns[k] = pat
        return pat
    
    def _option_flag(self, i, options):
        if i and not (re.IGNORECASE in options):
            options += (re.IGNORECASE,)        
        return reduce(lambda a, b: a + b, options, 0)
    
    def m(self, string, pattern, i=False, options=()):
        u"""matching like "string" =~ /pattern/

        * i: ignore case (re.IGNORECASE)
        * options: tuple of regexp options of python (such as re.L, re.M)
        
        Simple mathing
        >>> PyRExp().m(u'abc', u'def') is None
        True
        >>> PyRExp().m(u'abc', u'^a').group()
        u'a'

        Multibytes matching
        期待値「u'いろ'」は、Unicode かつエスケープして表現しています。
        >>> PyRExp().m(u'いろは', u'^いろ').group()
        u'\\u3044\\u308d'
        
        Case sensitive/insensitive matching
        >>> PyRExp().m(u'abc', u'^ABC$') is None
        True
        >>> PyRExp().m(u'abc', u'^ABC$', i=True).group()
        u'abc'
        >>> PyRExp().m(u'abc', u'^ABC$', options=(re.I,)).group()
        u'abc'
        
        Grouping result of matching
        >>> PyRExp().m(u'2015-12-28T10:16:23+0900', u'^(\d{,4})-(\d{,2})-(\d{,2})T(\d{,2}):(\d{,2}):(\d{,2}(?:\.\d+)?)\+(\d{4})').groups()
        (u'2015', u'12', u'28', u'10', u'16', u'23', u'0900')
        >>> PyRExp().m(u'2015-12-28T10:16:23.123+0900', u'^(\d{,4})-(\d{,2})-(\d{,2})T(\d{,2}):(\d{,2}):(\d{,2}(?:\.\d+)?)\+(\d{4})').groups()
        (u'2015', u'12', u'28', u'10', u'16', u'23.123', u'0900')
        """
        
        pat = self._retrieve_pattern(pattern, self._option_flag(i, options))
        return pat.match(string)

    def s(self, string, pattern, replace, i=False, options=()):
        u"""Substitution like "string =~ s/pattern/replace/"
        
        Success matching and replacing
        >>> PyRExp().s(u'blue socks and red shoes', u'(blue|white|red)', u'colour')
        u'colour socks and colour shoes'
        
        Does not match and replace
        >>> PyRExp().s(u'blue socks and red shoes', u'(violette|orange|rainbow)', u'colour')
        u'blue socks and red shoes'

        Case insensitive matching
        >>> PyRExp().s(u'Blue socks and RED shoes', u'(blue|white|red)', u'colour', i=True)
        u'colour socks and colour shoes'

        """
        pat = self._retrieve_pattern(pattern, self._option_flag(i, options))
        
        return pat.sub(replace, string)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
