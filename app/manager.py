from .processor import DataProcessor
class AnalysisManager:
    def __init__(self, data: dict):
        self.raw_data = data['raw_data']
        self.data_as_df = None
        self.path_weapons = "data/weapons.txt"
        self.weapons = self._load_weapons()
        self.processor = DataProcessor()

    def start_analysis(self):
        self.data_as_df = DataProcessor().convert_to_df(self.raw_data)
        self.data_as_df["rarest_word"] = self.data_as_df["Text"].apply(self.processor.find_first_rarest_word)
        self.data_as_df["weapons_detected"] = self.data_as_df["Text"].apply(lambda txt: self.processor.find_weapons(txt, self.weapons))
        self.data_as_df["sentiment"] = self.data_as_df["Text"].apply(self.processor.get_sentiment)
        self.data_as_df = self.data_as_df.rename(columns={"Text": "original_text"})
    def get_processed_data(self):
        return self.data_as_df.to_dict("records")


    def _load_weapons(self):
        with open(self.path_weapons, "r") as f:
            return {line.strip() for line in f}