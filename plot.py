import matplotlib.pyplot as plt

def plot_position_mean(x,y,filename):
    plt.plot(x,y)
    plt.title("Mean quality per position")
    plt.axhline(y=20,color="red",linestyle="--",label="Q20")
    plt.axhline(y=30,color="green",linestyle="--",label="Q30")
    plt.xlabel("Position")
    plt.ylabel("Mean quality score (Phred)")
    plt.legend()
    plt.savefig(filename)
    plt.close()

def plot_read_lengths(y,filename):
    plt.hist(y, bins=range(min(y),max(y)+2))
    plt.title("Read length Distribution")
    plt.xlabel("Read length")
    plt.ylabel("Number of reads having read length")
    plt.savefig(filename)
    plt.close()

def plot_gc_percentage(y,filename):
    plt.hist(y,bins=range(0,101,2))
    plt.title("GC content per read")
    plt.xlabel("GC content (%)")
    plt.ylabel("Number of reads")
    plt.savefig(filename)
    plt.close
    

