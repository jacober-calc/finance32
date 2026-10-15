import os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from fin import M, E2, solve
os.makedirs("assets", exist_ok=True)
INK="#1f2933"; GRID="#d9dee3"; BLUE="#2563eb"; ORANGE="#e8702a"; GREEN="#2f9e44"; GREY="#8a949e"; PURPLE="#7048e8"; GOLD="#f2a900"; RED="#c92a2a"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK,"axes.labelcolor":INK,"xtick.color":INK,"ytick.color":INK,
 "text.color":INK,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.color":GRID,"grid.linewidth":0.8,
 "figure.facecolor":"white","axes.facecolor":"white","svg.fonttype":"path","axes.titleweight":"bold","axes.titlesize":13})
PREVIEW=os.environ.get("PREVIEW")
def save(fig,name):
    fig.savefig(f"assets/{name}.svg",bbox_inches="tight",facecolor="white",dpi=200)
    if PREVIEW: fig.savefig(f"/tmp/fn_{name}.png",bbox_inches="tight",facecolor="white",dpi=70)
    plt.close(fig)
def box(ax,x,y,w,h,c,lw=1.8): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=.08",fc="white",ec=c,lw=lw))
money=lambda v,p=0: f"{v:,.{p}f}"

# 1 Program map
fig,ax=plt.subplots(figsize=(10,3.7)); ax.axis("off"); ax.set_xlim(0,10.2); ax.set_ylim(0,3.6)
ax.text(.1,3.45,"Program Map",fontsize=13,fontweight="bold",va="center")
items=[("LBL M","TVM, annual rate","SOLVE N, I, B, P or F","prompts P Y I F N B",BLUE,.1),
       ("Equation 1","TVM, periodic rate","EQN, SOLVE N, I, B, P or F","prompts P I N F B",GREEN,2.6),
       ("Equation 2","Annuity future value","EQN, then XEQ or ENTER","prompts P I N",PURPLE,5.1),
       ("LBL K","Percent of total","total ENTER part, XEQ K","X: part as % of total",ORANGE,7.6)]
for k,t,how,o,c,x0 in items:
    box(ax,x0,1.2,2.35,1.75,c)
    ax.text(x0+1.175,2.6,k,ha="center",fontsize=12.5,fontweight="bold",color=c)
    ax.text(x0+1.175,2.22,t,ha="center",fontsize=10.5)
    ax.text(x0+1.175,1.82,how,ha="center",fontsize=9,color=INK)
    ax.text(x0+1.175,1.45,o,ha="center",fontsize=9,color=GREY)
ax.text(.1,.7,"N periods   I interest rate %   Y payments per year   B present value   P payment   F future value",fontsize=9.5,color=GREY)
ax.text(.1,.25,"Cash received is positive; cash paid out is negative",fontsize=9.5,color=GREY)
save(fig,"program_map")

# 2 Cash-flow diagram, car loan (Example 6.1)
P=float(solve(M,'P',-100,Y=12,I=4.5,F=0,N=48,B=17900))
fig,ax=plt.subplots(figsize=(10,3.9)); ax.grid(False); ax.spines["left"].set_visible(False); ax.set_yticks([])
ax.axhline(0,color=INK,lw=1.4)
ax.annotate("",xy=(0,3.2),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color=GREEN,lw=2.6,mutation_scale=18))
ax.text(0.6,3.0,"B = 17,900\nreceived",color=GREEN,fontsize=10.5,fontweight="bold",va="top")
for n in range(1,49):
    ax.annotate("",xy=(n,-1.25),xytext=(n,0),arrowprops=dict(arrowstyle="-|>",color=RED,lw=1.3,mutation_scale=9))
ax.text(24.5,-1.75,f"48 payments, P = {P:,.2f}",color=RED,fontsize=10.5,fontweight="bold",ha="center",va="top")
ax.text(48.5,0.25,"F = 0",color=GREY,fontsize=10,ha="left")
ax.set_xlim(-1.5,51); ax.set_ylim(-2.6,3.6); ax.set_xticks([0,12,24,36,48]); ax.set_xlabel("Month n")
ax.set_title("Cash Flow from the Borrower's Side: 4.5% Car Loan (Example 6.1)",loc="left"); save(fig,"cash_flow")

# 3 Amortization, mortgage (Example 6.4)
Pm=float(solve(M,'P',-1000,Y=12,I=6.5,F=0,N=360,B=300000))
bal=[300000.0]+[-float(solve(M,'F',0,P=Pm,Y=12,I=6.5,N=k,B=300000)) for k in range(12,361,12)]
yrs=np.arange(1,31); princ=np.array([bal[k-1]-bal[k] for k in yrs]); intr=-Pm*12-princ
fig,(a1,a2)=plt.subplots(2,1,figsize=(10,6.8),sharex=True,gridspec_kw=dict(height_ratios=[1,1]))
a1.plot(range(0,31),[b/1000 for b in bal],color=BLUE,lw=2.4); a1.fill_between(range(0,31),[b/1000 for b in bal],color=BLUE,alpha=.12,lw=0)
a1.plot(10,bal[10]/1000,"o",color=BLUE,ms=8); a1.annotate(f"After 10 years: {money(bal[10])} owed\n(SOLVE F with N = 120)",xy=(10,bal[10]/1000),xytext=(12.5,262),fontsize=10,color=BLUE,arrowprops=dict(arrowstyle="->",color=BLUE))
a1.set_ylabel("Balance ($ thousands)"); a1.set_ylim(0,320)
a1.set_title(f"Amortization: $300,000 at 6.5% for 30 Years, P = {Pm:,.2f} (Example 6.4)",loc="left")
a2.bar(yrs,intr/1000,color=ORANGE,label="Interest"); a2.bar(yrs,princ/1000,bottom=intr/1000,color=GREEN,label="Principal")
a2.set_ylabel("Paid per year ($ thousands)"); a2.set_xlabel("Year"); a2.legend(frameon=False,ncol=2,loc="lower right",bbox_to_anchor=(1,1.0),fontsize=9.5)
a2.set_xlim(0,30.6); fig.tight_layout(); save(fig,"amortization")

# 4 Savings growth (Example 6.6)
ks=np.arange(0,121); F=[0.0]+[float(solve(M,'F',0,P=-200,Y=12,I=5,N=k,B=0)) for k in ks[1:]]
dep=200*ks
fig,ax=plt.subplots(figsize=(10,4.3))
ax.fill_between(ks/12,0,dep/1000,color=BLUE,alpha=.25,lw=0,label="Deposits")
ax.fill_between(ks/12,dep/1000,np.array(F)/1000,color=GOLD,alpha=.35,lw=0,label="Interest earned")
ax.plot(ks/12,np.array(F)/1000,color=INK,lw=2,label="F, future value")
ax.annotate(f"F = {money(F[-1],2)}\n{money(F[-1]-24000,2)} interest",xy=(10,F[-1]/1000),xytext=(5.6,27),fontsize=10,fontweight="bold",arrowprops=dict(arrowstyle="->",color=INK))
ax.set_xlim(0,10.2); ax.set_ylim(0,34); ax.set_xlabel("Years"); ax.set_ylabel("$ thousands"); ax.legend(frameon=False,loc="upper left",fontsize=9.5)
ax.set_title("Saving $200 a Month at 5% (Example 6.6)",loc="left"); save(fig,"savings_growth")

# 5 Payment against rate (Example 6.4 data)
rates=np.linspace(2,10,81); pays=[-float(solve(M,'P',-1000,Y=12,I=r,F=0,N=360,B=300000)) for r in rates]
fig,ax=plt.subplots(figsize=(10,4.2))
ax.plot(rates,pays,color=PURPLE,lw=2.4)
for r in (4,6.5,8):
    p=-float(solve(M,'P',-1000,Y=12,I=r,F=0,N=360,B=300000)); ax.plot(r,p,"o",color=PURPLE,ms=8)
    ax.text(r-0.12,p+70,f"{r:g}%: {money(p,2)}",fontsize=10,color=PURPLE,ha="right")
ax.set_xlabel("Annual interest rate I (%)"); ax.set_ylabel("Monthly payment (−P)"); ax.set_xlim(2,10)
ax.set_title("Monthly Payment on $300,000 over 30 Years",loc="left"); save(fig,"rate_payment")
