#!/usr/bin/env python3
"""Edit painted Bambu Studio 3MF projects (single painted object).
Usage: python3 -I bambu3mf.py <cmd> <work_dir> [options]
  unpack <file.3mf> <work_dir>          extract (always work on a copy)
  info <work_dir>                       slots, colours, presets, painted area/z-range per slot
  render <work_dir> <out.png> [--highlight N] [--zmin Z] [--zmax Z]
  repaint <work_dir> --from N --to M [--zmin --zmax --xmin --xmax --ymin --ymax]
  colors <work_dir> N=#RRGGBB [N=#RRGGBB ...]
  prune <work_dir>                      drop unused slots, renumber paint + per-filament settings
  simplify <work_dir> --target FACES    decimate, transfer paint to new mesh
  pack <work_dir> <out.3mf>
Slot numbers are 1-based like in Bambu Studio. Coordinates are object-local (see info)."""
import sys, os, re, json, glob, zipfile, argparse
import numpy as np

ENC = "utf-8"

def code(n):   # Bambu paint_color for a whole triangle painted with filament n
    return f"{n*4:X}" if n <= 2 else f"{n-3:X}C"
def slot_of(c):
    if c == "": return 0
    for n in range(1, 19):
        if code(n) == c: return n
    return -1  # sub-triangle paint string (mixed) - not handled per triangle

def model_path(d):
    p = glob.glob(os.path.join(d, "3D", "Objects", "*.model"))
    if len(p) != 1: sys.exit(f"expected exactly one object model, found {p}")
    return p[0]

VRE = re.compile(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"')
TRE = re.compile(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"([^>]*?)/>')
PRE = re.compile(r'\s*paint_color="([^"]*)"')
def load(d):
    """Returns text, vertices, faces, paint codes and the other triangle attributes
    (e.g. paint_supports / paint_seam), which are written back unchanged."""
    t = open(model_path(d), encoding=ENC).read()
    V = np.array(VRE.findall(t), float)
    T = TRE.findall(t)
    F = np.array([x[:3] for x in T], int)
    C, X = [], []
    for x in T:
        m = PRE.search(x[3]); C.append(m.group(1) if m else ""); X.append(PRE.sub("", x[3]).rstrip())
    return t, V, F, np.array(C, dtype=object), np.array(X, dtype=object)
def save(d, t, V, F, C, X):
    head = t[:t.index('<mesh>')]; tail = t[t.index('</mesh>') + 7:]
    out = [head, '<mesh>\n    <vertices>\n']
    out += ['     <vertex x="%.9g" y="%.9g" z="%.9g"/>\n' % tuple(v) for v in V]
    out.append('    </vertices>\n    <triangles>\n')
    out += ['     <triangle v1="%d" v2="%d" v3="%d"%s%s/>\n' % (a, b, c, f' paint_color="{p}"' if p else '', x)
            for (a, b, c), p, x in zip(F, C, X)]
    out += ['    </triangles>\n   </mesh>', tail]
    open(model_path(d), 'w', encoding=ENC).write(''.join(out))
def settings(d):
    p = os.path.join(d, "Metadata", "project_settings.config"); return p, json.load(open(p, encoding=ENC))
def write_settings(p, s): json.dump(s, open(p, "w", encoding=ENC), indent=4)
def model_settings(d): return os.path.join(d, "Metadata", "model_settings.config")
EXT_RE = re.compile(r'(<metadata key="extruder" value=")(\d+)(")')
def default_extruder(d):
    """Slot that unpainted faces print with: the object's extruder in model_settings.config."""
    p = model_settings(d)
    if not os.path.exists(p): return 1
    m = EXT_RE.search(open(p, encoding=ENC).read()); return int(m.group(2)) if m else 1

def nslots(d): return len(settings(d)[1]["filament_colour"])
def check_slot(d, n, what):
    if n is not None and not 1 <= n <= nslots(d): sys.exit(f"{what} slot {n} out of range 1..{nslots(d)}")

def areas(V, F):
    a = V[F]; return 0.5 * np.linalg.norm(np.cross(a[:, 1] - a[:, 0], a[:, 2] - a[:, 0]), axis=1)

def cmd_info(d):
    _, s = settings(d); _, V, F, C, X = load(d)
    S = np.array([slot_of(c) for c in C]); A = areas(V, F); cz = V[F].mean(1)
    print("faces", len(F), "bbox min", V.min(0).round(1), "max", V.max(0).round(1))
    cols = s.get("filament_colour", []); presets = s.get("filament_settings_id", [])
    for i, col in enumerate(cols, 1):
        m = S == i
        rng = f"z {cz[m,2].min():.1f}..{cz[m,2].max():.1f}" if m.any() else "UNUSED"
        print(f"slot {i}: {col} {presets[i-1] if i-1 < len(presets) else ''} faces={m.sum()} area={A[m].sum():.0f}mm2 {rng}")
    if (S == 0).any(): print(f"unpainted faces: {(S == 0).sum()} (print with object extruder {default_extruder(d)})")
    if (S == -1).any(): print("WARNING mixed sub-triangle paint faces:", (S == -1).sum(), "- left untouched")
    if any(X): print("other triangle paint (supports/seam) on", sum(1 for x in X if x), "faces - kept by repaint/prune, lost by simplify")

def cmd_render(d, out, hl=None, zmin=None, zmax=None):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    check_slot(d, hl, "highlight")
    _, s = settings(d); _, V, F, C, _ = load(d)
    cols = [c[:7] for c in s["filament_colour"]]; S = np.array([slot_of(c) for c in C])
    S[S == 0] = default_extruder(d)
    c = V[F].mean(1); keep = np.ones(len(F), bool)
    if zmin is not None: keep &= c[:, 2] >= zmin
    if zmax is not None: keep &= c[:, 2] <= zmax
    fc = np.array([cols[k-1] if 0 < k <= len(cols) else "#999999" for k in S], dtype=object)
    if hl: fc[S == hl] = "#FF00FF"
    fig, ax = plt.subplots(1, 3, figsize=(15, 7))
    # (horizontal axis, flip, depth axis, viewer side); points drawn far-to-near
    for a, (h, flip, dep, side, title) in zip(ax, [(0, 1, 1, -1, "front (from -Y)"), (0, -1, 1, 1, "back (from +Y)"), (1, 1, 0, 1, "side (from +X)")]):
        idx = np.where(keep)[0]; o = idx[np.argsort(side * c[idx, dep])]
        a.scatter(flip * c[o, h], c[o, 2], c=list(fc[o]), s=0.5, marker="s", linewidths=0)
        a.set_aspect("equal"); a.set_title(title)
    plt.tight_layout(); plt.savefig(out, dpi=90); print("wrote", out)

def cmd_repaint(d, a):
    if a.src is None or a.dst is None: sys.exit("repaint needs --from and --to")
    check_slot(d, a.src, "--from"); check_slot(d, a.dst, "--to")
    t, V, F, C, X = load(d); P = V[F]
    m = np.array([slot_of(c) == a.src for c in C])
    for ax, lo, hi in ((0, a.xmin, a.xmax), (1, a.ymin, a.ymax), (2, a.zmin, a.zmax)):
        if lo is not None: m &= P[:, :, ax].min(1) >= lo
        if hi is not None: m &= P[:, :, ax].max(1) <= hi
    C = C.copy(); C[m] = code(a.dst); save(d, t, V, F, C, X)
    print(f"repainted {m.sum()} faces slot {a.src} -> {a.dst}; still painted with slot {a.src}: {sum(slot_of(c)==a.src for c in C)}")

def cmd_colors(d, pairs):
    if not pairs: sys.exit("colors needs N=#RRGGBB arguments")
    p, s = settings(d)
    for pr in pairs:
        n, h = pr.split("="); n = int(n); h = h.upper().lstrip("#")
        check_slot(d, n, "colors")
        if not re.fullmatch(r"[0-9A-F]{6}", h): sys.exit(f"bad colour {pr}")
        s["filament_colour"][n - 1] = f"#{h}FF"
    write_settings(p, s); print(s["filament_colour"])

# Per-filament settings without the "filament_" prefix (from a Bambu Studio 2.x project).
# Selected by key, not by array length, so printer/process arrays that happen to have
# the same length (bed outline, machine limits, extruder variants) are never touched.
FILAMENT_KEYS = {
    "activate_air_filtration", "additional_cooling_fan_speed", "additional_fan_full_speed_layer",
    "chamber_temperatures", "circle_compensation_speed", "close_additional_fan_first_x_layers",
    "close_fan_the_first_x_layers", "complete_print_exhaust_fan_speed", "cool_plate_temp",
    "cool_plate_temp_initial_layer", "cooling_perimeter_transition_distance", "cooling_slowdown_logic",
    "counter_coef_1", "counter_coef_2", "counter_coef_3", "counter_limit_max", "counter_limit_min",
    "diameter_limit", "during_print_exhaust_fan_speed", "eng_plate_temp", "eng_plate_temp_initial_layer",
    "fan_cooling_layer_time", "fan_max_speed", "fan_min_speed", "full_fan_speed_layer",
    "hole_coef_1", "hole_coef_2", "hole_coef_3", "hole_limit_max", "hole_limit_min", "hot_plate_temp",
    "hot_plate_temp_initial_layer", "impact_strength_z", "long_retractions_when_ec",
    "no_slow_down_for_cooling_on_outwalls", "nozzle_temperature", "nozzle_temperature_initial_layer",
    "nozzle_temperature_range_high", "nozzle_temperature_range_low", "overhang_fan_speed",
    "overhang_fan_threshold", "override_process_overhang_speed", "reduce_fan_stop_start_freq",
    "required_nozzle_HRC", "retraction_distances_when_ec", "slow_down_for_layer_cooling",
    "slow_down_layer_time", "slow_down_min_speed", "supertack_plate_temp",
    "supertack_plate_temp_initial_layer", "temperature_vitrification", "textured_plate_temp",
    "textured_plate_temp_initial_layer", "volumetric_speed_coefficients",
}
def is_filament_key(k): return k.startswith("filament_") or k in FILAMENT_KEYS

def cmd_prune(d):
    t, V, F, C, X = load(d); p, s = settings(d)
    S = np.array([slot_of(c) for c in C]); nf = len(s["filament_colour"])
    if (S == -1).any(): sys.exit("mixed sub-triangle paint present; prune would corrupt it")
    dext = default_extruder(d)
    used = sorted({int(x) for x in S[S > 0]} | ({dext} if (S == 0).any() else set()))
    keep = [u - 1 for u in used]; remap = {u: i + 1 for i, u in enumerate(used)}
    print("keeping slots", used, "->", list(remap.values()))
    vk = len(s.get("filament_extruder_variant", [])) // nf if nf else 0
    for k, v in list(s.items()):
        if not isinstance(v, list): continue
        if k == "flush_volumes_matrix" and len(v) == nf * nf:
            s[k] = [v[r * nf + c] for r in keep for c in keep]
        elif k in ("different_settings_to_system", "inherits_group") and len(v) == nf + 2:
            s[k] = [v[0]] + [v[1 + i] for i in keep] + [v[-1]]   # [process, filaments..., printer]
        elif is_filament_key(k):
            if len(v) == nf: s[k] = [v[i] for i in keep]
            elif vk > 1 and len(v) == nf * vk: s[k] = [v[i * vk + j] for i in keep for j in range(vk)]
    if "filament_self_index" in s and vk:
        s["filament_self_index"] = [str(i + 1) for i in range(len(keep)) for _ in range(vk)]
    C = np.array([code(remap[x]) if x > 0 else "" for x in S], dtype=object)
    save(d, t, V, F, C, X); write_settings(p, s)
    mp = model_settings(d)
    if os.path.exists(mp):   # object/part default extruder must follow the renumbering
        x = open(mp, encoding=ENC).read()
        x = EXT_RE.sub(lambda m: f"{m.group(1)}{remap.get(int(m.group(2)), 1)}{m.group(3)}", x)
        open(mp, "w", encoding=ENC).write(x)
    print("colours", s["filament_colour"])

def cmd_simplify(d, target):
    if not target: sys.exit("simplify needs --target FACES")
    import fast_simplification
    from scipy.spatial import cKDTree
    t, V, F, C, X = load(d)
    if target >= len(F): sys.exit(f"target {target} >= current {len(F)} faces")
    if any(X): print("WARNING: support/seam painting cannot be transferred and is dropped")
    V2, F2 = fast_simplification.simplify(V.astype(np.float32), F.astype(np.int32), target_reduction=1 - target / len(F), agg=7)
    tree = cKDTree(V[F].mean(1)); tri = V2[F2]
    pts = [tri.mean(1)] + [(2 * tri[:, k] + tri.sum(1) - tri[:, k]) / 4 for k in range(3)]
    lab = C[tree.query(np.concatenate(pts))[1]].reshape(4, -1)
    C2 = []
    for j in range(len(F2)):  # majority of 4 nearest-face samples; all-different -> centre sample
        v, n = np.unique(lab[:, j].astype(str), return_counts=True)
        C2.append(v[n.argmax()] if n.max() > 1 else lab[0, j])
    C2 = np.array(C2, dtype=object)
    A0, A2 = areas(V, F), areas(V2.astype(float), F2)
    for c in sorted(set(C), key=str): print(f"paint {c!r}: area {A0[C==c].sum():.0f} -> {A2[C2==c].sum():.0f} mm2")
    save(d, t, V2, F2, C2, np.array([""] * len(F2), dtype=object))
    mp = model_settings(d)
    if os.path.exists(mp):
        x = open(mp, encoding=ENC).read(); x = re.sub(r'face_count="\d+"', f'face_count="{len(F2)}"', x)
        open(mp, "w", encoding=ENC).write(x)
    print("faces", len(F), "->", len(F2))

def cmd_pack(d, out):
    outabs = os.path.abspath(out)
    first = ["[Content_Types].xml", "_rels/.rels"]
    files = [os.path.relpath(os.path.join(r, f), d) for r, _, fs in os.walk(d) for f in fs
             if os.path.abspath(os.path.join(r, f)) != outabs and not f.endswith(".3mf")]
    files = first + sorted(f for f in files if f not in first)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in files: z.write(os.path.join(d, f), f)
    with zipfile.ZipFile(out) as z: assert z.testzip() is None
    print("wrote", out, os.path.getsize(out) // 1024, "KB")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(usage=__doc__); ap.add_argument("cmd"); ap.add_argument("args", nargs="*")
    for o in ("from", "to", "highlight"): ap.add_argument("--" + o, type=int, dest={"from": "src", "to": "dst"}.get(o, o))
    for o in ("xmin", "xmax", "ymin", "ymax", "zmin", "zmax"): ap.add_argument("--" + o, type=float)
    ap.add_argument("--target", type=int)
    a = ap.parse_args(); g = a.args
    need = {"unpack": 2, "info": 1, "render": 2, "repaint": 1, "colors": 1, "prune": 1, "simplify": 1, "pack": 2}
    if a.cmd not in need or len(g) < need[a.cmd]: sys.exit(__doc__)
    if a.cmd == "unpack":
        os.makedirs(g[1], exist_ok=False); zipfile.ZipFile(g[0]).extractall(g[1]); cmd_info(g[1])
    elif a.cmd == "info": cmd_info(g[0])
    elif a.cmd == "render": cmd_render(g[0], g[1], a.highlight, a.zmin, a.zmax)
    elif a.cmd == "repaint": cmd_repaint(g[0], a)
    elif a.cmd == "colors": cmd_colors(g[0], g[1:])
    elif a.cmd == "prune": cmd_prune(g[0])
    elif a.cmd == "simplify": cmd_simplify(g[0], a.target)
    elif a.cmd == "pack": cmd_pack(g[0], g[1])
