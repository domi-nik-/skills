"""End-to-end tests for scripts/bambu3mf.py on the synthetic figurine fixture.

Run from the repo root:
  python3 -m unittest discover -s bambu-3mf-figurine-edit/tests
Needs numpy, matplotlib, scipy and fast-simplification (as the skill does).

The fixture (evals/make_figurine_fixture.py): slot 1 black legs, slot 2 grey
jacket + pupils (Z 28..30), slot 3 skin = unpainted head via the object's
default extruder, slot 4 red unused. flush_volumes_matrix[r][c] = 280+10r+c.
"""
import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TOOL = SKILL / "scripts" / "bambu3mf.py"
FIXTURE = SKILL / "evals" / "make_figurine_fixture.py"

VRE = re.compile(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"')
TRE = re.compile(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"([^>]*?)/>')


def run(*args, ok=True):
    p = subprocess.run([sys.executable, "-I", str(TOOL), *map(str, args)], capture_output=True, text=True)
    if ok and p.returncode:
        raise AssertionError(f"{args} failed:\n{p.stdout}\n{p.stderr}")
    return p


def triangles(work):
    """[(min z, max z, paint code, other attributes)] per triangle."""
    t = (work / "3D" / "Objects" / "object_1.model").read_text(encoding="utf-8")
    zs = [float(v[2]) for v in VRE.findall(t)]
    out = []
    for a, b, c, rest in TRE.findall(t):
        z = [zs[int(a)], zs[int(b)], zs[int(c)]]
        m = re.search(r'paint_color="([^"]*)"', rest)
        out.append((min(z), max(z), m.group(1) if m else "", re.sub(r'\s*paint_color="[^"]*"', "", rest).strip()))
    return out


def settings(work):
    return json.loads((work / "Metadata" / "project_settings.config").read_text(encoding="utf-8"))


def default_extruder(work):
    x = (work / "Metadata" / "model_settings.config").read_text(encoding="utf-8")
    return int(re.search(r'key="extruder" value="(\d+)"', x).group(1))


class Bambu3mfTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.fixture = Path(cls.tmp.name) / "figur.3mf"
        subprocess.run([sys.executable, "-I", str(FIXTURE), str(cls.fixture)], check=True, capture_output=True)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def setUp(self):
        self.work = Path(tempfile.mkdtemp(dir=self.tmp.name)) / "work"
        run("unpack", self.fixture, self.work)

    def test_info_reports_slots_and_default_extruder(self):
        out = run("info", self.work).stdout
        self.assertIn("faces 19840", out)
        self.assertRegex(out, r"slot 2: #8E9089FF .* faces=7616 .* z 12\.0\.\.29\.8")
        self.assertRegex(out, r"slot 4: #C12E1FFF .*UNUSED")
        self.assertIn("unpainted faces: 6848 (print with object extruder 3)", out)

    def test_repaint_with_zmax_moves_jacket_but_not_pupils(self):
        run("repaint", self.work, "--from", 2, "--to", 1, "--zmax", 24)
        tris = triangles(self.work)
        grey = [t for t in tris if t[2] == "8"]
        self.assertEqual(len(grey), 64)
        self.assertTrue(all(t[0] >= 28 for t in grey), "only the pupils stay grey")
        self.assertFalse([t for t in tris if t[1] <= 24 and t[0] >= 12 and t[2] == "8"])

    def test_repaint_keeps_other_triangle_attributes(self):
        model = self.work / "3D" / "Objects" / "object_1.model"
        t = model.read_text(encoding="utf-8")
        t = t.replace('paint_color="8"/>', 'paint_color="8" paint_supports="4"/>', 1)
        model.write_text(t, encoding="utf-8")
        run("repaint", self.work, "--from", 2, "--to", 1)
        self.assertEqual(sum(1 for x in triangles(self.work) if x[3] == 'paint_supports="4"'), 1)

    def test_repaint_rejects_slot_out_of_range(self):
        p = run("repaint", self.work, "--from", 2, "--to", 9, ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("out of range", p.stderr)

    def test_prune_keeps_default_extruder_slot_and_drops_unused(self):
        run("prune", self.work)
        s = settings(self.work)
        self.assertEqual(s["filament_colour"], ["#000000FF", "#8E9089FF", "#F7E6DEFF"])
        self.assertEqual(len(s["nozzle_temperature"]), 3)
        self.assertEqual(len(s["flush_volumes_matrix"]), 9)
        self.assertEqual(len(s["different_settings_to_system"]), 5)
        self.assertEqual(s["printable_area"], ["0x0", "256x0", "256x256", "0x256"], "printer setting untouched")
        self.assertEqual(default_extruder(self.work), 3)

    def test_prune_renumbers_paint_matrix_and_default_extruder(self):
        run("repaint", self.work, "--from", 1, "--to", 2)   # slot 1 now unused
        run("prune", self.work)
        s = settings(self.work)
        self.assertEqual(s["filament_colour"], ["#8E9089FF", "#F7E6DEFF"])
        # rows/cols 1 and 2 of the original 4x4 matrix (280 + 10r + c, 0 on the diagonal)
        self.assertEqual(s["flush_volumes_matrix"], ["0", "292", "301", "0"])
        self.assertEqual(default_extruder(self.work), 2)
        codes = {t[2] for t in triangles(self.work)}
        self.assertEqual(codes, {"4", ""}, "old slot 2 is now slot 1 (code 4)")

    def test_prune_refuses_sub_triangle_paint(self):
        model = self.work / "3D" / "Objects" / "object_1.model"
        model.write_text(model.read_text(encoding="utf-8").replace('paint_color="4"', 'paint_color="4C08"', 1), encoding="utf-8")
        p = run("prune", self.work, ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("mixed sub-triangle paint", p.stderr)

    def test_colors_sets_rgba_and_rejects_bad_hex(self):
        run("colors", self.work, "1=#6f5034", "3=BF9573")
        s = settings(self.work)
        self.assertEqual(s["filament_colour"][0], "#6F5034FF")
        self.assertEqual(s["filament_colour"][2], "#BF9573FF")
        self.assertNotEqual(run("colors", self.work, "2=#12345", ok=False).returncode, 0)

    def test_simplify_transfers_paint_and_updates_face_count(self):
        run("simplify", self.work, "--target", 5000)
        tris = triangles(self.work)
        self.assertLessEqual(len(tris), 5000)
        self.assertGreater(len(tris), 4000)
        self.assertEqual({t[2] for t in tris}, {"4", "8", ""})
        self.assertTrue(any(t[2] == "8" and t[0] >= 27 for t in tris), "pupils survive")
        ms = (self.work / "Metadata" / "model_settings.config").read_text(encoding="utf-8")
        self.assertEqual(set(re.findall(r'face_count="(\d+)"', ms)), {str(len(tris))})

    def test_render_writes_png(self):
        out = self.work.parent / "hl.png"
        run("render", self.work, out, "--highlight", 2)
        self.assertEqual(out.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

    def test_pack_round_trip(self):
        out = self.work.parent / "out.3mf"
        run("pack", self.work, out)
        with zipfile.ZipFile(out) as z:
            self.assertEqual(z.namelist()[:2], ["[Content_Types].xml", "_rels/.rels"])
            self.assertIsNone(z.testzip())
        again = self.work.parent / "again"
        self.assertIn("faces 19840", run("unpack", out, again).stdout)

    def test_unpack_refuses_existing_directory(self):
        self.assertNotEqual(run("unpack", self.fixture, self.work, ok=False).returncode, 0)


if __name__ == "__main__":
    unittest.main()
