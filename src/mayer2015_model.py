"""The one offset-correction model in this line of work that was published.

The CHI '18 paper under audit fits 8 models (4 ray casts x 2 environments), each
15 coefficients per angle, and prints none of them. Its predecessor does print
its f4 coefficients, so this module exists to show what the missing artifact
would have looked like -- and to give a reader something they can actually
apply.

Source: Mayer, Wolf, Schneegass, Henze. "Modeling Distant Pointing for
Compensating Systematic Displacements." CHI '15 LBW, Table 3: "The coefficients
for the correction function f4 (in 10^-5)". The functional form is printed in
the same paper:

    f4(x, y) = a x^4 + b y^4 + c x^3 y + d x y^3 + e x^3 + f y^3
             + g x^2 y^2 + h x^2 y + i x y^2 + j x^2 + k y^2 + l x y
             + m x + n y + o

with x = alpha_lr (horizontal deviation) and y = alpha_bt (vertical deviation).
Caveats a user must keep in mind: it was fitted on index-finger ray casts in the
real world only, at 2m and 3m, sitting and standing, from 12 participants. It is
NOT the CHI '18 model and must not be presented as such.
"""

import numpy as np

SCALE = 1e-5

# Table 3, columns "lr" and "bt", in the order a..o.
COEFFICIENTS = {
    "lr": dict(a=0.0296, b=0.0190, c=-0.0258, d=-0.0634, e=-7.7225, f=-3.0723,
               g=-0.1239, h=-2.4860, i=-2.6181, j=-144.4819, k=239.7431,
               l=77.4749, m=2863.6584, n=4786.0898, o=528615.8408),
    "bt": dict(a=-0.0439, b=0.1070, c=-0.0070, d=0.0212, e=-2.2891, f=-19.5427,
               g=0.0598, h=-0.6280, i=-1.1506, j=-72.1956, k=310.0211,
               l=151.2857, m=-1495.0381, n=-8136.1496, o=-522112.5319),
}


def correction(alpha_lr, alpha_bt, axis: str) -> np.ndarray:
    """Correction angle in degrees for axis 'lr' (horizontal) or 'bt' (vertical)."""
    c = COEFFICIENTS[axis]
    x = np.asarray(alpha_lr, float)
    y = np.asarray(alpha_bt, float)
    value = (c["a"] * x ** 4 + c["b"] * y ** 4 + c["c"] * x ** 3 * y
             + c["d"] * x * y ** 3 + c["e"] * x ** 3 + c["f"] * y ** 3
             + c["g"] * x ** 2 * y ** 2 + c["h"] * x ** 2 * y
             + c["i"] * x * y ** 2 + c["j"] * x ** 2 + c["k"] * y ** 2
             + c["l"] * x * y + c["m"] * x + c["n"] * y + c["o"])
    return value * SCALE


if __name__ == "__main__":
    for lr, bt in ((0.0, 0.0), (10.0, -5.0), (-20.0, 12.0)):
        print(f"alpha_lr={lr:6.1f} alpha_bt={bt:6.1f} -> "
              f"delta_lr={correction(lr, bt, 'lr'):+.3f} deg, "
              f"delta_bt={correction(lr, bt, 'bt'):+.3f} deg")
