import pandas as pd
import json


class Generate_JUNO_json:
    @staticmethod
    def JUNO_TT_config(args, infile_HV, infile_mask, outfile):
        df_hv = pd.read_csv(infile_HV, header=None)
        print(df_hv)
        df_mask = pd.read_csv(infile_mask, sep="\t")
        # channel_mask = df_mask["gain_correction"].tolist()
        channel_mask = df_mask.iloc[:, -1].tolist()
        # pmt_id = args.PMT
        pmt_id = str(args.PMT)  # Ensure PMT ID is a string
        hv_calibration = df_hv.iloc[0, 0]
        print(channel_mask, pmt_id, hv_calibration)

        # Define the JSON structure
        data = {
            "pm_id": pmt_id,
            "valeur_haute_tension": hv_calibration,
            "maroc_sc": {
                "dac_0": 500,
                "pm_gain": channel_mask,
                "pm_mask": [1] * len(channel_mask),  # Assuming mask is all 1s
            },
        }

        # Save the JSON file
        with open(outfile, "w") as json_file:
            json.dump(data, json_file, indent=4)

        print(f"JSON file '{outfile}' created successfully!")
