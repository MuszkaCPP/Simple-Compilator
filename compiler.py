import code_parser
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
        lexer = code_parser.get_lexer()
        parser = code_parser.get_parser()
        code_generator = code_parser.get_code_generator()
    except:
        print("[ERROR] Failed to initialize parser")
        exit(-1)

    with open(input_file,'r') as file:
        for line in file:
            _input += line

    res = parser.parse(_input, tracking=True)
    with open(output_file,'w') as file:
        file.writelines(code_generator.get_generated_code())