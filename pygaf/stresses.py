class StressSeries:
    """Stress series class containing a timeseries of times and values.

    The stress series can be set manually using lists or loaded from a csv file
    containing comma separated pairs of times and values, one per line.
    Exceptions will occur if a period is negative or if the number of periods
    and stresses do not match.

    Attributes:
        periods (float) : List of stress period lengths; used if from_csv is
            an empty string (units T, default [1.0]).
        values (float) : List of stress period values, one per stress period;
            used if from_csv is an empty string (units consistent,
            default [0.0]).
        from_csv (str) : File path of csv file to read stress data from; no
            data are read if the string is empty (default '').

    """
    def __init__(self, periods=[1], values=[0], from_csv='',
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
        """list (float) : List of stress period lengths.

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
        """list (float) : List of stress period values.

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
        """ pandas dataframe : Stress series dataframe."""
        from pandas import DataFrame
        d = {'periods':self.periods, 'values':self.values}
        return DataFrame(data=d)

    def plot(self, dw=8):
        """Plot the stress series.

        Args:
            dw (float) : Width of plotted figure (default 8).

        Returns:
            Screen output.

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
