---
name: organizador-academico
description: Ordena automáticamente el material universitario de Matías desde una carpeta "inbox" hacia la subcarpeta correcta de cada ramo en OneDrive UC. Úsalo cuando Matías diga "ordena la U", "ordena mis materiales", "revisa el inbox", o cuando suba archivos a la carpeta "📥 Por ordenar" y quiera repartirlos (ayudantías, apuntes, tareas, exámenes, lecturas...).
---

# Organizador académico — inbox → auto-orden

Matías tira TODO el material nuevo en una sola carpeta inbox. Esta skill lo reparte a la
subcarpeta correcta de cada ramo, **proponiendo primero y moviendo solo con su OK**.

## Rutas

- **Raíz UC:** `C:\Users\matia\OneDrive - Universidad Católica de Chile`
- **Inbox:** `<raíz>\📥 Por ordenar`
- **Destino:** `<raíz>\<año>\<semestre>\<Ramo>\<subcarpeta>`

El año y semestre **cambian con el tiempo**: detecta el semestre activo como el más reciente
que contenga ramos (carpetas no vacías). Hoy (2026) es `2026\Quinto semestre`. No hardcodees —
lista las carpetas y elige el semestre vigente; si hay duda, pregunta.

## Convenciones de subcarpetas por ramo

Cada ramo tiene sus propias subcarpetas. Lee las subcarpetas reales del ramo antes de decidir
(no inventes nombres). Patrones típicos observados:

- **Ayudantías** → `Ayudantías`, `Ayudantía 1`, `Ayudantía 2`, ...
- **Apuntes de clase** → `Apuntes y clases ...`
- **Tareas / entregas** → `Tareas`, `Entregas`
- **Evaluaciones** → `Exámenes`, `I1`, `I2`, `Material controles`
- **Lecturas** → `Lecturas`
- **Material de estudio general** → `Material de estudio`
- **Resumen maestro** → `<Ramo> MAESTRO`

Si el ramo no tiene una subcarpeta que calce, **propón crearla** (no la crees sin avisar).

## Flujo

1. **Detectar contexto:** año y semestre activos + lista de ramos con sus subcarpetas reales.
2. **Leer el inbox:** listar todos los archivos en `📥 Por ordenar` (incluye subcarpetas).
3. **Clasificar cada archivo** por nombre y, si hace falta, por contenido:
   - ¿A qué **ramo** pertenece? (menciones al nombre del ramo, profesor, sigla, tema).
   - ¿A qué **subcarpeta**? (ayudantía / apunte / tarea / examen / lectura / material).
   - Si un archivo es ambiguo, márcalo como **"revisar"** en vez de adivinar.
4. **Proponer un plan** en tabla: `archivo → Ramo\subcarpeta` (+ los "revisar" aparte).
5. **Pedir confirmación.** Solo tras el OK, mover los archivos (mueve, no copia).
6. **Reportar:** qué se movió, qué quedó en el inbox por ambiguo, qué carpetas se crearon.

## Reglas
- **Nunca muevas sin confirmar el plan.** Los archivos son material real de la U.
- Mover (no copiar) para vaciar el inbox; conserva el nombre original del archivo.
- Si dos archivos colisionan en destino, no sobrescribas: renombra con sufijo o pregunta.
- Los archivos ambiguos se quedan en el inbox marcados, nunca se borran.
- No toques nada fuera del inbox salvo para depositar en el destino confirmado.
