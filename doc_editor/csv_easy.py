import csv 

the_file=open(r"D:\jadi_py_dore\practises/1741502118270796.csv")
csv_reader=csv.reader(the_file)
outfile= open(r"D:\jadi_py_dore\practises/out.csv",mode="w",newline='')
csv_write=csv.writer(outfile,delimiter=',')
csv_write.writerow(["Product Name","Price","Quantity","sum"])

next(csv_reader)
for row in csv_reader:
    if row :
        name,price,tedad=row
        sum=int(price)*int(tedad)
        csv_write.writerow([name,price,tedad,sum])
