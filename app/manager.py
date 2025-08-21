# import pandas as pd
# from processor import DataProcessor
#
#
# class AnalysisManager:
#     def __init__(self, df: pd.DataFrame):
#         self.raw_data_df = df
#         self.processor = DataProcessor()
#         self.processed_data = None
#
#     def run_full_analysis(self):
#         if self.raw_data_df.empty:
#             self.processed_data = []
#             return
#
#         processed_df = self.processor.process_data(self.raw_data_df)
#         self.processed_data = processed_df.to_dict(orient='records')
#
#     def get_processed_data(self):
#         return self.processed_data