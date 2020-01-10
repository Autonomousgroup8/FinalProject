def genome_protocol(genome):
    print("Which protocol do you want to run?")
    i=1
    j=i
    nummer=input()
    if nummer == "1":
        meme=genome
    elif nummer == "2":
        meme = genome
        if meme[0] == 'A':
            meme = 'T' + meme[2:]
        elif meme[0] == 'T':
            meme = 'A' + meme[2:]
        elif meme[0] == 'C':
            meme = 'G' + meme[2:]
        elif meme[0] == 'G':
            meme= 'C'+ meme[2:]
        while i < 100: 
            if meme[i] == 'A':
                if(j == '\0'):
                    meme = meme[:i] + 'T' # + meme[i:]
                else:
                    meme = meme[:i] + 'T' + meme[j:]
            elif meme[i] == 'T':
                if(j == '\0'):
                    meme = meme[:i] + 'A' # + meme[i:]
                else:
                    meme = meme[:i] + 'A' + meme[j:]
            elif meme[i] == 'C':
                if(j == '\0'):
                    meme = meme[:i] + 'G' # + meme[i:]
                else:
                    meme = meme[:i] + 'G' + meme[j:]
            elif meme[i] == 'G':
                if(j == '\0'):
                    meme = meme[:i] + 'C' # + meme[i:]
                else:
                    meme = meme[:i] + 'C' + meme[j:]
            i+=1
            j=i
            j+=1       
    elif nummer == "3":
        meme = genome
        if meme[0] == 'A':
            meme = 'C' + meme[2:]
        elif meme[0] == 'T':
            meme = 'G' + meme[2:]
        elif meme[0] == 'C':
            meme = 'A' + meme[2:]
        elif meme[0] == 'G':
            meme= 'T'+ meme[2:]
        while i < 100: 
            if meme[i] == 'A':
                if(j == '\0'):
                    meme = meme[:i] + 'C' # + meme[i:]
                else:
                    meme = meme[:i] + 'C' + meme[j:]
            elif meme[i] == 'T':
                if(j == '\0'):
                    meme = meme[:i] + 'G' # + meme[i:]
                else:
                    meme = meme[:i] + 'G' + meme[j:]
            elif meme[i] == 'C':
                if(j == '\0'):
                    meme = meme[:i] + 'A' # + meme[i:]
                else:
                    meme = meme[:i] + 'A' + meme[j:]
            elif meme[i] == 'G':
                if(j == '\0'):
                    meme = meme[:i] + 'T' # + meme[i:]
                else:
                    meme = meme[:i] + 'T' + meme[j:]
            i+=1
            j=i
            j+=1
    
    elif nummer == "4":
        meme = genome
        if meme[0] == 'A':
            meme = 'G' + meme[2:]
        elif meme[0] == 'T':
            meme = 'C' + meme[2:]
        elif meme[0] == 'C':
            meme = 'T' + meme[2:]
        elif meme[0] == 'G':
            meme= 'A'+ meme[2:]
        while i < 100: 
            if meme[i] == 'A':
                if(j == '\0'):
                    meme = meme[:i] + 'G' # + meme[i:]
                else:
                    meme = meme[:i] + 'G' + meme[j:]
            elif meme[i] == 'T':
                if(j == '\0'):
                    meme = meme[:i] + 'C' # + meme[i:]
                else:
                    meme = meme[:i] + 'C' + meme[j:]
            elif meme[i] == 'C':
                if(j == '\0'):
                    meme = meme[:i] + 'T' # + meme[i:]
                else:
                    meme = meme[:i] + 'T' + meme[j:]
            elif meme[i] == 'G':
                if(j == '\0'):
                    meme = meme[:i] + 'A' # + meme[i:]
                else:
                    meme = meme[:i] + 'A' + meme[j:]
            i+=1
            j=i
            j+=1
            
    print(meme)
    global meme
  
    
genome="AAAACCCCGGGGTTTTAAAAAAAACCCCGGGGTTTTAAAAAAAACCCCGGGGTTTTAAAAAAAACCCCGGGGTTTTAAAAAAAACCCCGGGGTTTTAAAA"
a=genome_protocol(genome)
print(meme)

  
