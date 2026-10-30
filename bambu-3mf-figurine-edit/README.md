# bambu-3mf-figurine-edit

A [Claude Agent Skill](https://support.claude.com/en/articles/12512176-what-are-skills) for editing painted **Bambu Studio 3MF** projects, such as MakerLab PrintU figurines, without opening Bambu Studio:

- **Recolor parts:** move painted areas (jacket, eyes, hands, eyebrows) to another filament slot, optionally limited to a height or region, with a preview render before and after.
- **Remove unused slots:** drop filaments no longer used and renumber the paint and every per-filament setting, including the purge matrix.
- **Simplify:** cut the triangle count (Bambu's "more than 1M triangles" warning) and transfer the paint to the new mesh.
- **Filament advice:** match the colors to real Bambu Lab and Polymaker Panchroma filaments and set them as preview colors.

## What's inside

```
bambu-3mf-figurine-edit/
├── SKILL.md              # workflow, how Bambu stores paint, filament notes
└── scripts/
    └── bambu3mf.py       # unpack, info, render, repaint, colors, prune, simplify, pack
```

`bambu3mf.py` needs Python 3 with numpy and matplotlib; `simplify` also needs `fast-simplification` and `scipy` (installed from PyPI). It only reads and writes the 3MF you give it and makes no network calls.

## Limits

- One painted object per project.
- Only whole-triangle paint (as produced by MakerLab). Fine brush painting from Bambu Studio is detected and left untouched, and `prune` refuses to run on it.
- Results are checked with the tool's own renders, not inside Bambu Studio. Check the preview there before printing.

## Install

See the [repo README](../README.md#how-to-install-a-skill).

## License

[MIT](./LICENSE)
