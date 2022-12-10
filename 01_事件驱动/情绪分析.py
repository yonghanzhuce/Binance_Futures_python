# 使用Paddlenlp, 分析一句话是正向还是负向情绪，并导入相应的模块
import paddle
import paddle.nn.functional as F
import paddlenlp as ppnlp
from paddlenlp import Taskflow

def sentiment_analysis(sentence):
    
    schema = '情感倾向[正向，负向]'
    few_ie = Taskflow("sentiment_analysis", schema=schema,model="skep_ernie_1.0_large_ch", batch_size=16)

    result=few_ie(sentence)
    return result

if __name__ == '__main__':
    # 测试
    sentence = '这个电影真的很好看'
    print(sentiment_analysis(sentence))
    sentence = '这个电影真的很差劲'
    print(sentiment_analysis(sentence))
    