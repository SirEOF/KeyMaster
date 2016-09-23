from cipherenum import CipherType
from raildecoder import RailDecoder
from copy import copy


##################
# Cipher Classes #
##################

class CipherHistory:

    def __init__(self):
        self.history = []

    def prev(self):
        if len(self.history) <= 1:
            return None
        return self.history[-2]

    def curr(self):
        if len(self.history) < 1:
            self.history.append(CipherInstance())
        return self.history[-1]


    def __add_next_inst(self) -> bool:
        """
        Append the next cipher instance.
        """
        
        next_inst = self.curr().result_instance()
        if next_inst is None:
            return False

        self.history.append(next_inst)
        return True

class CipherInstance:

    def __init__(self, inputs: list = None):
        if inputs is None:
            self.inputs = []
        else:
            self.inputs = map((lambda input_: InputText(input_)), inputs)
        self.results = None
        self.decoder = None


    def get_inputs(self):
        print(self.inputs)


    def add_input(self, input_: str):
        self.inputs.append(InputText(input_))


    def result_instance(self):
        if results is None:
            return None
        return CipherInstance(self.results)


    def decode(self):
        if self.cipher_type is None:
            return False


        outputs = []
        for text in self.inputs:
            outputs.append(outputs.append(self.decoder.decode(text)))
        return outputs

    
    def has_decoder(self):
        return self.decoder is not None


    def set_type(self, cipher_type: CipherType):
        if cipher_type == CipherType.RAIL_FENCE:
            self.decoder = RailDecoder()
        else:
            return False
        
        # Return True if a type was found
        return True


    def get_type(self) -> CipherType:
        if self.decoder is None:
            return None

        return self.decoder.type()

class InputText:
    """
    This class should only be used internally.
    """

    def __init__(self, start_text: str):
        self.__text_history = [start_text]
        self.__key_history = [None]
        self.__decoder_type = [None]
    

    def add_decoded_output(self, decoded_text: str, decoder: BaseDecoder) -> None:
            # decoded_text: str, key_values: dict, decoder_type: CipherType) -> None:

        self.__text_history.append(decoded_text)
        self.__key_history.append(decoder.key_values)
        self.__decoder_type.append(decoder.type())


    def copy(self):
        copy_obj = InputText(None)
        copy_obj.__text_history = copy(self.__text_history)
        copy_obj.__key_history = copy(self.__key_history)
        copy_obj.__decoder_type = copy(self.__decoder_type)
        return copy
    

    def text():
        return self.__text_history[-1]


    def __str__(self):
        return self.__text_history


########################
# Standalone Functions #
########################
