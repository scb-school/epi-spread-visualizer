import matplotlib.pyplot as plt
import pandas as pd


class TimeSeries:
    def __init__(self, df, date_col, line_col, indep_col):
        self.df = df
        self.date_col = date_col
        self.line_col = line_col
        self.indep_col = indep_col

    def plot(self):
        """plot first converts the values in the "date_col" column of the dataframe to datetime,
        and then calls pandas.pivot_table to plot each of the "line_col" columns by date and their "indep_col" variable.
        """
        self.df[self.date_col] = pd.to_datetime(self.df[self.date_col])
        pivot = self.df.pivot_table(index=self.date_col, columns=self.line_col, values=self.indep_col, aggfunc='sum')
        pivot.plot()
        plt.show()
