from pathlib import Path

from puild import Command, find_files, needs_rebuild, rm, set_default_indent

set_default_indent("              ")

FRONTEND_DIR = Path("src/frontend")
FRONTEND_OUT_DIR = FRONTEND_DIR / "out"

def _frontend_build():
    # If package lock is outdated Or node_modules is missing
    # -> Install dependencies
    target = FRONTEND_DIR / "node_modules" / ".package-lock.json"
    source = FRONTEND_DIR / "package-lock.json"
    if needs_rebuild(target=target, sources=source, log=True):
        res = (
            Command("npm", "install")
            .run(cwd="src/frontend", capture=False)
        )
        res.exit_for_error()

    # If the source codes are newer than built index.html
    # -> Rebuild
    sources = [
        *find_files(FRONTEND_DIR / "src", recursive=True),
        *find_files(FRONTEND_DIR, "*.json"),
        *find_files(FRONTEND_DIR, "*.mjs"),
        *find_files(FRONTEND_DIR, "*.ts")
    ]

    target = FRONTEND_OUT_DIR / "index.html"

    if needs_rebuild(target=target, sources=sources, log=True):
        res = (
            Command("npm", "run", "build")
            .run(cwd="src/frontend", capture=False)
        )
        res.exit_for_error()

def _frontend_clean():
    rm(FRONTEND_OUT_DIR)


def _install_backend_deps():
    res = (
        Command("uv", "sync", "--frozen", "--no-dev")
        .run()
    )

    res.exit_for_error()

def build():
    _frontend_build()
    _install_backend_deps()

def run():
    build()

    res = (
        Command("uv", "run", "-m", "src.backend.main")
        .run(stream=True, text=True)
    )

    res.exit_for_error()


def clean():
    _frontend_clean()
