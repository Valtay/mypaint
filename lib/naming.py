# This file is part of MyPaint.
# Copyright (C) 2017 by the MyPaint Development Team.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

"""Stuff for making names and keeping them unique."""

import re
from lib.gettext import C_

# TRANSLATORS: UNIQUE_NAME_TEMPLATE. Must match its regex.
# TRANSLATORS: Leave this untranslated if you are unsure.
# TRANSLATORS: Change only if your lang *REQUIRES* a different order or
# TRANSLATORS: if raw digits and a space aren't enough.
UNIQUE_NAME_TEMPLATE = C_(
    "unique names: serial number needed: template",
    u'{name} {number}',
)

# TRANSLATORS: UNIQUE_NAME_REGEX. Must match its template.
# TRANSLATORS: Leave this untranslated if you are unsure.
UNIQUE_NAME_REGEX = re.compile(C_(
    "unique names: regex matching a string with a serial number",
    u'^(?P<name>.*?)\\s+(?P<number>\\d+)$',
))


def make_unique_name(name, existing, start=1, always_number=None):
    """Ensures that a name is unique.

    :param unicode name: Name to be made unique.
    :param existing: An existing list or set of names.
    :type existing: anything supporting ``in``
    :param int start: starting number for numbering.
    :param unicode always_number: always number if name is this value.
    :returns: A unique name.
    :rtype: unicode

    >>> existing = set([u"abc 1", u"abc 2", u"abc"])
    >>> make_unique_name(u"abc", existing)
    u'abc 3'
    >>> u'abc 3' not in existing
    True
    >>> make_unique_name(u"abc 1", existing)
    u'abc 3'

    Sometimes you may want a serial number every time if the given name
    is some specific value, normally a default. This allows your first
    item to be, for example, "Widget 1", not "Widget".

    >>> make_unique_name(u"xyz", {}, start=1, always_number=u"xyz")
    u'xyz 1'
    >>> make_unique_name(u"xyz", {}, start=2, always_number=u"xyz")
    u'xyz 2'

    """
    name = unicode(name)
    match = UNIQUE_NAME_REGEX.match(name)
    if match:
        base = match.group("name")
        num = int(match.group("number"))
    else:
        base = name
        num = max(0, int(start))
    force_numbering = (name == always_number)
    while (name in existing) or force_numbering:
        name = UNIQUE_NAME_TEMPLATE.format(name=base, number=num)
        num += 1
        force_numbering = False
    return name


assert UNIQUE_NAME_REGEX.match(
    UNIQUE_NAME_TEMPLATE.format(
        name="testing",
        number=12,
    )
), (
    "Translation error: lib.naming.UNIQUE_NAME_REGEX "
    "must match UNIQUE_NAME_TEMPLATE."
)
