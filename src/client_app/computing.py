
from numpy import *
#from math import *    ##we can use numpy or math

def solve_simple_problem(p1,p2,p3,p4,p5):
    return p1+p2+p3+p4+p5

def solve_problem(p1,p2,p3,p4,p5):
    '''solve the function with Newton's method
    '''
    def f(x):
        return p1*sin(p2*x)-p3-p4*exp(int(p5)*x)

    def df(x):
        return p1*p2*cos(p2*x)-p4*p5*exp((p5*x))
    
    tolerance=.0000001
    
    x=2*pi
    while x>=0:
        x1 = x - f(x)/df(x)
        t = abs(x1 - x)
        if t < tolerance:
            break
        x = x1
   
    if x==0 or x<0:
        print('can not find the approx. answer')
        return None
    else:
        return x
###############################test
#7.12530535898?1.7841188001?-0.676578247777?0.625368322208?1.17482593761
#1.57335759382
# p1=7.12530535898
# p2=1.784118800
# p3=-0.676578247777
# p4=0.625368322208
# p5=1.17482593761
# # 
# a=solve_problem(p1,p2,p3,p4,p5)
# print(a)   