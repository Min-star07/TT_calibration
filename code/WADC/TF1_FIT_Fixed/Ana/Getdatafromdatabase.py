import pymysql as ms
import uproot
import pandas as pd
from datetime import datetime
import math
import argparse
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import re
from scipy.optimize import curve_fit


# Define the Gaussian function
def gaussian(x, a1, b1, c1):
    """Double Gaussian function used for curve fitting."""
    return a1 * np.exp(-((x - b1) ** 2) / (2 * c1**2))


# Apply a custom plotting style
plt.style.use("mystyle.txt")


class DatabaseConnector:
    """
    Class for connecting to a MySQL database and fetching data.
    """

    def __init__(
        self, host="localhost", user="root", password="@Min08240707", database="test"
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """Establish connection to the MySQL database."""
        try:
            self.connection = ms.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset="utf8mb4",
                cursorclass=ms.cursors.DictCursor,
            )
        except ms.MySQLError as e:
            print(f"Error connecting to the database: {e}")
            raise

    def fetch_data(self, feb_id, ch):
        """Fetch data from the MySQL database based on FEB_ID and CH."""
        try:
            if self.connection is None:
                self.connect()
            with self.connection.cursor() as cursor:
                sql_query = (
                    "SELECT * FROM web_tt_calibration WHERE FEB_ID = %s AND CH = %s"
                )
                cursor.execute(sql_query, (feb_id, ch))
                rows = cursor.fetchall()
                if rows:
                    df = pd.DataFrame(rows)
                    df.to_csv("tt_calibration.csv", sep="\t", index=False)
                    return df
                else:
                    print(f"No data found for FEB_ID={feb_id}, CH={ch}")
                    return pd.DataFrame()
        finally:
            if self.connection:
                self.connection.close()


class DataAnalyzer:
    """
    Class for analyzing and processing calibration data.
    """

    @staticmethod
    def gain_calibration_result(args, infile):
        """Calculate gain calibration results and save to file."""
        df = pd.read_csv(infile, sep="\t", header=None)
        gain_result = []

        for i, charge_value in enumerate(df[6]):
            db_connector = DatabaseConnector()
            db_connector.connect()
            data = db_connector.fetch_data(args.FEB, i)

            if not data.empty:
                a1 = data.loc[0, "a1"]
                charge = charge_value / a1
                gain = charge * (1e-12) / (1.602 * 1e-19)
                gain_result.append(gain)
            else:
                gain_result.append(None)

        df[21] = gain_result
        df.to_csv(infile, sep="\t", header=None, index=False)
        print("Gain calibration results saved.")

    @staticmethod
    def gain_distribution_histogram(args, path, infile):
        """Plot histogram of gain distribution and save the result to PDF."""
        df = pd.read_csv(infile, sep="\t", header=None)
        y = df[21].dropna()

        y_min, y_max = np.min(y), np.max(y)
        y_mean, y_std = np.mean(y), np.std(y)
        xrange = [y_min - 500000, y_max + 500000]

        # Create a histogram from the data
        hist, bin_edges = np.histogram(y, range=xrange, bins=80, density=False)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        # Fit the histogram data to a Gaussian function
        popt, _ = curve_fit(gaussian, bin_centers, hist, p0=[40, y_mean, y_std])

        # Calculate chi-squared
        observed_data = hist
        expected_data = gaussian(bin_centers, *popt)
        residuals = observed_data - expected_data
        chi_squared = np.sum(residuals**2)
        ndf = len(observed_data) - len(popt)
        chi_squared_ndf = chi_squared / ndf

        print(f"Chi-squared: {chi_squared}")
        print(f"Chi-squared per degree of freedom: {chi_squared_ndf}")

        # Plot the histogram and fitted curve
        plt.hist(
            y,
            range=xrange,
            bins=80,
            label=f"Q$_{{1}}$: mean = {y_mean:.2e}, std = {y_std:.2e}",
        )
        plt.plot(
            bin_centers,
            gaussian(bin_centers, *popt),
            "r-",
            linewidth=2,
            label=r"Fit: $\mu$ = {:.2e}, $\sigma$ = {:.2e}".format(popt[1], popt[2]),
        )

        plt.xlabel("Gain")
        plt.ylabel("# of events")
        title = f"WALL{args.WALL}_CB{args.CB}_ROB{args.ROB}_{args.mode}_Gain_correction"
        plt.title(title)
        plt.legend(fontsize=12)

        figname = f"{path}/{title}_hist1D.pdf"
        plt.savefig(figname)
        plt.show()

    @staticmethod
    def get_amplification_factor(infile, outfile):
        """Calculate amplification factors and save them to a file."""
        df = pd.read_csv(infile, sep="\t", header=None)

        max_channel = df.iloc[0, 20]
        gain_factors, gain_corrections = [], []

        for i, gain in df[6].items():
            factor = df.iloc[max_channel, 6] / gain
            gain_factors.append(factor)
            gain_corrections.append(math.ceil(64 * factor))

        result = pd.DataFrame(
            {
                "channel": df[0],
                "gain_ini": df[6],
                "gain_factor": gain_factors,
                "gain_correction": gain_corrections,
            }
        )

        result.to_csv(outfile, sep="\t", index=False)
        print(f"Amplification factors saved to {outfile}")

    @staticmethod
    def get_max_channel(infile):
        """Determine the channel with the maximum gain."""
        df = pd.read_csv(infile, sep="\t", header=None)
        max_channel = df[6].idxmax()
        df[20] = max_channel
        df.to_csv(infile, sep="\t", header=None, index=False)
        print(f"Max channel updated: {max_channel}")


# Example usage
# if __name__ == "__main__":
#     # Example to use DataAnalyzer and DatabaseConnector
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--FEB", type=int, help="FEB ID")
#     parser.add_argument("--WALL", type=int, help="WALL")
#     parser.add_argument("--CB", type=int, help="CB")
#     parser.add_argument("--ROB", type=int, help="ROB")
#     parser.add_argument("--mode", type=str, help="Mode")
#     parser.add_argument("--path", type=str, help="Path to save files")

#     args = parser.parse_args()

#     # Perform some operations as needed
#     analyzer = DataAnalyzer()
# Example:
# analyzer.gain_calibration_result(args, 'input_file.txt')
# analyzer.gain_distribution_histogram(args, 'input_file.txt')
