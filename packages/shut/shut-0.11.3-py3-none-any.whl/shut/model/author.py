# -*- coding: utf8 -*-
# Copyright (c) 2020 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from databind.core import datamodel
import re


@datamodel
class Author:
  """
  Represents information about an author. Can be deserialized from a string of the form
  `Name <user@domain.name>`
  """

  AUTHOR_EMAIL_REGEX = re.compile(r'([^<]+)<([^>]+)>')
  name: str
  email: str

  @classmethod
  def parse(cls, string: str) -> 'Author':
    match = Author.AUTHOR_EMAIL_REGEX.match(string)
    if not match:
      raise ValueError('not a valid author string: {!r}'.format(string))
    name = match.group(1).strip()
    email = match.group(2).strip()
    return cls(name, email)

  def __str__(self):
    return '{} <{}>'.format(self.name, self.email)

  @classmethod
  def databind_json_load(cls, value, context):
    if isinstance(value, str):
      return cls.parse(value)
    return NotImplemented

  def databind_json_dump(self, context):
    return str(self)
