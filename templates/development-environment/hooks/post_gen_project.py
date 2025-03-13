import os
import subprocess


def user_wants_postgres():
    return "{{ cookiecutter.install_postgres }}"


def remove_paths():
    REMOVE_PATHS = [
        "{%if cookiecutter.install_postgres != true %}postgres.docker-compose.yml{%endif%}"
    ]

    for path in REMOVE_PATHS:
        if path and os.path.exists(path):
            os.unlink(path) if os.path.isfile(path) else os.rmdir(path)


def is_postgres_running():
    try:
        output = subprocess.check_output(["docker", "ps", "-f", "name=postgres"])
        return output.decode("utf-8").split("\n")[1] != ""
    except subprocess.CalledProcessError:
        return False


def volume_exists():
    try:
        volume_exists = subprocess.check_output(
            ["docker", "volume", "ls", "-f", "name={{ cookiecutter.volume_name }}"]
        )
        return volume_exists.decode("utf-8").split("\n")[1] != ""
    except subprocess.CalledProcessError:
        return False


def create_postgres_volume():
    try:
        subprocess.run(["docker", "volume", "create", "{{ cookiecutter.volume_name }}"])
        return True
    except subprocess.CalledProcessError:
        return False


def start_postgres():
    subprocess.run(
        ["docker", "compose", "-f", "postgres.docker-compose.yml", "up", "-d"]
    )


def create_venv_for_uv():
    subprocess.run(["uv", "venv", "--directory", "{{ cookiecutter.backend_slug }}"])


def install_dependencies_for_uv():
    subprocess.run(["uv", "sync", "--directory", "{{ cookiecutter.backend_slug }}"])


def install_pnpm_dependencies():
    subprocess.run(["pnpm", "install", "--dir", "{{ cookiecutter.frontend_slug }}"])


if __name__ == "__main__":
    remove_paths()
    if user_wants_postgres():
        if not volume_exists():
            create_postgres_volume()
        if not is_postgres_running():
            start_postgres()
    create_venv_for_uv()
    install_dependencies_for_uv()
    install_pnpm_dependencies()
