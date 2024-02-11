with open("txt1.txt", "r") as file:
    x = file.readlines()
with open("txt1.txt","w") as file:
    y = x[1].split(" = ")
    y[1] = "4\n"
    n_data = list(y[0]+" = "+y[1])
    print(type(x[0]), type(n_data), type(x[2:]))
    all_data = list(x[0]) + n_data + x[2:]
    file.writelines(all_data)
with open("txt1.txt", "r") as file:
    x = file.readlines()
print(x)
