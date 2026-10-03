import shutil
from pathlib import Path

from puild import Command, find_files, needs_rebuild, rm, set_default_indent

set_default_indent("              ")

FRONTEND_DIR = Path("src/frontend")
FRONTEND_EXPORT_DIR = FRONTEND_DIR / "out"
BUILD_DIR = Path("build")
FRONTEND_BUILD_DIR = BUILD_DIR / "frontend"


def _frontend_build():
    # If package lock is outdated or node_modules is missing -> install dependencies
    target = FRONTEND_DIR / "node_modules" / ".package-lock.json"
    source = FRONTEND_DIR / "package-lock.json"
    if needs_rebuild(target=target, sources=source, log=True):
        res = Command("npm", "install").run(cwd="src/frontend", capture=False)
        res.exit_for_error()

    # If the source codes are newer than built index.html -> rebuild
    public_dir = FRONTEND_DIR / "public"
    public_files = (
        find_files(public_dir, recursive=True) if public_dir.exists() else []
    )

    sources = [
        *find_files(FRONTEND_DIR / "src", recursive=True),
        *find_files(FRONTEND_DIR, "*.json"),
        *find_files(FRONTEND_DIR, "*.mjs"),
        *find_files(FRONTEND_DIR, "*.ts"),
        *public_files,
    ]

    target = FRONTEND_BUILD_DIR / "index.html"

    if needs_rebuild(target=target, sources=sources, log=True):
        res = Command("npm", "run", "build").run(
            cwd="src/frontend", capture=False
        )
        res.exit_for_error()

        FRONTEND_BUILD_DIR.parent.mkdir(parents=True, exist_ok=True)
        if FRONTEND_BUILD_DIR.exists():
            shutil.rmtree(FRONTEND_BUILD_DIR)
        shutil.copytree(FRONTEND_EXPORT_DIR, FRONTEND_BUILD_DIR)


def _frontend_clean():
    rm(BUILD_DIR)
    rm(FRONTEND_EXPORT_DIR)


def _install_backend_deps():
    res = Command("uv", "sync", "--frozen", "--no-dev").run()
    res.exit_for_error()


def build():
    _frontend_build()
    _install_backend_deps()


def run():
    build()

    res = Command("uv", "run", "-m", "src.backend.main").run(
        stream=True, text=True
    )
    res.exit_for_error()


def clean():
    _frontend_clean()
