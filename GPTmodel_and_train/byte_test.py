import sentencepiece as spm

# 设置训练参数
input_file = 'big_liu.txt'  # 训练数据文件路径
model_prefix = 'my_bpe_model'  # 输出模型文件的前缀
vocab_size = 8000  # 目标词汇表大小
model_type = 'bpe'  # 使用BPE模型类型

# 初始化训练配置
spm.SentencePieceTrainer.Train(
    f'--input={input_file} '
    f'--model_prefix={model_prefix} '
    f'--vocab_size={vocab_size} '
    f'--model_type={model_type} '
    '--max_sentence_length=1000 '  # 可选，设置句子的最大长度
    '--pad_id=0 --pad_piece=[PAD] '  # 定义PAD符号
    '--unk_id=1 --unk_piece=[UNK] '  # 定义UNK符号
    '--bos_id=2 --bos_piece=[BOS] '  # 定义BOS符号
    '--eos_id=3 --eos_piece=[EOS] '  # 定义EOS符号
    #分别指定了填充（PAD）、未知（UNK）、开始（BOS）、结束（EOS）符号的ID及它们对应的符号文本。
)

print(f"Model has been trained and saved as {model_prefix}.model")