import sys
import subprocess


def if_docker_installed():
    try:
        subprocess.check_output(["docker", "--version"])
        return True
    except subprocess.CalledProcessError:
        return False


def if_docker_compose_installed():
    try:
        subprocess.check_output(["docker-compose", "--version"])
        return True
    except subprocess.CalledProcessError:
        return False


if __name__ == "__main__":
    if not if_docker_installed():
        print("Docker is not installed")
        sys.exit(1)
    if not if_docker_compose_installed():
        print("Docker Compose is not installed")
        sys.exit(1)
