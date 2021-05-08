from invoke import task


@task
def run(c):
    c.run("flask run")


@task
def test(c):
    c.run("pytest")


@task
def lint(c):
    c.run("black --check .")


@task
def fix(c):
    c.run("black .")
