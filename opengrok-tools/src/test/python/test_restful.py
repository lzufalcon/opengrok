#!/usr/bin/env python3

#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# See LICENSE.txt included in this distribution for the specific
# language governing permissions and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at LICENSE.txt.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#

#
# Copyright (c) 2019, Oracle and/or its affiliates. All rights reserved.
#

import pytest
from opengrok_tools.utils.restful import call_rest_api


def test_restful_verbs(monkeypatch):
    okay_status = 200

    class MockResponse:
        def __init__(self):
            self.status_code = okay_status

    def mock_response(command, uri, verb, headers, json_data):
        # Spying on mocked function is maybe too much so verify
        # the arguments here.
        assert uri == "http://localhost:8080/source/api/v1/BAR"
        assert json_data == '"fooBARbar"'

        return MockResponse()

    for verb in ["PUT", "POST", "DELETE"]:
        command = {"command": ["http://localhost:8080/source/api/v1/%FOO%",
                               verb, "foo%FOO%bar"]}
        pattern = "%FOO%"
        value = "BAR"
        with monkeypatch.context() as m:
            m.setattr("opengrok_tools.utils.restful.do_api_call",
                      mock_response)
            assert call_rest_api(command, pattern, value). \
                status_code == okay_status


def test_unknown_verb():
    command = {"command": ["http://localhost:8080/source/api/v1/foo",
                           "FOOBAR", "data"]}
    pattern = "%FOO%"
    value = "BAR"
    with pytest.raises(Exception):
        call_rest_api(command, pattern, value)
