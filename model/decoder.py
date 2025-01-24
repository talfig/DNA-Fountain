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

        print()
        print("Decoded Droplets:")
        print("-----------------")
        for i, droplet in enumerate(droplets, start=1):
            print(f"Droplet {i}: {droplet}")
        print()

        # Split droplets into seeds and remaining parts
        seeds = [droplet[:4] for droplet in droplets]
        remaining_droplets = [droplet[4:] for droplet in droplets]

        print("Generator Seeds and Ranks:")
        print("---------------------------")
        for i, (seed, rank) in enumerate(zip(seeds, self.ranks), start=1):
            print(f"Seed {i}: {seed}, Rank: {rank}")
        print()

        # Initialize the graph
        graph = []

        print("Graph Construction:")
        print("--------------------")
        for i, (seed, droplet, rank) in enumerate(zip(seeds, remaining_droplets, self.ranks), start=1):
            random.seed(int(seed, 2))  # Seed the random generator
            droplet_int = int(droplet, 2)
            connections = random.sample(self.segments, rank)
            graph.append((droplet_int, connections))
            print(f"Node {i}: Droplet {droplet_int}, Connections: {connections}")

        return graph

    @staticmethod
    def update_graph(graph, droplet, segment):
        # Traverse the graph and update
        for idx, (key, segments) in enumerate(graph):
            # Remove segment if it exists in segments
            if segment in segments:
                segments.remove(segment)
                graph[idx] = (droplet ^ key, segments)
                if not segments:
                    graph.pop(idx)

    def decode_oligomers(self):
        graph = self.generate_graph()
        predicted_segments = [''] * 9

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
                    print(f"Current Graph: {[{'node': n, 'edges': e} for n, e in graph]}")
                    print(f"Selected Edge: Node {droplet}, Segment {segments}")
                    print(f"Predicted Segments: {predicted_segments}")
                    print()

                    # Process and update the graph
                    predicted_segments[segments[0]] = bin(droplet)[2:].zfill(4)  # 4-bit binary format
                    graph.remove((droplet, segments))  # Remove the processed droplet
                    self.update_graph(graph, droplet, segments[0])
                    updated = True

            # Exit the loop if no updates were made
            if not updated:
                break

        print("Final Bipartite Graph:")
        print("----------------------")
        for node, edges in graph:
            print(f"Node: {node}, Edges: {edges}")
        print()

        print("Final Predicted Segments:")
        print("--------------------------")
        for i, segment in enumerate(predicted_segments[1:], start=1):
            print(f"Segment {i}: {segment}")

        return predicted_segments[1:]
