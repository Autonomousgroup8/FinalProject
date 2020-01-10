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
    #print(memes_read)
    memes_split = memes_read.split(";")
    #print(memes_split)
    memes_final = []
    for i in range(len(memes_split)-1):
        temp_meme = []
        temp_split = memes_split[i].split(",")
        temp_meme += [temp_split[0]]
        temp_meme += [temp_split[1]]
        temp_meme += [temp_split[2]]
        memes_final += [temp_meme]
    total_memes = curr_meme + list(set(memes_final)-set(curr_meme))
    write_genome(total_memes)
    return total_memes

