#!/usr/bin/env python3
"""Integra la segunda pasada visual del capítulo 30."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "chapters" / "30-nueva-capa-abstraccion.md"

REPLACEMENTS = {
    "❌ Sin docs/:": """<picture>
  <source media="(max-width: 820px)" srcset="../assets/diagrams/cap30-contexto-vigente-mobile.svg">
  <img src="../assets/diagrams/cap30-contexto-vigente.svg" alt="Una intención acotada usa documentación y convenciones vigentes para seleccionar archivos relevantes, producir un cambio pequeño y comprobarlo con evidencia; una discrepancia obliga a corregir el contexto o la implementación.">
</picture>""",
    "ESTRUCTURA CLARA → MENOS AMBIGÜEDAD": """> Una estructura clara reduce ambigüedad para todos: acelera el *onboarding* humano y ayuda al agente a localizar contratos, imitar convenciones y limitar el cambio. No elimina los errores; hace más visibles los supuestos y más barata su comprobación.""",
    "Función tradicional:": """<picture>
  <source media="(max-width: 820px)" srcset="../assets/diagrams/cap30-modelos-ejecucion-mobile.svg">
  <img src="../assets/diagrams/cap30-modelos-ejecucion.svg" alt="Comparación entre una función con regla explícita, un modelo lingüístico con salida probabilística y un agente que añade herramientas y efectos externos; cada nivel exige más evaluación y control.">
</picture>""",
    "MENTALIDAD DE CONSTRUCTOR": """<picture>
  <source media="(max-width: 820px)" srcset="../assets/diagrams/cap30-constructor-jardinero-mobile.svg">
  <img src="../assets/diagrams/cap30-constructor-jardinero.svg" alt="Comparación entre controlar directamente cada paso como constructor y preparar contexto, límites y feedback como jardinero; ambos enfoques se combinan según el riesgo y la verificabilidad.">
</picture>""",
    "CREAR CONDICIONES A NIVEL ORGANIZACIONAL": """<picture>
  <source media="(max-width: 820px)" srcset="../assets/diagrams/cap30-condiciones-organizacionales-mobile.svg">
  <img src="../assets/diagrams/cap30-condiciones-organizacionales.svg" alt="La organización combina contexto vigente, convenciones, guardrails y prácticas de revisión para producir cambios acotados, verificables y con una persona responsable.">
</picture>""",
    "Prompt 1: \"Crea un componente de login\"": """1. Pide un primer cambio pequeño: «Crea un componente de acceso».
2. Revisa estructura, accesibilidad, supuestos y alcance.
3. Añade las reglas de validación documentadas y los errores que no revelen datos sensibles.
4. Revisa de nuevo y agrega el manejo de respuestas del API.
5. Termina cuando los criterios de aceptación y la evidencia acordada estén satisfechos.

Cada iteración debe reducir incertidumbre; no es una invitación a aprobar cambios por partes sin entender el resultado completo.""",
    "❌ \"Refactoriza todo el módulo de auth\"": """> **Confiar ciegamente:** pedir un cambio amplio y hacer *commit* sin revisar puede alterar reglas, introducir vulnerabilidades o romper casos límite. Reduce el alcance, define invariantes y revisa el diff completo.""",
    "❌ \"Genera tests\" → aceptar sin leer": """> **Aceptar pruebas sin leer:** una prueba generada puede omitir riesgos, ser frágil o comprobar la implementación en vez del comportamiento. Revisa que falle por la razón correcta y que represente el dominio.""",
    "ORQUESTADOR": """<picture>
  <source media="(max-width: 820px)" srcset="../assets/diagrams/cap30-orquestacion-multiagente-mobile.svg">
  <img src="../assets/diagrams/cap30-orquestacion-multiagente.svg" alt="Un orquestador delega tareas independientes con entradas y entregables definidos; backend, frontend y verificación producen resultados que vuelven a una integración con pruebas, resolución de conflictos y revisión.">
</picture>""",
}


def replace_blocks(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    index = 0
    replaced = 0

    while index < len(lines):
        if not lines[index].strip().startswith("```"):
            output.append(lines[index])
            index += 1
            continue

        end = index + 1
        while end < len(lines) and lines[end].strip() != "```":
            end += 1
        if end >= len(lines):
            raise RuntimeError(f"Bloque sin cierre en la línea {index + 1}")

        block = "".join(lines[index : end + 1])
        match = next(
            (key for key in sorted(REPLACEMENTS, key=len, reverse=True) if key in block),
            None,
        )
        if match is None:
            output.extend(lines[index : end + 1])
        else:
            output.append(REPLACEMENTS[match].rstrip() + "\n")
            replaced += 1
        index = end + 1

    return "".join(output), replaced


def main() -> None:
    updated, count = replace_blocks(CHAPTER.read_text(encoding="utf-8"))
    CHAPTER.write_text(updated, encoding="utf-8")
    print(f"Capítulo 30: {count} bloques consolidados")


if __name__ == "__main__":
    main()
