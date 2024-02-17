import subprocess


def get_git_root(path: str) -> str:
    """Returns the root folder of the git repository if the input path is part of the git repository.
    """
    try:
        return subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=path).decode().strip()
    except subprocess.CalledProcessError:
        raise ValueError(f"Path {path} is not part of a git repository.") from None
