import code_parser as parser
import sys

if __name__ == "__main__":

    try:
        input_file = sys.argv[1]
        _input = ""
        output_file = sys.argv[2]
        _output = ""
    except:
        print("[ERROR] You forgot to pass program arguments!")
        exit(-1)

    try:
        lexer = parser.get_lexer()
        parser = parser.get_parser()
    except:
        print("[ERROR] Failed to initialize parser")
        exit(-1)

    with open(input_file,'r') as file:
        for line in file:
            _input += line

    res = parser.parse(_input)