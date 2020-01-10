def write_genome(memes):
    f = open("MemeStorage.txt","w")
    for i in range(len(memes)):
        f.write(str(memes[i][0]))
        f.write(",")
        f.write(str(memes[i][1]))
        f.write(",")
        f.write(str(memes[i][2]))
        f.write(";")
    f.close
    #print("Memes saved in MemeStorage.txt")

def read_genome(curr_meme):
    f = open("MemeStorage.txt","r")
    memes_read = f.read()
    f.close()
    memes_split = memes_read.split(";")
    memes_final = []
    for i in range(len(memes_split)-1):
        temp_meme = []
        temp_split = memes_split[i].split(",")
        temp_meme += [temp_split[0]]
        temp_meme += [temp_split[1]]
        temp_meme += [temp_split[2]]
        memes_final += [temp_meme]

    memes_final += curr_meme
    new_list = []
    for elem in memes_final:
        if elem not in new_list:
            new_list += [elem]



    write_genome(memes_final)
    return memes_final

