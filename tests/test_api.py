from mock import Mock, patch
from pytest import fixture

from pwned_password_checker.api import get_password_results


@fixture
def mocked_request_result():
    mock = Mock
    mock.text = """0018A45C4D1DEF81644B54AB7F969B88D65:3
00D4F6E8FA6EECAD2A3AA415EEC418D38EC:3
011053FD0102E94D6AE2F8B83D76FAF94F6:1
012A7CA357541F0AC487871FEEC1891C49C:3
0136E006E24E7D152139815FB0FC6A50B15:4
01561D5D4D893ADDA894DD9484C145323E3:1
017E166DC997380CA0E599165FBDD311D15:1
01A85766CD276B17DE6DA022AA3CADAC3CE:4"""
    return mock


@patch("pwned_password_checker.api.requests.get")
def test_get_password_result_appears_in_api_result(mocked_get, mocked_request_result):
    mocked_get.return_value = mocked_request_result

    result = get_password_results("21BD10018A45C4D1DEF81644B54AB7F969B88D65")
    assert result == 3


@patch("pwned_password_checker.api.requests.get")
def test_get_password_result_does_not_appear_in_api_result(mocked_get, mocked_request_result):
    mocked_get.return_value = mocked_request_result

    result = get_password_results("21BD10018A45C4D1DEF81644B54AB7F969B8aewf")
    assert result == 0
