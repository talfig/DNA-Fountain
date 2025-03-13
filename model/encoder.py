import random
import operator
from functools import reduce


class Encoder:
    def __init__(self, seeds, ranks, bits, segment_size=36, pad_value='0'):
        if len(bits) % segment_size != 0:
            padding_length = segment_size - (len(bits) % segment_size)
            bits += pad_value * padding_length
        self.seeds = seeds
        self.ranks = ranks
        self.segment_size = segment_size
        self.segments = [bits[i:i + segment_size] for i in range(0, len(bits), segment_size)]

    @staticmethod
    def generate_barcode(length=10):
        """
        Generates a random DNA sequence of the given length.

        Parameters:
        length (int): The length of the DNA sequence to generate. Default is 10.

        Returns:
        str: A string representing a random DNA sequence composed of A, C, T, and G.
        """
        bases = ['A', 'C', 'T', 'G']
        return ''.join(random.choices(bases, k=length))

    def generate_droplets(self):
        droplets = []
        for seed in self.seeds:
            random.seed()
            d = random.sample(self.ranks, 1)[0]

            # Randomly select `rank` segments
            random.seed(int(seed, 2))
            chosen_segments = random.sample(self.segments, d)

            # Convert strings to integers
            chosen_segments = [int(segment, 2) for segment in chosen_segments]

            # XOR the selected segments
            xor_result = reduce(operator.xor, chosen_segments)

            # Store the rank in binary
            d_bin = bin(d)[2:].zfill(6)

            binary_result = bin(xor_result)[2:].zfill(self.segment_size)

            droplet = f"{seed}{d_bin}{binary_result}"

            # Append the droplet to the droplets list
            droplets.append(droplet)

        return droplets

    @staticmethod
    def bits_to_dna(bits, pad_value='0'):
        bit_to_word_mapping = {'000': 'AL', '001': 'AM',
                               '010': 'CL', '011': 'CM',
                               '100': 'TL', '101': 'TM',
                               '110': 'GL', '111': 'GM'}
        letter_to_dna_mapping = {'L': ['CT', 'TC'], 'M': ['AG', 'GA']}

        # Convert bits to words
        words = ''.join(bit_to_word_mapping[bits[i:i + 3]] for i in range(0, len(bits), 3))

        # Convert words to DNA sequence
        dna_sequence = ''.join(random.choice(letter_to_dna_mapping[char])
                               if char in letter_to_dna_mapping
                               else char for char in words)
        return dna_sequence

    def encode_oligomers(self):
        """
        Encodes droplets into DNA oligomers.

        First, droplets are generated using the `generate_droplets` method. Then, each droplet
        is converted into a DNA oligomer using the `droplet_to_dna` method. The method prints
        intermediate steps to provide transparency.

        Returns:
            list of str: A list of DNA oligomers.
        """
        droplets = self.generate_droplets()

        print("Droplet Generation:")
        print("-------------------")
        for i, droplet in enumerate(droplets, start=1):
            print(f"Droplet {i}: {droplet}")
        print()

        oligomers = []
        print("Encoding Droplets to DNA Oligomers:")
        print("-----------------------------------")
        for i, droplet in enumerate(droplets, start=1):
            barcode = self.generate_barcode()
            for j in range(1, 101):
                words = self.bits_to_dna(droplet)
                oligomer = barcode + words
                oligomers.append(oligomer)
                print(f"Droplet {i} -> Oligomer {j}: {oligomer}")

        random.shuffle(oligomers)
        return oligomers
