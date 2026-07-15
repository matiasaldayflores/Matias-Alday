---
name: resumen-ramo
description: Genera un resumen de estudio en formato MAESTRO a partir de apuntes de un ramo. Úsalo cuando Matías pida resumir, ordenar o preparar material de estudio de un ramo teórico (Modelos Estocásticos, Micro, Ética, etc.).
---

# Resumen de ramo — formato MAESTRO

Cuando Matías pida un resumen de un ramo teórico, produce un documento Markdown limpio
listo para pegar en su vault de Obsidian / Notion.

## Estructura de salida

```markdown
# <Ramo> — Resumen: <tema>

## 🎯 Ideas clave
- Bullet conciso por concepto central (máx 7).

## 📖 Desarrollo
### <Subtema>
Explicación clara y breve. Fórmulas en LaTeX inline ($...$) o bloque ($$...$$).

## 🧮 Fórmulas / Resultados importantes
| Concepto | Fórmula | Cuándo se usa |
|----------|---------|---------------|

## ❓ Preguntas de repaso
- Pregunta → respuesta corta.

## 🔗 Conexiones
- [[wikilinks]] a otros temas del vault cuando apliquen.
```

## Reglas
- Prioriza claridad sobre exhaustividad: es material de estudio, no un libro.
- Usa LaTeX para toda notación matemática.
- Mantén los emojis de sección (son parte del formato MAESTRO del vault).
- Si faltan apuntes o el tema es ambiguo, pregunta antes de inventar contenido.
- No inventes fórmulas ni resultados; si no estás seguro, márcalo con ⚠️.
