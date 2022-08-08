class The_Input:
    def __init__(self):
        self.the_input = None
        self.type = "root"
        self.value = None
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
        self.type="list"
        self.value = []
        self.reference = "Each_Test_Case"  # 根据cases判断这是一个列表，得到列表长度为T，列表中的值为Each_Test_Case
        self.Each_Test_Case=Each_Test_Case()
class Each_Test_Case:
    def __init__(self):
        self.each_test_case = None
        self.type = "int"
        self.value = None