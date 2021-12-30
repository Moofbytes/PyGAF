class StressSeries:
    """
    Timeseries of stress periods and stress values.

    Arguments:
    ---------
    periods : float
        List of stress period lengths [units: T], (default [])
    values : float
        List of stress period values [units: consistent], (default [])
    from_csv : bool
        Read stress data from a csv file (default False)
    csv : str
        File path of csv file to read (default ''). If empty, then
        no data are imported.
    dw : float
        Width of stress series plot (default 8)

    Returns:
    -------
    Pandas dataframe
    """
    def __init__(self, periods=[], values=[], from_csv=False, csv='', dw=8):
        import pandas
        self.periods = periods
        self.values = values
        self.dw = dw
        if from_csv:
            self.series = pandas.read_csv(csv, names=['periods', 'values'])
            self.periods = list(self.series['periods'])
            self.values = list(self.series['values'])
        else:
            if len(periods) != len(values):
                print('Error! the number of periods and values do not match.')
                return
            else:
                self.series = pandas.DataFrame()
                self.series['periods'] = periods
                self.series['values'] = values
        return

    def plot(self):
        """Plot the stress series."""
        import matplotlib.pyplot as plt
        plot_times, plot_values = [], []
        for i in range(len(self.periods)):
            plot_times.append(sum(self.periods[0:i]))
            plot_times.append(sum(self.periods[0:i+1]))
            plot_values.append(self.values[i])
            plot_values.append(self.values[i])
        fig = plt.figure(figsize=(self.dw, self.dw/3))
        plt.plot(plot_times, plot_values, color='orange', linewidth=3)
        plt.title('Stress Series')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.grid(True)
        plt.show()
        return
