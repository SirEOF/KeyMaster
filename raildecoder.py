from basedecoder import BaseDecoder
from cipher import CipherType
import math

class RailDecoder(BaseDecoder):
    
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


    def __init__(self, inputs: list):
        super().__init__(inputs)
        self.add_key([('rails', self.key_rails_validate, 'Number of rails to use to decode')])


    def __rail_chunk_size(rails):
        if rails < 3:
            raise ValueError('Must have at least 3 rails.')

        return (rails * 2) - 2 

    def __rail_char_count(rails, str_len):
        if rails < 3:
            raise ValueError('Must have at least 3 rails')

        chunk_size = rail_chunk_size(rails)
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


    def __solve_rail_fence(rails, text, strip_spaces=True):
        if strip_spaces:
            text = text.replace(' ', '')
        pattern = __rail_char_count(rails, len(text))

        working_text = text
        rail_text = [None] * rails
        for rail in range(rails):
            rail_text[rail] = working_text[:pattern[rail]]
            working_text = working_text[pattern[rail]:]

        final_str = ''
        chunk_size = rail_chunk_size(rails)
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


    def decode(self) -> bool:
        """
        Returns a True if there is suffecient information (keys)
        provided to decode the input text provided. Otherwise false
        is returned by this function.
        """

        if not self.can_decode():
            return False

        start_rails = None
        end_raiuls = None
        val_rails = self.get_key('rails')
        if ':' in val_rails:
            start_rails, end_rails = val_rails.split(':')
        
            # Convert the strings to integers
            start_rails = int(start_rails)
            end_rails = int(end_rails)
        else:
            start_rails = val_rails
            
            # Convert the strings to integers
            start_rails = int(start_rails)
            end_rails = start_rails + 1

        print("Decoding")
        for input_ in inputs:
            for rail_count in range(start_rails, end_rails + 1):
                input_solution_set.append(self.__solve_rail_fence(input_, rail_count))
            self.results.append(input_solution_set)
        return True

    
    @staticmethod
    def key_rails_validate(value: str):
        """
        Validates that the key the user set is valid.
        
        Parsing or processing of the value can happen here.
        The value returned will be stored automatically, and
        if the value is not valid at all this function returns None.
        """
        
        if value is None:
            return None
                
        if '-' in value:
            arr = value.split('-')
            
            if len(arr) != 2:
                return None
            
            start = arr[0].strip()
            end = arr[1].strip()
            return start + ':' + end


        try:
            rail_num = int(value)
            return rail_num
        except ValueError:
            # Not an int value
            pass
       
        return None

    @staticmethod
    def type():
        return CipherType.RAIL_FENCE
