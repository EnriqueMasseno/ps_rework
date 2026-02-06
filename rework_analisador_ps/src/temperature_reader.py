import pandas as pd

class TemperatureReader():
    def __init__(self):
        self.temperature_path = r'data\input\external_temperature\temperature.csv'
    
    def read_temperature(self):
        desired_columns = ['Data','Hora (UTC)', 'Temp. Max. (C)', 'Temp. Min. (C)']
        self.temperature_df = pd.read_csv(self.temperature_path,
                                          sep=";",
                                          usecols=desired_columns)
        
        self.brt_column()
        self.average_temperature()
        self.calculate_ghr(21)
        return self.temperature_df
    
    def brt_column(self):
        ts = pd.to_datetime(
            self.temperature_df['Data'] + " " +
            self.temperature_df['Hora (UTC)'].astype(str).str.zfill(4),
            dayfirst=True
        ) - pd.Timedelta(hours=3)

        self.temperature_df = (
            self.temperature_df
            .assign(
                **{
                    "Data (BRT)": ts.dt.strftime("%d/%m/%Y"),
                    "Hora (BRT)": ts.dt.strftime("%H:%M:%S"),
                    "Timestamp": ts,
                }
            )
            .set_index("Timestamp")
            .loc[:, ["Data (BRT)", "Hora (BRT)", "Temp. Max. (C)", "Temp. Min. (C)"]]
            .sort_index()
        )
        return self.temperature_df
    
    def average_temperature(self):
        convert_cols = ["Temp. Max. (C)", "Temp. Min. (C)"]

        self.temperature_df[convert_cols] = (
            self.temperature_df[convert_cols]
            .replace(",", ".", regex=True)
            .astype(float)
        )        
        self.temperature_df["Temp. Med. (C)"] = (self.temperature_df["Temp. Max. (C)"] + self.temperature_df["Temp. Min. (C)"])/2
        return self.temperature_df
    
    def calculate_ghr(self, confort_temperature):
        self.temperature_df["GHR"] = (self.temperature_df["Temp. Med. (C)"] - confort_temperature).clip(lower=0)
        return self.temperature_df
    
reader = TemperatureReader()
print(reader.read_temperature().head())
print('Sucesso')