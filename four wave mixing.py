import qutip as qt
import matplotlib.pyplot as pl
import matplotlib as mpl
import numpy as np


def exp_t(t, args):
    return np.exp(1j * t * args['w_r'])

N = 20
wa = 2
wr = 2
kappar = 0.5
drive = 1
a = qt.tensor(qt.destroy(N), qt.qeye(N))
r = qt.tensor(qt.qeye(N), qt.destroy(N))
    
    
if 1:
    chiaa = 0
    chirr = 0
    g = 1
    psi0 =  (qt.tensor(qt.coherent(N, 0), qt.coherent(N,0))).unit()
    opts = qt.Options(store_states=True, nsteps=100000)
    num_steps=5
    times = np.linspace(0.0, 5, num_steps)
    xvec =  np.linspace(-5, 5, 51)

    args = {'w_r':wr}
    H = [wa*a.dag()*a + wr*r.dag()*r + chirr*r.dag()**2*r**2 + chiaa*a.dag()**2*a**2 
         + g*(r.dag()*a**2+r*a.dag()**2),
        [drive*(r.dag()+r), exp_t]]   
    result = qt.mesolve(H, psi0, times, kappar*r, [], options=opts, progress_bar = True,
                        args=args)
   
    fig = pl.figure(figsize=(2 * num_steps, 4))
    for i in range(num_steps):
        pl.subplot(2, num_steps, i+1)
        W1 = qt.wigner((result.states[i].ptrace(0)).unit(), xvec, xvec) 
        pl.contourf(xvec, xvec, W1, np.linspace(-1, 1, 41, endpoint=True), cmap=mpl.cm.RdBu_r)
        pl.subplot(2, num_steps, i+1 + num_steps)
        W2 = qt.wigner((result.states[i].ptrace(1)).unit(), xvec, xvec)
        pl.contourf(xvec, xvec, W2, np.linspace(-1, 1, 41, endpoint=True), cmap=mpl.cm.RdBu_r)

    

