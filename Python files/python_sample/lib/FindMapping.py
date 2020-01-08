def find_mapping(gen1,gen2):
    Nucleotides = ['A', 'C', 'T', 'G']
    mappings = [0,0,0,0]
    for i in range(len(Nucleotides)):
        temp_ind = (gen1.find(Nucleotides[i]))
        mappings[i] = gen2[temp_ind]
    return mappings

