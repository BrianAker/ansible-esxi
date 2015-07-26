# Copyright 2015 Brian Aker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

__author__ = "Brian Aker <brian@tangent.org>"
__copyright__ = "Copyright 2015 by Brian Aker <brian@tangent.org>"
__license__ = "BSD"

CHECK_FOR_DNS_RESOLVER=False
try:
    import dns.resolver
    from dns.exception import DNSException
    CHECK_FOR_DNS_RESOLVER=True
except ImportError:
    pass

from ansible import utils, errors
from ansible import __version__ as __ansible_version__
class LookupModule (object):
  def __init__(self, basedir=None, **kwargs):
    self.basedir = basedir

  def run(self, terms, inject=None, **kwargs):

    if CHECK_FOR_DNS_RESOLVER == False:
      raise errors.AnsibleError("Cannot resolve IP Addresss: module dns.resolver is not installed")
          
    terms = utils.listify_lookup_plugin_terms(terms, self.basedir, inject)
    ret = []

    if isinstance(terms, basestring):
      terms = [ terms ]

    for term in terms:
      hostname = term.split()[0]
      try:
        answers = dns.resolver.query(hostname, 'A')
        for rdata in answers:
          ret.append(''.join(rdata.to_text()))

      except dns.resolver.NXDOMAIN:
        string = 'NXDOMAIN'
      except dns.resolver.Timeout:
        string = ''
      except dns.exception.DNSException as e:
        raise errors.AnsibleError("dns.resolver unhandled exception", e)

    return ret
