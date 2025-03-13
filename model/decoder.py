import random
from collections import defaultdict
from itertools import chain


class Decoder:
    def __init__(self, oligomers, msg_size, segment_size=36, sample_size=100):
        self.padding_length = 0
        if msg_size % segment_size != 0:
            self.padding_length = segment_size - (msg_size % segment_size)
        self.segment_size = segment_size
        self.sample_size = sample_size
        self.oligomers = oligomers
        self.segments = [i for i in range(1, (msg_size + self.padding_length) // segment_size + 1)]

    @staticmethod
    def dna_to_bits(dna):
        word_to_bit_mapping = {'AL': '000', 'AM': '001',
                               'CL': '010', 'CM': '011',
                               'TL': '100', 'TM': '101',
                               'GL': '110', 'GM': '111'}
        dna_to_letter_mapping = {'CT': 'L', 'TC': 'L',
                                 'AG': 'M', 'GA': 'M'}

        # Build droplet string by iterating through DNA sequence
        droplet = ''
        for i in range(0, len(dna), 3):
            pair = dna[i + 1:i + 3]  # Two characters
            letter = dna_to_letter_mapping.get(pair, '')  # Get corresponding letter

            if letter:
                word = dna[i] + letter  # Combine the first character and the mapped letter
                droplet += word_to_bit_mapping.get(word, '')  # Append the corresponding bit sequence

        return droplet

    def generate_graph(self, min_droplet_sample=10):
        """
        Generates a bipartite graph based on the decoded droplets and their connections.

        - Converts DNA oligomers to droplet representations.
        - Splits the droplets into seeds and remaining parts.
        - Generates graph nodes with droplets and connections based on random seeding.

        Returns:
            list: A list of tuples representing the graph, where each tuple contains:
                  (droplet, list of connected segments).
        """
        # Create droplets by grouping oligomers with the same barcode
        droplets = defaultdict(list)

        # Group oligomers based on the barcode
        for oligomer in self.oligomers:
            barcode = oligomer[:10]
            droplets[barcode].append(oligomer[10:])

        # Randomly sample 10 oligomers from each barcode group (if there are at least 10, otherwise take all)
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

        seeds = [droplet[:9] for droplet in droplets]
        ranks = [droplet[9:15] for droplet in droplets]
        remaining_droplets = [droplet[15:] for droplet in droplets]

        print("Generator Seeds and Ranks:")
        print("--------------------------")
        for i, (seed, rank) in enumerate(zip(seeds, ranks), start=1):
            print(f"Seed {i}: {seed}, Rank: {rank}")
        print()

        # Combine seeds, droplets, and ranks, then select a random sample
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
            connections = random.sample(self.segments, int(rank, 2))
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
        graph = self.generate_graph()
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
                    predicted_segments[segments[0]] = bin(droplet)[2:].zfill(self.segment_size)  # 6-bit binary format
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
