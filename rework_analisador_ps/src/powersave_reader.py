import pandas as pd

class PowersaveReader:
    def __init__(self):
        self.ps_files = r'data\input\powersave'

    def read_ps_file(self, ps_file):
        ps_df = pd.read_excel(ps_file, skiprows=4)
        return ps_df

    

reader = PowersaveReader()
reader.read_ps_file('data\input\powersave\ET0098_from-2025_12_16-14h29m03s-to-2026_01_16-18h00m00s_powersave.xlsx')
