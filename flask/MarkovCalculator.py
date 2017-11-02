import numpy as np
import MarkovParameters as params
from discreteMarkovChain import markovChain

class MarkovCalculator:
    # TODO: Add class description
    """
    Args:
        a:              Equipment failure rate
        b:              Equipment replacement rate
        sr:             Equipment installation rate
        n:              Unit count
        matrix_0Spare:  Markov transition matrix for 0 spares
        matrix_1Spare:  Markov transition matrix for 1 spare
        matrix_2Spare:  Markov transition matrix for 2 spares
        matrix_3Spare:  Markov transition matrix for 3 spares
        matrix_4Spare:  Markov transition matrix for 4 spares
    """
    a = b = sr = n = None

    matrix_0Spare = matrix_1Spare = matrix_2Spare = matrix_3Spare = matrix_4Spare = None

    def __init__(self, units, leadTime, installationTime, failureRate, 
                d_installationTime, d_leadTime):
        """Initializes markov parameters and calculator parameters.

            Args:
                units:              Unit count.
                leadTime:           Value of equipment lead time.
                installationTime:   Value of equipment installation time.
                failureRate:        Equipment failure rate.
                d_installationTime: Duration of installation (i.e. weeks, months, years, etc.).
                d_leadTime:         Duration of lead time (i.e. weeks, months, years, etc.).
        """
        markov_params = params.MarkovParameters(leadTime, 
                                                installationTime, 
                                                failureRate,
                                                d_installationTime,
                                                d_leadTime)
        
        installationRate    = markov_params.getInstallationRate()
        replacementRate     = markov_params.getReplacementRate()

        self.__initCalculator(units, installationRate, replacementRate, failureRate)

    def __initCalculator(self, units, installationRate, replacementRate, failureRate):
        """Initializes variable of the markov calculator

            Args:
                units:              Unit count.
                installationRate:   Rate at which equipment is installed (measured yearly).
                replacementRate:    Rate at which equipment is replace (measured yearly).
                failureRate:        Rate at which equipment fails (measured yearly).
        """
        self.a = float(failureRate)
        self.n = int(units)
        self.b = float(replacementRate)
        self.sr = float(installationRate)
        self.__create_transition_matrix()

    def __create_transition_matrix(self):
        """Function for creating transition matrices"""
        self.__create_0spare_transition_matrix(self.n, self.a, self.sr, self.b)
        self.__create_1spare_transition_matrix(self.n, self.a, self.sr, self.b)
        self.__create_2spare_transition_matrix(self.n, self.a, self.sr, self.b)

    def __create_0spare_transition_matrix(self, n, a, sr, b):
        """Creates transition matrix for markov model with 0 spares
            
            Args:
                n:  Unit count
                a:  Equipment failure rate
                sr: Installation rate
                b:  Replacement rate
        """
        self.matrix_0Spare = np.array((  [1-n*a,n*a,0,0,0,0],
                                        [0,1-a*n-a,b,n*a-a,0,0],
                                        [sr,0,1-sr-n*a-a,0,n*a-a,0],
                                        [0,0,0,1-2*b,2*b,0],
                                        [0,sr,0,0,1-sr-b,0],
                                        [0,0,sr,0,0,1-sr]
                                    ), dtype=float)

    def __create_1spare_transition_matrix(self, n, a, sr, b):
        """Creates transition matrix for markov model with 1 spare
            
            Args:
                n:  Unit count
                a:  Equipment failure rate
                sr: Installation rate
                b:  Replacement rate
        """
        self.matrix_1Spare = np.array((  [1-(n*a),0,0,n*a,0,0,0,0,0],
                                        [b,1-(n*a)-b,0,0,n*a,0,0,0,0],
                                        [sr,0,1-sr-(n-1)*a,0,0,0,(n-1)*a,0,0],
                                        [0,sr,b,1-sr-b-(n-1)*a,0,0,0,(n-1)*a,0],
                                        [0,0,0,2*b,1-2*b-(n-1)*a,0,0,0,(n-1)*a],
                                        [0,0,sr,0,0,1-sr,0,0,0],
                                        [0,0,0,sr,0,b,1-sr-b,0,0],
                                        [0,0,0,0,sr,0,2*b,1-sr-2*b,0],
                                        [0,0,0,0,0,0,0,3*b,1-3*b]
                                    ), dtype=float)
    
    def __create_2spare_transition_matrix(self, n, a, sr, b):
        """Creates transition matrix for markov model with 2 spares
            
            Args:
                n:  Unit count
                a:  Equipment failure rate
                sr: Installation rate
                b:  Replacement rate
        """
        self.matrix_2Spare = np.array(([1-n*a,0,0,0,n*a,0,0,0,0,0,0,0],
                                        [b,1-b-n*a,0,0,0,n*a,0,0,0,0,0,0],
                                        [0,2*b,1-2*b-n*a,0,0,0,n*a,0,0,0,0,0],
                                        [sr,0,0,1-sr-(n-1)*a,0,0,0,0,(n-1)*a,0,0,0],
                                        [0,sr,0,b,1-sr-b-(n-1)*a,0,0,0,0,(n-1)*a,0,0],
                                        [0,0,sr,0,2*b,1-sr-2*b-(n-1)*a,0,0,0,0,(n-1)*a,0],
                                        [0,0,0,0,0,3*b,1-3*b-(n-1)*a,0,0,0,0,(n-1)*a],
                                        [0,0,0,sr,0,0,0,1-sr,0,0,0,0],
                                        [0,0,0,0,sr,0,0,b,1-sr-b,0,0,0],
                                        [0,0,0,0,0,sr,0,0,2*b,1-sr-2*b,0,0],
                                        [0,0,0,0,0,0,sr,0,0,3*b,1-sr-3*b,0],
                                        [0,0,0,0,0,0,0,0,0,0,4*b,1-4*b]), dtype = float)

    #TODO Add transition matrices for 3 and 4 spares.


    def get_0spare_transition_matrix(self):
        return self.matrix_0Spare

    def get_1spare_transition_matrix(self):
        return self.matrix_1Spare

    def get_2spare_transition_matrix(self):
        return self.matrix_2Spare

    def calculate_steadyState(self, transitionMatrix):
        """Function for calculating the steady state probability from the markov
           transition matrix.

           Args:
                transition_matrix:  Markov model transition matrix

           Returns:
                calculated steady state matrix of the input transition matrix
        """
        mc = markovChain(transitionMatrix)
        mc.computePi('linear')
        return mc.pi

    def calculate_groupProbability(self, steadyState_matrix, spare_count):
        """Function to calculate the group probability of the steady state matrix
            depending on the spare count.
            
            Args:
                steadState_matrix:      Markov model steady state matrix
                spare_count:            Spare count for the required probabilities

            Returns:
                group probability for each contingency level based on the number
                of spares
        """
        if int(spare_count) == 0:
            return round(np.sum(steadyState_matrix[:1]),3), round(np.sum(steadyState_matrix[:3]),3), round(np.sum(steadyState_matrix),3)

        elif int(spare_count) == 1:
            return round(np.sum(steadyState_matrix[:2]),3), round(np.sum(steadyState_matrix[:5]),3), round(np.sum(steadyState_matrix),3)

        else:
            return round(np.sum(steadyState_matrix[:3]),3), round(np.sum(steadyState_matrix[:8]),3), round(np.sum(steadyState_matrix),3)