# MediLogic - Entrega No. 1

Prototipo academico minimo de un sistema experto de orientacion diagnostica.

## Requisitos

- Python 3.10 o superior
- SWI-Prolog disponible mediante el comando `swipl`

## Ejecucion

```bash
cd backend
python app.py
```

Abrir `http://localhost:8000` en el navegador.

Para ejecutar las cinco consultas de evidencia:

```bash
cd backend
python prolog_service.py
```

## Estructura

- `prolog/medilogic.pl`: hechos, contraindicaciones y reglas preliminares.
- `backend/prolog_service.py`: puente controlado entre Python y SWI-Prolog.
- `backend/app.py`: servidor y endpoint de consulta.
- `frontend/`: prototipo del modulo de pacientes.

## Aviso

MediLogic es un prototipo educativo. No sustituye el diagnostico ni la atencion de profesionales de salud.
