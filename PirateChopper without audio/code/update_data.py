def update_data(filename, variable, new_data):
    num = 0
    if(variable=="start_game"):
        num = 0
    elif(variable=="max_level"):
        num = 1
    with open(filename,"r") as file:
        data = file.readlines()
    with open(filename,"w") as file:
        n_data = data[num].split(" = ")
        if num==0:
            n_data[1] = new_data+"\n"
            write_data = list(n_data[0]+" = "+n_data[1]) + data[1:]
        elif num==1:
            n_data[1] = str(new_data)+"\n"
            write_data = list(data[0])+list(n_data[0]+" = "+n_data[1]) + data[2:]
        file.writelines(write_data)
def read_data(filename, variable):
    num = 0
    if(variable=="start_game"):
        num = 0
    elif(variable=="max_level"):
        num = 1
    with open(filename,"r") as file:
        data = file.readlines()
        info = data[num].split(" = ")[1].split("\n")[0]
    return info
# print(read_data("txt1.txt", "max_level"))
