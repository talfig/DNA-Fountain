import random


class Decoder:
    def __init__(self, oligomers, ranks):
        self.oligomers = oligomers
        self.ranks = ranks
        self.segments = [i for i in range(1, 9)]

    @staticmethod
    def dna_to_droplet(dna):
        mapping = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}
        return ''.join([mapping[base] for base in dna])

    def generate_graph(self):
        # Create droplets by converting DNA sequences to droplet representations
        droplets = [self.dna_to_droplet(oligomer) for oligomer in self.oligomers]

        # Split droplets into seeds and remaining parts
        seeds = [droplet[:4] for droplet in droplets]
        droplets = [droplet[4:] for droplet in droplets]

        # Initialize the graph
        graph = []

        # Populate the graph
        for seed, droplet, rank in zip(seeds, droplets, self.ranks):
            random.seed(int(seed, 2))  # Seed the random generator

            # Convert droplet to an integer and append to graph as a tuple
            graph.append((int(droplet, 2), random.sample(self.segments, rank)))

        return graph

    @staticmethod
    def update_graph(graph, key, value):
        # Traverse the graph and update
        for idx, (key1, value1) in enumerate(graph):
            # Remove value if it exists in value1
            if value in value1:
                value1.remove(value)
                graph[idx] = (key1 ^ key, value1)

    def decode_oligomers(self):
        graph = self.generate_graph()

        predicted_segments = [''] * 9
        for (droplet, segments) in graph[:]:
            if (droplet, segments) in graph and len(segments) == 1:
                predicted_segments[segments[0]] = bin(droplet)[2:].zfill(4)  # Ensuring 4-bit binary format
                graph.remove((droplet, segments))
                self.update_graph(graph, droplet, segments[0])

        return predicted_segments[1:]
