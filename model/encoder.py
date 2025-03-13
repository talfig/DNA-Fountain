import random
import operator
from functools import reduce


class Encoder:
    """
    A class that encodes a sequence of bits into segments based on a specified segment size.
    The class handles padding the bits to ensure that their length is a multiple of the segment size.

    Attributes:
        seeds (list): A list of seed values used for encoding (specific usage depends on context).
        ranks (list): A list of ranks corresponding to each segment.
        segment_size (int): The size of each segment to which the bits will be divided. Defaults to 36.
        segments (list): A list of bit segments of the specified segment size.
    """

    def __init__(self, seeds, ranks, bits, segment_size=36, pad_value='0'):
        """
        Initializes the Encoder object with the provided bit sequence, seeds, and ranks.

        Args:
            seeds (list): A list of seed values used for encoding. The exact use of these values is dependent on the encoding process.
            ranks (list): A list of ranks that correspond to the segments. The relationship between ranks and segments should be defined in the context.
            bits (str): A string of bits to be encoded. The length of the string is adjusted to be a multiple of segment_size.
            segment_size (int, optional): The desired size for each segment. Defaults to 36.
            pad_value (str, optional): The character used to pad the bit string to the required length. Defaults to '0'.
        """
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
        """
        Generates droplets by selecting random segments based on seeds and ranks,
        XORing them, and returning the encoded droplets as a list of strings.

        For each seed, a random rank is chosen, and corresponding segments are selected
        based on that rank. These segments are XORed, and the result is combined with
        the rank to create a droplet.

        Returns:
            list of str: A list of encoded droplets, each represented as a string.
        """
        droplets = []
        for seed in self.seeds:
            # Randomly select a `rank`
            random.seed()
            d = random.sample(self.ranks, 1)[0]

            # Randomly select `rank` segments
            random.seed(int(seed, 2))
            chosen_segments = random.sample(self.segments, d)

            # Convert strings to integers
            chosen_segments = [int(segment, 2) for segment in chosen_segments]

            # XOR the selected segments
            xor_result = reduce(operator.xor, chosen_segments)

            # Store the `rank` in binary
            d_bin = bin(d)[2:].zfill(6)

            # Convert the XOR result into a binary string
            binary_result = bin(xor_result)[2:].zfill(self.segment_size)

            # Combine the data into a droplet
            droplet = f"{seed}{d_bin}{binary_result}"

            # Append the droplet to the droplets list
            droplets.append(droplet)

        return droplets

    @staticmethod
    def bits_to_dna(bits):
        """
        Converts a bit sequence into a DNA sequence by mapping bits to words and words to DNA strands.

        The method maps each triplet of bits to a corresponding word, and then maps each word to
        a DNA sequence using predefined mappings. Random choices are made for each DNA strand.

        Args:
            bits (str): A string of bits to be converted into a DNA sequence.

        Returns:
            str: A DNA sequence represented as a string.
        """
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

        First, droplets are generated using the `generate_droplets` method. Each droplet is then
        converted to a DNA sequence using the `bits_to_dna` method, combined with a unique barcode
        generated by `generate_barcode`, and appended to a list. The method prints intermediate steps
        for transparency.

        Returns:
            list of str: A shuffled list of DNA oligomers.
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
                # Convert droplet to DNA
                words = self.bits_to_dna(droplet)

                # Combine the barcode and DNA sequence
                oligomer = barcode + words
                oligomers.append(oligomer)
                print(f"Droplet {i} -> Oligomer {j}: {oligomer}")

        random.shuffle(oligomers)
        return oligomers
