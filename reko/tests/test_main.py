from click.testing import CliRunner

from reko.main import main

runner = CliRunner()


def test_main_help():
    response = runner.invoke(main, ["-h"])
    assert response.exit_code == 0
    assert "" in response.output
