
import optuna

class BaseTuner:
    def __init__(self):
        pass

    def subsample_tune(self, n = 10000):
        """
        This method is good for tuning really big datasets.

        It does an optuna experiment for each
        subsample and then reports the results
        and the statistics (confidence intervals,
        credible intervals, etc.) std dev., etc.
        associated with all of the experiments.

        :return:
        """



class ClassificationTuner:
    def __init__(self):
        pass

class RegressionTuner:
    def __init__(self):
        pass



