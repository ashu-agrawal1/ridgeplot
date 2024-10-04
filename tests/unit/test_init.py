from __future__ import annotations

from pathlib import Path


def test_packaged_installed() -> None:
    """Assert that ridgeplot has been properly installed and isn't simply under
    the current working directory."""
    import ridgeplot

    # By definition, if a module has a __path__ attribute, it is a package.
    assert hasattr(ridgeplot, "__path__")
    assert len(ridgeplot.__path__) == 1
    package_path = Path(ridgeplot.__path__[0])
    assert package_path.exists()
    assert package_path.is_dir()
    assert package_path.name == "ridgeplot"
    assert Path.cwd().resolve() != package_path.parent.resolve()


def test_import_all() -> None:
    """Assert that the package's __all__ attribute is correctly defined."""
    from ridgeplot import __all__ as public_api

    assert set(public_api) == {"ridgeplot", "list_all_colorscale_names", "__version__"}
