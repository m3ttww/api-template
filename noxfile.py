import nox

nox.options.default_venv_backend = "uv"
nox.options.reuse_existing_virtualenvs = True


@nox.session(tags=["tests"], python=["3.13"])
def integration(session: nox.Session) -> None:
    session.run_install(
        "uv",
        "sync",
        "--frozen",
        f"--python={session.python}",
    )
    session.run("pytest", "tests/integration")
