#!/usr/bin/env python3
"""Genera la segunda pasada visual del capítulo 30."""

from xml.sax.saxutils import escape

from generate_second_pass_visuals import (
    OUT,
    card_comparison,
    end_svg,
    node,
    start_svg,
    title_block_mobile,
)


def write(name: str, desktop: list[str], mobile: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.svg").write_text("".join(desktop), encoding="utf-8")
    (OUT / f"{name}-mobile.svg").write_text("".join(mobile), encoding="utf-8")


def label(ident: str, x: int, y: int, width: int, copy: str) -> str:
    return (
        f'<rect id="{ident}" x="{x}" y="{y}" width="{width}" height="36" '
        'rx="8" fill="#FFFDFA"/>'
        f'<text data-container="{ident}" data-padding="6" x="{x + width / 2:g}" '
        f'y="{y + 24}" class="sans label">{escape(copy)}</text>'
    )


def generate_context_path() -> None:
    title = "Contexto vigente · explorar menos, verificar mejor"
    desc = "Una intención acotada apunta a documentación y convenciones vigentes; el agente selecciona los archivos relevantes, propone un cambio coherente y verifica el resultado con pruebas y revisión."
    desktop = [start_svg(1200, 720, title, desc, "La estructura compartida ayuda a humanos y agentes")]
    steps = [
        ("Intención", ("alcance y criterio", "de aceptación"), "#E8EEF1", "#31536A"),
        ("Contexto", ("docs · ADR · reglas", "y ejemplos vigentes"), "#F5ECD8", "#C59132"),
        ("Selección", ("archivos y contratos", "realmente relevantes"), "#FFFDFA", "#A9A49B"),
        ("Cambio", ("diff pequeño", "alineado al sistema"), "#F3E6DF", "#B95736"),
        ("Evidencia", ("pruebas · revisión", "comportamiento"), "#E8EEF1", "#31536A"),
    ]
    for i, (heading, copy, fill, stroke) in enumerate(steps):
        x = 35 + i * 232
        desktop.append(node(f"ctx-step-{i}", x, 220, 205, 175, heading, copy, fill, stroke))
        if i < len(steps) - 1:
            desktop.append(f'<path class="flow" d="M{x + 205} 307H{x + 228}"/>')
    desktop.append('<path class="risk-flow" d="M1070 395V510H370V399"/>')
    desktop.append(label("ctx-loop", 475, 492, 450, "si la evidencia contradice el contexto, corregir ambos"))
    desktop.append('<rect id="ctx-note" x="225" y="575" width="750" height="88" rx="14" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text data-container="ctx-note" data-padding="16" x="600" y="610" class="sans node-copy"><tspan x="600">Documentar no evita explorar; reduce el espacio de búsqueda.</tspan><tspan x="600" dy="25">La documentación desactualizada puede dirigir el cambio al lugar equivocado.</tspan></text>')
    desktop.append(end_svg())

    mobile = [title_block_mobile(1300, title, desc, "CONTEXTO Y EVIDENCIA")]
    for i, (heading, copy, fill, stroke) in enumerate(steps):
        y = 92 + i * 205
        mobile.append(node(f"ctx-mobile-{i}", 52, y, 316, 140, heading, copy, fill, stroke))
        if i < len(steps) - 1:
            mobile.append(f'<path class="flow" d="M210 {y + 140}V{y + 197}"/>')
    mobile.append('<rect id="ctx-mobile-note" x="52" y="1125" width="316" height="150" rx="14" fill="#F3E6DF" stroke="#B95736" stroke-width="2"/><text data-container="ctx-mobile-note" data-padding="16" x="210" y="1158" class="sans node-copy"><tspan x="210">Si código y documentación</tspan><tspan x="210" dy="25">difieren, la discrepancia</tspan><tspan x="210" dy="25">es evidencia: investiga</tspan><tspan x="210" dy="25">y corrige la fuente.</tspan></text>')
    mobile.append(end_svg())
    write("cap30-contexto-vigente", desktop, mobile)


def generate_execution_models() -> None:
    card_comparison(
        "cap30-modelos-ejecucion",
        "Tres contratos de ejecución",
        "Una función determinista aplica una regla explícita; un modelo lingüístico produce una salida condicionada por prompt y contexto; un agente añade decisiones, herramientas y estado externo que deben observarse y limitarse.",
        "Cuanto más abierta es la ejecución, más importante es el oráculo",
        [
            {
                "title": "Función",
                "model": "entrada + estado|regla explícita",
                "fit": "contrato estable|resultado reproducible",
                "cost": "depurar variables|y flujo observable",
            },
            {
                "title": "Modelo lingüístico",
                "model": "prompt + contexto|salida probabilística",
                "fit": "síntesis · lenguaje|propuestas variadas",
                "cost": "muestreo y evaluación|supuestos no visibles",
            },
            {
                "title": "Agente",
                "model": "modelo + herramientas|decisiones y efectos",
                "fit": "tarea multietapa|con feedback externo",
                "cost": "permisos · trazas|parada y recuperación",
            },
        ],
    )


def generate_builder_gardener() -> None:
    title = "Constructor y jardinero · dos formas de intervenir"
    desc = "La mentalidad de constructor controla cada paso de una implementación; la de jardinero prepara contexto, límites y evidencia para orientar resultados variables. El trabajo real combina ambas según el riesgo."
    desktop = [start_svg(1200, 720, title, desc, "No son roles excluyentes: cambia el grado de control directo")]
    desktop.append(node("bg-builder", 65, 150, 490, 450, "Constructor", (), "#E8EEF1", "#31536A", 205))
    desktop.append(node("bg-gardener", 645, 150, 490, 450, "Jardinero", (), "#F5ECD8", "#C59132", 205))
    rows = [
        ("INTERVENCIÓN", "decide cada paso", "define condiciones y límites"),
        ("CONTROL", "flujo explícito", "feedback y ajuste"),
        ("DEPURACIÓN", "código y estado", "contexto, herramientas y salida"),
        ("EVIDENCIA", "pruebas del programa", "diff, pruebas, trazas y revisión"),
    ]
    for i, (tag, left, right) in enumerate(rows):
        y = 270 + i * 78
        desktop.append(f'<text x="105" y="{y}" class="sans tag">{tag}</text><text x="105" y="{y + 28}" class="sans small">{escape(left)}</text>')
        desktop.append(f'<text x="685" y="{y}" class="sans tag">{tag}</text><text x="685" y="{y + 28}" class="sans small">{escape(right)}</text>')
    desktop.append('<rect id="bg-note" x="260" y="625" width="680" height="58" rx="12" fill="#F3E6DF" stroke="#B95736" stroke-width="2"/><text data-container="bg-note" data-padding="12" x="600" y="661" class="sans node-copy">Usa control directo donde el riesgo o el oráculo lo exijan.</text>')
    desktop.append(end_svg())

    mobile = [title_block_mobile(1110, title, desc, "CONTROL DIRECTO · CONDICIONES")]
    cards = [
        ("Constructor", ("decide cada paso", "depura código y estado", "prueba el programa"), "#E8EEF1", "#31536A"),
        ("Jardinero", ("prepara contexto y límites", "observa herramientas y salida", "ajusta con evidencia"), "#F5ECD8", "#C59132"),
        ("Decisión", ("combinar según riesgo", "reversibilidad y oráculo"), "#F3E6DF", "#B95736"),
    ]
    for i, (heading, copy, fill, stroke) in enumerate(cards):
        y = 92 + i * 285
        mobile.append(node(f"bg-mobile-{i}", 52, y, 316, 210, heading, copy, fill, stroke))
        if i < len(cards) - 1:
            mobile.append(f'<path class="flow" d="M210 {y + 210}V{y + 277}"/>')
    mobile.append('<rect id="bg-mobile-note" x="52" y="935" width="316" height="110" rx="14" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text data-container="bg-mobile-note" data-padding="16" x="210" y="970" class="sans node-copy"><tspan x="210">Delegar la construcción no delega</tspan><tspan x="210" dy="25">la responsabilidad por</tspan><tspan x="210" dy="25">el resultado del sistema.</tspan></text>')
    mobile.append(end_svg())
    write("cap30-constructor-jardinero", desktop, mobile)


def generate_organization_conditions() -> None:
    title = "La organización prepara el terreno"
    desc = "Documentación y contexto, estructura y convenciones, herramientas y procesos, y cultura y prácticas se refuerzan para producir cambios pequeños, revisables y coherentes."
    desktop = [start_svg(1200, 760, title, desc, "La efectividad del agente también es una propiedad del sistema de trabajo")]
    cards = [
        ("Contexto", ("arquitectura · ADR", "instrucciones vigentes"), "#E8EEF1", "#31536A"),
        ("Convenciones", ("nombres · módulos", "contratos predecibles"), "#F5ECD8", "#C59132"),
        ("Guardrails", ("CI · tests · linters", "permisos y aprobaciones"), "#F3E6DF", "#B95736"),
        ("Prácticas", ("delegación consciente", "revisión y aprendizaje"), "#FFFDFA", "#A9A49B"),
    ]
    positions = [(80, 155), (665, 155), (80, 430), (665, 430)]
    for i, ((heading, copy, fill, stroke), (x, y)) in enumerate(zip(cards, positions)):
        desktop.append(node(f"org-card-{i}", x, y, 455, 190, heading, copy, fill, stroke))
    desktop.append(node("org-outcome", 430, 330, 340, 125, "Cambio revisable", ("alcance · evidencia", "responsable"), "#FFFDFA", "#A9A49B"))
    desktop.append('<path class="flow" d="M535 250H600V326"/><path class="flow" d="M665 250H600V326"/><path class="flow" d="M535 525H600V459"/><path class="flow" d="M665 525H600V459"/>')
    desktop.append(end_svg())

    mobile = [title_block_mobile(1370, title, desc, "CONDICIONES DE EQUIPO")]
    for i, (heading, copy, fill, stroke) in enumerate(cards):
        y = 92 + i * 230
        mobile.append(node(f"org-mobile-{i}", 52, y, 316, 165, heading, copy, fill, stroke))
        mobile.append(f'<path class="flow" d="M210 {y + 165}V{y + 222}"/>')
    mobile.append(node("org-mobile-result", 52, 1015, 316, 175, "Cambio revisable", ("alcance · evidencia", "responsable"), "#F3E6DF", "#B95736"))
    mobile.append('<rect id="org-mobile-note" x="52" y="1240" width="316" height="80" rx="14" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text data-container="org-mobile-note" data-padding="14" x="210" y="1273" class="sans node-copy"><tspan x="210">Una herramienta no compensa</tspan><tspan x="210" dy="24">un sistema de trabajo ambiguo.</tspan></text>')
    mobile.append(end_svg())
    write("cap30-condiciones-organizacionales", desktop, mobile)


def generate_multiagent() -> None:
    title = "Multiagente · paralelizar sin perder integración"
    desc = "El orquestador delega tareas independientes con contratos de entrada y salida; cada agente produce un entregable verificable; la integración detecta conflictos y reúne evidencia antes de aceptar."
    desktop = [start_svg(1200, 760, title, desc, "La concurrencia sirve cuando los límites y entregables son explícitos")]
    desktop.append(node("ma-orch", 430, 125, 340, 130, "Orquestador", ("divide · limita", "define aceptación"), "#E8EEF1", "#31536A"))
    agents = [
        ("Backend", ("API y dominio", "contrato A")),
        ("Frontend", ("interfaz y estados", "contrato B")),
        ("Verificación", ("pruebas y revisión", "evidencia C")),
    ]
    for i, (heading, copy) in enumerate(agents):
        x = 55 + i * 390
        desktop.append(node(f"ma-agent-{i}", x, 350, 310, 175, heading, copy, "#FFFDFA", "#A9A49B"))
        desktop.append(f'<path class="flow" d="M600 255V300H{x + 155}V346"/>')
    desktop.append(node("ma-integrate", 390, 610, 420, 110, "Integración", ("conflictos · pruebas · revisión",), "#F3E6DF", "#B95736"))
    for i in range(3):
        x = 210 + i * 390
        desktop.append(f'<path class="flow" d="M{x} 525V565H600V606"/>')
    desktop.append(label("ma-contract", 490, 282, 220, "entrada y salida definidas"))
    desktop.append(end_svg())

    mobile = [title_block_mobile(1370, title, desc, "DELEGAR · VERIFICAR · INTEGRAR")]
    mobile.append(node("ma-mobile-orch", 52, 92, 316, 155, "Orquestador", ("divide y define aceptación",), "#E8EEF1", "#31536A"))
    mobile.append('<path class="flow" d="M210 247V310"/>')
    for i, (heading, copy) in enumerate(agents):
        y = 320 + i * 225
        mobile.append(node(f"ma-mobile-agent-{i}", 52, y, 316, 160, heading, copy, "#FFFDFA", "#A9A49B"))
        mobile.append(f'<path class="flow" d="M210 {y + 160}V{y + 217}"/>')
    mobile.append(node("ma-mobile-integrate", 52, 1005, 316, 175, "Integración", ("conflictos · pruebas", "revisión humana"), "#F3E6DF", "#B95736"))
    mobile.append('<rect id="ma-mobile-note" x="52" y="1225" width="316" height="110" rx="14" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text data-container="ma-mobile-note" data-padding="14" x="210" y="1258" class="sans node-copy"><tspan x="210">Si las tareas se solapan,</tspan><tspan x="210" dy="24">integrar puede costar más</tspan><tspan x="210" dy="24">que el paralelismo ganado.</tspan></text>')
    mobile.append(end_svg())
    write("cap30-orquestacion-multiagente", desktop, mobile)


def main() -> None:
    generate_context_path()
    generate_execution_models()
    generate_builder_gardener()
    generate_organization_conditions()
    generate_multiagent()
    print("Generados 5 pares SVG para la segunda pasada del capítulo 30.")


if __name__ == "__main__":
    main()
