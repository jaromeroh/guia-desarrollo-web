#!/usr/bin/env python3
"""Genera la serie editorial de diagramas ancla para los capítulos 10–19."""

import argparse
from html import escape
from pathlib import Path
from textwrap import wrap

OUT = Path(__file__).resolve().parents[1] / "assets" / "diagrams"

DIAGRAMS = [
    ("cap10-proceso-diseno", "DISEÑAR ES REDUCIR INCERTIDUMBRE", "Proceso de diseño de producto", "Entender, explorar, definir y validar forman un ciclo que reduce incertidumbre antes de aumentar fidelidad.", [
        ("Entender", "usuario · tarea · contexto"), ("Explorar", "alternativas · supuestos"), ("Definir", "flujo · alcance · criterios"), ("Validar", "evidencia · aprendizaje")], "La fidelidad aumenta después de aclarar el problema, no antes."),
    ("cap10-estados-ui", "UNA PANTALLA, VARIOS ESTADOS", "Estados esenciales de una interfaz", "Vacío, carga, error, parcial, éxito y permisos requieren contenido y acciones distintas.", [
        ("Vacío", "orientar el primer paso"), ("Carga", "mostrar progreso"), ("Error", "explicar y recuperar"), ("Parcial", "degradar con honestidad"), ("Éxito", "confirmar el resultado"), ("Permisos", "explicar el límite")], "Diseñar solo el camino feliz deja decisiones críticas al momento de implementar."),
    ("cap11-dependencias-arquitectura", "LA ARQUITECTURA ORDENA DEPENDENCIAS", "Dependencias hacia el núcleo", "Entrada e infraestructura dependen de contratos; los casos de uso y el dominio no dependen de frameworks ni bases de datos.", [
        ("Entrada", "HTTP · CLI · eventos"), ("Casos de uso", "coordinar la intención"), ("Dominio", "reglas e invariantes"), ("Adaptadores", "BD · correo · proveedores")], "Protege las reglas que cambian por negocio de los detalles que cambian por tecnología."),
    ("cap12-contrato-api", "EL CONTRATO COORDINA DOS LADOS", "Contrato de una API", "Consumidor y proveedor acuerdan solicitud, respuesta, errores, seguridad y evolución antes de acoplar implementaciones.", [
        ("Necesidad", "acción del consumidor"), ("Solicitud", "método · URL · datos"), ("Contrato", "esquema · errores · seguridad"), ("Respuesta", "estado · contenido · metadatos")], "API-first permite validar el intercambio antes de terminar la implementación."),
    ("cap13-niveles-modelado", "TRES MODELOS, TRES PREGUNTAS", "Niveles del modelado de datos", "El modelo conceptual identifica conceptos, el lógico define relaciones y restricciones, y el físico decide almacenamiento e índices.", [
        ("Conceptual", "¿qué existe?"), ("Lógico", "¿cómo se relaciona?"), ("Físico", "¿cómo se almacena?"), ("Evolución", "¿cómo cambia sin perder datos?")], "Las tablas son una implementación del modelo, no el punto de partida."),
    ("cap14-slice-vertical", "ENTREGAR UNA CAPACIDAD COMPLETA", "Slice vertical frente a capas aisladas", "Un slice vertical atraviesa interfaz, aplicación y datos para entregar una conducta verificable; un slice horizontal termina una capa sin valor observable.", [
        ("Usuario", "acción y resultado"), ("Interfaz", "estado y feedback"), ("Aplicación", "reglas y autorización"), ("Datos", "persistencia e integridad")], "Corta por resultado de usuario; coordina el trabajo técnico dentro del corte."),
    ("cap15-estrategias-renderizado", "ELIGE DÓNDE Y CUÁNDO RENDERIZAR", "Estrategias de renderizado frontend", "CSR, SSR, SSG y revalidación distribuyen trabajo, frescura y complejidad de forma diferente.", [
        ("CSR", "navegador · interacción rica"), ("SSR", "servidor por solicitud"), ("SSG", "construcción anticipada"), ("Revalidación", "estático con frescura controlada")], "La mejor estrategia puede variar por ruta; no tiene que ser una decisión global."),
    ("cap16-pipeline-backend", "UNA SOLICITUD CRUZA RESPONSABILIDADES", "Pipeline de backend", "La entrada recibe y correlaciona, el middleware aplica políticas, el caso de uso coordina, el dominio decide y la salida traduce el resultado.", [
        ("Entrada", "parsear · request ID"), ("Políticas", "auth · límites · validación"), ("Caso de uso", "coordinar dependencias"), ("Dominio y salida", "decidir · persistir · responder")], "Los errores conservan causa y contexto; la respuesta pública no filtra detalles sensibles."),
    ("cap17-flujos-identidad", "IDENTIDAD NO ES UNA SOLA TECNOLOGÍA", "Capas de un flujo de identidad", "Credencial, autenticación, sesión, autorización y auditoría resuelven preguntas distintas en cada solicitud.", [
        ("Credencial", "passkey · contraseña · proveedor"), ("Autenticación", "¿quién demostró ser?"), ("Sesión", "¿cómo continúa el contexto?"), ("Autorización", "¿puede hacer esta acción?"), ("Auditoría", "¿qué evidencia queda?")], "JWT, cookie y OAuth no sustituyen el modelo de permisos."),
    ("cap18-eleccion-tiempo-real", "USA EL CANAL MÁS SIMPLE QUE CUMPLA", "Elección de comunicación en tiempo real", "Polling, SSE, WebSocket y WebTransport cubren necesidades crecientes de dirección, frecuencia y control.", [
        ("Polling", "cambios ocasionales"), ("SSE", "servidor → cliente"), ("WebSocket", "bidireccional persistente"), ("WebTransport", "flujos especializados")], "Decide también reconexión, orden, backpressure, autorización y escalado."),
    ("cap19-transaccion-consistencia", "LA INVARIANTE DEFINE LA TRANSACCIÓN", "De la intención a una transacción consistente", "Una operación lee estado, valida una invariante, escribe cambios atómicos y publica efectos externos después del commit.", [
        ("Leer", "estado visible"), ("Validar", "saldo · stock · versión"), ("Escribir", "cambios atómicos"), ("Confirmar", "commit o rollback"), ("Propagar", "evento · caché · búsqueda")], "El nivel de aislamiento se elige por la anomalía que rompería la invariante."),
    ("cap20-ciclo-job-confiable", "ASÍNCRONO NO SIGNIFICA INCONTROLADO", "Ciclo de un trabajo confiable", "Una solicitud confirma la aceptación después de persistir el trabajo; un worker ejecuta con idempotencia, reintentos limitados y evidencia observable.", [
        ("Aceptar", "validar · idempotency key"), ("Persistir", "job y estado durable"), ("Ejecutar", "worker con límites"), ("Recuperar", "backoff · DLQ · compensación"), ("Observar", "estado · métricas · trazas")], "No confirmes al usuario un trabajo que todavía no puede recuperarse tras un fallo."),
    ("cap21-estrategia-testing", "CONFIANZA CON FEEDBACK PROPORCIONAL", "Capas de una estrategia de pruebas", "Cada capa responde preguntas distintas; la mayor inversión suele estar en integración y contratos, con pocos recorridos completos de alto valor.", [
        ("Análisis estático", "tipos · lint · build"), ("Unidad", "reglas e invariantes"), ("Integración", "fronteras y contratos"), ("Extremo a extremo", "recorridos críticos"), ("Producción", "señales y aprendizaje")], "Optimiza el tiempo hasta obtener evidencia útil, no la cantidad bruta de tests."),
    ("cap22-pipeline-entrega", "UN CAMBIO DEBE PRODUCIR EVIDENCIA", "Pipeline de integración y entrega", "El pipeline transforma un cambio revisable en un artefacto trazable, lo despliega de forma repetible y separa despliegue de exposición al usuario.", [
        ("Cambio", "commit pequeño · revisión"), ("Validar", "tests · seguridad · build"), ("Artefacto", "inmutable · identificado"), ("Desplegar", "ambiente · migración"), ("Liberar", "flag · observación · reversión")], "La misma versión validada avanza entre ambientes; no se reconstruye en cada etapa."),
    ("cap23-despliegue-progresivo", "DESPLEGAR ES CAMBIAR UN SISTEMA VIVO", "Despliegue progresivo y reversible", "Una versión se verifica en un entorno efímero, recibe una porción controlada de tráfico y solo se promueve cuando las señales cumplen los criterios.", [
        ("Construir", "artefacto y configuración"), ("Previsualizar", "entorno efímero"), ("Exponer", "canary · porcentaje"), ("Evaluar", "salud · negocio · errores"), ("Promover o revertir", "decisión automatizable")], "Una reversión de código no deshace automáticamente datos, mensajes ni efectos externos."),
    ("cap24-correlacion-senales", "LAS SEÑALES RESPONDEN JUNTAS", "Correlación para explicar un incidente", "Un identificador de solicitud y el contexto de traza conectan eventos detallados, comportamiento agregado y causalidad entre servicios.", [
        ("Pregunta", "impacto y periodo"), ("Métricas", "dónde y cuándo"), ("Trazas", "camino y dependencia"), ("Logs", "detalle con contexto"), ("Acción", "mitigar · verificar · aprender")], "Instrumenta fronteras para conservar identidad, tiempo, resultado y causa."),
    ("cap25-ciclo-capacidad", "ESCALAR EMPIEZA POR MEDIR", "Ciclo de capacidad y rendimiento", "Un presupuesto convierte expectativas en límites; la medición localiza el cuello de botella y los controles evitan que la saturación se propague.", [
        ("Presupuestar", "latencia · volumen · costo"), ("Medir", "carga representativa"), ("Localizar", "recurso saturado"), ("Proteger", "límites · backpressure"), ("Verificar", "repetir y planificar")], "Añadir réplicas no corrige una base de datos caliente, una cola ilimitada ni trabajo innecesario."),
    ("cap26-fronteras-confianza", "CADA FRONTERA CAMBIA LA CONFIANZA", "Controles a través de fronteras de confianza", "Datos y acciones cruzan cliente, edge, aplicación, persistencia y terceros; cada cruce exige validar identidad, intención, formato y capacidad.", [
        ("Cliente", "entrada no confiable"), ("Edge", "TLS · límites · origen"), ("Aplicación", "authn · authz · validación"), ("Datos", "mínimo privilegio · cifrado"), ("Terceros", "allowlist · timeout · evidencia")], "La autorización se verifica en el servidor para cada acción sensible, aunque la interfaz la oculte."),
    ("cap27-slice-nextjs", "MISMO SLICE, MECANISMOS DE NEXT.JS", "Slice vertical: solicitud de soporte", "El recorrido conserva contrato, caso de uso e invariante; Next.js aporta entradas de servidor, renderizado y caché que deben mantenerse fuera del dominio.", [
        ("Entrada HTTP", "Route Handler · Server Action"), ("Caso de uso", "TypeScript · puertos"), ("Dominio", "reglas sin framework"), ("Persistencia", "consulta · transacción"), ("Operación", "tests · logs · deploy")], "Server Components y caché son decisiones de entrega; no sustituyen el modelo del dominio."),
    ("cap28-slice-fastapi", "MISMO SLICE, MECANISMOS DE FASTAPI", "Slice vertical: solicitud de soporte", "FastAPI y Pydantic traducen HTTP; el caso de uso conserva las reglas y SQLAlchemy ejecuta la unidad de trabajo sin invadir el dominio.", [
        ("Entrada HTTP", "FastAPI · Pydantic"), ("Caso de uso", "Python · dependencias"), ("Dominio", "reglas sin framework"), ("Persistencia", "SQLAlchemy · transacción"), ("Operación", "pytest · logs · contenedor")], "Una sesión de base de datos pertenece a la unidad de trabajo, no a la identidad del usuario."),
    ("cap29-slice-go", "MISMO SLICE, MECANISMOS DE GO", "Slice vertical: solicitud de soporte", "net/http adapta la entrada, funciones explícitas coordinan el caso de uso y database/sql protege la transacción con contexto y límites.", [
        ("Entrada HTTP", "net/http · JSON limitado"), ("Caso de uso", "interfaces pequeñas"), ("Dominio", "reglas y errores"), ("Persistencia", "database/sql · tx"), ("Operación", "httptest · métricas · binario")], "Las goroutines no convierten trabajo sin dueño en trabajo confiable; conserva cancelación y límites."),
    ("cap30-ciclo-agente", "ACTUAR REQUIERE CERRAR EL CICLO", "Ciclo de trabajo de un agente", "Un agente recibe una intención, reúne contexto suficiente, propone o decide un plan, actúa mediante herramientas y verifica evidencia antes de declarar el resultado.", [
        ("Intención", "objetivo · límites · criterio"), ("Contexto", "instrucciones · archivos · estado"), ("Plan", "pasos · riesgos · permisos"), ("Acción", "herramientas · cambios"), ("Verificación", "tests · diff · evidencia")], "El resultado no es el texto del modelo: es el estado observable después de verificar la acción."),
    ("cap30-mcp-interoperabilidad", "EL PROTOCOLO NO CONCEDE PERMISOS", "Interoperabilidad mediante MCP", "El host conecta un cliente MCP con servidores que publican capacidades; autenticación, consentimiento y políticas siguen perteneciendo al sistema que los integra.", [
        ("Persona", "intención y aprobación"), ("Host", "contexto · política · modelo"), ("Cliente MCP", "negocia capacidades"), ("Servidor MCP", "tools · resources · prompts"), ("Sistema externo", "datos y efectos reales")], "MCP reduce adaptadores específicos; no vuelve confiable una herramienta ni autoriza su uso automáticamente."),
    ("cap30-control-autonomia", "LA AUTONOMÍA SE DISEÑA POR CAPAS", "Superficie de control de un agente", "El control efectivo combina un alcance explícito, contexto limitado, permisos mínimos, aprobaciones para efectos sensibles y evidencia que permita detener o revertir.", [
        ("Alcance", "objetivo y exclusiones"), ("Contexto", "mínimo suficiente"), ("Permisos", "leer · actuar · denegar"), ("Aprobaciones", "efectos sensibles"), ("Evidencia y parada", "logs · pruebas · límites")], "Más autonomía solo es razonable cuando el trabajo es acotado, observable y recuperable."),
    ("cap31-filtro-adopcion", "DE LA NOVEDAD A UNA DECISIÓN OPERABLE", "Filtro para adoptar una tecnología", "Una tendencia solo avanza si resuelve un problema real, cuenta con evidencia, supera un experimento acotado y tiene propietario, operación y salida.", [
        ("Problema", "necesidad y contexto"), ("Evidencia", "estándar · soporte · casos"), ("Experimento", "hipótesis · límite · métrica"), ("Operación", "costo · seguridad · dueño"), ("Decisión", "adoptar · observar · salir")], "Revisa la decisión en una fecha explícita; madurez y necesidades cambian."),
    ("apc-ruta-aprendizaje", "APRENDER ES CERRAR RECORRIDOS", "Ruta de aprendizaje del desarrollo web", "La ruta avanza desde la plataforma web hasta datos, operación y distribución; luego compara stacks y usa IA con un diario de calibración.", [
        ("Plataforma web", "HTML · CSS · JS · red"), ("Aplicación con datos", "contrato · auth · transacción"), ("Calidad y operación", "tests · entrega · señales"), ("Sistemas distribuidos", "fallos · colas · consistencia"), ("Comparar stacks", "mismo slice · trade-offs"), ("IA asistida", "delegar · verificar · calibrar")], "Cada etapa produce un proyecto y una explicación; acumular recursos no sustituye la práctica."),
]

COLORS = [("#E8EEF1", "#31536A"), ("#FFFDFA", "#A9A49B"), ("#F5ECD8", "#C59132"), ("#E8EEF1", "#31536A"), ("#F3E6DF", "#B95736"), ("#FFFDFA", "#A9A49B")]

def text_lines(value, limit):
    return wrap(value, width=limit, break_long_words=False, break_on_hyphens=False) or [value]

def centered_tspans(value, x, y, css_class, limit, line_height, container=None, padding=20):
    lines = text_lines(value, limit)
    start = y - (len(lines) - 1) * line_height / 2
    spans = "".join(
        f'<tspan x="{x:.1f}" y="{start + i * line_height:.1f}">{escape(line)}</tspan>'
        for i, line in enumerate(lines)
    )
    container_attrs = (
        f' data-container="{escape(container)}" data-padding="{padding}"'
        if container else ""
    )
    return f'<text class="s {css_class}"{container_attrs}>{spans}</text>'

def desktop(name, tag, title, desc, cards, footer):
    n = len(cards); gap = 22; left = 72; total = 1056; width = (total - gap * (n - 1)) / n
    head_size = 18 if n >= 6 else 20
    head_padding = 18 if n >= 6 else 20
    copy_size = 16 if n >= 6 else 18
    boxes = []
    for i, (heading, copy) in enumerate(cards):
        x = left + i * (width + gap); fill, stroke = COLORS[i]
        copy_limit = max(13, int(width / 13))
        card_id = f"{name}-card-{i + 1}"
        boxes.append(f'<rect id="{card_id}" x="{x:.1f}" y="210" width="{width:.1f}" height="270" rx="22" fill="{fill}" stroke="{stroke}" stroke-width="3"/><circle cx="{x+width/2:.1f}" cy="254" r="22" fill="{stroke}"/><text x="{x+width/2:.1f}" y="261" class="s num" fill="#fff" data-container="{card_id}" data-padding="20">{i+1}</text>{centered_tspans(heading, x+width/2, 316, "head", copy_limit, 28, card_id, head_padding)}{centered_tspans(copy, x+width/2, 382, "copy", copy_limit, 24, card_id)}')
    arrows = ''.join(f'<path d="M{left+(i+1)*width+i*gap:.1f} 345H{left+(i+1)*width+(i+1)*gap-8:.1f}" stroke="#31536A" stroke-width="4" marker-end="url(#a)"/>' for i in range(n-1))
    footer_id = f"{name}-footer"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 720" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc><defs><style>.s{{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#20262E}}.tag{{font-size:21px;font-weight:760;letter-spacing:2px;fill:#31536A}}.title{{font-size:30px;font-weight:760}}.head{{font-size:{head_size}px;font-weight:760;text-anchor:middle}}.copy{{font-size:{copy_size}px;fill:#59636D;text-anchor:middle}}.num{{font-size:17px;font-weight:780;text-anchor:middle}}.foot{{font-size:20px;font-weight:700;text-anchor:middle}}</style><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#31536A"/></marker></defs><rect width="1200" height="720" fill="#F2EEE6"/><rect x="38" y="38" width="1124" height="644" rx="26" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2.5"/><text x="72" y="84" class="s tag">{escape(tag)}</text><text x="72" y="146" class="s title">{escape(title)}</text>{''.join(boxes)}{arrows}<rect id="{footer_id}" x="126" y="548" width="948" height="90" rx="18" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/>{centered_tspans(footer, 600, 598, "foot", 78, 25, footer_id)}</svg>'''

def mobile(name, tag, title, desc, cards, footer):
    n = len(cards); h = 176; gap = 46; start = 108
    footer_limit = 32
    footer_lines = text_lines(footer, footer_limit)
    total_h = start + n * h + (n-1)*gap + 90 + len(footer_lines) * 24
    boxes=[]
    for i,(heading,copy) in enumerate(cards):
        y=start+i*(h+gap); fill,stroke=COLORS[i]
        card_id = f"{name}-mobile-card-{i + 1}"
        boxes.append(f'<rect id="{card_id}" x="38" y="{y}" width="344" height="{h}" rx="20" fill="{fill}" stroke="{stroke}" stroke-width="3"/><circle cx="72" cy="{y+38}" r="20" fill="{stroke}"/><text x="72" y="{y+44}" class="s num" fill="#fff" data-container="{card_id}" data-padding="20">{i+1}</text><text x="108" y="{y+44}" class="s head" data-container="{card_id}" data-padding="20">{escape(heading)}</text>{centered_tspans(copy, 210, y+108, "copy", 28, 22, card_id)}')
        if i<n-1: boxes.append(f'<path d="M210 {y+h}V{y+h+38}" stroke="#31536A" stroke-width="4" marker-end="url(#a)"/>')
    fy=start+n*h+(n-1)*gap+56
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 {total_h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)} en composición vertical</title><desc id="desc">{escape(desc)}</desc><defs><style>.s{{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#20262E}}.tag{{font-size:16px;font-weight:760;letter-spacing:1.15px;fill:#31536A}}.head{{font-size:21px;font-weight:760}}.copy{{font-size:17px;fill:#59636D;text-anchor:middle}}.num{{font-size:15px;font-weight:780;text-anchor:middle}}.foot{{font-size:16px;font-weight:700;text-anchor:middle}}</style><marker id="a" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#31536A"/></marker></defs><rect width="420" height="{total_h}" fill="#F2EEE6"/><rect x="16" y="16" width="388" height="{total_h-32}" rx="22" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text x="38" y="58" class="s tag">{escape(tag)}</text>{''.join(boxes)}{centered_tspans(footer, 210, fy, "foot", footer_limit, 24)}</svg>'''

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--only",
        nargs="*",
        metavar="NAME",
        help="Genera únicamente los nombres indicados (sin extensión).",
    )
    args = parser.parse_args()
    selected = set(args.only or [])
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in DIAGRAMS:
        name, tag, title, desc, cards, footer = spec
        if selected and name not in selected:
            continue
        (OUT / f"{name}.svg").write_text(desktop(*spec), encoding="utf-8")
        (OUT / f"{name}-mobile.svg").write_text(mobile(*spec), encoding="utf-8")

if __name__ == "__main__":
    main()
