import matplotlib.pyplot as plt
import pandas as pd

plt.style.use("mystyle.txt")

infilepath = "compare.txt"

df = pd.read_csv(infilepath, sep="\t", header=None)

plt.figure(figsize=(8, 6))
plt.errorbar(df[0], df[1], df[3], fmt=".", capsize=7, label="Fit two times")
plt.errorbar(df[0], df[2], df[3], fmt=".", capsize=7, label="Fit three times")
plt.xlabel("Bin Number")
plt.ylabel("y_exp - y_obs")
plt.legend()
plt.savefig("compare.pdf")
plt.show()
