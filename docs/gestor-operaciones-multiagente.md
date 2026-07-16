# Gestor de operaciones multiagéntico — plan

> Estado: **idea / diseño**. Aún no construido. Objetivo: mandar instrucciones de alto nivel
> ("analiza estas 3 acciones", "diseña e imprime un soporte", "arma un mini-negocio de X")
> y que un orquestador reparta el trabajo entre agentes que usan las skills de este repo.

## Idea
Un **orquestador** recibe una instrucción, la descompone en subtareas, y delega cada una a un
**agente worker** que corre con un modelo barato/gratis (ej. Qwen) y tiene acceso a las skills
relevantes (trading, print-design, video-analyzer, etc.). El orquestador junta resultados y decide
siguientes pasos.

## Piezas candidatas
- **Hermes** — ya está instalado en `C:\Users\matia\AppData\Local\hermes` (hermes-agent). Trae un
  set grande de optional-skills. Candidato a runtime del orquestador/workers.
- **Modelos baratos/gratis para workers:** Qwen (via API gratuita o local con Ollama), para tareas
  mecánicas (fetch de datos, correr screeners, formatear). Reservar Opus/Sonnet solo para
  razonamiento/síntesis.
- **Skills de este repo** como herramientas de los workers (trading screeners, print-design, etc.).

## Arquitectura tentativa
```
Instrucción del usuario
        │
        ▼
   Orquestador (modelo capaz)  ──► descompone en subtareas
        │
        ├─► worker Qwen: correr screener VCP  (skill trading)
        ├─► worker Qwen: fetch calendario económico (skill trading)
        ├─► worker Qwen: diseñar pieza (skill print-design)
        │
        ▼
   Orquestador junta + verifica + reporta
```

## Preguntas a resolver antes de construir
1. **Runtime:** ¿Hermes, o el propio Workflow/Agent de Claude Code, o LangGraph/CrewAI?
2. **Modelos:** ¿Qwen local (Ollama) o API? ¿Qué tareas justifican un modelo capaz vs. uno barato?
3. **Alcance real de "crear negocios/inversiones":** empezar acotado — un flujo de análisis de
   inversión end-to-end usando los screeners — antes de generalizar.
4. **Seguridad/limites:** un agente que "invierte" o "gasta" necesita gates de confirmación humana.
   Nada de ejecución de órdenes reales sin aprobación explícita.

## Agentes con rol dedicado (ideas de Matías)
Además de workers efímeros, algunos agentes tienen un **rol fijo y recurrente**:
- **Trading scout** — busca oportunidades y corre filtros (skills `trading/`).
- **Ordenador académico** — organiza materiales de la U.
- **Buscador de ideas de negocio** — usa `business-career/`.
- **Optimizador de procesos/skills** — reparte roles, usa `meta/` (find-skills, task-observer).
- **Admin del hub personal (Netlify + Supabase)** 🆕 — agente dedicado a administrar el servidor:
  estado de deploys y logs en **Netlify**, y base de datos / auth / storage en **Supabase**.
  Requiere: Netlify CLI o API (token) + Supabase CLI o MCP (token). Podría correr como cron
  (chequeo periódico del hub) y avisar por Telegram si algo falla. Candidato a **skill propia**
  (`devops/netlify-supabase-hub`) o a MCPs de Netlify/Supabase conectados a este agente.

## Primer hito sugerido (MVP acotado)
"Analista de inversión multiagente": el orquestador toma un universo de tickers → dispara N workers
Qwen que corren distintos screeners de `claude-trading-skills` en paralelo → sintetiza un reporte
rankeado. Reutiliza lo que ya tenemos y prueba el patrón sin riesgo de ejecutar operaciones reales.
Encaja con `analisis-inversion` (pendiente del material del amigo).
