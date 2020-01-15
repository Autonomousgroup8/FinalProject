def genome_protocol(protocol, genome):
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
    elif nummer!=1:
        print('protocol does not exist')        
    return "".join(meme)
  
    
#genome="AAAACCCCGGGGTTTTAAAAAAAACCCCGGGGTTTTAAAAAAAACCCCGGGGTTTTAAAAAAAACCCCGGGGTTTTAAAAAAAACCCCGGGGTTTTAAAA"
#a=genome_protocol(genome)
#print(meme)
