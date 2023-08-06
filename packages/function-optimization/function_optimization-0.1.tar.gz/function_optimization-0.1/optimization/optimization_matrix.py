from scipy.misc import derivative
import matplotlib.pyplot as plt

class Optimization_function:
    def __init__(self,formula,init_value = 0,rate = 0.1,
    max_iter = 200 ,epsilon = 0.01, method = 'Newton',show = True,plot = True):
        """Finding optimal solution of the function

        Attributes:
            formula - the function for which we are looking for a solution
            init_value (float): the initial guess where we start to optimize
            rate (float): the learning rate of the optimization,GradientDescent
            max_iter (int): maximum number of iterations
            epsilon (float): benchmark for the error. When to stop the algorithm
            method (str): Method to optimize
            show (Boolean): Print optimization results per every loop
            plot (boolean): show the plot of iterations

        Returns:
            float: minimal value of the function
        """
        self.rate = rate
        self.formula = formula
        self.max_iter = max_iter
        self.method = method
        self.init_value = init_value
        self.epsilon = epsilon
        self.show = show
        self.plot = plot
    def find_derivative(self,point_at,n=1):
        """Function to calculate derivative of the function at the point

        Args:
            point_at (float): the point at which calculate derivative
            n (int): number of the derivative

        Returns:
            float: the value of the derivative
        """
        derivative_value = derivative(self.formula, point_at, dx=1e-6 , n = n)
        return derivative_value
    def plot_iter(self,x,y):
        """Function to plot the data

        Args:
            x - data for X axis
            y - data for Y axis

        Returns:
            None
        """

        plt.plot(x, y, ls='--')
        plt.xlabel('Iterations')
        plt.ylabel('Value')
        plt.title('Optimization')
        plt.show()

    def optimize(self):
        """Function to calculate the minimum of the Function

        Args:
            None

        Returns:
            float: the minimal value of the function

        """
        Xn = self.init_value
        iter = []
        values = []

        #Check existent methods
        if self.method not in ('Newton','GradientDescent'):
            print('Method is not on the list yet')
            return None


        for i in range(0,self.max_iter):
            #Calculate value of the function at the point
            F_xn = self.formula(Xn)
            iter.append(i)
            values.append(F_xn)

            #Calculate derivatives at the point
            D_xn = self.find_derivative(Xn)
            D_second_xn = self.find_derivative(Xn,n=2)
            if D_xn == 0 and self.method == 'Newton':
                print('Derivative zero.')
                result = None
                break

            #Update the point
            if self.method == 'Newton':
                X_new = Xn - D_xn / D_second_xn
            else:
                X_new = Xn - D_xn * self.rate

            #Check converged
            if abs(X_new - Xn) < self.epsilon :
                print('Solution was found after {} interations'.format(i))
                result = Xn
                break

            #Assign new point
            Xn = X_new

            #Print number of the iteration and function value at this iteration
            if self.show:
                print('For iteration number {} , for x: {} ,value is {}'.format(i,Xn,F_xn))

        #Plot the values and interations
        if self.plot:
            self.plot_iter(iter,values)

        return result
