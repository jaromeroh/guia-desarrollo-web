#!/usr/bin/env python3
"""Valida estructura, paleta y desbordamientos aproximados de un SVG editorial."""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


ALLOWED_COLORS = {
    "#20262e",
    "#31536a",
    "#b95736",
    "#c59132",
    "#a9a49b",
    "#59636d",
    "#72706c",
    "#f2eee6",
    "#fffdfa",
    "#ffffff",
    "#e8eef1",
    "#f3e6df",
    "#f5ecd8",
    "#d8d2c7",
    "#b68125",
    "#8f3f26",
    "#f7f4ed",
}

HEX_COLOR_RE = re.compile(r"#[0-9a-fA-F]{6}\b")
CSS_RULE_RE = re.compile(r"\.([\w-]+)\s*\{([^}]*)\}", re.DOTALL)
CSS_PROPERTY_RE = re.compile(r"([\w-]+)\s*:\s*([^;]+)")
NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")
TRANSLATE_RE = re.compile(
    r"translate\(\s*(-?\d+(?:\.\d+)?)"
    r"(?:[\s,]+(-?\d+(?:\.\d+)?))?\s*\)"
)


@dataclass
class Issue:
    level: str
    message: str


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def number(value: str | None, default: float = 0.0) -> float:
    if value is None:
        return default
    match = NUMBER_RE.search(value)
    return float(match.group()) if match else default


def parse_style_declarations(value: str | None) -> dict[str, str]:
    if not value:
        return {}
    return {
        key.strip(): val.strip()
        for key, val in CSS_PROPERTY_RE.findall(value)
    }


def parse_css(root: ET.Element) -> dict[str, dict[str, str]]:
    classes: dict[str, dict[str, str]] = {}
    for element in root.iter():
        if local_name(element.tag) != "style" or not element.text:
            continue
        for class_name, body in CSS_RULE_RE.findall(element.text):
            classes[class_name] = parse_style_declarations(body)
    return classes


def computed_property(
    element: ET.Element,
    property_name: str,
    css: dict[str, dict[str, str]],
    fallback: str | None = None,
) -> str | None:
    inline = parse_style_declarations(element.get("style"))
    if property_name in inline:
        return inline[property_name]
    if element.get(property_name):
        return element.get(property_name)
    for class_name in element.get("class", "").split():
        if property_name in css.get(class_name, {}):
            return css[class_name][property_name]
    return fallback


def estimate_text_width(text: str, font_size: float, monospaced: bool) -> float:
    factor = 0.61 if monospaced else 0.56
    return len(text.strip()) * font_size * factor


def translation(
    element: ET.Element,
    parents: dict[ET.Element, ET.Element],
) -> tuple[float, float]:
    tx = 0.0
    ty = 0.0
    current: ET.Element | None = element
    while current is not None:
        transform = current.get("transform", "")
        for x_value, y_value in TRANSLATE_RE.findall(transform):
            tx += float(x_value)
            ty += float(y_value) if y_value else 0.0
        current = parents.get(current)
    return tx, ty


def horizontal_bounds(x: float, width: float, anchor: str) -> tuple[float, float]:
    if anchor == "middle":
        return x - width / 2, x + width / 2
    if anchor == "end":
        return x - width, x
    return x, x + width


def text_lines(
    element: ET.Element,
    css: dict[str, dict[str, str]],
) -> list[tuple[str, float, float, float, str, bool]]:
    root_x = number(element.get("x"))
    current_y = number(element.get("y"))
    root_size = number(computed_property(element, "font-size", css), 16)
    root_anchor = computed_property(element, "text-anchor", css, "start") or "start"
    root_mono = "mono" in element.get("class", "").split()
    tspans = [child for child in element if local_name(child.tag) == "tspan"]

    if not tspans:
        return [
            (
                "".join(element.itertext()),
                root_x,
                current_y,
                root_size,
                root_anchor,
                root_mono,
            )
        ]

    lines = []
    for tspan in tspans:
        x = number(tspan.get("x"), root_x)
        if tspan.get("y") is not None:
            current_y = number(tspan.get("y"))
        elif tspan.get("dy") is not None:
            current_y += number(tspan.get("dy"))
        size = number(
            computed_property(tspan, "font-size", css, str(root_size)),
            root_size,
        )
        anchor = (
            computed_property(tspan, "text-anchor", css, root_anchor)
            or root_anchor
        )
        monospaced = root_mono or "mono" in tspan.get("class", "").split()
        lines.append(
            (
                "".join(tspan.itertext()),
                x,
                current_y,
                size,
                anchor,
                monospaced,
            )
        )
    return lines


def validate(path: Path) -> list[Issue]:
    issues: list[Issue] = []
    try:
        tree = ET.parse(path)
    except (ET.ParseError, OSError) as error:
        return [Issue("ERROR", f"No se pudo leer el SVG: {error}")]

    root = tree.getroot()
    if local_name(root.tag) != "svg":
        return [Issue("ERROR", "El elemento raíz no es <svg>.")]

    view_box = [number(part) for part in root.get("viewBox", "").split()]
    if len(view_box) != 4 or view_box[2] <= 0 or view_box[3] <= 0:
        issues.append(Issue("ERROR", "Falta un viewBox válido."))
        view_box = [0, 0, float("inf"), float("inf")]
    vx, vy, vw, vh = view_box

    if root.get("role") != "img":
        issues.append(Issue("ERROR", 'El SVG debe declarar role="img".'))
    if root.get("aria-labelledby") != "title desc":
        issues.append(
            Issue("ERROR", 'Usar aria-labelledby="title desc" en <svg>.')
        )

    children_by_id = {
        element.get("id"): element
        for element in root.iter()
        if element.get("id")
    }
    ids = [
        element.get("id")
        for element in root.iter()
        if element.get("id")
    ]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        issues.append(
            Issue("ERROR", f"IDs duplicados: {', '.join(duplicates)}.")
        )

    for required_id, expected_tag in (("title", "title"), ("desc", "desc")):
        element = children_by_id.get(required_id)
        if element is None or local_name(element.tag) != expected_tag:
            issues.append(
                Issue("ERROR", f"Falta <{expected_tag} id=\"{required_id}\">.")
            )
        elif not "".join(element.itertext()).strip():
            issues.append(Issue("ERROR", f"<{expected_tag}> está vacío."))

    if any(
        local_name(element.tag) in {"linearGradient", "radialGradient"}
        for element in root.iter()
    ):
        issues.append(Issue("ERROR", "No usar degradados en este sistema visual."))

    serialized = ET.tostring(root, encoding="unicode")
    used_colors = {color.lower() for color in HEX_COLOR_RE.findall(serialized)}
    unexpected_colors = sorted(used_colors - ALLOWED_COLORS)
    if unexpected_colors:
        issues.append(
            Issue(
                "ERROR",
                "Colores fuera de la paleta: " + ", ".join(unexpected_colors),
            )
        )

    css = parse_css(root)
    parents = {
        child: parent
        for parent in root.iter()
        for child in parent
    }
    for element in root.iter():
        if local_name(element.tag) != "text":
            continue
        lines = text_lines(element, css)
        element_id = element.get("id") or element.get("data-container") or "texto"
        text_tx, text_ty = translation(element, parents)

        for content, x, y, font_size, anchor, monospaced in lines:
            x += text_tx
            y += text_ty
            if font_size < 12:
                issues.append(
                    Issue(
                        "ERROR",
                        f"{element_id}: tipografía menor de 12 px ({font_size:g}).",
                    )
                )
            elif font_size < 14 and element.get("data-small-ok") != "true":
                issues.append(
                    Issue(
                        "WARN",
                        f"{element_id}: tipografía secundaria de {font_size:g} px.",
                    )
                )

            width = estimate_text_width(content, font_size, monospaced)
            left, right = horizontal_bounds(x, width, anchor)
            top = y - font_size * 0.82
            bottom = y + font_size * 0.24

            if left < vx or right > vx + vw or top < vy or bottom > vy + vh:
                issues.append(
                    Issue(
                        "ERROR",
                        f"{element_id}: texto fuera del viewBox: {content!r}.",
                    )
                )

            container_id = element.get("data-container")
            if not container_id:
                continue
            container = children_by_id.get(container_id)
            if container is None:
                issues.append(
                    Issue(
                        "ERROR",
                        f"{element_id}: no existe el contenedor #{container_id}.",
                    )
                )
                continue
            if local_name(container.tag) != "rect":
                issues.append(
                    Issue(
                        "WARN",
                        f"{element_id}: #{container_id} no es un <rect>; revisar manualmente.",
                    )
                )
                continue

            padding = number(element.get("data-padding"), 20)
            container_tx, container_ty = translation(container, parents)
            cx = number(container.get("x")) + container_tx
            cy = number(container.get("y")) + container_ty
            cw = number(container.get("width"))
            ch = number(container.get("height"))
            safe_left = cx + padding
            safe_right = cx + cw - padding
            safe_top = cy + padding
            safe_bottom = cy + ch - padding

            if (
                left < safe_left
                or right > safe_right
                or top < safe_top
                or bottom > safe_bottom
            ):
                issues.append(
                    Issue(
                        "ERROR",
                        (
                            f"{element_id}: posible desbordamiento en #{container_id}: "
                            f"{content!r}."
                        ),
                    )
                )

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida SVG del sistema editorial del libro."
    )
    parser.add_argument("svg", nargs="+", type=Path)
    parser.add_argument(
        "--warnings-as-errors",
        action="store_true",
        help="Falla también ante advertencias.",
    )
    args = parser.parse_args()

    exit_code = 0
    for path in args.svg:
        issues = validate(path)
        print(f"\n{path}")
        if not issues:
            print("  OK: validación superada.")
            continue
        for issue in issues:
            print(f"  {issue.level}: {issue.message}")
        has_error = any(issue.level == "ERROR" for issue in issues)
        has_warning = any(issue.level == "WARN" for issue in issues)
        if has_error or (args.warnings_as_errors and has_warning):
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
