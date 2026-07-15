# claude-skills

Skills personales de Matías, reutilizables en **Claude Code**, **Cowork** y **Design**.

Un *skill* es una carpeta con un archivo `SKILL.md` (y opcionalmente recursos: scripts,
plantillas, datos). El `SKILL.md` empieza con un frontmatter YAML que le dice a Claude
cuándo y cómo usar el skill.

## Estructura

```
claude-skills/
├── README.md
└── skills/
    └── <nombre-del-skill>/
        └── SKILL.md          ← instrucciones + frontmatter
        └── (recursos opcionales)
```

## Formato de un SKILL.md

```markdown
---
name: nombre-en-kebab-case
description: Una línea que explica QUÉ hace y CUÁNDO usarlo. Claude lee esto para decidir si activarlo.
---

# Título del skill

Instrucciones detalladas para Claude: pasos, ejemplos, formato de salida, restricciones.
```

Reglas clave del frontmatter:
- `name`: kebab-case, único, coincide con el nombre de la carpeta.
- `description`: la parte más importante — debe describir el disparador ("cuándo") con claridad,
  porque es lo único que Claude ve antes de decidir cargar el skill.

## Cómo usarlas en cada entorno

### Claude Code (esta terminal)
Los skills personales viven en `~/.claude/skills/`. Este repo está conectado ahí con un
*junction* (symlink de Windows), así que cualquier skill que agregues a `skills/` aparece
automáticamente. Invócalos con `/nombre-del-skill`.

### Cowork y Design (claude.ai)
Sube la carpeta del skill (comprimida en .zip) desde la sección **Skills** de la app,
o conecta este repo de GitHub si el entorno lo permite. El mismo `SKILL.md` funciona en
los tres lados sin cambios.

## Desarrollar un skill nuevo

1. `mkdir skills/mi-skill`
2. Crea `skills/mi-skill/SKILL.md` con el frontmatter.
3. Pruébalo en Claude Code con `/mi-skill`.
4. `git add . && git commit -m "add mi-skill" && git push`
