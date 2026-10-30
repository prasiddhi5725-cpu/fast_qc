import argparse
import plot
from plot import plot_position_mean,plot_read_lengths

def main():
    parser=argparse.ArgumentParser(description="Upload a file in .fastq format.")
    parser.add_argument("-i","--input",required=True,help="Input a file in fastq format")
    parser.add_argument("-t","--threshold",type=int, help="Choose the quality threshold for you file", default=20)
    parser.add_argument("-o","--output",default="filtered.fastq", help="Output file")

    args=parser.parse_args()
    uploaded_file=args.input
    quality_threshold=args.threshold
    output_file=args.output

    line_number,total_bases,n_count,total_score,gc_count,read_length_list,read_gc_list,passed_reads,low_quality_reads,q_20,q_30,position_total,position_count,correct_file=process_file(uploaded_file,quality_threshold,output_file)
    if correct_file:
        print_report(line_number,total_bases,n_count,total_score,gc_count,read_length_list,read_gc_list,quality_threshold,passed_reads,low_quality_reads,q_20,q_30,position_total,position_count)
        means=list(position_mean(position_total,position_count))
        positions=list(range(1,len(means)+1))
        plot_position_mean(positions,means,"quality_plot.png")
        plot_read_lengths(read_length_list,"read_length_plot.png")

    if not correct_file:
        print("Warning!! filtered.fastq is incomplete.")

def process_file(filename,quality_threshold,output_file):

    line_number=0
    correct_file=True
    total_bases=0
    n_count=0
    read_length_list=[]
    gc_count=0
    total_score=0

    low_quality_reads=0
    passed_reads=0

    q_20=0
    q_30=0

    read_gc_list=[]

    position_total=[]
    position_count=[]

    with open(filename) as open_file, open(output_file,"w") as out_file:
        for line in open_file:
            line=line.strip()
            
            if line=="":
                continue

            if line_number % 4==0:
                header=line

            elif line_number % 4==1:
                original_sequence=line
                sequence=line.upper()
                read_length=len(sequence)
                read_n=sequence.count("N")
                read_gc, read_identified=calculate_gc(sequence)

                read_gc_percentage=gc_percentage(read_gc,read_identified)

                total_bases+=read_length
                n_count+=read_n
                
                read_length_list.append(read_length)
                gc_count+=read_gc
        
            elif line_number % 4==2:
                plus=line

            elif line_number % 4==3:
                quality_score=line
                read_number=line_number//4 + 1

                error_validity=validity(header,sequence,plus,quality_score)
                
                if error_validity!="":
                    print("Read",read_number,":",error_validity)
                    correct_file=False
                    break

                individual_score=0
                position=0

                scores=decode_quality(quality_score)
                for score in scores:
                    individual_score+=score
                    total_score+=score

                    if score>=20:
                        q_20+=1
                    if score>=30:
                        q_30+=1

                    if position==len(position_total):
                        position_total.append(0)
                        position_count.append(0)

                    position_total[position]+=score
                    position_count[position]+=1
                    position+=1
                    
                mean_individual_score=individual_score/len(quality_score)

                if mean_individual_score<quality_threshold:
                    low_quality_reads+=1
                else:
                    passed_reads+=1
                    out_file.write(header + "\n")
                    out_file.write(original_sequence + "\n")
                    out_file.write(plus +"\n")
                    out_file.write(quality_score + "\n")

                print("Mean quality of read",read_number,":",round(mean_individual_score,2))
                print("GC % for read",read_number,"is: ",read_gc_percentage)

                read_gc_list.append(read_gc_percentage)

            line_number+=1
    
    if correct_file and line_number==0:
        print("The file is empty.")
        correct_file=False

    if correct_file and line_number%4!=0:
        print("The number of lines is not a multiple of 4.")
        correct_file=False

    return line_number,total_bases,n_count,total_score,gc_count,read_length_list,read_gc_list,passed_reads,low_quality_reads,q_20,q_30,position_total,position_count,correct_file

def calculate_gc(sequence):
    gc=sequence.count("G")+sequence.count("C")
    identified=len(sequence)-sequence.count("N")
    return gc,identified
def gc_percentage(gc,identified):
    if identified!=0:
        return (gc/identified)*100
    else:
        return 0
 
def decode_quality(quality):
    scores=[]
    for char in quality:
        scores.append(ord(char)-33)
    return scores

def validity(header,sequence,plus,quality_score):
    if not header.startswith ("@"):
        return "Header must start with @ ."
    if not plus.startswith("+"):
        return "Third line must start with + ."
    if len(sequence)!=sequence.count("A")+sequence.count("T")+sequence.count("G")+sequence.count("C")+sequence.count("N"):
        return "The sequence contains invalid characters ."
    if len(sequence)!=len(quality_score):
        return "Sequence and quality lengths differ ."
    return ""

def position_mean(position_total,position_count):
    mean=[]
    for i in range(len(position_total)):
        mean.append(round(position_total[i]/position_count[i],2))
    return mean

def print_report(line_number,total_bases,n_count,total_score,gc_count,read_length_list,read_gc_list,quality_threshold,passed_reads,low_quality_reads,q_20,q_30,position_total,position_count):
    total_reads=line_number//4
    actual_bases=total_bases-n_count
    mean_total_score=total_score/total_bases
    print("Mean quality of the file:",round(mean_total_score,2))
    if actual_bases>0:
        file_gc_percentage=(gc_count/actual_bases)*100
        print("GC content is:",round(file_gc_percentage,2),"% .")
    else:
        file_gc_percentage=0
        print("The file contains only unknown bases.")

    for i in range (len(read_length_list)):
        print("Read",i+1,"length:", read_length_list[i])
        
    print("Maximum read length is: ", max(read_length_list))
    print("Minimum read length is: ",min(read_length_list))
    print("The average read length is: ", round(sum(read_length_list)/len(read_length_list),2))

    print("Total number of reads is: ",total_reads)
    print("Total number of bases is: ", total_bases)
    print(n_count," bases were unidentified.")
    print(actual_bases,"bases were identified as nucleotide bases.")
    
    print("Quality threshold: ",quality_threshold)
    print("Reads passed: ",passed_reads)
    print("Reads removed: ",low_quality_reads)
 
    q_20_percentage=(q_20/total_bases)*100
    q_30_percentage=(q_30/total_bases)*100
    print("Bases with Q20 or higher: ", round(q_20_percentage,2),"%")
    print("Bases with Q30 or higher: ", round(q_30_percentage,2),"%")

    minimum_gc=min(read_gc_list)
    maximum_gc=max(read_gc_list)
    average_gc=sum(read_gc_list)/len(read_gc_list)
    print("Minimum GC content: ", round(minimum_gc,2))
    print("Maximum GC content: ", round(maximum_gc,2))
    print("Average GC content: ", round(average_gc,2))

    print("Mean quality per position:")
    means=position_mean(position_total,position_count)
    for i in range (len(means)):
        print("Mean of position",i+1,"is:",means[i])

if  __name__=="__main__":
    main()




