# DNA-Fountain

## Overview
DNA-Fountain is a project that simulates encoding and decoding DNA sequences to represent binary data using a bipartite graph. It uses random sampling, XOR operations, and DNA base encoding to generate and decode droplets representing binary sequences. The project consists of two main components:
- **Encoder**: Converts a 32-bit binary sequence into DNA oligomers through random selection, XOR operations, and seed-based generation.
- **Decoder**: Decodes the DNA oligomers back into binary segments using a bipartite graph structure, processing droplets and their connections.

## Features
- **DNA to Binary Encoding**: Encodes binary data into DNA sequences.
- **Bipartite Graph Construction**: Generates a graph of droplets and their associated segments.
- **Decoding**: Decodes the oligomers back to their original binary representation.
  
## Components
### Encoder
The `Encoder` class encodes binary data into DNA sequences by:
- Dividing the binary sequence into 4-bit segments.
- Using random seeds and ranks to select segments.
- Performing XOR operations on the selected segments to generate droplets.
- Converting these droplets into DNA sequences.

### Decoder
The `Decoder` class decodes DNA sequences by:
- Converting the DNA oligomers back into droplets.
- Constructing a bipartite graph with droplets and their associated segments.
- Iteratively processing the graph to predict and remove single-segment droplets.

## Requirements
- Python 3.x
- Python Libraries: `random`, `operator`, `functools`

## How to Use
1. **Encoding**:
   - Initialize the `Encoder` class with a binary sequence, seeds, and ranks.
   - Use the `encode_oligomers()` method to generate DNA oligomers.

2. **Decoding**:
   - Initialize the `Decoder` class with the encoded DNA oligomers and ranks.
   - Use the `decode_oligomers()` method to decode the oligomers back to binary data.

To run the DNA-Fountain demo, ensure you have the required dependencies installed (Python 3.x), and run the script:
```bash
python dna_fountain
```
