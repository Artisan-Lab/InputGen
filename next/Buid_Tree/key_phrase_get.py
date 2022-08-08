import jieba.analyse

corpus = "Create a custom attribute on the project,the project id is #%1,key is #%authority,the value is #%0."
#textrank
keywords_textrank = jieba.analyse.textrank(corpus, withWeight=True, allowPOS=('ns', 'n'), withFlag=True)
print(keywords_textrank)


