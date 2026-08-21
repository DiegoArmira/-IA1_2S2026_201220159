"""Puente minimo Python -> SWI-Prolog para MediLogic."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
KNOWLEDGE_BASE = BASE_DIR / "prolog" / "medilogic.pl"


class PrologError(RuntimeError):
    """Error controlado al consultar el motor logico."""


def query(goal: str) -> list[str]:
    """Ejecuta una meta Prolog y devuelve cada solucion como texto."""
    executable = shutil.which("swipl")
    if not executable:
        raise PrologError("SWI-Prolog no esta instalado o no esta en PATH.")

    command = [
        executable,
        "-q",
        "-s",
        str(KNOWLEDGE_BASE),
        "-g",
        f"forall(({goal}), (write_canonical(resultado), write('='), writeln({goal}))),halt.",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=10)
    if completed.returncode != 0:
        raise PrologError(completed.stderr.strip() or "La consulta Prolog fallo.")
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def run_named_query(name: str, params: dict[str, str]) -> dict[str, object]:
    """Construye una de cinco consultas permitidas evitando metas arbitrarias."""
    goals = {
        "enfermedades": "enfermedad(E)",
        "sintomas": f"sintoma({params.get('enfermedad', 'gripe')}, S)",
        "diagnostico": f"posible_enfermedad({params.get('sintoma', 'tos')}, E)",
        "medicamentos": f"medicamento({params.get('enfermedad', 'gripe')}, M)",
        "seguridad": (
            "medicamento_seguro("
            f"{params.get('enfermedad', 'migrana')},"
            f"{params.get('alergia', 'ninguna')},"
            f"{params.get('condicion', 'ninguna')},M)"
        ),
    }
    if name not in goals:
        raise PrologError("Consulta no admitida.")
    goal = goals[name]
    return {"consulta": name, "meta": goal, "resultados": query(goal)}


if __name__ == "__main__":
    examples = [
        ("enfermedades", {}),
        ("sintomas", {"enfermedad": "gripe"}),
        ("diagnostico", {"sintoma": "tos"}),
        ("medicamentos", {"enfermedad": "migrana"}),
        ("seguridad", {"enfermedad": "migrana", "alergia": "ninguna", "condicion": "gastritis"}),
    ]
    for query_name, parameters in examples:
        print(json.dumps(run_named_query(query_name, parameters), ensure_ascii=False, indent=2))
