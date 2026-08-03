#!/usr/bin/env python3
"""Renderiza un SVG a PNG sin sobrescribir archivos por defecto."""

from __future__ import annotations

import argparse
import math
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


def run(command: list[str]) -> None:
    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def quicklook_size(source: Path, width: int) -> int:
    """Calcula el lado máximo necesario para conservar el ancho solicitado."""
    try:
        root = ET.parse(source).getroot()
        view_box = [float(value) for value in root.get("viewBox", "").split()]
        if len(view_box) == 4 and view_box[2] > 0 and view_box[3] > 0:
            return math.ceil(width * max(1, view_box[3] / view_box[2]))
    except (ET.ParseError, OSError, ValueError):
        pass
    return width


def render_with_quicklook(
    source: Path,
    target: Path,
    width: int,
    qlmanage: str,
    magick: str | None,
) -> None:
    with tempfile.TemporaryDirectory(prefix="diagram-preview-") as temp:
        temp_path = Path(temp)
        run(
            [
                qlmanage,
                "-t",
                "-s",
                str(quicklook_size(source, width)),
                "-o",
                str(temp_path),
                str(source),
            ]
        )
        rendered = temp_path / f"{source.name}.png"
        if not rendered.exists():
            raise RuntimeError("Quick Look no produjo el PNG esperado.")
        if magick:
            run(
                [
                    magick,
                    str(rendered),
                    "-trim",
                    "+repage",
                    "-resize",
                    f"{width}x",
                    str(target),
                ]
            )
        else:
            shutil.copy2(rendered, target)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Genera una previsualización PNG de un SVG."
    )
    parser.add_argument("svg", type=Path)
    parser.add_argument("png", nargs="?", type=Path)
    parser.add_argument("--width", type=int, default=1200)
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Permite sobrescribir el PNG de destino.",
    )
    args = parser.parse_args()

    source = args.svg.resolve()
    target = (
        args.png.resolve()
        if args.png
        else source.with_name(f"{source.stem}-preview-{args.width}.png")
    )

    if not source.is_file():
        print(f"No existe el SVG: {source}", file=sys.stderr)
        return 2
    if target.exists() and not args.overwrite:
        print(
            f"El destino ya existe: {target}. Usa --overwrite solo con autorización.",
            file=sys.stderr,
        )
        return 2
    target.parent.mkdir(parents=True, exist_ok=True)

    rsvg = shutil.which("rsvg-convert")
    inkscape = shutil.which("inkscape")
    qlmanage = shutil.which("qlmanage")
    magick = shutil.which("magick")

    try:
        if rsvg:
            run([rsvg, "-w", str(args.width), "-o", str(target), str(source)])
        elif inkscape:
            run(
                [
                    inkscape,
                    str(source),
                    f"--export-filename={target}",
                    f"--export-width={args.width}",
                ]
            )
        elif magick:
            try:
                run(
                    [
                        magick,
                        "-background",
                        "none",
                        str(source),
                        "-resize",
                        f"{args.width}x",
                        str(target),
                    ]
                )
            except subprocess.CalledProcessError:
                if not qlmanage:
                    raise
                render_with_quicklook(
                    source, target, args.width, qlmanage, magick
                )
        elif qlmanage:
            render_with_quicklook(
                source, target, args.width, qlmanage, magick
            )
        else:
            print(
                "No se encontró rsvg-convert, Inkscape, qlmanage ni ImageMagick.",
                file=sys.stderr,
            )
            return 3
    except (subprocess.CalledProcessError, RuntimeError) as error:
        print(f"No se pudo renderizar: {error}", file=sys.stderr)
        return 1

    print(target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
