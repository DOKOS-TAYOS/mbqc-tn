from __future__ import annotations

from project_name import get_template_metadata


def main() -> None:
    metadata = get_template_metadata()
    print(f"Library example using {metadata.package_name}")
    print(f"Bootstrap required: {metadata.bootstrap_required}")


if __name__ == "__main__":
    main()
