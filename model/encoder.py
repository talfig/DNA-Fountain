import random
import operator
from functools import reduce


class Encoder:
    """
    The Encoder class is responsible for encoding a 32-bit binary sequence into DNA-based oligomers
    using random sampling and XOR operations. It simulates the process of generating droplets from
    binary segments, and then maps these droplets to DNA sequences.

    Attributes:
        seeds (list of str): A list of binary seed values (strings).
        ranks (list of int): A list of integers indicating the number of segments to select randomly for each seed.
        segments (list of str): A list of 4-bit binary segments derived from the input binary sequence.
    """

    def __init__(self, seeds, ranks, bits):
        """
        Initializes the Encoder instance.

        Args:
            seeds (list of str): A list of binary strings to serve as seeds.
            ranks (list of int): A list of integers specifying how many segments to choose for each seed.
            bits (str): A 32-bit binary sequence to be divided into 4-bit segments.

        Raises:
            AssertionError: If the input binary sequence is not 32 bits long.
        """
        assert len(bits) == 32, "Input must be a 32-bit binary sequence."
        self.seeds = seeds
        self.ranks = ranks
        self.segments = [bits[i:i + 4] for i in range(0, len(bits), 4)]

    def generate_droplets(self):
        """
        Generates droplets by randomly selecting segments and performing XOR operations.

        For each seed, `rank` segments are selected at random, their integer values are XORed,
        and the result is converted back to a 4-bit binary string. The droplet is created by
        concatenating the seed with this binary result.

        Returns:
            list of str: A list of generated droplets, each represented as a binary string.
        """
        droplets = []
        for seed, rank in zip(self.seeds, self.ranks):
            random.seed(int(seed, 2))

            # Randomly select `rank` segments
            chosen_segments = random.sample(self.segments, rank)

            # Convert strings to integers
            chosen_segments = [int(segment, 2) for segment in chosen_segments]

            # XOR the selected segments
            xor_result = reduce(operator.xor, chosen_segments)

            # Convert XOR result to binary string and ensure it's 4 bits long
            binary_result = bin(xor_result)[2:].zfill(4)

            # Concatenate the seed to the droplet
            droplet = f"{seed}{binary_result}"

            # Append the droplet to the droplets list
            droplets.append(droplet)

        return droplets

    @staticmethod
    def droplet_to_dna(droplet):
        """
        Converts a binary droplet string into a DNA sequence.

        Args:
            droplet (str): A binary string representing a droplet.

        Returns:
            str: A DNA sequence mapped from the binary droplet.

        Mapping:
            '00' -> 'A', '01' -> 'C', '10' -> 'G', '11' -> 'T'
        """
        mapping = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}
        return ''.join([mapping[droplet[i:i + 2]] for i in range(0, len(droplet), 2)])

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
            oligomer = self.droplet_to_dna(droplet)
            oligomers.append(oligomer)
            print(f"Droplet {i} -> Oligomer: {oligomer}")

        return oligomers
