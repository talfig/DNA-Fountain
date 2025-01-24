from model.encoder import Encoder
from model.decoder import Decoder

# Seeds and ranks used for encoding and decoding
seeds = [
    '0000', '0001', '0010', '0011',
    '0100', '0101', '0110', '0111',
    '1000', '1001', '1010', '1011',
    '1100', '1101', '1110', '1111',
]
ranks = [
    2, 2, 1, 1,
    2, 4, 2, 1,
    6, 1, 1, 2,
    7, 2, 1, 4
]

if __name__ == "__main__":
    bits = '01000001101011110000010110100101'

    # Encode and decode the DNA sequence
    encoder = Encoder(seeds, ranks, bits)
    oligomers = encoder.encode_oligomers()
    decoder = Decoder(oligomers, ranks)
    predicted_bits = decoder.decode_oligomers()

    # Print the decoded bits
    print('Predicted bits:')
    print("---------------")
    print(" ".join(predicted_bits))
