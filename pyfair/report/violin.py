"""Violin plot for plotting metamodel risk"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import StrMethodFormatter

from ..utility.fair_exception import FairException
from .base_curve import FairBaseCurve


class FairViolinPlot(FairBaseCurve):
    """Provides a violin-style area plot to summarize MetaModels."""

    def __init__(self, metamodel):
        super().__init__()
        if not metamodel.__class__.__name__ == "FairMetaModel":
            raise FairException("This requires a metamodel")
        self._metamodel = metamodel
        # Store the model risks in a separate dictionary for easier access later
        self._model_risks = self._metamodel.export_results()

        # Define a default colormap for the violin plots
        self._color_map = {
            model_name: plt.cm.tab10(i)
            for i, model_name in enumerate(self._model_risks.keys())
        }

    def generate_image(self):
        """Generate violin plot image."""
        # Setup plots
        fig, ax = plt.subplots(figsize=(16, 8))

        # Calculate width for each violin plot based on number of models
        width = 0.8 / len(self._model_risks)

        violin_plots = []  # Store violin plot objects
        for i, (name, model_data) in enumerate(self._model_risks.items()):
            vp = ax.violinplot(
                model_data,
                positions=[i + 1],
                widths=width,
                showmeans=False,
                showmedians=True,
            )
            violin_plots.append(vp)

            # If the model name is not in the colormap, use the default color 'blue'
            for pc in vp["bodies"]:
                pc.set_facecolor(self._color_map.get(name, "blue"))
                pc.set_edgecolor("black")

            quartile1, medians, quartile3 = np.percentile(model_data, [25, 50, 75])
            ax.scatter(
                [i + 1],
                [medians],
                marker="o",
                color="white",
                s=30,
                zorder=3,
            )

        # Reset default x-ticks
        ax.tick_params(axis="x", reset=True)

        # Set custom x ticks and labels after creating the violin plots
        # Manually set tick locations at the center of each violin plot
        tick_positions = [
            vp["bodies"][0].get_paths()[0].vertices[:, 0].mean()
            for vp in violin_plots
        ]
        tick_labels = self._model_risks.keys()
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(tick_labels)

        ax.set_title("Components And Aggregate Risk", fontsize=20)
        ax.yaxis.set_major_formatter(
            matplotlib.ticker.StrMethodFormatter("${x:,.0f}")
        )
        plt.subplots_adjust(left=0.2)
        return fig, ax

