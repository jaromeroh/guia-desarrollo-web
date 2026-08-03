#!/usr/bin/env python3
"""Genera la segunda pasada visual de los capítulos 17–20.

Cada concepto tiene una composición de escritorio y otra móvil. Las variantes
móviles reorganizan la información; no son una miniatura del diagrama ancho.
"""

from pathlib import Path
from xml.sax.saxutils import escape

from generate_second_pass_visuals import (
    COLORS,
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


def flow_label(ident: str, x: int, y: int, width: int, text: str) -> str:
    return (
        f'<rect id="{ident}" x="{x}" y="{y}" width="{width}" height="34" '
        'rx="8" fill="#FFFDFA"/>'
        f'<text data-container="{ident}" data-padding="6" x="{x + width / 2:g}" '
        f'y="{y + 23}" class="sans label">{escape(text)}</text>'
    )


def generate_session_token() -> None:
    title = "Sesión referenciada o token autocontenido"
    desc = (
        "Una sesión referenciada permite revocar el estado en el servidor de forma directa; "
        "un token autocontenido se verifica localmente pero necesita expiración breve, rotación "
        "o estado adicional cuando la revocación debe ser inmediata."
    )
    desktop = [start_svg(1200, 720, title, desc, "La diferencia decisiva es dónde vive el estado y cómo se revoca")]
    desktop.append('<rect x="38" y="125" width="1124" height="535" rx="24" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/>')
    desktop.append(node("st-browser-a", 75, 205, 220, 125, "Cliente web", ("cookie con ID opaco",), "#E8EEF1", "#31536A"))
    desktop.append(node("st-app-a", 430, 205, 220, 125, "Aplicación", ("resuelve el ID",), "#FFFDFA", "#A9A49B"))
    desktop.append(node("st-store", 785, 205, 300, 125, "Almacén de sesiones", ("identidad · riesgo · vigencia",), "#F5ECD8", "#C59132"))
    desktop.append('<path class="flow" d="M295 268H426"/><path class="flow" d="M650 268H781"/>')
    desktop.append(flow_label("st-label-a", 310, 218, 100, "ID opaco"))
    desktop.append(flow_label("st-label-b", 665, 218, 104, "consulta"))
    desktop.append('<path class="risk-flow" d="M935 330V375H540V407"/>')
    desktop.append(flow_label("st-label-revoke", 690, 342, 210, "invalidación inmediata"))
    desktop.append(node("st-client-b", 75, 455, 220, 125, "Cliente API", ("access token breve",), "#E8EEF1", "#31536A"))
    desktop.append(node("st-api", 430, 455, 220, 125, "Resource API", ("firma · emisor", "audiencia · vigencia"), "#FFFDFA", "#A9A49B"))
    desktop.append(node("st-policy", 785, 455, 300, 125, "Estado adicional", ("bloqueo · permisos · revocación",), "#F3E6DF", "#B95736"))
    desktop.append('<path class="flow" d="M295 518H426"/><path class="risk-flow" d="M650 518H781"/>')
    desktop.append(flow_label("st-label-token", 310, 468, 100, "token"))
    desktop.append(flow_label("st-label-current", 660, 468, 116, "si hace falta"))
    desktop.append(end_svg())

    mobile = [title_block_mobile(1260, title, desc, "ESTADO Y REVOCACIÓN")]
    steps = [
        ("Sesión referenciada", "cookie con ID opaco", "#E8EEF1", "#31536A"),
        ("Aplicación", "consulta la sesión vigente", "#FFFDFA", "#A9A49B"),
        ("Almacén", "revocación directa", "#F5ECD8", "#C59132"),
        ("Token autocontenido", "firma · emisor · audiencia", "#E8EEF1", "#31536A"),
        ("Estado actual", "solo cuando la regla lo exige", "#F3E6DF", "#B95736"),
    ]
    for i, (heading, copy, fill, stroke) in enumerate(steps):
        y = 92 + i * 205
        mobile.append(node(f"st-mobile-{i}", 52, y, 316, 140, heading, (copy,), fill, stroke))
        if i < len(steps) - 1:
            klass = "risk-flow" if i == 2 else "flow"
            mobile.append(f'<path class="{klass}" d="M210 {y + 140}V{y + 197}"/>')
    mobile.append('<rect id="st-mobile-note" x="52" y="1115" width="316" height="85" rx="14" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text data-container="st-mobile-note" data-padding="15" x="210" y="1148" class="sans node-copy"><tspan x="210">Ningún formato elimina</tspan><tspan x="210" dy="25">la autorización de cada acción.</tspan></text>')
    mobile.append(end_svg())
    write("cap17-sesion-token-revocacion", desktop, mobile)


def generate_passkey() -> None:
    title = "Passkey · demostrar sin compartir un secreto"
    desc = "El servidor envía un desafío único; el autenticador autoriza el uso de la clave privada vinculada al sitio, firma el desafío y el servidor verifica la firma con la clave pública registrada."
    desktop = [start_svg(1200, 700, title, desc, "La clave privada permanece bajo control del autenticador")]
    desktop.append(node("pk-user", 65, 245, 210, 145, "Persona", ("desbloquea el uso", "con PIN o biometría"), "#E8EEF1", "#31536A"))
    desktop.append(node("pk-auth", 365, 215, 300, 205, "Autenticador", ("conserva la clave privada", "vinculada al sitio"), "#F5ECD8", "#C59132"))
    desktop.append(node("pk-server", 780, 215, 350, 205, "Servidor", ("guarda la clave pública", "y emite un desafío único"), "#FFFDFA", "#A9A49B"))
    desktop.append('<path class="flow" d="M275 315H361"/>')
    desktop.append(flow_label("pk-label-unlock", 278, 266, 80, "autoriza"))
    desktop.append('<path class="flow" d="M955 215V150H515V211"/>')
    desktop.append(flow_label("pk-label-challenge", 665, 133, 152, "1 · desafío"))
    desktop.append('<path class="flow" d="M515 420V510H955V424"/>')
    desktop.append(flow_label("pk-label-sign", 660, 493, 165, "2 · firma y datos"))
    desktop.append('<rect id="pk-result" x="275" y="545" width="650" height="105" rx="14" fill="#F3E6DF" stroke="#B95736" stroke-width="2"/><text data-container="pk-result" data-padding="18" x="600" y="578" class="sans node-copy"><tspan x="600">El servidor verifica origen, RP ID, desafío, flags y firma.</tspan><tspan x="600" dy="25">Registro, recuperación y pérdida de dispositivos</tspan><tspan x="600" dy="25">siguen siendo decisiones del producto.</tspan></text>')
    desktop.append(end_svg())

    mobile = [title_block_mobile(1100, title, desc, "DESAFÍO Y FIRMA")]
    items = [
        ("Servidor", ("crea un desafío único",), "#FFFDFA", "#A9A49B"),
        ("Autenticador", ("verifica el sitio", "y pide autorización"), "#F5ECD8", "#C59132"),
        ("Clave privada", ("firma dentro", "del autenticador"), "#E8EEF1", "#31536A"),
        ("Servidor", ("verifica con", "la clave pública"), "#F3E6DF", "#B95736"),
    ]
    for i, (heading, copy, fill, stroke) in enumerate(items):
        y = 92 + i * 205
        mobile.append(node(f"pk-mobile-{i}", 52, y, 316, 140, heading, copy, fill, stroke))
        if i < len(items) - 1:
            mobile.append(f'<path class="flow" d="M210 {y + 140}V{y + 197}"/>')
    mobile.append('<rect id="pk-mobile-note" x="52" y="920" width="316" height="115" rx="14" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text data-container="pk-mobile-note" data-padding="16" x="210" y="955" class="sans node-copy"><tspan x="210">La biometría desbloquea</tspan><tspan x="210" dy="25">la credencial local.</tspan><tspan x="210" dy="25">No se envía al servidor.</tspan></text>')
    mobile.append(end_svg())
    write("cap17-passkey-desafio", desktop, mobile)


def generate_pkce() -> None:
    title = "Authorization Code con PKCE"
    desc = "La aplicación crea un verifier y envía solo su challenge al servidor de autorización; después canjea el código junto con el verifier. Un código interceptado no basta para obtener tokens."
    desktop = [start_svg(1200, 780, title, desc, "PKCE vincula el código de autorización con la instancia que inició el flujo")]
    actors = [("pkce-user", 50, "Persona"), ("pkce-app", 325, "Aplicación"), ("pkce-auth", 650, "Autorizador"), ("pkce-api", 975, "API")]
    for ident, x, heading in actors:
        desktop.append(node(ident, x, 130, 180, 90, heading, (), "#FFFDFA", "#A9A49B", 182))
        desktop.append(f'<path class="relation" stroke-dasharray="7 8" d="M{x + 90} 220V710"/>')
    messages = [
        (270, 415, 640, "1 · challenge + state", "flow"),
        (340, 740, 425, "2 · autenticar y consentir", "flow"),
        (410, 740, 415, "3 · redirect + code", "flow"),
        (485, 415, 740, "4 · code + verifier", "flow"),
        (560, 740, 415, "5 · tokens", "flow"),
        (635, 505, 1065, "6 · access token", "flow"),
    ]
    for i, (y, x1, x2, label, klass) in enumerate(messages):
        direction = "" if x2 > x1 else ""
        desktop.append(f'<path class="{klass}" d="M{x1} {y}H{x2}"/>')
        width = max(150, min(230, len(label) * 9))
        desktop.append(flow_label(f"pkce-message-{i}", int((x1 + x2 - width) / 2), y - 40, width, label))
    desktop.append('<rect id="pkce-local" x="280" y="235" width="270" height="70" rx="12" fill="#E8EEF1" stroke="#31536A" stroke-width="2"/><text data-container="pkce-local" data-padding="12" x="415" y="263" class="sans node-copy"><tspan x="415">Genera verifier aleatorio</tspan><tspan x="415" dy="23">y lo conserva temporalmente</tspan></text>')
    desktop.append('<rect id="pkce-note" x="320" y="700" width="560" height="55" rx="12" fill="#F3E6DF" stroke="#B95736" stroke-width="2"/><text data-container="pkce-note" data-padding="12" x="600" y="735" class="sans node-copy">El código robado no se canjea sin el verifier correcto.</text>')
    desktop.append(end_svg())

    mobile = [title_block_mobile(1370, title, desc, "SECUENCIA PKCE")]
    steps = [
        ("1 · Preparar", ("verifier · challenge", "state")),
        ("2 · Autorizar", ("enviar challenge", "autenticar a la persona")),
        ("3 · Recibir código", ("validar respuesta", "y contexto")),
        ("4 · Canjear", ("código + verifier", "al token endpoint")),
        ("5 · Usar token", ("limitar audiencia", "alcance y vigencia")),
    ]
    colors = [("#E8EEF1", "#31536A"), ("#FFFDFA", "#A9A49B"), ("#F5ECD8", "#C59132"), ("#F3E6DF", "#B95736"), ("#E8EEF1", "#31536A")]
    for i, ((heading, copy), (fill, stroke)) in enumerate(zip(steps, colors)):
        y = 92 + i * 220
        mobile.append(node(f"pkce-mobile-{i}", 52, y, 316, 150, heading, copy, fill, stroke))
        if i < len(steps) - 1:
            mobile.append(f'<path class="flow" d="M210 {y + 150}V{y + 212}"/>')
    mobile.append('<rect id="pkce-mobile-note" x="52" y="1190" width="316" height="115" rx="14" fill="#F3E6DF" stroke="#B95736" stroke-width="2"/><text data-container="pkce-mobile-note" data-padding="16" x="210" y="1226" class="sans node-copy"><tspan x="210">PKCE protege el canje del código.</tspan><tspan x="210" dy="25">OIDC añade identidad;</tspan><tspan x="210" dy="25">OAuth delega acceso.</tspan></text>')
    mobile.append(end_svg())
    write("cap17-oauth-pkce", desktop, mobile)


def generate_realtime_patterns() -> None:
    title = "Cuatro formas de mantener datos recientes"
    desc = "Polling repite solicitudes; long polling mantiene una solicitud hasta que hay datos; SSE abre un flujo del servidor al cliente; WebSocket mantiene un canal bidireccional."
    desktop = [start_svg(1200, 760, title, desc, "La dirección y la duración del intercambio cambian el contrato operativo")]
    rows = [
        ("Polling", "preguntar", "responder", "intervalo", "#E8EEF1", "#31536A"),
        ("Long polling", "preguntar y esperar", "responder al tener datos", "nueva solicitud", "#FFFDFA", "#A9A49B"),
        ("SSE", "abrir stream", "eventos sucesivos", "auto: EventSource", "#F5ECD8", "#C59132"),
        ("WebSocket", "handshake", "mensajes ↔", "definida por app", "#F3E6DF", "#B95736"),
    ]
    for i, (heading, request, response, operation, fill, stroke) in enumerate(rows):
        y = 135 + i * 145
        desktop.append(node(f"rt-kind-{i}", 55, y, 210, 105, heading, (), fill, stroke, y + 60))
        desktop.append(node(f"rt-client-{i}", 355, y, 210, 105, "Cliente", (), "#E8EEF1", "#31536A", y + 60))
        desktop.append(node(f"rt-server-{i}", 825, y, 210, 105, "Servidor", (), "#FFFDFA", "#A9A49B", y + 60))
        desktop.append(f'<path class="flow" d="M565 {y + 35}H821"/>')
        desktop.append(f'<path class="flow" d="M825 {y + 78}H569"/>')
        desktop.append(flow_label(f"rt-req-{i}", 610, y + 4, 164, request))
        desktop.append(flow_label(f"rt-res-{i}", 590, y + 75, 205, response))
        desktop.append(f'<text x="1055" y="{y + 45}" class="sans small"><tspan x="1055">{escape(operation)}</tspan></text>')
    desktop.append(end_svg())

    mobile = [title_block_mobile(1630, title, desc, "PATRONES DE CONEXIÓN")]
    for i, (heading, request, response, operation, fill, stroke) in enumerate(rows):
        y = 92 + i * 365
        mobile.append(node(f"rt-mobile-{i}", 38, y, 344, 285, heading, (), fill, stroke, y + 45))
        mobile.append(f'<text x="62" y="{y + 100}" class="sans tag">CLIENTE → SERVIDOR</text>')
        mobile.append(f'<text x="62" y="{y + 130}" class="sans small">{escape(request)}</text>')
        mobile.append(f'<text x="62" y="{y + 180}" class="sans tag">SERVIDOR → CLIENTE</text>')
        mobile.append(f'<text x="62" y="{y + 210}" class="sans small">{escape(response)}</text>')
        mobile.append(f'<text x="62" y="{y + 255}" class="sans small">Operación: {escape(operation)}</text>')
    mobile.append(end_svg())
    write("cap18-patrones-conexion", desktop, mobile)


def generate_realtime_scale() -> None:
    title = "Escalar conexiones exige un backplane"
    desc = "Cada instancia conserva sus conexiones locales; un backplane distribuye mensajes entre instancias para alcanzar al destinatario conectado en otro proceso. La durabilidad depende de la tecnología elegida."
    desktop = [start_svg(1200, 720, title, desc, "El balanceador reparte conexiones; el backplane coordina mensajes")]
    desktop.append(node("rt-lb", 435, 125, 330, 105, "Balanceador", ("establece la ruta de conexión",), "#E8EEF1", "#31536A"))
    for i, x in enumerate((95, 475, 855), 1):
        desktop.append(node(f"rt-instance-{i}", x, 310, 250, 130, f"Instancia {i}", (f"conexiones locales {chr(64 + i)}",), "#FFFDFA", "#A9A49B"))
        desktop.append(f'<path class="flow" d="M600 230V270H{x + 125}V306"/>')
    desktop.append(node("rt-bus", 305, 495, 590, 185, "Backplane de mensajería", ("fan-out entre instancias", "Pub/Sub no aporta replay", "un broker durable", "añade retención o replay"), "#F5ECD8", "#C59132"))
    for x in (220, 600, 980):
        desktop.append(f'<path class="flow" d="M{x} 440V465H600V491"/>')
    desktop.append(end_svg())

    mobile = [title_block_mobile(1210, title, desc, "CONEXIONES DISTRIBUIDAS")]
    mobile.append(node("rtm-lb", 52, 92, 316, 130, "Balanceador", ("asigna cada conexión",), "#E8EEF1", "#31536A"))
    mobile.append('<path class="flow" d="M210 222V280"/>')
    for i, x in enumerate((38, 222), 1):
        mobile.append(node(f"rtm-instance-{i}", x, 290, 160, 170, f"Instancia {i}", ("clientes", "locales"), "#FFFDFA", "#A9A49B"))
    mobile.append('<path class="flow" d="M118 460V535H210V600"/><path class="flow" d="M302 460V535H210V600"/>')
    mobile.append(node("rtm-bus", 52, 610, 316, 165, "Backplane", ("distribuye entre procesos", "según su semántica"), "#F5ECD8", "#C59132"))
    mobile.append('<path class="flow" d="M210 775V845"/>')
    mobile.append(node("rtm-delivery", 52, 855, 316, 165, "Entrega local", ("cada instancia emite", "a sus conexiones"), "#F3E6DF", "#B95736"))
    mobile.append('<rect id="rtm-note" x="52" y="1070" width="316" height="85" rx="14" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text data-container="rtm-note" data-padding="15" x="210" y="1102" class="sans node-copy"><tspan x="210">Presencia, orden y replay</tspan><tspan x="210" dy="25">requieren decisiones adicionales.</tspan></text>')
    mobile.append(end_svg())
    write("cap18-escalado-backplane", desktop, mobile)


def generate_lost_update() -> None:
    title = "Concurrencia · una actualización perdida"
    desc = "Dos transacciones leen el mismo saldo; ambas calculan desde el valor anterior y la segunda escritura oculta la primera. La invariante debe protegerse con una operación atómica, bloqueo, restricción o aislamiento adecuado."
    desktop = [start_svg(1200, 760, title, desc, "Una transacción no corrige por sí sola una lectura y escritura mal coordinadas")]
    desktop.append(node("lu-a", 120, 130, 260, 110, "Transacción A", (), "#E8EEF1", "#31536A", 194))
    desktop.append(node("lu-db", 470, 130, 260, 110, "Cuenta", ("saldo inicial · 100",), "#F5ECD8", "#C59132", 170))
    desktop.append(node("lu-b", 820, 130, 260, 110, "Transacción B", (), "#E8EEF1", "#31536A", 194))
    for x in (250, 600, 950):
        desktop.append(f'<path class="relation" stroke-dasharray="7 8" d="M{x} 225V690"/>')
    events = [
        (285, 250, 600, "lee 100", "flow"),
        (345, 950, 600, "lee 100", "flow"),
        (430, 250, 600, "escribe 20", "flow"),
        (510, 950, 600, "escribe 50", "risk-flow"),
    ]
    for i, (y, x1, x2, label, klass) in enumerate(events):
        desktop.append(f'<path class="{klass}" d="M{x1} {y}H{x2}"/>')
        desktop.append(flow_label(f"lu-event-{i}", int((x1 + x2) / 2 - 70), y - 38, 140, label))
    desktop.append('<rect id="lu-failure" x="330" y="565" width="540" height="125" rx="14" fill="#F3E6DF" stroke="#B95736" stroke-width="2"/><text data-container="lu-failure" data-padding="18" x="600" y="600" class="sans node-copy"><tspan x="600">Saldo final 50: la retirada de A desapareció.</tspan><tspan x="600" dy="25">Protege la invariante con una operación atómica,</tspan><tspan x="600" dy="25">una restricción, un bloqueo o el aislamiento adecuado.</tspan></text>')
    desktop.append(end_svg())

    mobile = [title_block_mobile(1260, title, desc, "ACTUALIZACIÓN PERDIDA")]
    steps = [
        ("Estado inicial", "saldo = 100", "#F5ECD8", "#C59132"),
        ("A y B leen", "ambas observan 100", "#E8EEF1", "#31536A"),
        ("A escribe", "100 − 80 = 20", "#FFFDFA", "#A9A49B"),
        ("B sobrescribe", "100 − 50 = 50", "#F3E6DF", "#B95736"),
        ("Invariante rota", "el sistema ocultó una retirada", "#F3E6DF", "#B95736"),
    ]
    for i, (heading, copy, fill, stroke) in enumerate(steps):
        y = 92 + i * 205
        mobile.append(node(f"lu-mobile-{i}", 52, y, 316, 140, heading, (copy,), fill, stroke))
        if i < len(steps) - 1:
            klass = "risk-flow" if i >= 2 else "flow"
            mobile.append(f'<path class="{klass}" d="M210 {y + 140}V{y + 197}"/>')
    mobile.append(end_svg())
    write("cap19-concurrencia-perdida", desktop, mobile)


def generate_mvcc() -> None:
    title = "MVCC · cada sentencia lee un snapshot permitido"
    desc = "Una transacción puede seguir viendo una versión anterior mientras otra confirma una versión nueva. Qué snapshot usa cada sentencia depende del nivel de aislamiento; MVCC no elimina los conflictos entre escritores."
    desktop = [start_svg(1200, 720, title, desc, "Versiones visibles en lugar de bloquear todas las lecturas")]
    desktop.append(node("mv-row-1", 430, 145, 340, 105, "Versión v1", ("precio = 100 · visible para A",), "#E8EEF1", "#31536A"))
    desktop.append(node("mv-a", 70, 300, 280, 150, "Transacción A", ("snapshot anterior", "continúa leyendo v1"), "#FFFDFA", "#A9A49B"))
    desktop.append(node("mv-b", 850, 300, 280, 150, "Transacción B", ("actualiza a 120", "y confirma"), "#F3E6DF", "#B95736"))
    desktop.append(node("mv-row-2", 430, 500, 340, 105, "Versión v2", ("precio = 120 · visible después",), "#F5ECD8", "#C59132"))
    desktop.append('<path class="flow" d="M350 365H426"/><path class="flow" d="M850 365H774"/>')
    desktop.append('<path class="risk-flow" d="M990 450V552H774"/>')
    desktop.append('<path class="flow" d="M430 552H350V454"/>')
    desktop.append(flow_label("mv-label-old", 350, 315, 80, "lee v1"))
    desktop.append(flow_label("mv-label-write", 770, 315, 80, "escribe"))
    desktop.append(flow_label("mv-label-new", 350, 535, 80, "después"))
    desktop.append('<rect id="mv-note" x="300" y="620" width="600" height="70" rx="12" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text data-container="mv-note" data-padding="12" x="600" y="662" class="sans node-copy">El aislamiento decide cuándo una transacción puede observar v2.</text>')
    desktop.append(end_svg())

    mobile = [title_block_mobile(1110, title, desc, "VERSIONES Y SNAPSHOTS")]
    items = [
        ("Versión v1", "precio = 100", "#E8EEF1", "#31536A"),
        ("Transacción A", "lee desde su snapshot permitido", "#FFFDFA", "#A9A49B"),
        ("Transacción B", "crea v2 y confirma", "#F3E6DF", "#B95736"),
        ("Versión v2", "precio = 120", "#F5ECD8", "#C59132"),
    ]
    for i, (heading, copy, fill, stroke) in enumerate(items):
        y = 92 + i * 205
        mobile.append(node(f"mv-mobile-{i}", 52, y, 316, 140, heading, (copy,), fill, stroke))
        if i < len(items) - 1:
            mobile.append(f'<path class="flow" d="M210 {y + 140}V{y + 197}"/>')
    mobile.append('<rect id="mv-mobile-note" x="52" y="920" width="316" height="125" rx="14" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text data-container="mv-mobile-note" data-padding="16" x="210" y="955" class="sans node-copy"><tspan x="210">MVCC mejora la concurrencia,</tspan><tspan x="210" dy="25">pero los escritores aún pueden</tspan><tspan x="210" dy="25">bloquearse o provocar abortos.</tspan></text>')
    mobile.append(end_svg())
    write("cap19-mvcc-snapshots", desktop, mobile)


def generate_cache_patterns() -> None:
    card_comparison(
        "cap19-patrones-cache",
        "Tres contratos de caché",
        "Cache-aside carga bajo demanda; actualizar después del commit coordina dos sistemas sin atomicidad; write-behind acepta una escritura diferida y necesita durabilidad, idempotencia y reconciliación.",
        "Cada patrón define frescura, pérdida posible y recuperación",
        [
            {"title": "Cache-aside", "model": "leer caché; ante miss|consultar origen y poblar", "fit": "lecturas repetidas|origen como fuente de verdad", "cost": "primer miss · stampede|expiración e invalidación"},
            {"title": "Después del commit", "model": "confirmar en DB; luego|actualizar o invalidar caché", "fit": "escrituras moderadas|ventana stale tolerable", "cost": "sin atomicidad entre sistemas|reparación o TTL"},
            {"title": "Write-behind", "model": "aceptar en capa rápida|persistir de forma asíncrona", "fit": "dominio tolera demora|y reconciliación", "cost": "pérdida · orden · duplicados|operación más compleja"},
        ],
    )


def generate_queue_architecture() -> None:
    title = "Una cola separa aceptación y ejecución"
    desc = "La aplicación persiste el trabajo y responde; la cola conserva trabajos pendientes; uno o más workers reservan y procesan cada trabajo, registrando éxito o fallo para reintento e intervención."
    desktop = [start_svg(1200, 720, title, desc, "La respuesta HTTP confirma un contrato; no necesariamente el resultado final")]
    desktop.append(node("q-client", 60, 260, 190, 130, "Cliente", ("solicita una tarea",), "#E8EEF1", "#31536A"))
    desktop.append(node("q-app", 315, 230, 230, 190, "Aplicación", ("valida", "persiste trabajo", "responde 202 o recurso"), "#FFFDFA", "#A9A49B"))
    desktop.append(node("q-queue", 620, 230, 230, 190, "Cola durable", ("espera · reserva", "reintenta · limita"), "#F5ECD8", "#C59132"))
    desktop.append(node("q-worker", 925, 230, 220, 190, "Workers", ("ejecutan", "idempotencia", "timeouts"), "#F3E6DF", "#B95736"))
    desktop.append('<path class="flow" d="M250 315H311"/><path class="flow" d="M545 315H616"/><path class="flow" d="M850 315H921"/>')
    desktop.append('<path class="flow" d="M315 370H254"/>')
    desktop.append(flow_label("q-label-job", 548, 265, 65, "job"))
    desktop.append(flow_label("q-label-reserve", 845, 265, 80, "reserva"))
    desktop.append(node("q-state", 405, 510, 390, 130, "Estado observable", ("pendiente · ejecutando", "completado · fallido"), "#E8EEF1", "#31536A"))
    desktop.append('<path class="flow" d="M1035 420V470H600V506"/>')
    desktop.append(end_svg())

    mobile = [title_block_mobile(1220, title, desc, "PRODUCTOR · COLA · WORKER")]
    steps = [
        ("Aplicación", "valida y persiste el trabajo", "#FFFDFA", "#A9A49B"),
        ("Cola", "conserva, reserva y limita", "#F5ECD8", "#C59132"),
        ("Worker", "ejecuta de forma repetible", "#F3E6DF", "#B95736"),
        ("Resultado", "éxito, retry o fallo terminal", "#E8EEF1", "#31536A"),
        ("Cliente", "consulta o recibe el estado", "#E8EEF1", "#31536A"),
    ]
    for i, (heading, copy, fill, stroke) in enumerate(steps):
        y = 92 + i * 205
        mobile.append(node(f"q-mobile-{i}", 52, y, 316, 140, heading, (copy,), fill, stroke))
        if i < len(steps) - 1:
            mobile.append(f'<path class="flow" d="M210 {y + 140}V{y + 197}"/>')
    mobile.append(end_svg())
    write("cap20-arquitectura-cola", desktop, mobile)


def generate_outbox() -> None:
    title = "Transactional outbox · cerrar la brecha de publicación"
    desc = "La transacción guarda el cambio de dominio y el mensaje de outbox en la misma base de datos; un relay publica después en el broker y marca el mensaje. La entrega suele ser al menos una vez, por lo que el consumidor debe deduplicar."
    desktop = [start_svg(1200, 760, title, desc, "Una transacción local evita confirmar el pedido sin conservar la intención de publicar")]
    desktop.append(node("ob-app", 55, 250, 210, 150, "Aplicación", ("crea pedido", "y evento"), "#E8EEF1", "#31536A"))
    desktop.append(node("ob-db", 355, 175, 250, 120, "orders", ("cambio de dominio",), "#F5ECD8", "#C59132"))
    desktop.append(node("ob-table", 355, 375, 250, 120, "outbox", ("mensaje pendiente",), "#F5ECD8", "#C59132"))
    desktop.append('<rect id="ob-tx" x="320" y="125" width="320" height="430" rx="22" fill="none" stroke="#B95736" stroke-width="3" stroke-dasharray="10 8"/><text x="345" y="155" class="sans tag">UNA TRANSACCIÓN LOCAL</text>')
    desktop.append(node("ob-relay", 705, 375, 190, 120, "Relay", ("publica y marca",), "#FFFDFA", "#A9A49B"))
    desktop.append(node("ob-broker", 965, 375, 190, 120, "Broker", ("distribuye",), "#E8EEF1", "#31536A"))
    desktop.append(node("ob-consumer", 840, 585, 250, 115, "Consumidor", ("deduplica por message ID",), "#F3E6DF", "#B95736"))
    desktop.append('<path class="flow" d="M265 325H316"/><path class="flow" d="M320 325H355"/>')
    desktop.append('<path class="flow" d="M605 435H701"/><path class="flow" d="M895 435H961"/><path class="flow" d="M1060 495V545H965V581"/>')
    desktop.append('<path class="risk-flow" d="M840 642H650V495H609"/>')
    desktop.append(flow_label("ob-label-retry", 650, 595, 170, "duplicado posible"))
    desktop.append(end_svg())

    mobile = [title_block_mobile(1330, title, desc, "CAMBIO Y MENSAJE ATÓMICOS")]
    steps = [
        ("Transacción local", "guardar pedido + fila outbox", "#F5ECD8", "#C59132"),
        ("Confirmar", "ambos cambios o ninguno", "#E8EEF1", "#31536A"),
        ("Relay", "publicar mensaje pendiente", "#FFFDFA", "#A9A49B"),
        ("Broker", "asumir y distribuir el mensaje", "#E8EEF1", "#31536A"),
        ("Consumidor", "deduplicar y aplicar el efecto", "#F3E6DF", "#B95736"),
    ]
    for i, (heading, copy, fill, stroke) in enumerate(steps):
        y = 92 + i * 205
        mobile.append(node(f"ob-mobile-{i}", 52, y, 316, 140, heading, (copy,), fill, stroke))
        if i < len(steps) - 1:
            mobile.append(f'<path class="flow" d="M210 {y + 140}V{y + 197}"/>')
    mobile.append('<rect id="ob-mobile-note" x="52" y="1125" width="316" height="125" rx="14" fill="#F3E6DF" stroke="#B95736" stroke-width="2"/><text data-container="ob-mobile-note" data-padding="16" x="210" y="1160" class="sans node-copy"><tspan x="210">Puede haber redelivery.</tspan><tspan x="210" dy="25">El message ID permite</tspan><tspan x="210" dy="25">deduplicar el efecto.</tspan></text>')
    mobile.append(end_svg())
    write("cap20-outbox-eventos", desktop, mobile)


def generate_cqrs() -> None:
    title = "CQRS · separar decisiones y proyecciones"
    desc = "Los comandos validan reglas y actualizan el modelo de escritura; los eventos o una sincronización alimentan una proyección de lectura optimizada para consultas. La vista puede retrasarse respecto a la escritura."
    desktop = [start_svg(1200, 720, title, desc, "Separar modelos solo cuando sus necesidades realmente divergen")]
    desktop.append(node("cq-command", 55, 205, 220, 130, "Command API", ("expresa una intención",), "#F3E6DF", "#B95736"))
    desktop.append(node("cq-write", 355, 205, 240, 130, "Write model", ("reglas e invariantes",), "#FFFDFA", "#A9A49B"))
    desktop.append(node("cq-db", 675, 205, 220, 130, "Write store", ("fuente de verdad",), "#F5ECD8", "#C59132"))
    desktop.append(node("cq-project", 675, 430, 220, 130, "Proyector", ("consume cambios",), "#FFFDFA", "#A9A49B"))
    desktop.append(node("cq-read", 355, 430, 240, 130, "Read model", ("vista optimizada",), "#E8EEF1", "#31536A"))
    desktop.append(node("cq-query", 55, 430, 220, 130, "Query API", ("responde consultas",), "#E8EEF1", "#31536A"))
    desktop.append('<path class="flow" d="M275 270H351"/><path class="flow" d="M595 270H671"/>')
    desktop.append('<path class="flow" d="M785 335V426"/><path class="flow" d="M675 495H599"/><path class="flow" d="M355 495H279"/>')
    desktop.append('<rect id="cq-delay" x="950" y="305" width="200" height="155" rx="14" fill="#F3E6DF" stroke="#B95736" stroke-width="2"/><text data-container="cq-delay" data-padding="18" x="1050" y="345" class="sans node-copy"><tspan x="1050">Coste explícito:</tspan><tspan x="1050" dy="28">la lectura puede</tspan><tspan x="1050" dy="24">estar rezagada.</tspan></text>')
    desktop.append(end_svg())

    mobile = [title_block_mobile(1260, title, desc, "ESCRIBIR Y LEER POR SEPARADO")]
    steps = [
        ("Command", ("solicita un cambio",), "#F3E6DF", "#B95736"),
        ("Write model", ("protege reglas", "e invariantes"), "#FFFDFA", "#A9A49B"),
        ("Proyección", ("transforma cambios", "de forma asíncrona"), "#F5ECD8", "#C59132"),
        ("Read model", ("optimiza una vista",), "#E8EEF1", "#31536A"),
        ("Query", ("lee sin modificar", "el dominio"), "#E8EEF1", "#31536A"),
    ]
    for i, (heading, copy, fill, stroke) in enumerate(steps):
        y = 92 + i * 205
        mobile.append(node(f"cq-mobile-{i}", 52, y, 316, 140, heading, copy, fill, stroke))
        if i < len(steps) - 1:
            mobile.append(f'<path class="flow" d="M210 {y + 140}V{y + 197}"/>')
    mobile.append(end_svg())
    write("cap20-cqrs-proyeccion", desktop, mobile)


def generate_event_sourcing() -> None:
    title = "Event Sourcing · el estado se deriva del historial"
    desc = "Cada evento aceptado se añade a un stream; un fold aplica los eventos en orden para reconstruir el estado. Un snapshot acelera la carga, pero no reemplaza los eventos posteriores ni el versionado del contrato."
    desktop = [start_svg(1200, 720, title, desc, "Guardar hechos inmutables cambia el modelo de escritura, lectura y evolución")]
    events = [("es-1", 55, "1 · Cuenta", "creada · saldo 0"), ("es-2", 300, "2 · Depositar", "+200"), ("es-3", 545, "3 · Retirar", "−50")]
    for ident, x, heading, copy in events:
        desktop.append(node(ident, x, 180, 205, 105, heading, (copy,), "#E8EEF1", "#31536A", 220))
    desktop.append('<path class="flow" d="M260 232H296"/><path class="flow" d="M505 232H541"/>')
    desktop.append(node("es-fold", 850, 180, 285, 105, "Fold", ("aplica eventos en orden",), "#FFFDFA", "#A9A49B", 222))
    desktop.append('<path class="flow" d="M750 232H846"/>')
    desktop.append(node("es-snapshot", 300, 425, 250, 120, "Snapshot opcional", ("estado hasta seq 2",), "#F5ECD8", "#C59132"))
    desktop.append(node("es-state", 750, 425, 300, 120, "Estado derivado", ("saldo = 150",), "#F3E6DF", "#B95736"))
    desktop.append('<path class="flow" d="M425 545V610H900V549"/>')
    desktop.append('<path class="flow" d="M992 285V421"/>')
    desktop.append(flow_label("es-label-replay", 580, 592, 180, "snapshot + eventos"))
    desktop.append('<rect id="es-note" x="300" y="620" width="600" height="70" rx="12" fill="#FFFDFA" stroke="#D8D2C7" stroke-width="2"/><text data-container="es-note" data-padding="12" x="600" y="662" class="sans node-copy">Replay exige eventos versionados y proyecciones deterministas.</text>')
    desktop.append(end_svg())

    mobile = [title_block_mobile(1280, title, desc, "STREAM · FOLD · ESTADO")]
    items = [
        ("Evento 1", "cuenta creada", "#E8EEF1", "#31536A"),
        ("Evento 2", "depósito +200", "#E8EEF1", "#31536A"),
        ("Evento 3", "retiro −50", "#E8EEF1", "#31536A"),
        ("Fold", "aplicar en orden", "#FFFDFA", "#A9A49B"),
        ("Estado derivado", "saldo = 150", "#F3E6DF", "#B95736"),
    ]
    for i, (heading, copy, fill, stroke) in enumerate(items):
        y = 92 + i * 205
        mobile.append(node(f"es-mobile-{i}", 52, y, 316, 140, heading, (copy,), fill, stroke))
        if i < len(items) - 1:
            mobile.append(f'<path class="flow" d="M210 {y + 140}V{y + 197}"/>')
    mobile.append('<rect id="es-mobile-note" x="52" y="1125" width="316" height="105" rx="14" fill="#F5ECD8" stroke="#C59132" stroke-width="2"/><text data-container="es-mobile-note" data-padding="16" x="210" y="1160" class="sans node-copy"><tspan x="210">Un snapshot acelera la carga;</tspan><tspan x="210" dy="25">el stream sigue siendo la fuente.</tspan></text>')
    mobile.append(end_svg())
    write("cap20-event-sourcing", desktop, mobile)


def main() -> None:
    generate_session_token()
    generate_passkey()
    generate_pkce()
    card_comparison(
        "cap17-modelos-autorizacion",
        "RBAC, ABAC o ReBAC",
        "RBAC deriva permisos de roles; ABAC evalúa atributos de sujeto, recurso y contexto; ReBAC recorre relaciones entre entidades. Los tres necesitan denegación por defecto y evidencia de decisión.",
        "Empieza con el modelo más simple que exprese el dominio",
        [
            {"title": "RBAC", "model": "usuario → rol → permiso", "fit": "puestos y responsabilidades|relativamente estables", "cost": "explosión de roles|excepciones por recurso"},
            {"title": "ABAC", "model": "atributos + política|→ permitir o denegar", "fit": "contexto, sensibilidad|y reglas combinadas", "cost": "explicabilidad · pruebas|calidad de atributos"},
            {"title": "ReBAC", "model": "relaciones en un grafo|→ permiso derivado", "fit": "recursos compartidos|equipos y jerarquías", "cost": "recorridos · consistencia|operación del grafo"},
        ],
    )
    generate_realtime_patterns()
    generate_realtime_scale()
    generate_lost_update()
    generate_mvcc()
    generate_cache_patterns()
    generate_queue_architecture()
    generate_outbox()
    generate_cqrs()
    generate_event_sourcing()


if __name__ == "__main__":
    main()
