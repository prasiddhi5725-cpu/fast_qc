uploaded_file=input("Enter the file name (.fastq format): ")
open_file=open(uploaded_file)

line_number=0
for line in open_file:
    line=line.strip()

    if line_number % 4==0:
        header=line

    elif line_number % 4==1:
        sequence=line

    elif line_number % 4==2:
        plus=line

    elif line_number % 4==3:
        quality_score=line

    
        print(header)
        print(sequence)
        print(quality_score)

    line_number+=1



