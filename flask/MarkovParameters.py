class MarkovParameters:
    """ Add description of class."""

    __replacementRate = __installationRate = __failureRate = None

    def __init__(self):
        """Initializes all class variables to 1."""
        self.__replacementRate = 1
        self.__installationRate = 1
        self.__failureRate = 1

    def __init__(self, leadTime, installationTime, failureRate, 
            d_installationTime, d_leadTime):
        """Initialize class variables

        Args:
            leadTime:           Value of equipment lead time.
            installationTime:   Value of equipment installation time.
            failureRate:        Equipment failure rate.
            d_installationTime: Duration of installation time (i.e. weeks, months, etc.).
            d_leadTime:         Duration of lead time (i.e. weeks, months, etc.).
        """
        self.__failureRate = float(failureRate)
        self.__setInstallationRate(float(installationTime), d_installationTime)
        self.__setReplacementRate(float(leadTime), d_leadTime)


    def __setInstallationRate(self, installationTime, d_installationTime):
        """Sets installation rate based on the installation time and duration
        
        Args:
            installationTime:   Value of equipment installation time.
            d_installationTime: Duration of installation time (i.e. weeks, months, etc.).
        """
        if d_installationTime == "Year(s)":
            self.__installationRate = 1.0 / installationTime

        elif d_installationTime == "Month(s)":
            self.__installationRate = 1.0 / (installationTime/12.0)

        elif d_installationTime == "Week(s)":
            self.__installationRate = 1.0 / (installationTime/52.0)

        else:
            self.__installationRate = 1.0 / (installationTime/365.0)

    def __setReplacementRate(self, leadTime, d_leadTime):
        """Sets replacement rate based on lead time and duration
        
        Args:
            leadTime:   Value of equipment lead time.
            d_leadTime: Duration of lead time (i.e. weeks, months, etc.)
        """
        if d_leadTime == "Year(s)":
            self.__replacementRate = 1 / leadTime

        elif d_leadTime == "Month(s)":
            self.__replacementRate = 1 / (leadTime/12)

        elif d_leadTime == "Week(s)":
            self.__replacementRate = 1 / (leadTime/52)

        else:
            self.__replacementRate = 1 / (leadTime/365)

    def getReplacementRate(self):
        return self.__replacementRate

    def getInstallationRate(self):
        return self.__installationRate

    def getFailureRate(self):
        return self.__failureRate