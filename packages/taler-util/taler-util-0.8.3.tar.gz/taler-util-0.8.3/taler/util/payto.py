# This file is part of GNU Taler
# (C) 2017-2020 Taler Systems SA
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later
# version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301  USA
#
# @author Marcello Stanisci
# @version 0.1
# @repository https://git.taler.net/taler-util.git/

import re
from urllib.parse import urlparse, parse_qsl
from .amount import Amount

class PaytoFormatError(Exception):
    def __init__(self, msg):
        super(PaytoFormatError, self).__init__(msg)
        self.msg = msg

class PaytoParse:
    def __init__(self, payto_uri):
        obj = urlparse(payto_uri)
        path = obj.path.split("/")
        if obj.scheme != "payto" or \
                len(path) != 3 or \
                not obj.netloc or \
                not re.match("^payto://", payto_uri):
            raise PaytoFormatError(f"Bad Payto URI: {payto_uri}")
        self.target = path.pop()
        self.bank = path.pop()
        self.authority = obj.netloc
        params = dict(parse_qsl(obj.query))
        self.message = params.get("message")
        self.amount = Amount.parse(params.get("amount")) if "amount" in params else None
