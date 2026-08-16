"""Figure 4 of the paper, redrawn from a run of the Study 1 pipeline.

Paper, Figure 4: "The average offset for each of the four ray cast techniques",
one panel per method, target grid versus the mean intersection in RW and VR.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def figure4(trials, path):
    methods = sorted(trials["method"].unique())
    fig, axes = plt.subplots(1, len(methods), figsize=(4 * len(methods), 3.2),
                             sharex=True, sharey=True)
    axes = [axes] if len(methods) == 1 else list(axes)
    for ax, method in zip(axes, methods):
        sub = trials[trials["method"] == method]
        tg = sub.groupby(["target_x", "target_y"]).size().reset_index()
        ax.scatter(tg["target_x"], tg["target_y"], marker="+", s=60,
                   color="black", label="Target")
        for env, colour in (("RealWorld", "tab:blue"),
                            ("VirtualReality", "tab:orange")):
            e = sub[sub["environment"] == env]
            if e.empty:
                continue
            m = (e.groupby(["target_x", "target_y"])[["hit_x", "hit_y"]]
                  .mean().reset_index())
            ax.scatter(m["hit_x"], m["hit_y"], s=14, color=colour, label=env)
        ax.set_title(method)
        ax.set_xlabel("x in cm")
        ax.set_aspect("equal")
    axes[0].set_ylabel("y in cm")
    axes[-1].legend(fontsize="small", loc="upper right")
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path
