class The_Input:
    def __init__(self):
        self.the_input = None
        self.type = None
        self.value = []
        self.reference = ['A_Custom_Attribute']
        self.A_Custom_Attribute=A_Custom_Attribute()
class A_Custom_Attribute:
    def __init__(self):
        self.a_custom_attribute = None
        self.type = None
        self.value = []
        self.reference = ['The_Project']
        self.The_Project=The_Project()
class The_Project:
    def __init__(self):
        self.the_project = None
        self.type = None
        self.value = []
        self.reference = ['Its_Key']
        self.Its_Key=Its_Key()
class Its_Key:
    def __init__(self):
        self.its_key = None
        self.type = 'list'
        self.value = []
        self.reference = ['Authority']
        self.Authority=Authority()
class Authority:
    def __init__(self):
        self.authority = None
        self.type = None
        self.value = []
        self.reference = ['The_Value']
        self.The_Value=The_Value()
class The_Value:
    def __init__(self):
        self.the_value = None
        self.type = "None"
        self.value = None


class The_Input:
    def __init__(self):
        self.the_input = None
        self.type = None
        self.value = []
        self.reference = ['A_Single_Integer_T', 'The_T_Cases']
        self.A_Single_Integer_T=A_Single_Integer_T()
        self.The_T_Cases=The_T_Cases()
class A_Single_Integer_T:
    def __init__(self):
        self.a_single_integer_t = None
        self.type = "integer"
        self.value = None
class The_T_Cases:
    def __init__(self):
        self.the_t_cases = None
        self.type = 'list'
        self.value = []
        self.reference = ['Each_Test_Case']
        self.Each_Test_Case=Each_Test_Case()
class Each_Test_Case:
    def __init__(self):
        self.each_test_case = None
        self.type = None
        self.value = []
        self.reference = ['A_Line', 'Each_Line']
        self.A_Line=A_Line()
        self.Each_Line=Each_Line()
class A_Line:
    def __init__(self):
        self.a_line = None
        self.type = None
        self.value = []
        self.reference = ['An_Integer']
        self.An_Integer=An_Integer()
class An_Integer:
    def __init__(self):
        self.an_integer = None
        self.type = "integer"
        self.value = None
class Each_Line:
    def __init__(self):
        self.each_line = None
        self.type = None
        self.value = []
        self.reference = ['Characters']
        self.Characters=Characters()
class Characters:
    def __init__(self):
        self.characters = None
        self.type = "character"
        self.value = []
