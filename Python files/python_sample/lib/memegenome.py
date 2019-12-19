''' MemeGenome class can be used to handle memetic genomes. '''

from random import randint

class MemeGenome(object):

    '''MemeGenome class can be used to handle memetic genomes.'''

    # define the length of memetic genomes
    LENGTH = 100

    # valid symbols
    Nucleotides = ['A', 'C', 'G', 'T']

    # __init__ is called when an instance of the class is created
    def __init__(self, genomestr):
        if not isinstance(genomestr, str):
            raise Exception('genomestr must be a string')
        if len(genomestr) != MemeGenome.LENGTH:
            raise Exception('genomestr has the wrong length.')
        self._genomestr = genomestr

    def genomestring(self):
        ''' Returns the genome string. '''
        return self._genomestr

    def is_equal(self, memgen):
        '''Check if the two genomes are identical'''
        return self.genomestring() == memgen.genomestring()

    @staticmethod
    def random_meme_genome():
        ''' Generate a random meme genome. '''
        genomestr = ''
        for _ in range(0, 100):
            genomestr += MemeGenome.Nucleotides[randint(0, 3)]
        return MemeGenome(genomestr)

    # this function is called when the expression g[key] is used with a MemeGenome g and an integer key, 0<=key<100
    def __getitem__(self, key):
        # return symbol number key
        return self._genomestr[key]

    # this function is called when the statement g[key] = value is executed with a MemeGenome g and an integer key, 0<=key<100
    def __setitem__(self, key, value):
        if not value in MemeGenome.Nucleotides:
            raise Exception('Values in genome must be A, C, G, or T.')
        # strings cannot be modified in Python, so make a new string for it
        self._genomestr = self._genomestr[:key] + value + self._genomestr[key+1:]

    # create a textual representation of the MemeGenome as a string
    def __repr__(self):
        return "MemeGenome({0})".format(self._genomestr)

    # create a textual representation of the MemeGenome as a string
    def __str__(self):
        return self.__repr__()

    def __delitem__(self, key):
        raise Exception('Cannot delete elements from a genome.')
 