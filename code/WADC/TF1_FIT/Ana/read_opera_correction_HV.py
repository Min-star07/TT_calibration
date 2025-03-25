import pandas as pd
import json


class Generate_new_HV:
    @staticmethod
    def HV_correction(args, infile_config, infile_result, outfile):
        try:
            # Load the result file
            df = pd.read_csv(infile_result, sep="\t", header=None)
            abs_gain = df.iloc[args.max_channel, 21]
            ratio = (abs_gain - 1e6) / 1e6

            # Load the config file
            with open(infile_config, "r") as fcc_file:
                fcc_data = json.load(fcc_file)
                hv_opera = fcc_data["valeur_haute_tension"]

                # Calculate the corrected HV
                hv_juno = hv_opera / (1 + ratio)

                # Save the result as a single-row DataFrame
                pd.DataFrame([[hv_juno]]).to_csv(outfile, index=False, header=False)
                print(f"Corrected HV saved to {outfile}")

        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except KeyError as e:
            print(f"Missing key in config file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
