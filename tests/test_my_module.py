from unittest.mock import patch

from pottery_assistant.my_module import run_from_script


def test_run_from_script_calls_uvicorn():
    with patch("pottery_assistant.my_module.uvicorn.run") as mock_run:
        run_from_script()
    mock_run.assert_called_once_with(
        "pottery_assistant.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


def test_run_from_script_disables_reload_in_production():
    with (
        patch("pottery_assistant.my_module.uvicorn.run") as mock_run,
        patch.dict("os.environ", {"ENV": "production"}),
    ):
        run_from_script()
    _, kwargs = mock_run.call_args
    assert kwargs["reload"] is False
