from invoke import task


def _is_django_installed():
    try:
        import django
    except ImportError:
        return False
    else:
        return True


@task
def pyupgrade(c):
    """
    Upgrade Python syntax using pyupgrade.
    Exits non-zero if any changes are made, so doubles as a check.
    """
    c.run("pyupgrade --py38-plus $(find . -name '*.py')")


@task
def isort(c):
    """
    Check Python code for incorrectly-sorted imports.
    """
    c.run("isort . --check")


@task
def black(c):
    """
    Check Python code for style errors.
    """
    c.run("black . --check")


@task
def migrations(c):
    """
    Check Django models for outstanding changes.
    """
    c.run("./manage.py makemigrations --check")


@task(default=True)
def all(c):
    """
    Perform all checks.
    """
    pyupgrade(c)
    isort(c)
    black(c)

    # It only makes sense to perform migration checks on Django projects
    if _is_django_installed():
        migrations(c)
