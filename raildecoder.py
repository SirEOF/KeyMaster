from cipherenum import CipherType
import math

class RailDecoder:
    
    """
    A decoder class to decode rail ciphers (transposition ciphers)

    Given a text encoded like below
    'This is a test' encoded with 4 rails
    
    T     A
     H   S T
      I I   E T
       S     S
    
    A rail chunk consists of the characters from
    the top of one hump to the start of the next.
    So in this instance THISIS is the first rail
    chunk and ATEST is the begining of the second
    chunk but isn't complete.
    """

    def __init__(self):
        pass
        # super().__init__()


    def __rail_chunk_size(self, rails: int) -> int:
        if rails < 3:
            raise ValueError('Must have at least 3 rails.')

        return (rails * 2) - 2 

    def __rail_char_count(self, rails: int, str_len: str) -> str:
        if rails < 3:
            raise ValueError('Must have at least 3 rails')

        chunk_size = self.__rail_chunk_size(rails)
        chunk_multiplier = [2] * rails
        chunk_multiplier[0] -= 1
        chunk_multiplier[-1] -= 1

        chunk_count = str_len // chunk_size
        extra_chars = str_len % chunk_size

        rail_chars = [None] * rails
        for i, val in enumerate(chunk_multiplier):
            rail_chars[i] = val * chunk_count

        for i in range(extra_chars):
            rail_index = i
            if i >= rails:
                # It is on the upward slope of the last chunk
                rail_index = (rails - 1) - ((i + 1) % rails)
            rail_chars[rail_index] += 1

        return rail_chars 


    # Offset is not currently implemented
    def __solve_rail_fence(self, text: str, rails: int, offset: int = 0) -> str:
        pattern = self.__rail_char_count(rails, len(text))

        working_text = text
        rail_text = [None] * rails
        for rail in range(rails):
            rail_text[rail] = working_text[:pattern[rail]]
            working_text = working_text[pattern[rail]:]

        final_str = ''
        chunk_size = self.__rail_chunk_size(rails)
        for i in range(len(text)):
            i = i % chunk_size
            rail_index = i
            if i >= rails:
                # This char is on the upward slope
                rail_index = (rails - 1) - ((i + 1) % rails)

            # Take the first char from the rail and add it to the final string
            final_str += rail_text[rail_index][:1]
            rail_text[rail_index] = rail_text[rail_index][1:]

        return final_str


    def decode(self, rails, text):
        return self.__solve_rail_fence(text, rails)

    @staticmethod
    def type():
        return CipherType.RAIL_FENCE


# Test The Decoder
if __name__ == "__main__":
    obj = RailDecoder()
    print(obj.decode(3, "WLOEAAFEFRRAFSFSBKT"))
    print(obj.decode(3, "WLFBKTAFE O RAFSFSREA"))
    print(obj.decode(5, "WFKA OAFFSREAFE RSLBT"))
