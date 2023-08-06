#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###################################################################################
#                                                                                 #
# Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/               #
# Contact: beat.support@idiap.ch                                                  #
#                                                                                 #
# Redistribution and use in source and binary forms, with or without              #
# modification, are permitted provided that the following conditions are met:     #
#                                                                                 #
# 1. Redistributions of source code must retain the above copyright notice, this  #
# list of conditions and the following disclaimer.                                #
#                                                                                 #
# 2. Redistributions in binary form must reproduce the above copyright notice,    #
# this list of conditions and the following disclaimer in the documentation       #
# and/or other materials provided with the distribution.                          #
#                                                                                 #
# 3. Neither the name of the copyright holder nor the names of its contributors   #
# may be used to endorse or promote products derived from this software without   #
# specific prior written permission.                                              #
#                                                                                 #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND #
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED   #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE          #
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE    #
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL      #
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR      #
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER      #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,   #
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE   #
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.            #
#                                                                                 #
###################################################################################


import nose.tools

from ..database import Database
from . import prefix
from . import tmp_prefix
from .utils import cleanup


def test_export():
    for i in range(1, 3):
        yield export, f"integers_db/{i}"
        yield export, f"simple/{i}"
        yield export, f"large/{i}"
        yield export, f"simple_rawdata_access/{i}"


@nose.tools.with_setup(teardown=cleanup)
def export(db_name):

    obj = Database(prefix, db_name)
    nose.tools.assert_true(obj.valid, "\n  * %s" % "\n  * ".join(obj.errors))

    obj.export(tmp_prefix)

    # load from tmp_prefix and validates
    exported = Database(tmp_prefix, db_name)
    nose.tools.assert_true(exported.valid, "\n  * %s" % "\n  * ".join(exported.errors))


def test_rawdata_access():
    for i in range(1, 3):
        yield rawdata_access, f"integers_db/{i}", False
        yield rawdata_access, f"simple/{i}", False
        yield rawdata_access, f"large/{i}", False
        yield rawdata_access, f"simple_rawdata_access/{i}", True


@nose.tools.with_setup(teardown=cleanup)
def rawdata_access(db_name, rawdata_access_enabled):

    obj = Database(prefix, db_name)

    nose.tools.assert_true(obj.valid, "\n  * %s" % "\n  * ".join(obj.errors))
    nose.tools.assert_equal(
        obj.is_database_rawdata_access_enabled, rawdata_access_enabled
    )
