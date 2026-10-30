#!/usr/bin/env python3
"""Build a small synthetic Bambu Studio 3MF figurine for the eval cases.

Usage: python3 make_figurine_fixture.py <out.3mf>

The figure reproduces the traps the skill describes, on ~20k triangles
instead of a 1.5M-triangle MakerLab export:
  slot 1  black  #000000  legs            (z  0..12)
  slot 2  grey   #8E9089  jacket          (z 12..24)  AND the two pupils on
                                           the head front (z 28..30)
  slot 3  skin   #F7E6DE  head, unpainted (object default extruder = 3)
  slot 4  red    #C12E1F  unused
Object-local coordinates: Z up, the figure faces -Y. Deterministic output.
"""
import json
import sys
import zipfile

STEP = 0.5  # grid size in mm; sets the triangle count


def code(n):  # Bambu paint_color for a whole triangle painted with filament n
    return f"{n * 4:X}" if n <= 2 else f"{n - 3:X}C"


def box(x0, x1, y0, y1, z0, z1, paint):
    """Yield (v1, v2, v3, slot) triangles for a grid-subdivided box.
    paint(cx, cy, cz) returns the slot for a cell centre (0 = unpainted)."""
    def grid(a0, a1, b0, b1):
        na, nb = round((a1 - a0) / STEP), round((b1 - b0) / STEP)
        for i in range(na):
            for j in range(nb):
                yield a0 + i * STEP, a0 + (i + 1) * STEP, b0 + j * STEP, b0 + (j + 1) * STEP

    faces = []
    for y, flip in ((y0, False), (y1, True)):          # front (-Y) / back (+Y)
        for a, b, c, d in grid(x0, x1, z0, z1):
            faces.append(([(a, y, c), (b, y, c), (b, y, d), (a, y, d)], flip))
    for x, flip in ((x0, True), (x1, False)):          # left / right
        for a, b, c, d in grid(y0, y1, z0, z1):
            faces.append(([(x, a, c), (x, b, c), (x, b, d), (x, a, d)], flip))
    for z, flip in ((z0, True), (z1, False)):          # bottom / top
        for a, b, c, d in grid(x0, x1, y0, y1):
            faces.append(([(a, c, z), (b, c, z), (b, d, z), (a, d, z)], flip))
    for quad, flip in faces:
        cx, cy, cz = (sum(p[k] for p in quad) / 4 for k in range(3))
        s = paint(cx, cy, cz)
        t1, t2 = (quad[0], quad[1], quad[2]), (quad[0], quad[2], quad[3])
        if flip:
            t1, t2 = t1[::-1], t2[::-1]
        yield (*t1, s)
        yield (*t2, s)


def head_paint(cx, cy, cz):
    on_front = abs(cy - -6) < 1e-9
    pupil = on_front and 28 <= cz <= 30 and (-4 <= cx <= -2 or 2 <= cx <= 4)
    return 2 if pupil else 0


def build_mesh():
    tris = []
    tris += box(-6, 6, -4, 4, 0, 12, lambda *_: 1)       # legs
    tris += box(-8, 8, -5, 5, 12, 24, lambda *_: 2)      # jacket
    tris += box(-6, 6, -6, 6, 24, 36, head_paint)        # head with pupils
    verts, index, faces = [], {}, []
    for *pts, slot in tris:
        ids = []
        for p in pts:
            key = tuple(round(c, 6) for c in p)
            if key not in index:
                index[key] = len(verts)
                verts.append(key)
            ids.append(index[key])
        faces.append((*ids, slot))
    return verts, faces


def object_model(verts, faces):
    out = ['<?xml version="1.0" encoding="UTF-8"?>\n',
           '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
           'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" requiredextensions="p">\n',
           ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n',
           ' <resources>\n  <object id="1" type="model">\n   <mesh>\n    <vertices>\n']
    out += ['     <vertex x="%.9g" y="%.9g" z="%.9g"/>\n' % v for v in verts]
    out.append('    </vertices>\n    <triangles>\n')
    for a, b, c, s in faces:
        paint = f' paint_color="{code(s)}"' if s else ''
        out.append(f'     <triangle v1="{a}" v2="{b}" v3="{c}"{paint}/>\n')
    out.append('    </triangles>\n   </mesh>\n  </object>\n </resources>\n <build/>\n</model>\n')
    return ''.join(out)


CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
 <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
 <Default Extension="png" ContentType="image/png"/>
</Types>
'''
RELS = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>
'''
MAIN_MODEL = '''<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">
 <metadata name="Application">BambuStudio-02.03.00.70</metadata>
 <metadata name="BambuStudio:3mfVersion">1</metadata>
 <resources>
  <object id="2" type="model">
   <components>
    <component p:path="/3D/Objects/object_1.model" objectid="1" transform="1 0 0 0 1 0 0 0 1 0 0 0"/>
   </components>
  </object>
 </resources>
 <build>
  <item objectid="2" transform="1 0 0 0 1 0 0 0 1 128 128 0" printable="1"/>
 </build>
</model>
'''
OBJECT_RELS = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Target="/3D/Objects/object_1.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>
'''


def model_settings(nfaces):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<config>
  <object id="2">
    <metadata key="name" value="figur"/>
    <metadata key="extruder" value="3"/>
    <metadata face_count="{nfaces}"/>
    <part id="1" subtype="normal_part">
      <metadata key="name" value="figur"/>
      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>
      <mesh_stat face_count="{nfaces}" edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/>
    </part>
  </object>
</config>
'''


def project_settings():
    n = 4
    return {
        "filament_colour": ["#000000FF", "#8E9089FF", "#F7E6DEFF", "#C12E1FFF"],
        "filament_settings_id": ["Bambu PLA Basic @BBL P1S"] * n,
        "filament_type": ["PLA"] * n,
        "filament_vendor": ["Bambu Lab"] * n,
        "nozzle_temperature": ["220"] * n,
        "hot_plate_temp": ["55"] * n,
        "flush_volumes_matrix": [str(0 if r == c else 280 + 10 * r + c) for r in range(n) for c in range(n)],
        "different_settings_to_system": ["", "", "", "", "", ""],
        "inherits_group": ["", "", "", "", "", ""],
        # printer setting with the same length as the filament arrays: must survive prune
        "printable_area": ["0x0", "256x0", "256x256", "0x256"],
        "printer_settings_id": "Bambu Lab P1S 0.4 nozzle",
        "layer_height": "0.12",
    }


def main(out):
    verts, faces = build_mesh()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        def add(name, data):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
        add("[Content_Types].xml", CONTENT_TYPES)
        add("_rels/.rels", RELS)
        add("3D/3dmodel.model", MAIN_MODEL)
        add("3D/_rels/3dmodel.model.rels", OBJECT_RELS)
        add("3D/Objects/object_1.model", object_model(verts, faces))
        add("Metadata/model_settings.config", model_settings(len(faces)))
        add("Metadata/project_settings.config", json.dumps(project_settings(), indent=4))
    print(f"wrote {out}: {len(verts)} vertices, {len(faces)} triangles")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
