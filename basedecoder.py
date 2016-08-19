from cipher import CipherType

class BaseDecoder(object):
    
    def __init__(self, inputs: list):
        """
        Args
        -
        """
        self.inputs = inputs
        self.results = None

        self.key_functs = {}
        self.key_satified = {}
        self.key_description = {}
        self.key_values = {}


    def add_input(self, input_str: str) -> None:
        self.inputs.append(input_str)

    def add_key(self, key_list: list) -> None:
        """
        Add a key. Keys MUST be lowercase.

        A key is anything that is needed to help
        decode the input using a particulat method.
        All keys must be provided before decoding
        can being on the inputs.

        key_list -- list of tuples with the key id,
            followed by a function used to promt the
            user and set the key, followed by a description
            of what the key is and does
        """

        for key, funct, desc in key_list:
            
            # Force keys to be lowercase
            key = key.lower()
            
            self.key_functs[key] = funct
            self.key_satified[key] = False
            self.key_description[key] = desc
            self.key_values[key] = None
    

    def has_keys(self) -> bool:
        """
        Returns whether the all of the keys have been satisfied.
        """
        
        for key, value in self.key_satified.items():
            if value is not True:
                return False
        return True

    
    def can_decode(self) -> bool:
        """
        Does the decoder have enough information to decode the ciphertext.
        This can be overriden if more than just the value of has keys should
        determine if a message can be decoded.
        """
        return self.has_keys()


    def describe_key(self, key: str) -> str:
        return self.key_description[key]

    
    def set_key(self, key, value) -> True:
        """
        Sets the value of a key.

        Sets the value of a key, and validates that value.
        Returns True if the key was valid and set correctly.
        """

        if key in self.key_functs:
            # Validate the value
            real_val = self.key_functs[key](value)
            
            if real_val is not None:
                self.key_values[key] = real_val 
                self.key_satified[key] = True
                return True

        # Invalid key
        return False


    def get_key_list(self) -> list:
        """
        Get the list of keys this decoder needs.
        """
        return self.key_functs.keys()


    def get_key(self, key) -> dict:
        return self.key_values[key]


    def decode(self):
        raise NotImplementedError


    @property
    def results(self) -> list:
        """
        Get the results from the decoder.

        Returns the results from the decoder,
        or none if the inputs have not been
        decoded yet.
        """
        return self.__results


    @results.setter
    def results(self, results):
        self.__results = results

    @staticmethod
    def type() -> CipherType:
        raise NotImplementedError
