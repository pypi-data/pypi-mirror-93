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


# Tests for experiment execution within Docker containers

import os
import subprocess  # nosec

import nose.tools

from beat.core.database import Database

from ..dock import Host
from ..execution import DockerExecutor
from . import DOCKER_NETWORK_TEST_ENABLED
from . import network_name
from . import prefix as test_prefix
from . import prefix_folder
from . import setup_root_db_folder
from .test_execution import BaseExecutionMixIn
from .utils import DOCKER_TEST_IMAGES
from .utils import cleanup
from .utils import skipif
from .utils import slow

BUILDER_CONTAINER_NAME = "docker.idiap.ch/beat/beat.env.builder/beat.env.cxxdev"
BUILDER_IMAGE = (
    BUILDER_CONTAINER_NAME + ":" + DOCKER_TEST_IMAGES[BUILDER_CONTAINER_NAME]
)

# ----------------------------------------------------------


def write_rawdata_for_database(database_name, raw_data):
    """Generate raw data for give database"""

    db = Database(test_prefix, database_name)
    nose.tools.assert_true(db.valid, db.errors)

    data_sharing_path = db.data["root_folder"]

    with open(os.path.join(data_sharing_path, "datafile.txt"), "wt") as data_file:
        data_file.write("{}".format(raw_data))


# ----------------------------------------------------------


class TestDockerExecution(BaseExecutionMixIn):
    @classmethod
    def setup_class(cls):
        cls.host = Host(raise_on_errors=False)

    @classmethod
    def teardown_class(cls):
        cls.host.teardown()
        cleanup()

    def teardown(self):
        self.host.teardown()

    def create_executor(
        self,
        prefix,
        configuration,
        tmp_prefix,
        dataformat_cache,
        database_cache,
        algorithm_cache,
    ):
        executor = DockerExecutor(
            self.host,
            prefix,
            configuration,
            tmp_prefix,
            dataformat_cache,
            database_cache,
            algorithm_cache,
        )

        executor.debug = os.environ.get("DOCKER_TEST_DEBUG", False) == "True"
        return executor

    def build_algorithm(self, algorithm):
        test_folder = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        scripts_folder = os.path.abspath(os.path.join(test_folder, "scripts"))
        sources_folder = os.path.abspath(os.path.join(test_folder, algorithm))
        cmd = ["/build.sh"]
        builder_container = self.host.create_container(BUILDER_IMAGE, cmd)
        builder_container.add_volume("%s/build.sh" % scripts_folder, "/build.sh")
        builder_container.add_volume(sources_folder, "/sources", read_only=False)
        builder_container.uid = os.getuid()
        builder_container.set_workdir("/sources")
        builder_container.set_entrypoint("bash")

        self.host.start(builder_container)
        status = self.host.wait(builder_container)
        if status != 0:
            print(self.host.logs(builder_container))

        self.host.rm(builder_container)
        nose.tools.eq_(status, 0)

        # Update the tmp prefix with the latest content
        subprocess.check_call(  # nosec
            [
                "rsync",
                "-arz",
                '--exclude="*"',
                '--include="*.so"',
                os.path.join(test_folder, "prefix"),
                prefix_folder,
            ]
        )

        setup_root_db_folder()

    @slow
    @skipif(not DOCKER_NETWORK_TEST_ENABLED, "Network test disabled")
    def test_custom_network(self):
        result = self.execute(
            "user/user/integers_addition/1/integers_addition",
            [{"sum": 495, "nb": 9}],
            network_name=network_name,
        )

        nose.tools.assert_is_none(result)

    @slow
    def test_custom_port_range(self):
        result = self.execute(
            "user/user/integers_addition/1/integers_addition",
            [{"sum": 495, "nb": 9}],
            port_range="50000:50100",
        )

        nose.tools.assert_is_none(result)

    @slow
    def test_database_rawdata_access(self):
        offset = 12

        write_rawdata_for_database("simple_rawdata_access/1", offset)

        result = self.execute(
            "user/user/single/1/single_rawdata_access", [{"out_data": 42 + offset}]
        )

        nose.tools.assert_is_none(result)

    @slow
    def test_database_no_rawdata_access(self):
        write_rawdata_for_database("simple/1", "should not be loaded")

        result = self.execute("errors/user/single/1/single_no_rawdata_access", [None])

        nose.tools.eq_(result["status"], 1)
        nose.tools.assert_true("FileNotFoundError" in result["user_error"])

    @slow
    def test_single_1_prepare_error(self):
        result = self.execute("errors/user/single/1/prepare_error", [None])

        nose.tools.eq_(result["status"], 1)
        nose.tools.eq_(
            result["user_error"], "'Could not prepare algorithm (returned False)'"
        )

    @slow
    def test_single_1_setup_error(self):
        result = self.execute("errors/user/single/1/setup_error", [None])

        nose.tools.eq_(result["status"], 1)
        nose.tools.eq_(
            result["user_error"], "'Could not setup algorithm (returned False)'"
        )

    # NOT COMPATIBLE YET WITH THE NEW API
    # @slow
    # def test_cxx_double_1(self):
    #     assert self.execute('user/user/double/1/cxx_double', [{'out_data': 42}]) is None

    @slow
    def test_cxx_double_legacy(self):
        datasets_uid = os.getuid()
        self.build_algorithm("prefix/algorithms/user/cxx_integers_echo_legacy")

        result = self.execute(
            "user/user/double/1/cxx_double_legacy",
            [{"out_data": 42}],
            datasets_uid=datasets_uid,
        )
        nose.tools.assert_is_none(result)

    @slow
    def test_cxx_double_sequential(self):
        datasets_uid = os.getuid()
        self.build_algorithm("prefix/algorithms/user/cxx_integers_echo_sequential")

        nose.tools.assert_is_none(
            self.execute(
                "user/user/double/1/cxx_double_sequential",
                [{"out_data": 42}],
                datasets_uid=datasets_uid,
            )
        )

    @slow
    def test_cxx_double_offsetting_sequential(self):
        datasets_uid = os.getuid()
        self.build_algorithm("prefix/algorithms/user/cxx_integers_offsetter_sequential")

        nose.tools.assert_is_none(
            self.execute(
                "user/user/double/1/cxx_offsetting_sequential",
                [{"out_data": 77}],
                datasets_uid=datasets_uid,
            )
        )

    @slow
    def test_cxx_double_autonomous(self):
        datasets_uid = os.getuid()
        self.build_algorithm("prefix/algorithms/user/cxx_integers_echo_autonomous")

        nose.tools.assert_is_none(
            self.execute(
                "user/user/double/1/cxx_double_autonomous",
                [{"out_data": 42}],
                datasets_uid=datasets_uid,
            )
        )

    @slow
    def test_cxx_analyzer_error(self):
        datasets_uid = os.getuid()
        needed_alorithms = [
            "cxx_integers_echo_sequential",
            "cxx_integers_echo_analyzer",
        ]

        for algorithm in needed_alorithms:
            self.build_algorithm("prefix/algorithms/user/%s" % algorithm)

        result = self.execute(
            "errors/user/double/1/cxx_analyzer_error",
            [{"out_data": 42}],
            datasets_uid=datasets_uid,
        )

        nose.tools.eq_(result["status"], 255)
        nose.tools.assert_true(
            "[sys] C++ algorithm can't be analyzers" in result["stderr"]
        )

    @slow
    def test_read_only_error(self):
        result = self.execute("errors/user/single/1/write_error", [{"out_data": 42}])

        nose.tools.eq_(result["status"], 1)
        nose.tools.assert_true("Read-only" in result["user_error"])

    @slow
    def test_user_mismatch_error(self):
        result = self.execute(
            "errors/user/single/1/write_error", [{"out_data": 42}], datasets_uid=0
        )

        nose.tools.eq_(result["status"], 1)
        nose.tools.assert_true("Failed to create an user" in result["stderr"])

    @slow
    def test_loop_mix_db_env_error(self):
        with nose.tools.assert_raises(RuntimeError) as context:
            self.execute(
                "errors/user/loop/1/loop_mix_db_env", [None],
            )

        nose.tools.assert_true(
            "are not all providing an environment" in context.exception.args[0]
        )

    @slow
    def test_loop_two_db_env_error(self):
        with nose.tools.assert_raises(RuntimeError) as context:
            self.execute(
                "errors/user/loop/1/loop_two_db_environments", [None],
            )

        nose.tools.assert_true(
            "are requesting different environments" in context.exception.args[0]
        )

    @slow
    def test_single_not_existing_db_env_error(self):
        with nose.tools.assert_raises(RuntimeError) as context:
            self.execute(
                "errors/user/single/1/not_existing_db_env", [None],
            )

        nose.tools.assert_true(
            "not found - available environments are" in context.exception.args[0]
        )

    @slow
    def test_loop_1_two_db_env(self):
        nose.tools.assert_is_none(
            self.execute(
                "user/user/loop/1/loop_two_db_env",
                [{"sum": 135, "nb": 9}, {"sum": 9, "nb": 9}],
            )
        )
