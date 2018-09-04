class Calculator:
    def __init__(self, initial, rate):
        """
        Pass in the initial amount invested
        and the rate as a percentage (ie 50 for 50%)
        """
        self._initial = initial
        self._rate = rate/100

    def total_interest(self, time):
        """
        Returns the total amount of interest after a given length of time
        """
        return self._initial * self._rate * time

    def time_required(self, total):
        """
        Returns the length of time required to achieve a given total
        """
        return total/(self._initial * self._rate)
