import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from scipy.optimize import curve_fit


# Define the double Gaussian function
def gaussian(x, a1, b1, c1):
    """Gaussian function."""
    return a1 * np.exp(-((x - b1) ** 2) / (2 * c1**2))


class Plotter:
    def __init__(self, title="Plot", xlabel="X-axis", ylabel="Y-axis"):
        """Initialize the Plotter with title and axis labels."""
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

    def draw_scatter(self, x, chi2perndf, y, yerr, pdf_pages):
        """Draw a scatter plot with error bars."""
        y_min, y_max = np.min(y), np.max(y)
        lower = y_min - 0.5 * (y_max - y_min)
        upper = y_max + 0.5 * (y_max - y_min)

        print("Y-axis range:", lower, upper)

        # # Create a new figure and axis
        # fig, ax = plt.subplots()

        # # Plot with error bars
        # plt.errorbar(
        #     x, y, yerr=yerr, fmt=".", color="blue", capsize=7, ecolor="orangered"
        # )

        # # Prepare text annotation
        # text_max_min = (
        #     f"max: {y_max:.2f}\nmin: {y_min:.2f}"
        #     if y_min >= 0.001
        #     else f"max: {y_max:.2f}\nmin: {y_min:.4f}"
        # )

        # ax.text(
        #     0.15, 0.8, text_max_min, transform=ax.transAxes, fontsize=20, color="red"
        # )

        # # Set title and labels
        # ax.set_title(self.title)
        # ax.set_xlabel(self.xlabel)
        # ax.set_ylabel(self.ylabel)
        # ax.set_ylim(lower, upper)
        # ax.axhspan(y_min, y_max, color="lightblue", alpha=0.3)  # Highlight area

        # # Save the figure to PDF
        # pdf_pages.savefig()
        # plt.close()
        # plt.show()
        # Create the figure and axes
        fig, (ax1, ax2) = plt.subplots(
            2, 1, figsize=(10, 8), gridspec_kw={"height_ratios": [2, 1]}
        )
        mean_excluding_min_max = chi2perndf[
            (chi2perndf != chi2perndf.min()) & (chi2perndf != chi2perndf.max())
        ].mean()
        # Top plot: Values with error bars
        ax1.bar(x, y, yerr=yerr, capsize=5, color="skyblue", edgecolor="black")
        ax1.set_title(self.title)
        ax1.set_xlabel(self.xlabel)
        ax1.set_ylabel(self.ylabel)
        ax1.set_ylim(lower, upper)
        ax1.grid(axis="y")

        # Bottom plot: Reduced chi-squared
        ax2.plot(x, chi2perndf, marker="o", linestyle="-", color="orange")
        ax2.axhline(
            y=mean_excluding_min_max,
            color="red",
            linestyle="--",
            label=f"mean_excluding_min_max = {mean_excluding_min_max:.2f}",
        )
        ax2.set_xlabel(self.xlabel)
        ax2.set_ylabel("Chi2/NDF")
        # ax2.set_title("Reduced Chi-Squared")
        ax2.legend()
        ax2.grid()

        # # Save the figure to PDF
        plt.tight_layout()
        pdf_pages.savefig()

        plt.close()
        plt.show()

    def Q1_distri_hist1d(self, filepath, x, y):
        """Create a 1D histogram and fit a Gaussian."""
        y_min, y_max = np.min(y), np.max(y)
        y_mean, y_std = np.mean(y), np.std(y)
        lower = y_min - (y_max - y_min)
        upper = y_max + (y_max - y_min)

        print("Y-axis range:", lower, upper)

        # Create a histogram
        bins = 30
        hist, bin_edges = np.histogram(
            y, range=[lower, upper], bins=bins, density=False
        )
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        # Fit the histogram data to the Gaussian function
        popt, pcov = curve_fit(
            gaussian, bin_centers, hist, p0=[40, y_mean, y_std], maxfev=1000
        )
        print("Fitted parameters:", popt)

        # Calculate chi-squared
        chi_squared = np.sum((hist - gaussian(bin_centers, *popt)) ** 2)
        ndf = len(hist) - 3  # Degrees of freedom (bins - parameters)
        chi_squared_ndf = chi_squared / ndf if ndf > 0 else np.inf

        print(f"Chi-squared: {chi_squared}")
        print(f"Degrees of freedom: {ndf}")
        print(f"Chi-squared per degree of freedom: {chi_squared_ndf}")

        # Plot the histogram and the fitted Gaussian
        plt.hist(
            y,
            range=[lower, upper],
            bins=bins,
            label=f"Q$_{{1}}$: mean = {y_mean:.1f}, std = {y_std:.1f}",
        )
        plt.plot(
            bin_centers,
            gaussian(bin_centers, *popt),
            "r-",
            linewidth=2,
            label=r"fit: $\mu$ = %.1f, $\sigma$ = %.1f" % (popt[1], popt[2]),
        )

        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel("# of events")
        plt.legend()

        figname = f"{filepath}/{self.title}_hist1D.pdf"
        plt.savefig(figname)
        plt.show()

    def Q1_distri_hist2d(self, filepath, x, y):
        """Create a 2D histogram plot."""
        numbers = np.array(y)
        # Reshape the data into a square array (8x8)
        data = numbers.reshape(8, 8)

        # Create the 2D heatmap
        plt.figure(figsize=(10, 10))
        plt.imshow(data, cmap="viridis", interpolation="nearest")

        # Annotate each cell with its value
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                plt.text(
                    j, i, f"{data[i, j]:.1f}", ha="center", va="center", color="white"
                )

        plt.xlabel("Channel")
        plt.ylabel("Channel")
        plt.title(self.title)

        figname = f"{filepath}/{self.title}_hist2D.pdf"
        plt.savefig(figname)
        plt.show()
