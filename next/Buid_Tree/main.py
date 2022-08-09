import spacy


"""nlp处理数据"""
nlp = spacy.load("en_core_web_sm")

text = ["The input contains a single integer T that indicates the number of test cases.",
        "Then follow the T cases.",
        "Each test case begins with a line contains an Integer N, represent the original wall.",
        "Each line contains N characters"]

'''
all_key_phrases 记录文本的所有关键短语 [[句子1关键短语]...[句子n关键短语]]

[['The input', 'a single integer T'],  明显这个test case也是关键短语，但是把of当作关键短语的tag很不合理
['the T cases'], 
['Each test case', 'a line', 'an Integer N'], 
['Each line', 'characters']]  明显这个characters少了一个关键的组成N，关键短语应该是N characters（POS：{NNP,NN}）
'''
all_key_phrases = []
"""
map_key_list 记录每一句的第一个关键短语作为key，剩余所有关键短语作为value
对于['The input', 'a single integer T']
其对应map为{'The input':['The input', 'a single integer T']}
"""
map_key_list = {}

for t in text:
    doc = nlp(t)
    '''
    each_sent_noun_phrase 记录每个句子的名词短语
    [('The input', 'contains'), ('a single integer T', 'contains'), ...,  ('test cases', 'of')]
    '''
    each_sent_noun_phrase = []
    for np in doc.noun_chunks:
        each_sent_noun_phrase.append((np.text, np.root.head.text))
    # print(each_sent_noun_phrase)
    key_phrases_tag = ["begins", "contains", "with", "follow"]
    '''
    each_sent_key_phrases 记录每个句子的关键短语
    ['The input', 'a single integer T']
    '''
    each_sent_key_phrases = []
    for i in each_sent_noun_phrase:
        if i[1] in key_phrases_tag:
            each_sent_key_phrases.append(i[0])
    all_key_phrases.append(each_sent_key_phrases)
    map_key_list[each_sent_key_phrases[0]] = each_sent_key_phrases
print(all_key_phrases)
"""查找关键短语中是否有 数据类型"""


def find_type(key_phrase):
    def_type = ["integer", "string", "character", "char", "int", "boolean"]
    for tp in def_type:
        if tp in key_phrase:
            return tp


class Node:
    def __init__(self, noun, noun_type=None, parent=None):
        super(Node, self).__init__()
        self.value = noun
        self.type = noun_type
        self.index = 0
        self.parent = parent
        self.child = {}

    def get_child(self, name, def_value=None):
        """获取当前节点的子节点"""
        return self.child.get(name, def_value)

    def add_child(self, obj=None):
        """在当前节点处，增加子节点"""
        if not isinstance(obj, Node):
            raise ValueError("添加子节点的type错误，不是一个node")
        obj.parent = self
        self.child[self.index] = obj
        self.index += 1
        return obj

    def find_child(self):
        pass

    def items(self):
        return self.child.items()

    def dump(self, indent=0):
        """打印出树结构"""
        tab = "     " * (indent - 1) + "|-" if indent > 0 else ""
        print("%s%s" % (tab, self.value))
        for name, obj in self.items():
            obj.dump(indent + 1)


"""input_tag用于识别roots中是否有the input,etc作为一个需求对应的规范树的root"""
input_tags = ["the input"]

"""输入参数tree node为各个句子的子树根节点 ['The input', 'the T cases', 'Each test case', 'Each line']"""


def step1(tree_node):
    root = Node("the input")
    for node in tree_node:
        if node in input_tags:
            root = Node(node)
    return root


"""
roots一对多关系判断挖掘 return 0 一对多关系 1 多对一关系  
"""


def get_multi_relation(root_name1, root_name2):
    pass


"""
roots一对一关系判断挖掘 return 0 没有一对一关系 1 一对一关系  
"""


def get_single_relation(root_name1, root_name2):
    pass


# 假设一个需求只有10个句子
root_node_name = ["root1", "root2", "root3", "root4", "root5", "root6", "root7", "root8", "root9", "root10"]
"""subtree为1代表是子树，为0代表不是子树"""
subtree = []

if __name__ == '__main__':
    sent_root = list(map_key_list.keys())
    print(sent_root)
    for en in range(len(sent_root)):
        root_node_name[en] = Node(sent_root[en], find_type(sent_root[en]))
        subtree[en] = 1
    print(root_node_name[0])
    """
    构造规范树 基于Node类
        规则：
            1.首先查看子树的roots中有无the input类似节点，若有则作为规范树根节点，若无则创建根节点value（即name）= the input
            2.再查询所有子树roots，若有"一对多关系"，如the T cases |-> Each test case，则将Each test case作为the T cases的子节点
            3.对于所有不符合step2的句子（即仍是子树的句子），将这些句子的roots中的一个root1去遍历其他roots所代表子树的所有节点，
              如果有"一对一关系"，将这个root加到与其"一对一"节点的父节点上，如Each line == a line，则Each line所在子树加到a line所在子树上
            4.最终所有子树连接到the input节点，形成 Specification Tree，根节点为 the input
    """
    # step1
    spec_tree_root = step1(sent_root)
    try:
        subtree[sent_root.index(spec_tree_root.value)] = 0
    except:
        pass
    # step2
    for n in range(len(subtree)):
        ro = root_node_name[n]
        for m in range(len(subtree)):
            roo = root_node_name[m]
            if get_multi_relation(ro.value, roo.value) == 0:
                ro.add_child(roo)
                subtree[m] = 0
            elif get_multi_relation(ro.value, roo.value) == 0:
                roo.add_child(ro)
                subtree[n] = 0
            else:
                pass
    # step3
    for k in range(len(subtree)):
        if subtree[k] == 1:  # 是子树
            for sent_key_p in all_key_phrases:
                for k_p in sent_key_p:
                    if get_single_relation(root_node_name[k].value, k_p):
                        ind = sent_key_p.index(k_p) - 1
                        Node(sent_key_p[ind]).add_child(root_node_name[k])

    # step4
