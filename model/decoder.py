import random


class Decoder:
    def __init__(self, oligomers):
        self.oligomers = oligomers

    @staticmethod
    def dna_to_droplet(dna):
        mapping = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}
        return ''.join([mapping[base] for base in dna])

    def