#!/usr/bin/env python3
"""Genera la segunda pasada visual de los capítulos 11–15.

Las composiciones de escritorio y móvil responden a la misma pregunta
pedagógica, pero cambian de geometría para conservar legibilidad.
"""

from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "diagrams"
SKILL_ASSETS = ROOT / "skills" / "crear-diagramas-editoriales" / "assets"

COLORS = {
    "ink": "#20262E",
    "blue": "#31536A",
    "rust": "#B95736",
    "ochre": "#C59132",
    "gray": "#A9A49B",
    "line": "#59636D",
    "muted": "#72706C",
    "paper": "#F2EEE6",
    "surface": "#FFFDFA",
    "soft_blue": "#E8EEF1",
    "soft_rust": "#F3E6DF",
    "soft_ochre": "#F5ECD8",
    "border": "#D8D2C7",
}


def defs() -> str:
    return """
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 10 5 0 10z" fill="#31536A"/>
    </marker>
    <marker id="arrow-rust" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 10 5 0 10z" fill="#B95736"/>
    </marker>
    <style>
      .sans { font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #20262E; }
      .mono { font-family: ui-monospace, "SFMono-Regular", Consolas, monospace; fill: #20262E; }
      .title { font-size: 34px; font-weight: 750; }
      .subtitle { font-size: 17px; fill: #72706C; }
      .tag { font-size: 14px; font-weight: 750; letter-spacing: 1.5px; fill: #31536A; }
      .node-title { font-size: 19px; font-weight: 720; text-anchor: middle; }
      .node-copy { font-size: 15px; fill: #59636D; text-anchor: middle; }
      .label { font-size: 14px; font-weight: 680; text-anchor: middle; }
      .small { font-size: 14px; fill: #72706C; }
      .flow { fill: none; stroke: #31536A; stroke-width: 3; marker-end: url(#arrow); }
      .risk-flow { fill: none; stroke: #B95736; stroke-width: 3; marker-end: url(#arrow-rust); }
      .relation { fill: none; stroke: #59636D; stroke-width: 2.5; }
    </style>
  </defs>"""


def start_svg(width: int, height: int, title: str, desc: str, subtitle: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(desc)}</desc>
{defs()}
  <rect width="{width}" height="{height}" fill="{COLORS['paper']}"/>
  <text x="48" y="60" class="sans title">{escape(title)}</text>
  <text x="48" y="91" class="sans subtitle">{escape(subtitle)}</text>'''


def end_svg() -> str:
    return "\n</svg>\n"


def node(
    ident: str,
    x: float,
    y: float,
    width: float,
    height: float,
    title: str,
    lines: list[str] | tuple[str, ...] = (),
    fill: str = "#FFFDFA",
    stroke: str = "#A9A49B",
    title_y: float | None = None,
) -> str:
    cx = x + width / 2
    ty = title_y if title_y is not None else y + 42
    tspans = [f'<tspan x="{cx:g}" y="{ty:g}">{escape(title)}</tspan>']
    for index, line in enumerate(lines):
        tspans.append(
            f'<tspan x="{cx:g}" dy="{32 if index == 0 else 24}" class="node-copy">{escape(line)}</tspan>'
        )
    return (
        f'<rect id="{ident}" x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}" '
        f'rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>'
        f'<text data-container="{ident}" data-padding="18" x="{cx:g}" y="{ty:g}" class="sans node-title">'
        + "".join(tspans)
        + "</text>"
    )


def title_block_mobile(height: int, title: str, desc: str, tag: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 {height}" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(desc)}</desc>
{defs()}
  <rect width="420" height="{height}" fill="#F2EEE6"/>
  <rect x="16" y="16" width="388" height="{height - 32}" rx="22" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/>
  <text x="38" y="58" class="sans tag">{escape(tag)}</text>'''


def card_comparison(name: str, title: str, desc: str, subtitle: str, cards: list[dict[str, str]]) -> None:
    fills = [("#E8EEF1", "#31536A"), ("#F5ECD8", "#C59132"), ("#F3E6DF", "#B95736")]
    body = [start_svg(1200, 720, title, desc, subtitle)]
    for i, card in enumerate(cards):
        x = 55 + i * 382
        fill, stroke = fills[i]
        body.append(node(f"card-{i}", x, 145, 344, 465, card["title"], (), fill, stroke, 195))
        for row, key in enumerate(("model", "fit", "cost")):
            label = {"model": "MODELO", "fit": "ENCAJA CUANDO", "cost": "COSTE A OPERAR"}[key]
            y = 250 + row * 112
            body.append(f'<text x="{x + 28}" y="{y}" class="sans tag">{label}</text>')
            parts = card[key].split("|")
            text = "".join(
                f'<tspan x="{x + 28}" y="{y + 31 + j * 24}">{escape(part)}</tspan>'
                for j, part in enumerate(parts)
            )
            body.append(f'<text x="{x + 28}" y="{y + 31}" class="sans small">{text}</text>')
    body.append(end_svg())
    (OUT / f"{name}.svg").write_text("".join(body), encoding="utf-8")

    height = 1410
    mobile = [title_block_mobile(height, title, desc, "COMPARACIÓN ESTRUCTURADA")]
    for i, card in enumerate(cards):
        y = 92 + i * 420
        fill, stroke = fills[i]
        mobile.append(node(f"mobile-card-{i}", 38, y, 344, 372, card["title"], (), fill, stroke, y + 45))
        for row, key in enumerate(("model", "fit", "cost")):
            label = {"model": "MODELO", "fit": "ENCAJA CUANDO", "cost": "COSTE A OPERAR"}[key]
            yy = y + 92 + row * 88
            mobile.append(f'<text x="62" y="{yy}" class="sans tag">{label}</text>')
            for j, part in enumerate(card[key].split("|")):
                mobile.append(f'<text x="62" y="{yy + 25 + j * 21}" class="sans small">{escape(part)}</text>')
    mobile.append(end_svg())
    (OUT / f"{name}-mobile.svg").write_text("".join(mobile), encoding="utf-8")


def generate_mvc() -> None:
    title = "MVC · de la entrada a la respuesta"
    desc = "El usuario envía una acción al controlador; el controlador coordina el modelo y selecciona una vista que presenta el resultado al usuario."
    body = [start_svg(1200, 690, title, desc, "El controlador coordina; el modelo decide y la vista presenta")]
    body.append('<rect x="38" y="125" width="1124" height="505" rx="24" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/>')
    body.append(node("mvc-user", 75, 265, 190, 130, "Usuario", ("acción",), "#E8EEF1", "#31536A"))
    body.append(node("mvc-controller", 340, 185, 225, 150, "Controller", ("interpreta la entrada", "coordina el flujo")))
    body.append(node("mvc-model", 690, 185, 225, 150, "Model", ("datos y reglas", "sin HTML ni HTTP"), "#F5ECD8", "#C59132"))
    body.append(node("mvc-view", 515, 430, 225, 140, "View", ("presenta el resultado",), "#F3E6DF", "#B95736"))
    body.append('<path class="flow" d="M265 315H336"/><text x="300" y="296" class="sans label">entrada</text>')
    body.append('<path class="flow" d="M565 250H686"/><text x="625" y="231" class="sans label">consulta o cambio</text>')
    body.append('<path class="flow" d="M802 335V398H740"/><text x="845" y="380" class="sans label">datos</text>')
    body.append('<path class="flow" d="M452 335V500H511"/><text x="425" y="410" class="sans label">selecciona</text>')
    body.append('<path class="flow" d="M515 500H180V399"/><text x="335" y="480" class="sans label">respuesta</text>')
    body.append(end_svg())
    (OUT / "cap11-mvc-flujo.svg").write_text("".join(body), encoding="utf-8")

    mobile = [title_block_mobile(1130, title, desc, "FLUJO MVC")]
    steps = [
        ("Usuario", ["envía una acción"], "#E8EEF1", "#31536A"),
        ("Controller", ["interpreta y coordina"], "#FFFDFA", "#A9A49B"),
        ("Model", ["aplica datos y reglas"], "#F5ECD8", "#C59132"),
        ("View", ["presenta el resultado"], "#F3E6DF", "#B95736"),
        ("Usuario", ["recibe la respuesta"], "#E8EEF1", "#31536A"),
    ]
    for i, (heading, copy, fill, stroke) in enumerate(steps):
        y = 92 + i * 190
        mobile.append(node(f"mvc-mobile-{i}", 52, y, 316, 132, heading, copy, fill, stroke))
        if i < len(steps) - 1:
            mobile.append(f'<path class="flow" d="M210 {y + 132}V{y + 182}"/>')
    mobile.append(end_svg())
    (OUT / "cap11-mvc-flujo-mobile.svg").write_text("".join(mobile), encoding="utf-8")


def generate_architecture_comparison() -> None:
    source = (SKILL_ASSETS / "comparacion-patrones.svg").read_text(encoding="utf-8")
    source = source.replace("<text ", '<text data-small-ok="true" ')
    (OUT / "cap11-comparacion-patrones.svg").write_text(source, encoding="utf-8")

    title = "Capas, Clean y Hexagonal"
    desc = "Comparación vertical: capas separa responsabilidades, Clean dirige dependencias hacia el núcleo y Hexagonal conecta adaptadores mediante puertos."
    mobile = [title_block_mobile(1440, title, desc, "TRES VISTAS · UN OBJETIVO")]
    cards = [
        ("Capas", "separar responsabilidades", ["Presentación", "Aplicación", "Dominio", "Infraestructura"]),
        ("Clean Architecture", "dependencias hacia el núcleo", ["Tecnología", "Adaptadores", "Casos de uso", "Reglas"]),
        ("Arquitectura Hexagonal", "puertos y adaptadores", ["REST / CLI", "PUERTOS", "NÚCLEO", "BD / tests"]),
    ]
    fills = [("#E8EEF1", "#31536A"), ("#F5ECD8", "#C59132"), ("#F3E6DF", "#B95736")]
    for i, (heading, purpose, layers) in enumerate(cards):
        y = 92 + i * 420
        fill, stroke = fills[i]
        mobile.append(node(f"arch-card-{i}", 38, y, 344, 360, heading, (purpose,), fill, stroke, y + 42))
        for j, layer in enumerate(layers):
            ly = y + 125 + j * 50
            mobile.append(f'<rect id="arch-layer-{i}-{j}" x="78" y="{ly}" width="264" height="38" rx="9" fill="#FFFDFA" stroke="{stroke}" stroke-width="2"/>')
            mobile.append(f'<text data-container="arch-layer-{i}-{j}" data-padding="6" x="210" y="{ly + 25}" class="sans label">{escape(layer)}</text>')
    mobile.append(end_svg())
    (OUT / "cap11-comparacion-patrones-mobile.svg").write_text("".join(mobile), encoding="utf-8")


def generate_api_first() -> None:
    title = "API-first · trabajo paralelo con un contrato"
    desc = "Consumidor y proveedor acuerdan un contrato, desarrollan en paralelo contra mocks y pruebas, y se integran verificando el mismo contrato."
    body = [start_svg(1200, 720, title, desc, "Diseñar el intercambio antes de acoplar implementaciones")]
    body.append(node("api-contract", 420, 135, 360, 125, "Contrato acordado", ("OpenAPI · esquema · ejemplos",), "#F5ECD8", "#C59132"))
    body.append(node("api-front", 135, 350, 360, 150, "Consumidor", ("frontend o cliente", "trabaja contra un mock"), "#E8EEF1", "#31536A"))
    body.append(node("api-back", 705, 350, 360, 150, "Proveedor", ("backend o servicio", "implementa y valida"), "#F3E6DF", "#B95736"))
    body.append(node("api-integrate", 420, 555, 360, 105, "Integración verificable", ("pruebas de contrato",), "#FFFDFA", "#A9A49B"))
    body.append('<path class="flow" d="M510 260V315H315V346"/><path class="flow" d="M690 260V315H885V346"/>')
    body.append('<path class="flow" d="M315 500V530H510V551"/><path class="flow" d="M885 500V530H690V551"/>')
    body.append(end_svg())
    (OUT / "cap12-api-first-paralelo.svg").write_text("".join(body), encoding="utf-8")

    mobile = [title_block_mobile(1010, title, desc, "CONTRATO ANTES QUE IMPLEMENTACIÓN")]
    mobile.append(node("api-m-contract", 52, 92, 316, 140, "Contrato acordado", ("esquema · errores · ejemplos",), "#F5ECD8", "#C59132"))
    mobile.append('<path class="flow" d="M210 232V280"/>')
    mobile.append(node("api-m-front", 38, 290, 160, 205, "Consumidor", ("mock", "cliente"), "#E8EEF1", "#31536A"))
    mobile.append(node("api-m-back", 222, 290, 160, 205, "Proveedor", ("servicio", "validación"), "#F3E6DF", "#B95736"))
    mobile.append('<path class="relation" d="M210 280V270M118 280V290M302 280V290M118 270H302"/>')
    mobile.append('<path class="flow" d="M118 495V570H210V618"/><path class="flow" d="M302 495V570H210V618"/>')
    mobile.append(node("api-m-integrate", 52, 625, 316, 145, "Integración", ("pruebas de contrato", "evidencia compartida"), "#FFFDFA", "#A9A49B"))
    mobile.append('<rect id="api-m-note" x="52" y="825" width="316" height="105" rx="14" fill="#E8EEF1" stroke="#31536A" stroke-width="2"/><text data-container="api-m-note" data-padding="18" x="210" y="862" class="sans node-title"><tspan x="210">El contrato coordina</tspan><tspan x="210" dy="30" class="node-copy">no sustituye las conversaciones</tspan></text>')
    mobile.append(end_svg())
    (OUT / "cap12-api-first-paralelo-mobile.svg").write_text("".join(mobile), encoding="utf-8")


def generate_data_model() -> None:
    source = (SKILL_ASSETS / "modelo-datos.svg").read_text(encoding="utf-8")
    source = source.replace("<text ", '<text data-small-ok="true" ')
    (OUT / "cap13-modelo-ecommerce.svg").write_text(source, encoding="utf-8")

    title = "Modelo lógico · e-commerce"
    desc = "Relaciones principales del e-commerce: usuarios poseen direcciones y pedidos; pedidos contienen líneas y un pago; líneas apuntan a productos; productos se asocian con categorías mediante una tabla puente."
    mobile = [title_block_mobile(1490, title, desc, "ENTIDADES Y CARDINALIDADES")]
    relations = [
        ("Usuario", "1 : N", "Dirección"),
        ("Usuario", "1 : N", "Pedido"),
        ("Pedido", "1 : N", "Línea"),
        ("Pedido", "0..1", "Pago"),
        ("Producto", "1 : N", "Línea"),
        ("Producto", "N : M", "Categoría"),
    ]
    for i, (left, cardinality, right) in enumerate(relations):
        y = 100 + i * 210
        mobile.append(node(f"erd-left-{i}", 38, y, 142, 115, left, (), "#E8EEF1", "#31536A"))
        mobile.append(node(f"erd-right-{i}", 240, y, 142, 115, right, (), "#F5ECD8", "#C59132"))
        mobile.append(f'<path class="relation" d="M180 {y + 57}H240"/><rect id="erd-label-{i}" x="180" y="{y + 34}" width="60" height="44" rx="8" fill="#FFFDFA"/><text data-container="erd-label-{i}" data-padding="4" x="210" y="{y + 62}" class="sans label">{cardinality}</text>')
    mobile.append('<rect id="erd-note" x="38" y="1370" width="344" height="75" rx="14" fill="#F3E6DF" stroke="#B95736" stroke-width="2"/><text data-container="erd-note" data-padding="15" x="210" y="1400" class="sans node-copy"><tspan x="210">N : M requiere una tabla puente;</tspan><tspan x="210" dy="23">puede contener atributos propios.</tspan></text>')
    mobile.append(end_svg())
    (OUT / "cap13-modelo-ecommerce-mobile.svg").write_text("".join(mobile), encoding="utf-8")


def generate_btree() -> None:
    title = "Un índice reduce el espacio de búsqueda"
    desc = "Un árbol B compara una clave con nodos ordenados y desciende solo por la rama compatible, en lugar de recorrer todas las filas."
    body = [start_svg(1200, 720, title, desc, "Ejemplo conceptual: localizar «Pedro» en tres decisiones")]
    body.append(node("bt-root", 510, 130, 180, 90, "M", ("raíz",), "#E8EEF1", "#31536A", 165))
    body.append(node("bt-left", 250, 300, 210, 95, "D · H", ("claves menores",), title_y=335))
    body.append(node("bt-right", 740, 300, 210, 95, "R · V", ("claves mayores",), "#F5ECD8", "#C59132", 335))
    leaves = [(90, "A–C"), (300, "E–G"), (510, "I–L"), (710, "N–Q"), (910, "S–U"), (1060, "W–Z")]
    for i, (x, label) in enumerate(leaves):
        width = 130 if i < 5 else 105
        fill, stroke = ("#F3E6DF", "#B95736") if label == "N–Q" else ("#FFFDFA", "#A9A49B")
        body.append(node(f"bt-leaf-{i}", x, 500, width, 85, label, (), fill, stroke))
    body.append('<path class="relation" d="M600 220V260M355 260H845M355 260V296M845 260V296"/>')
    body.append('<path class="relation" d="M355 395V455M155 455H575M155 455V496M365 455V496M575 455V496"/>')
    body.append('<path class="relation" d="M845 395V455M775 455H1112M775 455V496M975 455V496M1112 455V496"/>')
    body.append('<path class="risk-flow" d="M690 175H845V296"/><path class="risk-flow" d="M845 395V455H775V496"/>')
    body.append('<text x="760" y="155" class="sans label" fill="#B95736">P &gt; M</text><text x="805" y="444" class="sans label" fill="#B95736">P &lt; R</text>')
    body.append(end_svg())
    (OUT / "cap13-indice-btree.svg").write_text("".join(body), encoding="utf-8")

    mobile = [title_block_mobile(930, title, desc, "RUTA DE BÚSQUEDA")]
    steps = [("M", "P > M · ir a la derecha"), ("R · V", "P < R · ir a la izquierda"), ("N–Q", "Pedro está en este rango")]
    for i, (heading, copy) in enumerate(steps):
        y = 110 + i * 230
        fill, stroke = ("#F3E6DF", "#B95736") if i == 2 else (("#F5ECD8", "#C59132") if i == 1 else ("#E8EEF1", "#31536A"))
        mobile.append(node(f"bt-mobile-{i}", 52, y, 316, 145, heading, (copy,), fill, stroke))
        if i < 2:
            mobile.append(f'<path class="risk-flow" d="M210 {y + 145}V{y + 220}"/>')
    mobile.append('<rect id="bt-mobile-note" x="52" y="790" width="316" height="85" rx="14" fill="#FFFDFA" stroke="#A9A49B" stroke-width="2"/><text data-container="bt-mobile-note" data-padding="16" x="210" y="825" class="sans node-copy"><tspan x="210">El índice evita recorrer</tspan><tspan x="210" dy="23">cada fila de la tabla.</tspan></text>')
    mobile.append(end_svg())
    (OUT / "cap13-indice-btree-mobile.svg").write_text("".join(mobile), encoding="utf-8")


def generate_risk_matrix() -> None:
    title = "Matriz de riesgo técnico"
    desc = "La acción recomendada surge al combinar probabilidad e impacto: ignorar o aceptar en la zona baja, vigilar en la intermedia y mitigar o actuar de inmediato en la alta."
    body = [start_svg(1200, 720, title, desc, "Prioriza incertidumbre por probabilidad e impacto, no por intuición")]
    x0, y0, cw, ch = 300, 180, 250, 125
    body.append('<text x="675" y="145" class="sans tag" text-anchor="middle">IMPACTO →</text><text x="120" y="380" class="sans tag" transform="rotate(-90 120 380)" text-anchor="middle">PROBABILIDAD →</text>')
    cols = ["Bajo", "Medio", "Alto"]
    rows = ["Alta", "Media", "Baja"]
    actions = [["Vigilar", "Mitigar", "Urgente"], ["Aceptar", "Vigilar", "Mitigar"], ["Ignorar", "Aceptar", "Vigilar"]]
    fill_for = {"Ignorar": "#FFFDFA", "Aceptar": "#E8EEF1", "Vigilar": "#F5ECD8", "Mitigar": "#F3E6DF", "Urgente": "#F3E6DF"}
    stroke_for = {"Ignorar": "#A9A49B", "Aceptar": "#31536A", "Vigilar": "#C59132", "Mitigar": "#B95736", "Urgente": "#B95736"}
    for i, label in enumerate(cols):
        body.append(f'<text x="{x0 + i * cw + cw / 2}" y="170" class="sans node-title">{label}</text>')
    for r, row in enumerate(rows):
        body.append(f'<text x="255" y="{y0 + r * ch + 72}" class="sans node-title">{row}</text>')
        for c, action in enumerate(actions[r]):
            ident = f"risk-{r}-{c}"
            x, y = x0 + c * cw, y0 + r * ch
            body.append(f'<rect id="{ident}" x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{fill_for[action]}" stroke="{stroke_for[action]}" stroke-width="2.5"/>')
            body.append(f'<text data-container="{ident}" data-padding="20" x="{x + cw / 2}" y="{y + 72}" class="sans node-title">{action}</text>')
    body.append(end_svg())
    (OUT / "cap14-matriz-riesgos.svg").write_text("".join(body), encoding="utf-8")

    mobile = [title_block_mobile(690, title, desc, "PROBABILIDAD × IMPACTO")]
    x0, y0, cw, ch = 80, 155, 102, 105
    for i, label in enumerate(cols):
        mobile.append(f'<text x="{x0 + i * cw + cw / 2}" y="138" class="sans label">{label}</text>')
    for r, row in enumerate(rows):
        mobile.append(f'<text x="62" y="{y0 + r * ch + 60}" class="sans label" text-anchor="end">{row}</text>')
        for c, action in enumerate(actions[r]):
            ident = f"risk-mobile-{r}-{c}"
            x, y = x0 + c * cw, y0 + r * ch
            short = "Ya" if action == "Urgente" else action
            mobile.append(f'<rect id="{ident}" x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{fill_for[action]}" stroke="{stroke_for[action]}" stroke-width="2"/>')
            mobile.append(f'<text data-container="{ident}" data-padding="9" x="{x + cw / 2}" y="{y + 60}" class="sans label">{short}</text>')
    mobile.append('<text x="210" y="510" class="sans tag" text-anchor="middle">IMPACTO →</text><text x="210" y="555" class="sans small" text-anchor="middle">La esquina alta/alta exige acción inmediata.</text>')
    mobile.append(end_svg())
    (OUT / "cap14-matriz-riesgos-mobile.svg").write_text("".join(mobile), encoding="utf-8")


def generate_diagram_examples() -> None:
    title = "Dos diagramas, dos preguntas"
    desc = "El mapa de contexto muestra quién usa el sistema y qué dependencias externas toca; el flujo de pago muestra el orden del proceso y sus salidas de error."
    body = [start_svg(1200, 790, title, desc, "Escoge la notación a partir de la pregunta que necesitas responder")]
    body.append('<rect x="38" y="125" width="545" height="610" rx="22" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><rect x="617" y="125" width="545" height="610" rx="22" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/>')
    body.append('<text x="66" y="165" class="sans tag">MAPA DE CONTEXTO · ¿QUIÉN SE CONECTA?</text>')
    body.append(node("ctx-users", 185, 195, 250, 85, "Usuarios", (), "#E8EEF1", "#31536A"))
    body.append(node("ctx-app", 185, 345, 250, 105, "Aplicación", ("responsabilidad propia",), "#F3E6DF", "#B95736"))
    for i, (label, meta) in enumerate((("Pagos", "Stripe"), ("Correo", "proveedor"), ("Archivos", "objetos"))):
        body.append(node(f"ctx-ext-{i}", 68 + i * 170, 540, 150, 100, label, (meta,), "#F5ECD8", "#C59132"))
    body.append('<path class="flow" d="M310 280V341"/><path class="relation" d="M310 450V500M143 500H483M143 500V536M313 500V536M483 500V536"/>')

    body.append('<text x="645" y="165" class="sans tag">FLUJO · ¿QUÉ OCURRE Y EN QUÉ ORDEN?</text>')
    flow_nodes = [(655, "Enviar"), (800, "Validar"), (945, "Cobrar")]
    for i, (x, label) in enumerate(flow_nodes):
        body.append(node(f"pay-step-{i}", x, 235, 125, 95, label, (), "#E8EEF1" if i == 0 else "#FFFDFA", "#31536A" if i == 0 else "#A9A49B"))
        if i < 2:
            body.append(f'<path class="flow" d="M{x + 125} 282H{x + 141}"/>')
    body.append(node("pay-confirm", 945, 420, 165, 100, "Confirmar", ("correo",), "#F5ECD8", "#C59132"))
    body.append(node("pay-user-error", 700, 420, 165, 100, "Corregir", ("datos",), "#F3E6DF", "#B95736"))
    body.append(node("pay-provider-error", 945, 575, 165, 100, "Recuperar", ("fallo de pago",), "#F3E6DF", "#B95736"))
    body.append('<path class="flow" d="M1007 330V416"/><path class="risk-flow" d="M862 330V416"/><path class="risk-flow" d="M1027 520V571"/>')
    body.append(end_svg())
    (OUT / "cap14-diagramas-utiles.svg").write_text("".join(body), encoding="utf-8")

    mobile = [title_block_mobile(1510, title, desc, "LA PREGUNTA ELIGE LA NOTACIÓN")]
    mobile.append('<rect x="32" y="90" width="356" height="620" rx="20" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text x="52" y="125" class="sans tag">MAPA DE CONTEXTO</text>')
    mobile.append(node("m-ctx-users", 68, 160, 284, 90, "Usuarios", (), "#E8EEF1", "#31536A"))
    mobile.append(node("m-ctx-app", 68, 330, 284, 110, "Aplicación", ("responsabilidad propia",), "#F3E6DF", "#B95736"))
    mobile.append('<path class="flow" d="M210 250V326"/>')
    for i, label in enumerate(("Pagos", "Email", "S3")):
        x = 42 + i * 121
        mobile.append(node(f"m-ctx-ext-{i}", x, 545, 94, 95, label, (), "#F5ECD8", "#C59132"))
    mobile.append('<path class="relation" d="M210 440V505M89 505H331M89 505V541M210 505V541M331 505V541"/>')
    mobile.append('<rect x="32" y="745" width="356" height="705" rx="20" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text x="52" y="780" class="sans tag">FLUJO DE PAGO</text>')
    steps = [("Enviar", "acción"), ("Validar", "datos"), ("Cobrar", "pago"), ("Confirmar", "correo")]
    for i, (heading, copy) in enumerate(steps):
        y = 815 + i * 145
        mobile.append(node(f"m-pay-step-{i}", 90, y, 240, 100, heading, (copy,), "#E8EEF1" if i == 0 else "#FFFDFA", "#31536A" if i == 0 else "#A9A49B"))
        if i < 3:
            mobile.append(f'<path class="flow" d="M210 {y + 100}V{y + 137}"/>')
    mobile.append(node("m-pay-note", 62, 1345, 296, 100, "Cada validación", ("necesita una salida de error",), "#F3E6DF", "#B95736", 1382))
    mobile.append(end_svg())
    (OUT / "cap14-diagramas-utiles-mobile.svg").write_text("".join(mobile), encoding="utf-8")


def generate_planning_cycle() -> None:
    title = "Planificar es un ciclo de aprendizaje"
    desc = "Planear conduce a ejecutar, ejecutar produce evidencia para revisar, revisar permite ajustar y el ajuste alimenta el siguiente plan."
    body = [start_svg(1200, 700, title, desc, "El plan cambia cuando la evidencia cambia")]
    positions = [(130, 180), (750, 180), (750, 430), (130, 430)]
    steps = [("Planear", "supuesto y alcance"), ("Ejecutar", "slice verificable"), ("Revisar", "resultado y señales"), ("Ajustar", "decisión y backlog")]
    fills = [("#E8EEF1", "#31536A"), ("#FFFDFA", "#A9A49B"), ("#F5ECD8", "#C59132"), ("#F3E6DF", "#B95736")]
    for i, ((x, y), (heading, copy), (fill, stroke)) in enumerate(zip(positions, steps, fills)):
        body.append(node(f"plan-{i}", x, y, 320, 130, heading, (copy,), fill, stroke))
    body.append('<path class="flow" d="M450 245H746"/><path class="flow" d="M910 310V426"/><path class="flow" d="M750 495H454"/><path class="flow" d="M290 430V314"/>')
    body.append('<rect id="plan-center" x="470" y="335" width="260" height="120" rx="18" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text data-container="plan-center" data-padding="20" x="600" y="375" class="sans node-title"><tspan x="600">Evidencia</tspan><tspan x="600" dy="28" class="node-copy">uso · fallos</tspan><tspan x="600" dy="22" class="node-copy">restricciones</tspan></text>')
    body.append(end_svg())
    (OUT / "cap14-ciclo-planificacion.svg").write_text("".join(body), encoding="utf-8")

    mobile = [title_block_mobile(1040, title, desc, "CICLO CONTINUO")]
    for i, ((heading, copy), (fill, stroke)) in enumerate(zip(steps, fills)):
        y = 95 + i * 205
        mobile.append(node(f"plan-mobile-{i}", 52, y, 316, 140, heading, (copy,), fill, stroke))
        mobile.append(f'<path class="flow" d="M210 {y + 140}V{y + 197}"/>')
    mobile.append('<path class="flow" d="M210 902V960H30V165H48"/><text x="55" y="940" class="sans label">nuevo ciclo</text>')
    mobile.append(end_svg())
    (OUT / "cap14-ciclo-planificacion-mobile.svg").write_text("".join(mobile), encoding="utf-8")


def generate_frontend_dependencies() -> None:
    title = "Las dependencias apuntan hacia módulos estables"
    desc = "El nivel app compone páginas y proveedores; las páginas consumen APIs públicas de features; las features usan shared. Las features no se importan entre sí ni dependen del nivel app."
    body = [start_svg(1200, 720, title, desc, "Componer arriba; reutilizar abajo; evitar atajos globales")]
    body.append(node("fe-app", 435, 135, 330, 110, "app", ("rutas · providers · composición",), "#F3E6DF", "#B95736"))
    body.append(node("fe-pages", 435, 310, 330, 110, "pages", ("ensamblan recorridos",), "#E8EEF1", "#31536A"))
    body.append(node("fe-auth", 105, 505, 250, 115, "feature/auth", ("API pública",), "#FFFDFA", "#A9A49B"))
    body.append(node("fe-cart", 475, 505, 250, 115, "feature/cart", ("API pública",), "#FFFDFA", "#A9A49B"))
    body.append(node("fe-products", 845, 505, 250, 115, "feature/products", ("API pública",), "#FFFDFA", "#A9A49B"))
    body.append(node("fe-shared", 875, 285, 250, 115, "shared", ("UI · hooks · utilidades",), "#F5ECD8", "#C59132"))
    body.append('<path class="flow" d="M600 245V306"/><path class="flow" d="M520 420V460H230V501"/><path class="flow" d="M600 420V501"/><path class="flow" d="M680 420V460H970V501"/>')
    body.append('<path class="flow" d="M970 505V404"/><path class="flow" d="M725 562H815V400H871"/><path class="flow" d="M355 562H410V365H431"/>')
    body.append('<path d="M355 470H845" stroke="#B95736" stroke-width="3" stroke-dasharray="10 8"/><text x="600" y="455" class="sans label" fill="#B95736">sin imports entre features</text>')
    body.append(end_svg())
    (OUT / "cap15-dependencias-features.svg").write_text("".join(body), encoding="utf-8")

    mobile = [title_block_mobile(1160, title, desc, "REGLAS DE DEPENDENCIA")]
    steps = [("app", "compone rutas y providers"), ("pages", "ensambla recorridos"), ("features", "expone APIs públicas"), ("shared", "UI, hooks y utilidades")]
    fills = [("#F3E6DF", "#B95736"), ("#E8EEF1", "#31536A"), ("#FFFDFA", "#A9A49B"), ("#F5ECD8", "#C59132")]
    for i, ((heading, copy), (fill, stroke)) in enumerate(zip(steps, fills)):
        y = 95 + i * 205
        mobile.append(node(f"fe-mobile-{i}", 52, y, 316, 140, heading, (copy,), fill, stroke))
        if i < 3:
            mobile.append(f'<path class="flow" d="M210 {y + 140}V{y + 197}"/>')
    mobile.append('<rect id="fe-mobile-rule" x="52" y="920" width="316" height="150" rx="14" fill="#F3E6DF" stroke="#B95736" stroke-width="2"/><text data-container="fe-mobile-rule" data-padding="18" x="210" y="958" class="sans node-copy"><tspan x="210">Las features no se importan</tspan><tspan x="210" dy="26">ni dependen de app/store.</tspan><tspan x="210" dy="26">La composición resuelve el cruce.</tspan></text>')
    mobile.append(end_svg())
    (OUT / "cap15-dependencias-features-mobile.svg").write_text("".join(mobile), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    generate_mvc()
    generate_architecture_comparison()
    generate_api_first()
    card_comparison(
        "cap12-eleccion-estilo-api",
        "REST, GraphQL o tRPC",
        "Comparación entre tres estilos: REST modela recursos y HTTP; GraphQL permite consultas declarativas; tRPC comparte tipos entre un frontend y un backend TypeScript.",
        "Elige por consumidores, límites operativos y evolución del contrato",
        [
            {"title": "REST", "model": "recursos y semántica HTTP", "fit": "API pública o heterogénea|operaciones predecibles", "cost": "versionado y coordinación|del contrato"},
            {"title": "GraphQL", "model": "consulta declarativa|sobre un esquema", "fit": "clientes con vistas distintas|datos muy conectados", "cost": "límites de consulta|caché y observabilidad"},
            {"title": "tRPC", "model": "procedimientos y tipos|TypeScript compartidos", "fit": "frontend y backend TS|evolucionan juntos", "cost": "acoplamiento de lenguaje|y ciclo de despliegue"},
        ],
    )
    generate_data_model()
    generate_btree()
    generate_risk_matrix()
    generate_diagram_examples()
    generate_planning_cycle()
    generate_frontend_dependencies()
    card_comparison(
        "cap15-tipos-estado",
        "Cada estado necesita un propietario",
        "El estado local pertenece a un componente o feature; el estado compartido pertenece a una experiencia del cliente; los datos del servidor conservan al servidor como fuente de verdad y usan una caché de consultas.",
        "Clasifica por fuente de verdad, alcance y ciclo de vida",
        [
            {"title": "Local", "model": "un componente o feature|es su propietario", "fit": "formularios · toggles|modales · animaciones", "cost": "transiciones explícitas|y limpieza"},
            {"title": "Compartido", "model": "varias vistas del cliente|coordinan una experiencia", "fit": "sesión visible · carrito|tema · notificaciones", "cost": "alcance global|y dependencias ocultas"},
            {"title": "Servidor", "model": "el servidor es la fuente|la UI mantiene una caché", "fit": "productos · pedidos|usuarios · comentarios", "cost": "frescura · reintentos|invalidación y errores"},
        ],
    )


if __name__ == "__main__":
    main()
