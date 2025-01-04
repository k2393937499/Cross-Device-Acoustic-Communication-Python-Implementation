import numpy as np
from commpy.channelcoding import Trellis, conv_encode, viterbi_decode

class ConvEncode:
    def __init__(self):
        self.memory= np.array([7])  # m
        self.generator_polynomials = np.array([[133, 171]])
        self.trellis = Trellis(self.memory, self.generator_polynomials)
    
    def convolutional_encode(self, bits: list[str]):
        """
        encode the binary list
        :param bits: binary list to be encoded (list of str)
        :return: encoded binary list (list of numpy array)
        """
        encoded_list = []
        original_lengths = []
        for bit_str in bits:
            bit_array = np.array(list(map(int, bit_str)), dtype=np.int8)
            encoded = conv_encode(bit_array, self.trellis)
            encoded = ''.join(map(str, encoded))
            encoded_list.append(encoded)
            original_lengths.append(len(bit_str))
        return encoded_list

    def convolutional_decode(self, encoded_bits):
        """
        decode the binary list
        :param bits: binary list to be encoded (list of str)
        :return: encoded binary list (list of numpy array)
        """
        decoded_list = []
        for encoded in encoded_bits: 
            encoded = np.array(list(map(int, encoded)))
            decoded = viterbi_decode(encoded, self.trellis, tb_depth=None)
            decoded_str = ''.join(map(str, decoded.astype(int)))  # convert to str
            decoded_str = decoded_str[:-7]  # remove 7 * zeros (padding)
            decoded_list.append(decoded_str)
        return decoded_list

    def calculate_ber(self, original_bits, decoded_bits):
        """
        calculate BER
        :param original_bits: original list (list of str)
        :param decoded_bits: decoded list (list of str)
        :return: BER
        """
        total_bits = sum(len(bit_str) for bit_str in original_bits)
        errors = sum(
            1 for original, decoded in zip(''.join(original_bits), ''.join(decoded_bits)) if original != decoded
        )
        ber = errors / total_bits
        return ber

if __name__ == "__main__":
    system = ConvEncode()
    bits = [
        "101010111100110111000011",
        "110011001010101011111000",
        "001100110011110000110011",
        "111111000000111111000111",
        "010101010101101010101010",
        "000011110000111100001111"
    ]
    print("original bits:", bits)

    # encoded
    encoded, original_lengths = system.convolutional_encode(bits)
    print("encoded bits:", encoded)

    # add noise
    noisy_encoded = []
    for enc in encoded:
        enc = list(enc)
        flip_indices = np.random.choice(len(enc), size=3, replace=False)  # size: the num of flip bits
        for idx in flip_indices:
            enc[idx] = '0' if enc[idx] == '1' else '1'
        enc = ''.join(map(str, enc))
        noisy_encoded.append(enc)
    print("noise added bits:", noisy_encoded)

    # decoded
    decoded = system.convolutional_decode(noisy_encoded, original_lengths)
    decoded1 = np.array(np.array(list(map(int, decoded[0])), dtype=np.int8))
    print("decoded bits:", decoded)

    # calculate BER
    ber = system.calculate_ber(bits, decoded)
    print(f"BER: {ber * 100:.2f}%")
