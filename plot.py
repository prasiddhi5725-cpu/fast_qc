import matplotlib.pyplot as plt

def plot_position_mean(x,y,filename):
    plt.figure(figsize=(9,5))
    plt.plot(x,y,color="steelblue",linewidth=2,label="Mean quality")
    plt.title("Mean quality per position",fontsize=14)
    plt.axhline(y=20,color="red",linestyle="--",label="Q20")
    plt.axhline(y=30,color="green",linestyle="--",label="Q30")
    plt.xlabel("Read")
    plt.ylabel("Mean quality score (Phred)")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename,dpi=150)
    plt.close()

def plot_read_lengths(y,filename):
    plt.figure(figsize=(9,5))
    plt.hist(y, bins=range(min(y),max(y)+2),color="steelblue",edgecolor="white")
    plt.yscale("log")
    plt.title("Read length distribution",fontsize=14)
    plt.xlabel("Read length")
    plt.ylabel("Number of reads (log scale)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename,dpi=150)
    plt.close()

def plot_gc_percentage(y,filename):
    plt.figure(figsize=(9,5))
    plt.hist(y,bins=range(0,101,2),color="steelblue",edgecolor="white")
    plt.xlim(0,100)
    plt.title("GC content per read",fontsize=14)
    plt.xlabel("GC content (%)")
    plt.ylabel("Number of reads")
    plt.tight_layout()
    plt.savefig(filename,dpi=150)
    plt.close()
    

