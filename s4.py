file = open("students.txt","w")

file.write("Hana\n")
file.write("lara\n")
file.write("noman\n")

file.close()


with open("students.txt","r") as file:
    print(file.read)


file = open("students.txt" , "a")
file.write("nomj\n")
file.close()

file = open("students.txt","r")
data = (file.read())
print(data)
file.close()