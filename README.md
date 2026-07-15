# claude-skills

Skills personales de Matías, reutilizables en **Claude Code**, **Cowork** y **Design**.

Un *skill* es una carpeta con un archivo `SKILL.md` (y opcionalmente recursos: scripts,
plantillas, datos). El `SKILL.md` empieza con un frontmatter YAML que le dice a Claude
cuándo y cómo usar el skill.

## Estructura

Los skills se organizan por **categoría**. Cada skill es una carpeta con su `SKILL.md`.

Cada categoría tiene un `README.md` índice con la lista de sus skills y qué hace cada una.

```
claude-skills/
├── README.md
├── docs/
│   └── gestor-operaciones-multiagente.md   ← plan orquestador + Qwen/Hermes
└── skills/
    ├── trading/          inversiones: screeners, calendarios, análisis  (~86)
    ├── business-career/  negocios, marketing, CV/carrera, decisiones     (64)
    ├── web-design/       UI/UX, SEO, diseño en vivo                       (33)
    ├── media/            video/contenido: análisis, edición, motion       (9)
    ├── dev/              disciplina de desarrollo (TDD, diagnose, specs)   (8)
    ├── 3d-printing/      print-design (propia) + alternativas             (5)
    ├── meta/             crear/descubrir/mejorar skills                    (3)
    ├── research/         investigación multi-fuente                        (2)
    └── writing/          humanización de textos                           (1)
```

_~211 skills en total. Los conteos van entre paréntesis; abre el README de cada categoría para el índice detallado._

> **Nota de origen y seguridad:** casi todas las skills son open-source de terceros (licencias en
> cada carpeta). Antes de incorporarlas se pasaron por revisión de seguridad: antivirus on-access
> (McAfee) + escaneo de patrones peligrosos (base64→exec, curl|bash, exfiltración) + verificación de
> dominios de red. Además **no se copiaron los scripts de instalación** (`install.sh`, etc.) de los
> repos de origen — solo las carpetas `SKILL.md`. Resultado: limpio.

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
