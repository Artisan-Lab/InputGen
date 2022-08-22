# InputGen
InputGen is a tool that automatically generates test cases based on unstructured natural language descriptions, and can be subsequently applied to automated requirement testing of REST APIs.

The main function of InputGen is to mine the format information of the test case according to the requirement description, and then combine the input information into the structure of the information tree according to the predefined rules. The specific steps can be divided into: noun phrase extraction, key phrase mining, information tree generation, test case structure code generation, test case generation.

## Using InputGen

1. First put the requirement description in the folder `./next/Build_Tree/requirements`, UTF-8 encoding.

2. Run the file `./next/generation/class_generation.py` to generate the structure file corresponding to the information tree.
```bash
python3 class_generation.py
```
3.The structure file is generated in the file `./next/pre_class.py`.

4.Run the file `./next/generation/test_case_generation.py`. Finally, specific test cases corresponding to the requirements will be generated.
```bash
python3 test_case_generation.py
```
