import matplotlib.pyplot as plt


class SimModel:
    # abstract class to be overridden by the simulation model to optimize
    def __init__(self):
        pass

    def get_obj_value(self, x):
        """ abstract method to return one realization of the objective function to optimize """
        raise NotImplementedError("This is an abstract method and needs to be implemented in derived classes.")


class StepSize:
    # step size: a/i where a>0 and i>=0 is the iteration of the optimization algorithm
    def __init__(self, a):
        self._a = a

    def get_value(self, i):
        return self._a/(i+1)


class StochasticApproximation:
    # stochastic approximation algorithm

    def __init__(self, sim_model, step_size, derivative_step):
        """
        :param sim_model: the simulation model to optimize
        :param step_size: the step size rule
        :param derivative_step: derivative step if calculating slopes
        """
        self._simModel = sim_model
        self._stepSize = step_size
        self._derivativeStep = derivative_step
        self._xStar = None
        self._fStar = None

        self._is = []
        self._xs = []
        self._fs = []

    def minimize(self, max_itr, x0):
        """
        :param max_itr: maximum iteration to terminate the algorithm
        :param x0: starting point
        :return:
        """

        x = x0
        f = self._simModel.get_obj_value(x)

        self._is.append(0)
        self._xs.append(x)
        self._fs.append(f)

        for i in range(1, max_itr):
            # estimate the derivative at x
            derivative = (self._simModel.get_obj_value(x+self._derivativeStep) - f)/self._derivativeStep
            # find a new x
            x = x - self._stepSize.get_value(i)*derivative
            # evaluate the model at x
            f = self._simModel.get_obj_value(x)

            self._is.append(i)
            self._xs.append(x)
            self._fs.append(f)

        # store the optimal x and optimal objective value
        self._xStar = x
        self._fStar = f

    def plot_fs(self, yStar=None):

        fig, ax = plt.subplots(figsize=(6, 5))
        ax.plot(self._is, self._fs)

        plt.xlabel('Iteration')
        plt.ylabel('Objective Function')
        if yStar is not None:
            plt.axhline(y=yStar, linestyle='--', color='black', linewidth=1)
        plt.show()

    def plot_xs(self, xStar=None):

        fig, ax = plt.subplots(figsize=(6, 5))
        ax.plot(self._is, self._xs)

        plt.xlabel('Iteration')
        plt.ylabel('x')
        if xStar is not None:
            plt.axhline(y=xStar, linestyle='--', color='black', linewidth=1)
        plt.show()