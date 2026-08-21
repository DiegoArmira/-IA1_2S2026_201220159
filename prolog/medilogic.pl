% MediLogic - base de conocimiento preliminar para la Entrega No. 1.
% Uso academico: orientacion diagnostica; no sustituye atencion medica.

enfermedad(gripe).
enfermedad(resfriado).
enfermedad(migrana).

sintoma(gripe, fiebre).
sintoma(gripe, tos).
sintoma(gripe, dolor_muscular).
sintoma(resfriado, congestion_nasal).
sintoma(resfriado, estornudos).
sintoma(resfriado, tos).
sintoma(migrana, dolor_cabeza).
sintoma(migrana, nausea).
sintoma(migrana, sensibilidad_luz).

medicamento(gripe, paracetamol).
medicamento(resfriado, loratadina).
medicamento(migrana, ibuprofeno).
medicamento(migrana, paracetamol).

contraindicado(ibuprofeno, gastritis).
contraindicado(ibuprofeno, alergia_aines).
contraindicado(paracetamol, enfermedad_hepatica).

% Una enfermedad es posible cuando comparte al menos un sintoma reportado.
posible_enfermedad(Sintoma, Enfermedad) :-
    sintoma(Enfermedad, Sintoma).

% Un medicamento es seguro si trata la enfermedad, no es alergeno y no esta
% contraindicado para una condicion cronica reportada.
medicamento_seguro(Enfermedad, Alergia, Condicion, Medicamento) :-
    medicamento(Enfermedad, Medicamento),
    Medicamento \= Alergia,
    \+ contraindicado(Medicamento, Condicion).

% Urgencia preliminar basada en la severidad declarada.
urgencia(severo, consulta_medica_inmediata).
urgencia(moderado, observacion_recomendada).
urgencia(leve, posible_automanejo).

% Peso requerido por el enunciado para el calculo posterior de afinidad.
peso_severidad(leve, 1).
peso_severidad(moderado, 2).
peso_severidad(severo, 3).
