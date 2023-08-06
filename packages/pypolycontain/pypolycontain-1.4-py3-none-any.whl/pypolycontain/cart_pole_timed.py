from __future__ import print_function
import sys
import threading
from time import sleep
try:
    import thread
except ImportError:
    import _thread as thread

from pwa_control.synthesis import affine_system,pwa_system,point_trajectory,polytopic_trajectory

 
    
import numpy as np
import scipy.linalg as spa
import pypolycontain as pp
import pydrake.solvers.mathematicalprogram as MP
import pydrake.solvers.gurobi as Gurobi_drake
# use Gurobi solver
global gurobi_solver, license
gurobi_solver=Gurobi_drake.GurobiSolver()
license = gurobi_solver.AcquireLicense()

import matplotlib.pyplot as plt


dt=0.05
g=10
m=1
M=10
l=1

a=0.1*l
K=200

u_max=100

# state= x, v, theta, w
A=np.array([[1,dt,0,0],[0,1,-m/M*g*dt,0],[0,0,1,dt],[0,0,g/l*(1-m/M)*dt,1]])
B=np.array([0,dt/M,0,-1/M/l*dt]).reshape(4,1)

c=np.array([0,0,0,0]).reshape(4,1)
C=pp.unitbox(N=5).H_polytope
h_contact=np.zeros((1,5))
h_contact[0,0],h_contact[0,2]=1,1
C.H=np.vstack(( C.H , h_contact  ))
C.h=np.array([0.15,1,0.1,  1,  u_max,   0.15,1,0.1,   1,  u_max  , 0.1   ]).reshape(11,1)
S1=affine_system(A,B,c,name='free',XU=C)



# X=pp.zonotope(G=np.array([[0.1,0],[0,1]]))
# U=pp.zonotope(G=np.ones((1,1))*4)
# W=pp.zonotope(G=np.array([[0.1,0],[0,1]]))
# Omega=rci_old(A, B, X, U , W, q=5,eta=0.001)

# import pickle
# (H,h)=pickle.load(open('inner_H.pkl','rb'))
# Omega=pp.H_polytope(H, h)

A=np.array([[1,dt,0,0],[0,1,-m/M*g*dt,0],[0,0,1,dt],[-K*dt,0,g/l*(1-m/M)*dt-K*dt*l,1]])
B=np.array([0,dt/M,0,-1/M/l*dt]).reshape(4,1)

c=np.array([0,0,0,K*a*dt]).reshape(4,1)


C=pp.unitbox(N=5).H_polytope
C.H[2,0]=0
C.H[7,0]=-1
C.h=np.array([0.15,1,0.1,  1,  u_max,   0.15,1,-0.1,   1,  u_max    ]).reshape(10,1)
S2=affine_system(A,B,c,name='contact',XU=C)


myS=pwa_system()   
myS.add_mode(S1)
myS.add_mode(S2)


if True:
    # Synthesis
    start=np.array([0.0,  0.3,  0,    0]).reshape(4,1)
    goal=np.zeros((4,1))
    T=40
    # x,u,mu=point_trajectory(myS,start,T,goal,Q=np.eye(2)*100)
    # try:
    x,u,mu=point_trajectory(myS,start,T,goal,Q=np.eye(4)*100,R=np.eye(1))
    mu[T,'free'],mu[T,'contact']=1,1
    plt.plot( [x[t][0] for t in range(T+1)] , [x[t][2] for t in range(T+1)] )
    plt.plot( [x[t][0] for t in range(T+1) if mu[t,'free']==0] , \
             [x[t][2] for t in range(T) if mu[t,'free']==0],'o',\
             color='red')
    plt.plot( [x[t][0] for t in range(T+1) if mu[t,'free']==1] , \
             [x[t][2] for t in range(T+1) if mu[t,'free']==1],'o',\
             color='blue')
    plt.figure()
    plt.plot( [t for t in range(T+1)] , [x[t][0]+x[t][2] for t in range(T+1)],color='green' )
    plt.plot( [t for t in range(T+1)] , [x[t][0]+x[t][2] for t in range(T+1)],'o',color='purple' )       
        
        
    # for t in range(T+1):
    #     fig,ax=plt.subplots()
    #     thickness=0.02
    #     wall=pp.zonotope(G=np.array([[thickness,0],[0,0.2]]),\
    #                       x=np.array([a+thickness,1]).reshape(2,1)  ,color='black' )
        
    #     x_cart=np.array([x[t][0],0]).reshape(2,1)
    #     cart=pp.zonotope(G=np.eye(2)*0.05,x=x_cart,color='green')
    #     x_pole=np.array([x[t][0]+l*np.sin(x[t][2]),l*np.cos(x[t][2])]).reshape(2,1)
    #     pole=pp.zonotope(G=np.array([[0.008,0],[0,0.025]]),x=x_pole,color='red')
    #     ax.plot( [x_cart[0],x_pole[0]] , [x_cart[1],x_pole[1]]    )
    #     pp.visualize([wall,cart,pole], ax=ax,fig=fig  )
    #     ax.set_xlim([-0.2,0.2])
    #     ax.set_ylim([-0.2,1.2])
        
    # except:
    #     print("nothing to plot")

# raise 1

if False:
    start=np.array([0.05,  0.2,  0,    0]).reshape(4,1)
    goals=[pp.zonotope(G=0.01*np.eye(4))]
    T=20
    x,u,mu,G,theta=polytopic_trajectory(myS, start, T, goals, \
                                        Q=np.eye(4)*1, R=np.eye(1)*1)
    Z={t: pp.zonotope(x=x[t],G=G[t],color=(t/T,1-t/T,0)) for t in range(T+1)}
    F={}
    for t in range(T):
        F[t]=pp.convex_hull(Z[t], Z[t+1])
        F[t].color=(1-t/T,t/T,1)
    fig,ax=plt.subplots()
    mu[T,'free'],mu[T,'contact']=1,1
    ax.plot( [x[t][0] for t in range(T+1)] , [x[t][2] for t in range(T+1)] )
    ax.plot( [x[t][0] for t in range(T+1) if mu[t,'free']==0] , \
             [x[t][2] for t in range(T) if mu[t,'free']==0],'o',\
             color='red')
    ax.plot( [x[t][0] for t in range(T+1) if mu[t,'free']==1] , \
             [x[t][2] for t in range(T+1) if mu[t,'free']==1],'o',\
             color='blue')
    pp.visualize([F[t] for t in range(T)],ax=ax,fig=fig,a=0.01,alpha=0.99,\
                 tuple_of_projection_dimensions=(0,2),equal_axis=True)
    
# raise 1    
xS=x
# raise 1

L=np.array([0.15,0.2,0.15,0.2])
x0=np.random.uniform(-L,L).reshape(4,1)


# try:
#     T=30
#     x,u,mu=point_trajectory(myS,x0,T,np.zeros((2,1)),Q=np.eye(2)*100)
    

def in_the_tree(x,list_of_polytopes):
    for P in list_of_polytopes:
        if np.all(np.dot(P.H,x)<=P.h):
            return True
    return False
    
   
    

    
def quit_function(fn_name):
    # print to stderr, unbuffered in Python 2.
    print('{0} took too long'.format(fn_name), file=sys.stderr)
    sys.stderr.flush() # Python 3 stderr is likely buffered.
    thread.interrupt_main() # raises KeyboardInterrupt

def exit_after(s):
    '''
    use as decorator to exit process if 
    function takes longer than s seconds
    '''
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, quit_function, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer


    
def extend(start,T,list_of_nodes):
    color=(np.random.random(),np.random.random(),np.random.random())
    x,u,mu,G,theta=polytopic_trajectory(myS, start, T, list_of_nodes)
    Z={t: pp.zonotope(x=x[t],G=G[t],color=color) for t in range(T+1)}
    funnel=[None]*T
    H_funnel=[None]*T
    contact_free=True
    for t in range(T):
        if mu[t,"contact"]==1:
            contact_free=False
            break
    if contact_free:
        print("it was contact free!")
        funnel[0]=Z[0]
        for t in range(T):
            funnel[0]=pp.convex_hull(funnel[0], Z[t+1])
        H_funnel=[pp.ray_shooting_hyperplanes(funnel[0],N=500,tol=1e-5)]
        funnel=[funnel[0]]
    else:
        print("Oh it had contact")
        for t in range(T):
            funnel[t]=pp.convex_hull(Z[t], Z[t+1])
            funnel[t].color=color
            H_funnel[t]=pp.ray_shooting_hyperplanes(funnel[t],N=500,tol=1e-5)
    # fig,ax=plt.subplots()
    # mu[T,'free'],mu[T,'contact']=1,1
    # ax.plot( [x[t][0] for t in range(T+1)] , [x[t][2] for t in range(T+1)] )
    # ax.plot( [x[t][0] for t in range(T+1) if mu[t,'free']==0] , \
    #          [x[t][2] for t in range(T) if mu[t,'free']==0],'o',\
    #          color='red')
    # ax.plot( [x[t][0] for t in range(T+1) if mu[t,'free']==1] , \
    #          [x[t][2] for t in range(T+1) if mu[t,'free']==1],'o',\
    #          color='blue')
    # pp.visualize([Omega]+[funnel[t] for t in range(T)],ax=ax,fig=fig,a=0.01,alpha=0.99,tuple_of_projection_dimensions=(0,2))
    return funnel,H_funnel,x,mu,G   


    
    
  

def sampler(i):
    L=np.array([0.15,1,0.15,1])
    if np.random.random()<0.4:
        return xS[np.random.randint(0,T)].reshape(4,1)
    else:
        return np.random.uniform(-L,L).reshape(4,1)    
    
T_synthesis=10
Omega=0.005*pp.unitbox(4).H_polytope
list_of_H_polytopes=[Omega]
list_of_nodes=[Omega]
list_of_all_nodes=[Omega]
stop_sampling=False
sample=lambda i:sampler(i)
branch=0
trajectory={}
for i in range(20):
    print("i:",i)
    while not stop_sampling:
        x0=sample(i)
        flag=in_the_tree(x0,list_of_H_polytopes)
        # flag=False
        stop_sampling=not flag
    try:
        print("sample:",x0.T)
        plt.plot(x0[0,0],x0[1,0],'o')
        x,u,mu=point_trajectory(myS,x0,T=30,goal=Omega,Q=np.eye(4)*0,R=np.eye(1)*0) 
        Y,YY,xx,mumu,G=extend(x0,T_synthesis,list_of_nodes)
        trajectory[branch]=(x,u,mu,xx,mumu,G)
        # Y,YY=extend(x0,T,[Omega])
        list_of_nodes.extend(Y[0:min(2,len(Y))])
        list_of_all_nodes.extend(Y)
        list_of_H_polytopes.extend(YY)
        branch+=1
    except:
        print('failed to extend')
    stop_sampling=False
        
fig,ax=plt.subplots()
pp.visualize([Omega]+list_of_all_nodes,a=0.01,ax=ax,fig=fig,tuple_of_projection_dimensions=(0,2),\
             title='Hybrid MPC Feasible Set')
ax.plot([1,-1],[-0.9,1.1]) 
ax.set_xlim([-0.17,0.17])
ax.set_ylim([-0.15,0.15])

    # Synthesis
ax.plot( [xS[t][0] for t in range(T+1)] , [xS[t][2] for t in range(T+1)] ,color='red')
ax.plot( [xS[t][0] for t in range(T+1)] , \
         [xS[t][2] for t in range(T+1)],'o',\
         color='red')

slicer=pp.unitbox(4).H_polytope    
slicer.h[1,0],slicer.h[3,0],slicer.h[5,0],slicer.h[7,0]=0.01,0.01,0.01,0.01

sliced=[pp.intersection(Q,slicer) for Q in list_of_all_nodes]
fig,ax=plt.subplots()
# for Q in sliced:
#        print( pp.check_non_empty(Q))
pp.visualize([Omega]+[Q for Q in sliced if pp.check_non_empty(Q)],\
             a=0.01,ax=ax,fig=fig,tuple_of_projection_dimensions=(0,2),\
                 title='Hybrid MPC Feasible Set')
        
ax.plot([1,-1],[-0.9,1.1]) 
ax.set_xlim([-0.17,0.17])
ax.set_ylim([-0.15,0.15])
    

raise 1
# pp.visualize([Omega]+list_of_H_polytopes,a=0.01)        

Trials=200
covered=0
false_positive=0
feasible=0
for N in range(Trials):
    x0=sample(N)
    print(N)
    try:
        x,u,mu=point_trajectory(myS,x0,T=40,goal=np.zeros((4,1)),Q=np.eye(4)*1)
        feasible+=1
        covered+=in_the_tree(x0,list_of_H_polytopes)
    except:
        false_positive+=in_the_tree(x0,list_of_H_polytopes)
print("feasible: %d    covered: %d"%(feasible,covered)) 
print("infeasible: %d    false positive: %d"%(Trials-feasible,false_positive)) 
raise 1
    
# x0=np.array([  0.105   ,   0.4]).reshape(2,1)
T=20
list_of_nodes=[Omega]
print(x0, in_the_tree(x0,list_of_nodes))
raise 1

Y,YY=extend(x0,T,list_of_nodes)


if True:
    # Synthesis
    start=np.array([ 0.11893429,0.28665095]).reshape(2,1)
    goal=np.zeros((2,1))
    T=2
    
    # x,u,mu=point_trajectory(myS,start,T,goal,Q=np.eye(2)*100)
    try:
        x,u,mu=point_trajectory(myS,start,T,goal,Q=np.eye(2)*100)
        mu[T,'free'],mu[T,'contact']=1,1
        plt.plot( [x[t][0] for t in range(T+1)] , [x[t][1] for t in range(T+1)] )
        plt.plot( [x[t][0] for t in range(T+1) if mu[t,'free']==0] , \
                 [x[t][1] for t in range(T) if mu[t,'free']==0],'o',\
                 color='red')
        plt.plot( [x[t][0] for t in range(T+1) if mu[t,'free']==1] , \
                 [x[t][1] for t in range(T+1) if mu[t,'free']==1],'o',\
                 color='blue')
            
        # V=[x[t].reshape(2,1) for t in range(T)]+[-x[t].reshape(2,1) for t in range(T)]
        # Set=pp.V_polytope(V)
        # pp.visualize([Set])
    except:
        print("nothing to plot")
        
elif True:
    start=np.array([  0.05   ,   0.7]).reshape(2,1)
    goals=[Omega]
    T=20
    x,u,mu,G,theta=polytopic_trajectory(myS, start, T, goals, \
                                        Q=np.eye(2)*0.01, R=np.eye(1)*0.01)
    Z={t: pp.zonotope(x=x[t],G=G[t],color=(t/T,1-t/T,0)) for t in range(T+1)}
    F={}
    for t in range(T):
        F[t]=pp.convex_hull(Z[t], Z[t+1])
        F[t].color=(1-t/T,t/T,1)
    fig,ax=plt.subplots()
    mu[T,'free'],mu[T,'contact']=1,1
    ax.plot( [x[t][0] for t in range(T+1)] , [x[t][1] for t in range(T+1)] )
    ax.plot( [x[t][0] for t in range(T+1) if mu[t,'free']==0] , \
             [x[t][1] for t in range(T) if mu[t,'free']==0],'o',\
             color='red')
    ax.plot( [x[t][0] for t in range(T+1) if mu[t,'free']==1] , \
             [x[t][1] for t in range(T+1) if mu[t,'free']==1],'o',\
             color='blue')
    pp.visualize([Omega]+[F[t] for t in range(T)],ax=ax,fig=fig,a=0.01,alpha=0.99)