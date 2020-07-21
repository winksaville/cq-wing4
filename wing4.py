import wing as w
import utils as ut
import cadquery as cq # type: ignore

tk = 0.25
wing = w.Wing.makeWing(ctx=globals(), thickness=tk)
ut.show(wing, ctx=globals())

import io
tolerance=0.001;
f = io.open(f'wing4-tol_{tolerance}-tk_{tk}.stl', 'w+')
cq.exporters.exportShape(wing, cq.exporters.ExportTypes.STL, f, tolerance)
f.close()
