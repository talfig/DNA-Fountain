import random
from functools import reduce
import operator


class Encoder:
    def __init__(self, seeds, ranks, bits):
        assert len(bits) == 32, "Input must be a 32-bit binary sequence."
        self.seeds = seeds
        self.ranks = ranks
        self.segments = [bits[i:i + 4] for i in range(0, len(bits), 4)]

    @staticmethod
    def _is_valid_droplet(droplet):
        """
        Checks if the droplet is valid:
        - GC content is at least 50%.
        - No long runs of the same base (e.g., AAAAA).
        """
        # Calculate GC content
        gc_count = sum(1 for base in droplet if base in "GC")
        gc_content = gc_count / len(droplet)

        # Check for long runs of the same base (e.g., AAAAA)
        has_long_run = any(droplet[i:i + 5] == droplet[i] * 5 for i in range(len(droplet) - 4))

        # Valid if GC content >= 50% and no long runs
        return gc_content >= 0.5 and not has_long_run

    def generate_droplets(self):
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
        mapping = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}
        return ''.join([mapping[droplet[i:i + 2]] for i in range(0, len(droplet), 2)])

    def encode_oligomers(self):
        droplets = self.generate_droplets()

        oligomers = []
        for droplet in droplets:
            oligomer = self.droplet_to_dna(droplet)
            oligomers.append(oligomer)

        return oligomers
