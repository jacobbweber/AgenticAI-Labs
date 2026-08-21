"""
Unit tests for MultiModelGatewayRouter (R5 Ollama Resilience)
"""

import urllib.error
from unittest.mock import MagicMock, call, patch

import pytest

from api.llm_gateway import MultiModelGatewayRouter


def test_llm_gateway_default_timeout_and_max_attempts():
    """Verifies that default timeout is >= 300s and max_attempts defaults to 5."""
    router = MultiModelGatewayRouter(
        ollama_host="http://192.168.1.29:11434", default_model="qwen3.6:35b-a3b-65k"
    )
    assert router.timeout >= 300
    assert router.max_attempts == 5


@patch("urllib.request.urlopen")
@patch("time.sleep")
def test_llm_gateway_exponential_backoff_and_runtime_error(mock_sleep, mock_urlopen, capsys):
    """
    Mocks Ollama failure across all retries.
    Verifies that:
    1. 5 retry attempts are made.
    2. Exponential backoff (5s, 15s, 45s, 135s) occurs between retries.
    3. Terminal output logs retry attempt details and sleep durations.
    4. A RuntimeError is raised when retries are exhausted (no silent fallback).
    """
    mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

    router = MultiModelGatewayRouter(
        ollama_host="http://192.168.1.29:11434",
        default_model="qwen3.6:35b-a3b-65k",
        timeout=300,
        max_attempts=5,
    )

    with pytest.raises(RuntimeError) as exc_info:
        router.generate("Test prompt")

    assert "Ollama LLM gateway failed after 5 attempts" in str(exc_info.value)
    assert mock_urlopen.call_count == 5

    # Check backoff sleep times: 5 * (3 ** 0)=5, 5 * (3 ** 1)=15, 5 * (3 ** 2)=45, 5 * (3 ** 3)=135
    expected_sleep_calls = [call(5), call(15), call(45), call(135)]
    assert mock_sleep.call_args_list == expected_sleep_calls

    captured = capsys.readouterr()
    assert "Retry attempt 1/5 failed" in captured.out
    assert "Sleeping for 5s before retrying" in captured.out
    assert "Retry attempt 4/5 failed" in captured.out
    assert "Sleeping for 135s before retrying" in captured.out


@patch("urllib.request.urlopen")
@patch("time.sleep")
def test_llm_gateway_retry_success_after_failure(mock_sleep, mock_urlopen):
    """
    Verifies that if initial attempts fail but a subsequent retry succeeds,
    the response is returned successfully.
    """
    success_response = MagicMock()
    success_response.status = 200
    success_response.read.return_value = b'{"response": "Successful response content"}'
    success_response.__enter__.return_value = success_response

    # Fail attempt 1 and 2, succeed on attempt 3
    mock_urlopen.side_effect = [
        urllib.error.URLError("Temporary outage"),
        urllib.error.URLError("Timeout"),
        success_response,
    ]


    router = MultiModelGatewayRouter(
        ollama_host="http://192.168.1.29:11434",
        default_model="qwen3.6:35b-a3b-65k",
        max_attempts=5,
    )

    result = router.generate("Test prompt")
    assert result == "Successful response content"
    assert mock_urlopen.call_count == 3
    assert mock_sleep.call_args_list == [call(5), call(15)]
