import toml
from model.encoder import Encoder
from model.decoder import Decoder


# Generate all 9-bit binary seeds
seeds = [format(i, '09b') for i in range(512)]

# ranks used for encoding and decoding
ranks = [
    3, 1, 5, 2,
    8, 1, 1, 6,
    2, 3, 10, 1,
    12, 1, 3, 7,
    4, 2, 1, 15,
    3, 1, 5, 8,
    1, 6, 2, 11,
    4, 1, 1, 9,
    3, 14, 2, 2,
    20, 11, 23, 24,
    26, 1, 30, 15
]

if __name__ == "__main__":
    toml_data = toml.load("binary_data.toml")
    binary_data = toml_data["binary_data"]
    binary_data = binary_data.replace("\n", "")

    # Encode and decode the DNA sequence
    encoder = Encoder(seeds, ranks, binary_data)
    oligomers = encoder.encode_oligomers()
    decoder = Decoder(oligomers, len(binary_data))
    predicted_bits = decoder.decode_oligomers()

    # Print the decoded bits
    print('Predicted binary data:')
    print("----------------------")
    print("".join(predicted_bits))
