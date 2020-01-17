
def genome_protocol(protocol, genome):
    try:
        nummer=protocol
        meme = list(genome)
        if nummer == 2:
            for i in range(100):
                if meme[i] == 'A':
                    meme[i] = 'T'
                elif meme[i] == 'T':
                    meme[i] = 'A'
                elif meme[i] == 'C':
                    meme[i] = 'G'
                elif meme[i] == 'G':
                    meme[i] = 'C'
        elif nummer == 3:
            for i in range(100):
                if meme[i] == 'A':
                    meme[i] = 'C'
                elif meme[i] == 'T':
                    meme[i] = 'G'
                elif meme[i] == 'C':
                    meme[i] = 'A'
                elif meme[i] == 'G':
                    meme[i] = 'T'
        elif nummer == 4:
            for i in range(100):
                if meme[i] == 'A':
                    meme[i] = 'G'
                elif meme[i] == 'T':
                    meme[i] = 'C'
                elif meme[i] == 'C':
                    meme[i] = 'T'
                elif meme[i] == 'G':
                    meme[i] = 'A'
        elif nummer == 5:
            for i in range(0,10):
                if meme[i] == 'A':
                    meme[i] = 'T'
                elif meme[i] == 'T':
                    meme[i] = 'A'
                elif meme[i] == 'C':
                    meme[i] = 'G'
                elif meme[i] == 'G':
                    meme[i] = 'C'
            for i in range(30,60):
                if meme[i] == 'A':
                    meme[i] = 'C'
                elif meme[i] == 'T':
                    meme[i] = 'G'
                elif meme[i] == 'C':
                    meme[i] = 'A'
                elif meme[i] == 'G':
                    meme[i] = 'T'
            for i in range(60,100):
                if meme[i] == 'A':
                    meme[i] = 'G'
                elif meme[i] == 'T':
                    meme[i] = 'C'
                elif meme[i] == 'C':
                    meme[i] = 'T'
                elif meme[i] == 'G':
                    meme[i] = 'A'
        elif nummer!=1:
            print('protocol does not exist')
        return "".join(meme)
    except:
        print("Genome Protocol Error")

