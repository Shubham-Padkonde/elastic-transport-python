#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import asyncio
from unittest.mock import AsyncMock, Mock

import pytest

from elastic_transport import AsyncTransport, NodeConfig, TlsError, Transport
from tests.conftest import AsyncDummyNode, DummyNode


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("retries", [0, 2])
def test_retry_errors_preserve_final_cause(asynchronous, retries):
    causes = [ValueError(f"certificate failure {i}") for i in range(retries + 1)]
    failures = [TlsError("TLS failed", errors=(cause,)) for cause in causes]
    transport = (AsyncTransport if asynchronous else Transport)(
        [NodeConfig("https", "localhost", 443)],
        node_class=AsyncDummyNode if asynchronous else DummyNode,
        max_retries=retries,
        retry_backoff_base=0,
    )
    node = transport.node_pool.all()[0]
    node.perform_request = (AsyncMock if asynchronous else Mock)(side_effect=failures)
    with pytest.raises(TlsError) as caught:
        if asynchronous:
            asyncio.run(transport.perform_request("GET", "/"))
        else:
            transport.perform_request("GET", "/")
    assert caught.value.errors == tuple(reversed(failures))
    assert [error.errors[0] for error in caught.value.errors] == list(reversed(causes))
    assert all(error is not caught.value for error in caught.value.errors)
