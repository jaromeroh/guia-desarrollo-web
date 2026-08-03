#!/usr/bin/env python3
"""Integra la segunda pasada visual y elimina recuadros ASCII redundantes.

La transformación es idempotente: solo reemplaza bloques ASCII cuyos títulos
editoriales siguen presentes en los capítulos 21–23.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REPLACEMENTS = {
    "chapters/21-testing.md": {
        "LA PARADOJA DEL TESTING": """> **Tres escenarios, una misma pregunta:** sin pruebas no hay evidencia; una gran cantidad de pruebas aisladas puede seguir sin cubrir el comportamiento real; una estrategia útil protege los flujos y riesgos que importan. El objetivo no es acumular casos, sino poder explicar qué confianza aporta cada uno.""",
        "TESTING PYRAMID": """La pirámide proponía muchas pruebas unitarias, algunas de integración y pocas pruebas de extremo a extremo. Su aporte duradero es pensar en coste y alcance; el número de pruebas de cada nivel depende del sistema y de sus riesgos.""",
        "TESTING TROPHY": """<picture>
  <source media="(max-width: 820px)" srcset="../assets/diagrams/cap21-modelos-confianza-mobile.svg">
  <img src="../assets/diagrams/cap21-modelos-confianza.svg" alt="Comparación entre la pirámide clásica, el Testing Trophy y una estrategia guiada por riesgo: cambian el foco y el coste, pero ninguna prescribe una cantidad universal de pruebas.">
</picture>""",
        "¿MERECE UN UNIT TEST?": """<picture>
  <source media="(max-width: 820px)" srcset="../assets/diagrams/cap21-eleccion-nivel-prueba-mobile.svg">
  <img src="../assets/diagrams/cap21-eleccion-nivel-prueba.svg" alt="Comparación para elegir pruebas unitarias, de integración o de extremo a extremo según la pregunta, la fidelidad necesaria y su coste operativo.">
</picture>""",
        "¿MERECE UN TEST E2E?": """> **Usa E2E de forma selectiva.** Reserva estos recorridos para flujos críticos que atraviesan varias fronteras, como registro, acceso o pago. Variaciones locales, reglas puras y estados de error suelen diagnosticarse mejor en pruebas más pequeñas.""",
        "TDD × AI: EL FLUJO": """<picture>
  <source media="(max-width: 820px)" srcset="../assets/diagrams/cap21-tdd-agente-evidencia-mobile.svg">
  <img src="../assets/diagrams/cap21-tdd-agente-evidencia.svg" alt="Proceso de TDD con un agente: definir un comportamiento, comprobar que la prueba falla, construir el cambio, revisar sus riesgos y ampliar la evidencia antes de aceptar.">
</picture>""",
        "CÓDIGO PLAUSIBLE, EVIDENCIA INSUFICIENTE": """> **Código plausible no significa código correcto.** Un agente puede usar una API inexistente, introducir lógica sutilmente incorrecta, vulnerabilidades o condiciones de carrera. Las pruebas aportan evidencia, pero deben combinarse con revisión del dominio, seguridad, tipos, análisis estático y observación del sistema.""",
        "REGLA DE LOS 3 FAILURES": """> **Política de tests inestables:** cuando una prueba falle de forma intermitente, asígnale responsable y prioridad. Corrige la condición de carrera, el aislamiento o la dependencia inestable; si bloquea al equipo, ponla en cuarentena de forma temporal y visible. Los reintentos pueden ayudar al diagnóstico, pero no convierten una prueba inestable en evidencia confiable.""",
        "TESTING TROPHY EN ACCIÓN": """La estrategia resultante combina:

- **Análisis estático** sobre todo el código para defectos detectables sin ejecutar.
- **Pruebas unitarias** para reglas puras y casos límite.
- **Pruebas de integración** para componentes, APIs, datos y contratos que colaboran.
- **Pruebas E2E** para pocos flujos críticos vistos desde la interfaz.
- **Señales de producción** para propiedades que solo aparecen bajo tráfico y condiciones reales.

Si dos pruebas aportan la misma evidencia, conserva la más pequeña y fácil de diagnosticar. Si una prueba aislada no representa el riesgo, aumenta la fidelidad del entorno.""",
    },
    "chapters/22-ci-cd.md": {
        "EL CICLO DEL MIEDO": """> Un lote grande tarda en integrarse, acumula incertidumbre y vuelve costoso averiguar qué salió mal. Cambios pequeños, feedback temprano y una mecánica repetible reducen ese ciclo; la frecuencia solo es segura cuando el pipeline produce evidencia útil.""",
        "LOS TRES NIVELES DE AUTOMATIZACIÓN": """<picture>
  <source media="(max-width: 820px)" srcset="../assets/diagrams/cap22-ci-entrega-despliegue-mobile.svg">
  <img src="../assets/diagrams/cap22-ci-entrega-despliegue.svg" alt="Comparación entre integración continua, entrega continua y despliegue continuo según la automatización, la decisión de promoción y los requisitos operativos.">
</picture>""",
        "GITFLOW": """<picture>
  <source media="(max-width: 820px)" srcset="../assets/diagrams/cap22-branching-lotes-mobile.svg">
  <img src="../assets/diagrams/cap22-branching-lotes.svg" alt="Comparación entre GitFlow, GitHub Flow y trunk-based development según su modelo de ramas, el contexto en que encajan y su coste de integración.">
</picture>""",
        "TRUNK-BASED DEVELOPMENT": """> Trunk-based development busca integrar lotes muy pequeños. Puede usar commits directos o ramas breves según las reglas de revisión del equipo; lo esencial es evitar que el trabajo permanezca aislado durante días o semanas.""",
        "GUÍA DE DECISIÓN": """| Contexto | Sesgo inicial |
|---|---|
| Producto con entrega frecuente y automatización sólida | Trunk-based o GitHub Flow con ramas muy breves |
| Release coordinado o varias versiones soportadas | Un flujo con ramas de release puede ser útil |
| Equipo que aún no domina integración frecuente | GitHub Flow ofrece una transición sencilla |
| Trabajo incompleto que debe integrarse pronto | Trunk-based con una bandera temporal y una fecha de retiro |

La decisión no depende solo del tamaño del equipo. Importan la frecuencia de integración, las versiones que deben mantenerse, las aprobaciones y la capacidad de recuperar `main`.""",
        "USOS DE FEATURE FLAGS": """<picture>
  <source media="(max-width: 820px)" srcset="../assets/diagrams/cap22-ciclo-feature-flag-mobile.svg">
  <img src="../assets/diagrams/cap22-ciclo-feature-flag.svg" alt="Ciclo de vida de una bandera: definir propietario y caducidad, desplegarla apagada, exponer por cohortes, decidir con señales y retirar el código temporal.">
</picture>

Una bandera puede habilitar desarrollo incremental, programas beta, experimentos, canary releases o un *kill switch*. En todos los casos necesita segmentación estable, telemetría y una estrategia de eliminación.""",
        "BUILD TIME TARGETS": """Define un presupuesto de feedback a partir del flujo real del equipo:

- Separa comprobaciones rápidas para PR de suites profundas o programadas.
- Mide p50 y p95, tiempo en cola, camino crítico y tasa de reintentos.
- Paraleliza trabajos independientes y divide suites cuando reduzca el camino crítico.
- Cachea dependencias con claves correctas; una caché inválida ahorra tiempo a costa de reproducibilidad.
- Ejecuta pruebas afectadas solo si conservas una suite que detecte errores del análisis de impacto.
- Ajusta capacidad de los *runners* cuando el coste de espera lo justifique.""",
        "ANTI-PATRONES CI/CD": """- **«Funciona en mi máquina».** Reproduce versiones, servicios y variables relevantes entre local y CI.
- **Pruebas que solo fallan en CI.** Investiga aislamiento, tiempo, recursos y diferencias de entorno.
- **Ignorar tests inestables.** Asigna responsable; corrige o pon en cuarentena temporal y visible.
- **Feedback habitualmente tardío.** Mide el camino crítico y separa suites profundas.
- **Pasos manuales ocultos.** Automatiza la mecánica y conserva las aprobaciones que controlan un riesgo real.
- **Ramas de larga vida.** Integra lotes más pequeños para descubrir conflictos antes.
- **CI solo en pull requests.** Verifica también la rama principal y cualquier ruta que produzca un artefacto.""",
        "CI/CD EN RESUMEN": """- **CI** integra cambios frecuentes y devuelve evidencia rápida.
- **Entrega continua** mantiene un artefacto listo para promover mediante una decisión explícita.
- **Despliegue continuo** automatiza también esa promoción bajo políticas observables.
- **Branching** controla coordinación y tamaño de lote; no sustituye pruebas ni revisión.
- **Feature flags** separan despliegue y liberación, pero añaden estado temporal que debe retirarse.
- **Pipeline** significa fallar pronto, construir una vez, promover el mismo artefacto y conservar una ruta de recuperación.

El principio guía es reducir el tamaño y la incertidumbre de cada cambio, no aumentar la frecuencia a cualquier precio.""",
    },
    "chapters/23-deployment.md": {
        "EL ESPECTRO DE ABSTRACCIÓN": """<picture>
  <source media="(max-width: 820px)" srcset="../assets/diagrams/cap23-espectro-hosting-mobile.svg">
  <img src="../assets/diagrams/cap23-espectro-hosting.svg" alt="Comparación entre infraestructura, plataformas administradas y funciones o edge según control, ajuste a los requisitos y responsabilidad operativa.">
</picture>""",
        "TRADICIONAL vs EDGE": """En una región única, el usuario distante recorre la red hasta el origen. Con ejecución distribuida, una parte del trabajo ocurre en un punto cercano, pero las solicitudes que necesitan datos remotos todavía deben alcanzar su origen. **Mover cómputo no mueve automáticamente los datos ni su consistencia.**""",
        "LIMITACIONES EDGE FUNCTIONS": """> **Edge es un contrato de ejecución, no solo una ubicación.** Verifica cuotas de CPU, memoria, duración y subsolicitudes; compatibilidad del runtime; distancia a los datos; estado efímero; y herramientas de observabilidad. Mantén en el borde el trabajo que realmente reduzca el camino completo y mide la latencia de extremo a extremo.""",
        "MANUAL vs IaC": """| Infraestructura manual | Infraestructura como código |
|---|---|
| Cambios difíciles de atribuir o repetir | Configuración versionada y revisable |
| Entornos que dependen de conocimiento tácito | Plan de cambios y módulos reutilizables |
| Diferencias que aparecen con el tiempo | Detección y reconciliación de *drift* |
| Recuperación improvisada | Estado remoto protegido, bloqueo y procedimientos probados |

IaC mejora la trazabilidad, pero no vuelve reversibles los cambios de datos ni elimina los efectos externos de una operación.""",
        "ESTRATEGIAS DE DEPLOYMENT": """<picture>
  <source media="(max-width: 820px)" srcset="../assets/diagrams/cap23-estrategias-despliegue-mobile.svg">
  <img src="../assets/diagrams/cap23-estrategias-despliegue.svg" alt="Comparación entre rolling, blue-green y canary según el cambio de capacidad, el contexto adecuado y el coste de recuperar la versión anterior.">
</picture>""",
        "GESTIÓN DE SECRETS": """**Nunca incluyas secretos en:**

- Código fuente, imágenes o archivos versionados.
- Archivos de composición incluidos en el repositorio.
- Logs, mensajes de error o artefactos de CI.
- Variables expuestas al navegador o a procesos que no las necesitan.

**En su lugar:** usa credenciales locales ignoradas por Git durante desarrollo; identidades federadas y secretos protegidos en CI; y un gestor de secretos o la configuración segura de la plataforma en producción. Limita cada identidad al secreto y a la operación que necesita, registra el acceso y diseña la rotación.""",
        "PIPELINE DE AMBIENTES": """<picture>
  <source media="(max-width: 820px)" srcset="../assets/diagrams/cap23-promocion-artefacto-mobile.svg">
  <img src="../assets/diagrams/cap23-promocion-artefacto.svg" alt="Un commit produce un artefacto inmutable que se promueve por preview y staging hasta producción, con configuración externa y una ruta para detener o revertir la aplicación.">
</picture>""",
        "ANTI-PATRONES DE DEPLOYMENT": """- **Servidores irrepetibles.** Versiona la configuración y automatiza su creación y recuperación.
- **Desplegar y esperar.** Define pruebas de salud, señales, responsables y una decisión de reversión.
- **Kubernetes prematuro.** Adopta su carga operativa solo cuando sus capacidades resuelvan requisitos concretos.
- **Configuración rígida en el código.** Separa configuración, valida su esquema y protege los secretos.
- **Despliegue masivo.** Reduce el tamaño del lote y conserva compatibilidad durante la transición.
- **«Rollback» sin alcance.** Volver a la aplicación anterior no deshace migraciones, mensajes enviados ni efectos externos.""",
        "DEPLOYMENT EN RESUMEN": """- Elige el modelo de hosting más simple que cumpla los requisitos y que el equipo pueda operar.
- Usa edge solo cuando mejore el camino completo, incluida la relación con los datos.
- Versiona la infraestructura y protege tanto sus credenciales como su estado.
- Construye un artefacto una vez y promueve esa identidad entre ambientes.
- Separa despliegue y liberación cuando necesites limitar exposición.
- Define observación, parada, reversión de aplicación y reconciliación de datos antes de cambiar producción.

Diseñar para recuperarse no significa aceptar cualquier fallo: significa limitar el impacto y poder restablecer el servicio con evidencia y procedimientos practicados.""",
    },
}


def replace_ascii_blocks(path: Path, replacements: dict[str, str]) -> int:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    output: list[str] = []
    replaced = 0
    index = 0

    while index < len(lines):
        if not lines[index].strip().startswith("```"):
            output.append(lines[index])
            index += 1
            continue

        end = index + 1
        while end < len(lines) and lines[end].strip() != "```":
            end += 1
        if end >= len(lines):
            raise RuntimeError(f"Bloque sin cierre en {path}:{index + 1}")

        block = "".join(lines[index : end + 1])
        match = next(
            (key for key in sorted(replacements, key=len, reverse=True) if key in block),
            None,
        )
        if match is None:
            output.extend(lines[index : end + 1])
        else:
            output.append(replacements[match].rstrip() + "\n")
            replaced += 1
        index = end + 1

    path.write_text("".join(output), encoding="utf-8")
    return replaced


def main() -> None:
    total = 0
    for relative, replacements in REPLACEMENTS.items():
        path = ROOT / relative
        count = replace_ascii_blocks(path, replacements)
        total += count
        print(f"{relative}: {count} bloques reemplazados")
    print(f"Total: {total} bloques ASCII consolidados")


if __name__ == "__main__":
    main()
