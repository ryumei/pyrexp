# pyrexp
regex wrapper like Perl

[Takaaki Nakajima](ryumei@users.noreply.github.com)

* `m(string, pattern)` for matching `string =~ /pattern/`
* `s(string, pattern, replace)` for substitution `string =~ s/pattern/replace/`.


## Usage

```
>>> from pyrexp import PyRExp
>>> regex = PyRExp()
>>> regex.m(u"192.168.99.100", u"(\d+)\.(\d+)\.(\d+)\.(\d+)").groups()
(u'192', u'168', u'99', u'100')
>>> regex.s(u"A seasonal greeting 2014", u"\d{4}", u"2015")
u'A seasonal greeting 2015'
```
