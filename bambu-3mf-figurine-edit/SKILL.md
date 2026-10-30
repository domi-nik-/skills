---
name: bambu-3mf-figurine-edit
description: Recolor, clean up and simplify painted Bambu Studio 3MF projects (e.g. MakerLab PrintU figurines) and pick matching real filaments. Use whenever a .3mf needs part colors changed, unused slots removed, triangle count reduced, or filament matches.
---

# Bambu Studio 3MF figurine editing

Painted Bambu Studio projects store the color of each triangle in the mesh, so the
work is: find out which slot paints which body part, move triangles between slots,
then tidy the project settings. All of this is done with the bundled tool
`scripts/bambu3mf.py`, which was proven on a 1.48M-triangle MakerLab figurine.

Answer in the user's language (usually German).

## Setup

Copy `scripts/bambu3mf.py` from this skill's folder into the working directory
(not into the user's upload folder). It needs numpy and
matplotlib; `simplify` additionally needs
`pip install --break-system-packages fast-simplification scipy`.
Always work on an extracted copy: `python3 -I bambu3mf.py unpack <in.3mf> work/`.

## How paint is stored (why the tool works this way)

- `3D/Objects/object_1.model`: each `<triangle>` has `paint_color` = slot code.
  Slot 1 = `4`, 2 = `8`, 3 = `0C`, 4 = `1C`, 5 = `2C`, ... (n>=3: hex(n-3)+`C`).
  No attribute = the object's default extruder (`<metadata key="extruder">` in
  `Metadata/model_settings.config`). Longer codes are sub-triangle paint; the
  tool leaves those alone and `prune` refuses to run on them. Other triangle
  attributes (`paint_supports`, `paint_seam`) are kept by `repaint`/`prune` but
  cannot survive `simplify`.
- `Metadata/project_settings.config` (JSON): `filament_colour` (#RRGGBBAA) and
  every per-filament setting. Arrays are length n (per slot), n*2 (per slot x
  extruder variant), n*n (`flush_volumes_matrix`) or n+2
  (`different_settings_to_system`, `inherits_group`). `prune` picks per-filament
  settings by key name, never by array length alone, because printer settings
  (bed outline, machine limits, extruder variants) can have the same length.
  After a Bambu Studio update, new per-filament keys without the `filament_`
  prefix would need adding to `FILAMENT_KEYS` in the script.
- Object-local coordinates: Z up, the figure's front faces -Y. Use `info` to see
  the bounding box and the Z range of each slot.

## Workflow

1. `info work/` then `render work/ overview.png` and look at the image.
2. Before repainting a slot, `render work/ hl.png --highlight N` and look. One
   slot often paints more than one part: in the reference figurine the "jacket
   grey" slot also coloured the eye pupils, and the "face detail" slot was mostly
   the hands plus the eyebrows. Tell the user what a slot really covers before
   changing it, and let them decide for the side parts.
3. Repaint, restricting with `--zmin/--zmax` (and x/y) when only part of a slot
   should move: e.g. `repaint work --from 2 --to 3 --zmax 24` moved the jacket but
   not the eyes above Z 24. The filter uses all three vertices of a triangle.
   Re-render to verify.
4. `colors work 1=6F5034 2=000000` to set preview colours to the real filaments
   the user will load, so Bambu Studio shows a realistic impression.
5. `prune work` once slots are unused (fewer filaments, less purging).
6. If the triangle count is over ~1M (Bambu warns "could be slow"), run
   `simplify work --target 400000`. It transfers the paint by nearest-face
   majority vote; check that the printed per-colour areas barely change (on the
   reference figurine: within 3 mm2) and re-render the face area (`--zmin`). Prefer this to Bambu's own
   "Simplify model" button, which is not known to keep the paint.
7. `pack work out.3mf`, send it, and give a different file name per variant so the
   user can compare versions side by side.

Tell the user, briefly: presets in the file are still whatever they were (switch
to e.g. "Bambu PLA Matte" or "Generic PLA" for non-Basic spools), the embedded
thumbnails show old colours until they save in Bambu Studio, and you checked the
file with your own renders, not in Bambu Studio itself.

## Filament advice

Look up hex codes and availability with web search each time (stock, prices and
ranges change); the notes below are what was found in October 2026.

- Bambu PLA Basic: Black #000000 (10101), Cocoa Brown #6F5034 (10802), Brown
  #9D432C, Beige #F7E6DE (10201, pale rosé-cream, slightly glossy).
- Bambu PLA Matte: Charcoal #000000, Dark Brown #7D6556, Caramel #AE835B,
  Terracotta #B15533, Latte Brown #D3B7A7, Desert Tan #E8DBB7.
- Skin: Bambu has no real warm skin tone. Latte Brown looked grey and pale to the
  user. Polymaker Panchroma Matte (formerly PolyTerra) has a skin-tone pack:
  Pastel Beige (light, warm peach), Pastel Peanut #BF9573 (close to the generator's
  own skin colour), Wood Brown #AB7449, Earth Brown. Army Beige (#DBBAA5/#CCA897)
  is about the same greyish tone as Latte Brown, so not a good face colour.
- An all-Panchroma-Matte set gives one uniform matte finish: Earth Brown hair,
  Charcoal Black (#2F2E30, a very dark anthracite) clothes, Pastel Beige or
  Pastel Peanut skin.
- Non-Bambu spools have no RFID: set the AMS slot to Generic PLA or the matching
  profile. Polymaker cardboard spools: newer ones have hardened edges, older ones
  can slip or shed dust in the AMS; the Panchroma "Refill" versions fit Bambu
  reusable spools. 3DJake ships in about 3 business days; Polymaker's own EU shop
  states 5-10 days.
