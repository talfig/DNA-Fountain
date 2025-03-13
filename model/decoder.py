import random
from collections import defaultdict
from itertools import chain


class Decoder:
    """
    A class for handling the decoding of encoded messages split into oligomers.

    Attributes:
        padding_length (int): The number of padding bytes needed to make the message size
                              a multiple of segment_size.
        segment_size (int): The size of each segment in which the message is divided.
        sample_size (int): The number of samples to be considered for decoding.
        oligomers (list): A list of oligomers containing encoded message segments.
        segments (list): A list of segment indices representing the divisions of the message.
    """

    def __init__(self, oligomers, msg_size, segment_size=36, sample_size=100):
        """
        Initializes the Decoder with the given oligomers, message size, segment size, and sample size.

        Args:
            oligomers (list): The list of encoded message segments.
            msg_size (int): The original message size before segmentation.
            segment_size (int, optional): The size of each segment. Default is 36.
            sample_size (int, optional): The number of samples considered for decoding. Default is 100.
        """
        self.padding_length = 0
        if msg_size % segment_size != 0:
            self.padding_length = segment_size - (msg_size % segment_size)
        self.segment_size = segment_size
        self.sample_size = sample_size
        self.oligomers = oligomers
        self.segments = [i for i in range(1, (msg_size + self.padding_length) // segment_size + 1)]

    @staticmethod
    def dna_to_bits(dna):
        """
        Converts a DNA sequence into a bit string using predefined mappings.

        Args:
            dna (str): The DNA sequence to be converted.

        Returns:
            str: The corresponding bit string representation of the input DNA sequence.

        The function maps specific DNA base pair combinations to letters (L, M) and then
        converts those into predefined bit sequences.
        """
        word_to_bit_mapping = {'AL': '000', 'AM': '001',
                               'CL': '010', 'CM': '011',
                               'TL': '100', 'TM': '101',
                               'GL': '110', 'GM': '111'}
        dna_to_letter_mapping = {'CT': 'L', 'TC': 'L',
                                 'AG': 'M', 'GA': 'M'}

        # Build droplet string by iterating through DNA sequence
        droplet = ''
        for i in range(0, len(dna), 3):
            pair = dna[i + 1:i + 3]
            letter = dna_to_letter_mapping.get(pair, '')  # Get corresponding letter

            if letter:
                word = dna[i] + letter  # Combine the first character and the mapped letter
                droplet += word_to_bit_mapping.get(word, '')  # Append the corresponding bit sequence

        return droplet

    def generate_graph(self, min_droplet_sample=10):
        """
         Generates a graph representation of the decoded message by grouping oligomers into droplets
         and establishing connections based on their extracted features.

         Args:
             min_droplet_sample (int, optional): The minimum number of oligomers sampled per barcode group. Default is 10.

         Returns:
             list: A list of tuples where each tuple contains a droplet's integer representation
                   and a list of its connected segments.

        The function:
        - Groups oligomers by their barcode (first 10 characters)
        - Samples oligomers from each group
        - Converts them into bit representation
        - Extracts seed values, ranks, and remaining segments
        - Constructs a graph based on seeded random sampling of segment connections
        """
        # Create droplets by grouping oligomers with the same barcode
        droplets = defaultdict(list)

        # Group oligomers based on the barcode
        for oligomer in self.oligomers:
            barcode = oligomer[:10]
            droplets[barcode].append(oligomer[10:])

        # Randomly sample 10 oligomers from each barcode group
        selected_oligomers = list(chain.from_iterable(
            random.sample(group, min(min_droplet_sample, len(group))) for group in droplets.values()
        ))

        # Convert selected oligomers into DNA representation
        droplets = [self.dna_to_bits(oligomer) for oligomer in selected_oligomers]

        print()
        print("Decoded Droplets:")
        print("-----------------")
        for i, droplet in enumerate(droplets, start=1):
            print(f"Droplet {i}: {droplet}")
        print()

        # Extract the first 9 elements of each droplet as seeds
        seeds = [droplet[:9] for droplet in droplets]

        # Extract elements 9 to 14 as ranks
        ranks = [droplet[9:15] for droplet in droplets]

        # Extract remaining elements after index 15
        remaining_droplets = [droplet[15:] for droplet in droplets]

        print("Generator Seeds and Ranks:")
        print("--------------------------")
        for i, (seed, rank) in enumerate(zip(seeds, ranks), start=1):
            print(f"Seed {i}: {seed}, Rank: {rank}")
        print()

        # Combine seeds, ranks, and droplets, then select a random sample
        random.seed()
        droplets_data = list(zip(seeds, ranks, remaining_droplets))
        chosen_droplets = random.sample(droplets_data, self.sample_size)

        # Initialize the graph
        graph = []

        print("Graph Construction:")
        print("-------------------")
        for i, (seed, rank, droplet) in enumerate(chosen_droplets, start=1):
            random.seed(int(seed, 2))  # Seed the random generator
            droplet_int = int(droplet, 2)
            connections = random.sample(self.segments, int(rank, 2))  # Choose the segments
            graph.append((droplet_int, connections))
            print(f"Node {i}: Droplet {droplet_int}, Connections: {connections}")

        return graph

    @staticmethod
    def update_graph(graph, droplet, segment):
        """
        Updates the graph by removing a specified segment from a droplet's connections.

        Args:
            graph (list): The current graph to be updated.
            droplet (int): The droplet node whose connections need to be updated.
            segment (int): The segment to remove from the droplet's connections.
        """
        for idx, (key, segments) in enumerate(graph):
            # Remove segment if it exists in segments
            if segment in segments:
                segments.remove(segment)
                graph[idx] = (droplet ^ key, segments)
                if not segments:
                    graph.pop(idx)

    def decode_oligomers(self):
        """
        Decodes the oligomers by processing the bipartite graph and reconstructing the original segments.

        Returns:
            list: A list of predicted segments representing the decoded message.
        """
        graph = self.generate_graph()

        # Stores predicted bit sequences with an extra placeholders
        predicted_segments = [''] * (len(self.segments) + 1)

        print()
        print("Initial Bipartite Graph:")
        print("------------------------")
        for node, edges in graph:
            print(f"Node: {node}, Edges: {edges}")
        print()

        # Keep processing the graph until no changes can be made
        while True:
            updated = False

            for droplet, segments in graph[:]:
                if (droplet, segments) in graph and len(segments) == 1:
                    print("Processing Droplet with Single Segment:")
                    print("---------------------------------------")
                    print(f"Current Graph: {[{'node': n, 'edges': e} for n, e in graph]}")  # Display current state
                    print(f"Selected Edge: Node {droplet}, Segment {segments}")
                    print(f"Predicted Segments: {predicted_segments[1:]}")
                    print()

                    # Process and update the graph
                    predicted_segments[segments[0]] = bin(droplet)[2:].zfill(self.segment_size)
                    graph.remove((droplet, segments))  # Remove the processed droplet
                    self.update_graph(graph, droplet, segments[0])
                    updated = True

            # Exit the loop if no updates were made
            if not updated:
                break

        predicted_segments[-1] = predicted_segments[-1][:-self.padding_length]

        print("Final Predicted Segments:")
        print("-------------------------")
        for i, segment in enumerate(predicted_segments[1:], start=1):
            print(f"Segment {i}: {segment}")

        print()
        return predicted_segments[1:]
