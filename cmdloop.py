from cmd import Cmd
from raildecoder import RailDecoder
from basedecoder import BaseDecoder
from cipher import *

class CmdRunner(Cmd):


    def __init__(self):
        super().__init__()

        # Cmd configuration vars
        self.prompt = '>>> '

        # Other vars
        self.history = CipherHistory()


    ####################
    # Helper Functions #
    ####################


    def _parse_line_args(self, line: str) -> list:
        within_quote = False
        escape_next_char = False
        arg_list = []
        word = ''
        for char in line:
            if not escape_next_char and char == '\\':
                escape_next_char = True

            elif escape_next_char:
                # Actually escape this character
                escape_next_char = False
                word += char

            elif not within_quote and char == '\"':
                within_quote = True

            elif within_quote and char == '\"':
                # End quotes, ignore the quote marks themselves
                within_quote = False

            elif not within_quote and char == ' ':
                # Skip spaces not within a quote
                if word != '':
                    # Push the word to the arg list
                    arg_list.append(word)
                    word = ''

            else:
                word += char

        # Push the last remaining word if it needs to be
        if word != '':
            arg_list.append(word)

        return arg_list

    
    def __inst(self) -> CipherInstance:
        return self.history.curr()

    def _decoder(self) -> BaseDecoder:
        return self.__inst().decoder

    #################
    # Cmd Functions #
    #################

    def do_key(self, line):
        args = self._parse_line_args(line)
        
        if len(args) == 0:
            print("Usage: key info")
            return
        
        if not self.__inst().has_decoder():
            print('Set the decoder type first')
            return
        
        sub_cmd = args[0]
        keys = self._decoder().get_key_list()

        if sub_cmd == 'info':
            print('=' * 15 + ' KEYS ' + '=' * 15)
            for key in keys:
                print('   ' + key.upper() + ': ' + self._decoder().describe_key(key))
        elif sub_cmd == 'set':
            if len(args) != 3:
                print('Need more arguments to set a key')
                return

            key = args[1].lower()
            val = args[2]
            if key in keys:
                valid = self._decoder().set_key(key, val)
                if valid:
                    print('Key set')
                else:
                    print('Value not valid for key')
        elif sub_cmd == 'list':
            if len(args) != 2:
                print('Need more arguments to set a key')
                return

            key = args[1].lower()
            print('   ' + key.upper() + ' = ' + str(self._decoder().get_key(key)))


    def do_addtext(self, line):
        args = self._parse_line_args(line)
        for arg in args:
            print('Added \'%s\'' % arg)
            self.__inst().add_input(arg)

    def do_type(self, line):
        args = self._parse_line_args(line)
        if len(args) == 0:
            type_ = self.__inst().get_type()
            print('Type: ' + str(type_))
            return
        elif len(args) != 1:
            print('Invalid type')
            return
        
        cipher_type = args[0]
        for enum_type in CipherType:
            print('Type: ' + str(enum_type))
        was_set = self.__inst().set_type(CipherType.RAIL_FENCE)
        print('Was set: ' + str(was_set))


    def do_decode(self, line):
        text = self.__inst().decode()
        print(text)


    def do_test(self, line):
        obj = self.history.curr()
        print(obj)
        obj.get_inputs()
        # self.decoder = RailDecoder(self._parse_line_args(line))
        # print('Decoder set')
        # decoder.decode()
        # print(decoder.type())
    

    def do_reset(self, line):
        self.history = CipherHistory()


    def do_EOF(self, line):
        return True


    def do_quit(self, line):
        return True


    def do_exit(self, line):
        return True


    ########################
    # Completion Functions #
    ########################
