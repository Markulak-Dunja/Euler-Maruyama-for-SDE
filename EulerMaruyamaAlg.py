import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sympy import symbols, exp, sqrt, integrate, Function
from sympy.stats import E
from scipy.integrate import quad
np.random.seed(42)

class SDJ:
    def __init__(self, X0, mu, sigma,theta,sdj):
        self.X0 = X0
        self.mu = mu
        self.sigma = sigma
        self.theta = theta
        self.name = sdj

    def Model(self,y):
        # elementi za SDJ Geometrijskog Brownovog gibanja 
        if self.name=="GBG":
            return (self.mu * y, self.sigma * y)
            
        # elementi za SDJ Ornstein–Uhlenbeck procesa 
        elif self.name == "OU":
            return(self.theta * (self.mu - y), self.sigma)
        

    # funkcija za egzaktno rješavanje SDJ Geometrijskog Brownovog gibanja 
    # #(za OU proces nije efikasno koristiti i egaktno rješenje)
    def Exact(self,t,dB):
        if self.name == "GBG":
            B = np.cumsum(dB)
            return (self.X0 * np.exp((self.mu - 0.5 * self.sigma**2) * t + B * self.sigma))
        else:
            pass
            '''B = np.cumsum(dB)
            s = symbols('s')
            res, _ = quad(np.exp(self.theta * s) * BG(dt, N),0,t)
            return (self.mu + exp(-self.theta * t)*(self.X0-self.mu)+ self.sigma*sqrt(2*self.sigma)*res)
            '''

    # Iterativni postupak Euler Maruyama metode
    def EM(self,N,dt,dB):
        XEm,X = [],self.X0
        for i in range (N):
            a, b = self.Model(X)
            X += a*dt + b*dB[i]
            XEm.append(X)
        return XEm

# generiranje Brownovog gibanja
def BG(dt,N):
    return (np.sqrt(dt) * np.random.randn(N))


def plotExEm(N,dt,S,ex,paths):
    fig, ax = plt.subplots();ax.grid()

    for i in range (paths):
        dB = BG(dt,N)
        XEm = S.EM(N,dt,dB)
        t = np.arange(0,1,dt)
        if ex:
            Exact = S.Exact(t,dB)
            plt.plot(t,Exact, label = "Exact ($X_t$)", color = 'b')
        plt.plot(t,XEm,label="EM ($X_t$)")
        if S.name == "GBG":
            plt.title("Geometrijsko Brownovo gibanje")

        else:
            plt.title("Ornstein-Uhlenbeck proces")
        plt.xlabel("vrijeme")
    plt.show()

def plotMoreEMInOne(N,dt,S,ex):
    np.random.seed(42)
    figure, axis = plt.subplots(2, 2)
    N = 1000
    d= np.random.randn(N)
    dt = 1/N
    dB = (np.sqrt(dt) * d)
    t = np.arange(0,1,dt)
    if ex:
        Exact = S.Exact(t,dB)
        axis[0,0].plot(t,Exact, label = "Exact ($X_t$)", color = 'b')
        axis[0,1].plot(t,Exact, label = "Exact ($X_t$)", color = 'b')
        axis[1,1].plot(t,Exact, label = "Exact ($X_t$)", color = 'b')
        axis[1,0].plot(t,Exact, label = "Exact ($X_t$)", color = 'b')


    N = 10
    d= np.random.randn(N)
    dt = 1/N
    t = np.arange(0,1,dt)
    XEm = S.EM(N,dt,dB)

    axis[0,0].plot(t,XEm,label="EM ($X_t$)", ls = '--',color = 'm')
    axis[0, 0].set_title("Simulacija s N = 10")


    N = 100
    dt = 1/N
    t = np.arange(0,1,dt)
    XEm = S.EM(N,dt,dB)
    t = np.arange(0,1,dt)
    axis[0,1].plot(t,XEm,label="EM ($X_t$)", ls = '--',color = 'm')
    axis[0,1].set_title("Simulacija s N = 100")

    N = 500
    dt = 1/N
    XEm = S.EM(N,dt,dB)
    t = np.arange(0,1,dt)
    axis[1,0].plot(t,XEm,label="EM ($X_t$)", ls = '--',color = 'm')
    axis[1, 0].set_title("Simulacija s N = 500")


    N = 1000
    dt = 1/N
    XEm = S.EM(N,dt,dB)
    t = np.arange(0,1,dt)
    axis[1,1].plot(t,XEm,label="EM ($X_t$)", ls = '--',color = 'm')
    axis[1, 1].set_title("Simulacija s N = 1000")
    plt.show()
    
def errorCalc(S,N,m):
#inicijaliziramo listu errora i dtGrid
    strongError, weakError = [], []
    dt_grid = [2 ** (R-10) for R in range(7)]
    numberOfSample = 1000
    # ponavljajmo po dt
    for dt in dt_grid: 
        t = np.arange(dt, 1 + dt, dt)
        N = len(t)
        # Initiate vectors to store errors and time series
        eulerError = np.zeros(N)
        YSum, XEmSum  = np.zeros(N), np.zeros(N)

        # generiramo 10000 uzoraka
        for i in range(m):
            dB = BG(dt,N)
            B = np.cumsum(dB)

            Y = S.Exact(t,dB)

            Xem = S.EM(N,dt,dB)

            # Računanje apsolutne pogreške 
            # i dodavanje onima iz prijašnjih uzoraka   
            eulerError  += abs(Y - Xem)
            
            # Dodamo Y,X onima iz prijašnjih uzoraka
            YSum += Y
            XEmSum += Xem

        # računamo maksimum prosjeka -> jaka konvergencija
        strongError.append(max(eulerError / numberOfSample))
        # računamo maksimum pogreške prosjeka -> slaba konvergencija 
        weakError.append(max(abs(YSum - XEmSum)/numberOfSample))
    # Primjenjujemo funkciju OLS na prijašnju simulaciju
    X = sm.add_constant(np.log(dt_grid))
    resultsS = sm.OLS(np.log(strongError),X).fit()
    resultsW = sm.OLS(np.log(weakError),X).fit()

    return(dt_grid,weakError,strongError,resultsS,resultsW)



def plotAprox(S,N):
    
    dt_grid,weakError,strongError, resultsS,resultsW = errorCalc(S,N,1000)

    plt.loglog(dt_grid, strongError, label="Jaka konvergencija",color='mediumvioletred')
    plt.loglog(dt_grid, weakError, label="Slaba konvergencija",color='lightseagreen',ls='--')
    plt.title('Konvergencija Euler-Maruyama metode')
    plt.xlabel('$dt$'); plt.ylabel('Pogreška'); plt.legend(loc=2)
    plt.show()

    print("\n Red Jake konvergencije EM metode      "+ str(resultsS.params[1]))

    print(" Red Slabe konvergencije EM metode     "+ str(resultsW.params[1]))

            

if __name__ == "__main__":

    T = 1.0
    N = 10000
    dt = T/N
    paths = 10
    gbg1 = SDJ(1,1.5,1,0,"GBG")
    gbg2 = SDJ(1,2,1,0,"GBG")

    ou = SDJ(2,0.5,3,0.5,"OU")
    ou2 = SDJ(3,10,-5,5,"OU")

    #plotAprox(gbg1,N)
    #plotExEm(N,dt,gbg2,False,1)

    #plotExEm(N,dt,ou2,False,1)
    plotMoreEMInOne(N,dt,gbg1,True)
    #plotAprox(gbg2,N)