# Copyright 2021 SAP SE
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import os

import manhole
from oslo_middleware import base
from oslo_service import _options as oslo_opts


LOG = logging.getLogger(__name__)

class Manhole(base.ConfigurableMiddleware):
    """Middleware that provides in-process service that will accept unix domain socket connections.

    Manhole is in-process service that will accept unix domain socket connections and present the stacktraces for
    all threads and an interactive prompt. It can either work as a python daemon thread waiting for connections
    at all times or a signal handler (stopping your application and waiting for a connection).
    """

    def __init__(self, application, *args, **kwargs):
        super(Manhole, self).__init__(application, *args, **kwargs)
        self.oslo_conf.register_opts(oslo_opts.eventlet_backdoor_opts)

        if self.oslo_conf.backdoor_socket:
            try:
                backdoor_socket_path = self.oslo_conf.backdoor_socket.format(pid=os.getpid())
            except (KeyError, IndexError, ValueError) as e:
                backdoor_socket_path = self.oslo_conf.backdoor_socket
                LOG.debug("Could not apply format string to manhole "
                            "backdoor socket path ({}) - continuing with "
                            "unformatted path"
                            "".format(e))
            manhole.install(socket_path=backdoor_socket_path)
            LOG.debug("Backdoor socket (Manhole) provided at %s", backdoor_socket_path)
