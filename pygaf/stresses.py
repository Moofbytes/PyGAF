class StressSeries:
    """
    Timeseries of stress periods and values.

    Arguments:
    ---------
    periods : float
        List of stress period lengths; used if from_csv is an empty string
        [units: T], (default [])
    values : float
        List of stress period values, one per stress period; used if from_csv is
        an empty string [units: consistent], (default [])
    from_csv : str
        File path of csv file to read stress data from; no data are read if the
        string is empty (default '')
    """
    def __init__(self, periods=[], values=[], from_csv=''):
        from pandas import read_csv
        self.periods = periods
        self.values = values
        if from_csv != '':
            df = read_csv(from_csv, names=['periods', 'values'])
            self.periods = list(df['periods'])
            self.values = list(df['values'])
        # Checks
        if len(self.periods) != len(self.values):
            print('Error! the number of periods and values do not match.')

    @property
    def series(self):
        """ Stress series dataframe."""
        if len(self.periods) != len(self.values):
            print('Error! the number of periods and values do not match.')
            return
        else:
            from pandas import DataFrame
            d = {'periods':self.periods, 'values':self.values}
            return DataFrame(data=d)

        return

    def plot(self, dw=8):
        """Plot the stress series.

        Arguments:
        ---------
        dw : float
            Width of plot figure (default 8)
        """
        import matplotlib.pyplot as plt
        if len(self.periods) != len(self.values):
            print('Error! the number of periods and values do not match.')
            return
        plot_times, plot_values = [], []
        for i in range(len(self.periods)):
            plot_times.append(sum(self.periods[0:i]))
            plot_times.append(sum(self.periods[0:i+1]))
            plot_values.append(self.values[i])
            plot_values.append(self.values[i])
        fig = plt.figure(figsize=(dw, dw/3))
        plt.plot(plot_times, plot_values, color='orange', linewidth=3)
        plt.title('Stress Series')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.grid(True)
        plt.show()
        return
