import util


class Slice:
    def __init__(self, address, offset, index_size):
        # Calculate address slices
        offset_start = 32 - offset
        index_start = offset_start - index_size

        # Convert address to binary string
        binary_string = util.hex_to_bin(address)

        self._tag = binary_string[0:index_start]
        self._index = binary_string[index_start:offset_start]
        self._offset = binary_string[offset_start:32]

    def get_tag(self):
        return self._tag

    def get_index(self):
        return self._index

    def get_offset(self):
        return self._offset
