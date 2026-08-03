#!/usr/bin/env python3
"""Genera la segunda pasada visual de los capítulos 21–23.

Las variantes móviles reorganizan la información para conservar la lectura;
no son miniaturas de la composición horizontal.
"""

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


def generate_testing_models() -> None:
    card_comparison(
        "cap21-modelos-confianza",
        "De la cantidad de tests a la evidencia útil",
        "La pirámide clásica optimiza coste por nivel; el Testing Trophy da más peso a la integración; una estrategia guiada por riesgo combina niveles según la propiedad que necesita demostrar.",
        "Los modelos orientan la inversión; ninguno prescribe una cuota universal",
        [
            {
                "title": "Pirámide clásica",
                "model": "muchos unitarios|menos integración y E2E",
                "fit": "unidades bien aisladas|E2E costosos o inestables",
                "cost": "puede premiar cantidad|sin validar colaboraciones",
            },
            {
                "title": "Testing Trophy",
                "model": "estático como base|integración como foco",
                "fit": "aplicaciones web|valor entre componentes",
                "cost": "fixtures y fronteras reales|deben ser mantenibles",
            },
            {
                "title": "Guiado por riesgo",
                "model": "propiedad → evidencia|entorno proporcional",
                "fit": "riesgos distintos|por flujo y dominio",
                "cost": "exige criterio explícito|y revisar la estrategia",
            },
        ],
    )


def generate_test_selection() -> None:
    card_comparison(
        "cap21-eleccion-nivel-prueba",
        "Elegir el nivel por la pregunta",
        "Una prueba unitaria aísla una regla, una de integración comprueba colaboraciones y una E2E recorre el sistema visible. El análisis estático atraviesa todo el código y detecta otra clase de defectos.",
        "Usa la prueba más pequeña que conserve la fidelidad necesaria",
        [
            {
                "title": "Unit",
                "model": "regla pura y determinista|sin red, DOM ni disco",
                "fit": "cálculos · validadores|transformaciones · estados",
                "cost": "mocks excesivos|pueden ocultar integración",
            },
            {
                "title": "Integration",
                "model": "piezas colaboran|en una frontera observable",
                "fit": "componentes · API · DB|contratos y errores",
                "cost": "datos de prueba|entorno y limpieza",
            },
            {
                "title": "End-to-end",
                "model": "flujo crítico completo|desde la interfaz",
                "fit": "checkout · acceso|onboarding · pago",
                "cost": "tiempo · diagnóstico|variabilidad del entorno",
            },
        ],
    )


def generate_tdd_ai() -> None:
    title = "TDD con un agente · evidencia antes que velocidad"
    desc = "La persona define un comportamiento observable y revisa el riesgo; el agente implementa hasta satisfacer la prueba; ambos refactorizan y amplían la evidencia antes de aceptar el cambio."
    desktop = [start_svg(1200, 720, title, desc, "La prueba es un criterio verificable, no una garantía completa")]
    steps = [
        ("1 · Definir", ("ejemplo · riesgo", "esperado"), "#E8EEF1", "#31536A"),
        ("2 · Comprobar", ("el test falla", "sin el cambio"), "#F3E6DF", "#B95736"),
        ("3 · Construir", ("el agente propone", "el cambio mínimo"), "#F5ECD8", "#C59132"),
        ("4 · Evaluar", ("dominio · seguridad", "alcance · claridad"), "#FFFDFA", "#A9A49B"),
        ("5 · Completar", ("límites · bordes", "regresión"), "#E8EEF1", "#31536A"),
    ]
    for i, (heading, copy, fill, stroke) in enumerate(steps):
        x = 35 + i * 232
        desktop.append(node(f"tdd-step-{i}", x, 225, 205, 175, heading, copy, fill, stroke))
        if i < len(steps) - 1:
            desktop.append(f'<path class="flow" d="M{x + 205} 312H{x + 228}"/>')
    desktop.append('<path class="risk-flow" d="M1065 400V525H140V404"/>')
    desktop.append(label("tdd-loop", 465, 507, 270, "nuevo riesgo o caso descubierto"))
    desktop.append('<rect id="tdd-note" x="225" y="585" width="750" height="80" rx="14" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text data-container="tdd-note" data-padding="16" x="600" y="618" class="sans node-copy"><tspan x="600">Un test puede aprobar una especificación incompleta.</tspan><tspan x="600" dy="25">La revisión humana decide si la evidencia representa el problema real.</tspan></text>')
    desktop.append(end_svg())

    mobile = [title_block_mobile(1280, title, desc, "TDD CON AGENTES")]
    for i, (heading, copy, fill, stroke) in enumerate(steps):
        y = 92 + i * 205
        mobile.append(node(f"tdd-mobile-{i}", 52, y, 316, 140, heading, copy, fill, stroke))
        if i < len(steps) - 1:
            mobile.append(f'<path class="flow" d="M210 {y + 140}V{y + 197}"/>')
    mobile.append('<rect id="tdd-mobile-note" x="52" y="1125" width="316" height="105" rx="14" fill="#F3E6DF" stroke="#B95736" stroke-width="2"/><text data-container="tdd-mobile-note" data-padding="16" x="210" y="1160" class="sans node-copy"><tspan x="210">Si aparece un riesgo nuevo,</tspan><tspan x="210" dy="25">vuelve a especificar y comprobar.</tspan></text>')
    mobile.append(end_svg())
    write("cap21-tdd-agente-evidencia", desktop, mobile)


def generate_ci_levels() -> None:
    card_comparison(
        "cap22-ci-entrega-despliegue",
        "CI, entrega continua y despliegue continuo",
        "Integración continua valida cambios frecuentes; entrega continua mantiene un artefacto apto para producción con una decisión de liberación; despliegue continuo automatiza también esa promoción cuando se cumplen las políticas.",
        "La diferencia está en qué se automatiza y dónde queda la decisión",
        [
            {
                "title": "Integración continua",
                "model": "cambio → build → pruebas|feedback al equipo",
                "fit": "cualquier equipo|que integra con frecuencia",
                "cost": "pipeline rápido|main siempre reparable",
            },
            {
                "title": "Entrega continua",
                "model": "artefacto listo|promoción controlada",
                "fit": "aprobación de negocio|o regulación",
                "cost": "ambientes repetibles|gates claros",
            },
            {
                "title": "Despliegue continuo",
                "model": "políticas cumplidas|promoción automática",
                "fit": "cambios pequeños|telemetría y reversión",
                "cost": "guardrails exigentes|respuesta operativa",
            },
        ],
    )


def generate_branching() -> None:
    card_comparison(
        "cap22-branching-lotes",
        "Branching · controlar el tamaño del lote",
        "GitFlow coordina releases mediante ramas especializadas; GitHub Flow usa una principal y ramas breves; trunk-based integra cambios mínimos directamente o mediante ramas de muy corta vida.",
        "La rama es un mecanismo de coordinación, no una medida de calidad",
        [
            {
                "title": "GitFlow",
                "model": "develop · release|feature · hotfix",
                "fit": "versiones programadas|múltiples líneas soportadas",
                "cost": "integración tardía|y más merges",
            },
            {
                "title": "GitHub Flow",
                "model": "main + rama breve|PR y despliegue",
                "fit": "revisión explícita|flujo simple",
                "cost": "necesita lotes pequeños|y checks confiables",
            },
            {
                "title": "Trunk-based",
                "model": "integración muy frecuente|ramas mínimas",
                "fit": "entrega continua|flags para trabajo oculto",
                "cost": "disciplina técnica|y reversión rápida",
            },
        ],
    )


def generate_flag_lifecycle() -> None:
    title = "Una feature flag también tiene ciclo de vida"
    desc = "El equipo crea una bandera con propietario y fecha de retiro, despliega el código inactivo, habilita por cohortes y señales, decide expandir o apagar, y finalmente elimina ambas rutas."
    desktop = [start_svg(1200, 720, title, desc, "Deploy no es release; una bandera temporal necesita retirada")]
    steps = [
        ("1 · Definir", ("dueño · propósito", "caducidad"), "#E8EEF1", "#31536A"),
        ("2 · Desplegar", ("ruta nueva apagada", "ruta estable activa"), "#FFFDFA", "#A9A49B"),
        ("3 · Exponer", ("cohorte estable", "señales del grupo"), "#F5ECD8", "#C59132"),
        ("4 · Decidir", ("expandir, pausar", "o desactivar"), "#F3E6DF", "#B95736"),
        ("5 · Retirar", ("borrar flag", "y código obsoleto"), "#E8EEF1", "#31536A"),
    ]
    for i, (heading, copy, fill, stroke) in enumerate(steps):
        x = 35 + i * 232
        desktop.append(node(f"flag-step-{i}", x, 225, 205, 175, heading, copy, fill, stroke))
        if i < len(steps) - 1:
            desktop.append(f'<path class="flow" d="M{x + 205} 312H{x + 228}"/>')
    desktop.append('<path class="risk-flow" d="M825 400V500H370V404"/>')
    desktop.append(label("flag-off", 485, 482, 225, "señal adversa · apagar"))
    desktop.append('<rect id="flag-note" x="225" y="575" width="750" height="90" rx="14" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text data-container="flag-note" data-padding="16" x="600" y="610" class="sans node-copy"><tspan x="600">Un kill switch reduce exposición, pero no revierte datos</tspan><tspan x="600" dy="25">ni sustituye la corrección y la investigación del incidente.</tspan></text>')
    desktop.append(end_svg())

    mobile = [title_block_mobile(1290, title, desc, "CREAR · EXPONER · RETIRAR")]
    for i, (heading, copy, fill, stroke) in enumerate(steps):
        y = 92 + i * 205
        mobile.append(node(f"flag-mobile-{i}", 52, y, 316, 140, heading, copy, fill, stroke))
        if i < len(steps) - 1:
            mobile.append(f'<path class="flow" d="M210 {y + 140}V{y + 197}"/>')
    mobile.append('<rect id="flag-mobile-note" x="52" y="1125" width="316" height="115" rx="14" fill="#F3E6DF" stroke="#B95736" stroke-width="2"/><text data-container="flag-mobile-note" data-padding="16" x="210" y="1160" class="sans node-copy"><tspan x="210">Si una señal empeora, apaga.</tspan><tspan x="210" dy="25">Después corrige, reconcilia</tspan><tspan x="210" dy="25">y retira la deuda temporal.</tspan></text>')
    mobile.append(end_svg())
    write("cap22-ciclo-feature-flag", desktop, mobile)


def generate_hosting_spectrum() -> None:
    card_comparison(
        "cap23-espectro-hosting",
        "Hosting · responsabilidad frente a abstracción",
        "Infraestructura ofrece mayor control operativo; una plataforma o contenedor administrado comparte responsabilidades; funciones y edge administran más del runtime, pero imponen contratos y límites específicos.",
        "Elige por requisitos y capacidad operativa, no por prestigio técnico",
        [
            {
                "title": "Infraestructura",
                "model": "VM · red · sistema|configurados por el equipo",
                "fit": "runtime o red especiales|control fino",
                "cost": "parches · capacidad|recuperación · guardias",
            },
            {
                "title": "Plataforma",
                "model": "app o contenedor|ciclo administrado",
                "fit": "servicio web común|equipo pequeño o medio",
                "cost": "límites del producto|red y portabilidad",
            },
            {
                "title": "Funciones y edge",
                "model": "ejecución por evento|distribución gestionada",
                "fit": "carga variable|trabajo cercano y acotado",
                "cost": "cuotas · latencia a datos|runtime específico",
            },
        ],
    )


def generate_deployment_strategies() -> None:
    card_comparison(
        "cap23-estrategias-despliegue",
        "Tres estrategias para cambiar una versión activa",
        "Rolling reemplaza capacidad por lotes; blue-green prepara dos entornos y conmuta tráfico; canary expone una fracción y decide con señales. Ninguna estrategia revierte por sí sola datos o efectos externos.",
        "Disponibilidad, exposición y coste cambian de forma distinta",
        [
            {
                "title": "Rolling",
                "model": "reemplazar instancias|por lotes graduales",
                "fit": "capacidad replicada|versiones compatibles",
                "cost": "v1 y v2 conviven|rollback vuelve a desplegar",
            },
            {
                "title": "Blue-green",
                "model": "dos entornos|conmutar el tráfico",
                "fit": "cambio rápido|validación previa",
                "cost": "capacidad duplicada|datos compartidos",
            },
            {
                "title": "Canary",
                "model": "exposición parcial|expandir por evidencia",
                "fit": "telemetría comparable|segmentación estable",
                "cost": "política y ventanas|reconciliar afectados",
            },
        ],
    )


def generate_promotion() -> None:
    title = "Promover el mismo artefacto entre ambientes"
    desc = "Un commit produce un artefacto inmutable; preview y staging verifican propiedades distintas; producción recibe ese mismo artefacto con configuración externa, y la liberación se observa y puede detenerse."
    desktop = [start_svg(1200, 720, title, desc, "Cambiar configuración no debe reconstruir el binario")]
    desktop.append(node("promo-source", 55, 215, 190, 150, "Commit", ("código revisado", "lockfile vigente"), "#E8EEF1", "#31536A"))
    desktop.append(node("promo-artifact", 310, 215, 215, 150, "Artefacto", ("inmutable", "ID verificable"), "#F5ECD8", "#C59132"))
    desktop.append(node("promo-preview", 590, 155, 245, 135, "Preview", ("cambio y UX", "datos aislados"), "#FFFDFA", "#A9A49B"))
    desktop.append(node("promo-staging", 590, 360, 245, 135, "Staging", ("integración y operación", "propiedades relevantes"), "#FFFDFA", "#A9A49B"))
    desktop.append(node("promo-production", 920, 255, 225, 155, "Producción", ("tráfico real", "señales y alertas"), "#F3E6DF", "#B95736"))
    desktop.append('<path class="flow" d="M245 290H306"/><path class="flow" d="M525 260H586"/><path class="flow" d="M525 320H555V427H586"/><path class="flow" d="M835 222H875V330H916"/><path class="flow" d="M835 427H875V335H916"/>')
    desktop.append(label("promo-config-a", 600, 300, 205, "configuración externa"))
    desktop.append('<path class="risk-flow" d="M1032 410V535H700V499"/>')
    desktop.append(label("promo-stop", 765, 517, 210, "detener o revertir app"))
    desktop.append('<rect id="promo-note" x="215" y="585" width="770" height="82" rx="14" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text data-container="promo-note" data-padding="16" x="600" y="618" class="sans node-copy"><tspan x="600">La paridad significa reproducir las propiedades que se validan.</tspan><tspan x="600" dy="25">Las diferencias inevitables deben ser explícitas y comprobables.</tspan></text>')
    desktop.append(end_svg())

    mobile = [title_block_mobile(1320, title, desc, "CONSTRUIR UNA VEZ · PROMOVER")]
    steps = [
        ("Commit", ("código revisado",), "#E8EEF1", "#31536A"),
        ("Artefacto", ("inmutable · identificado",), "#F5ECD8", "#C59132"),
        ("Preview", ("cambio · UX",), "#FFFDFA", "#A9A49B"),
        ("Staging", ("integración · operación",), "#FFFDFA", "#A9A49B"),
        ("Producción", ("tráfico · señales",), "#F3E6DF", "#B95736"),
    ]
    for i, (heading, copy, fill, stroke) in enumerate(steps):
        y = 92 + i * 205
        mobile.append(node(f"promo-mobile-{i}", 52, y, 316, 140, heading, copy, fill, stroke))
        if i < len(steps) - 1:
            mobile.append(f'<path class="flow" d="M210 {y + 140}V{y + 197}"/>')
    mobile.append('<rect id="promo-mobile-note" x="52" y="1125" width="316" height="135" rx="14" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text data-container="promo-mobile-note" data-padding="16" x="210" y="1160" class="sans node-copy"><tspan x="210">Mismo artefacto;</tspan><tspan x="210" dy="25">configuración externa.</tspan><tspan x="210" dy="25">Reversión de app ≠ datos.</tspan></text>')
    mobile.append(end_svg())
    write("cap23-promocion-artefacto", desktop, mobile)


def main() -> None:
    generate_testing_models()
    generate_test_selection()
    generate_tdd_ai()
    generate_ci_levels()
    generate_branching()
    generate_flag_lifecycle()
    generate_hosting_spectrum()
    generate_deployment_strategies()
    generate_promotion()
    print("Generados 9 pares SVG para los capítulos 21–23.")


if __name__ == "__main__":
    main()
