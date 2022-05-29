class StressSeries:
    """Stress series class defining sress periods and values.

    The default StressSeries object has default values periods=[1.0] and
    values=[0.0]. Stress periods and values are provided in corresponding lists,
    which can be created manually or loaded from a csv file containig
    comma-separated period and value pairs, one per line. Exceptions occur
    if a period is negative or if the number of periods and stresses do not
    match.

    The .plot method displays a timeseries graph of the stress series.

    Example csv file with three stress periods:

    10,25.6

    15.2,38.7
    
    48,-12

    Attributes:
        periods (float) : List of stress period lengths; used if from_csv is
            an empty string (units T, default [1.0]).
        values (float) : List of stress period values, one per stress period;
            used if from_csv is an empty string (units consistent,
            default [0.0]).
        from_csv (str) : File path of csv file to read stress data from; no
            data are read if the string is empty (default '').

    """
    def __init__(self, periods=[1.0], values=[0.0], from_csv='',
    title='Stress Series', xlabel='Time', ylabel='Value'):
        from pandas import read_csv
        self.periods = periods
        self.values = values
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        if from_csv != '':
            df = read_csv(from_csv, names=['periods', 'values'])
            self.periods = list(df['periods'])
            self.values = list(df['values'])

    @property
    def periods(self):
        """list (float) : list of stress period lengths.

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._periods

    @periods.setter
    def periods(self, v):
        if not (min(v) > 0):
            raise Exception('All stress periods must be positive.')
        self._periods = v

    @property
    def values(self):
        """list (float) : list of stress period values.

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._values

    @values.setter
    def values(self, v):
        if len(v) != len(self.periods):
            raise Exception(
                'The number of stress periods and values must match.'
            )
        self._values = v

    @property
    def series(self):
        """ pandas dataframe : stress series dataframe."""
        from pandas import DataFrame
        d = {'periods':self.periods, 'values':self.values}
        return DataFrame(data=d)

    def plot(self, dw=8):
        """Plot the stress series.

        Args:
            dw (float) : Width of figure (default 8).
        """
        import matplotlib.pyplot as plt
        plot_times, plot_values = [], []
        for i in range(len(self.periods)):
            plot_times.append(sum(self.periods[0:i]))
            plot_times.append(sum(self.periods[0:i+1]))
            plot_values.append(self.values[i])
            plot_values.append(self.values[i])
        fig = plt.figure(figsize=(dw, dw/3))
        plt.plot(plot_times, plot_values, linewidth=3)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.grid(True)
        plt.show()
        return
