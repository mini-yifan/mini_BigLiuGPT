import sentencepiece as spm
import random
import torch

class GPTDataset():
    def __init__(self, model_path, file_path):
        self.model_path = model_path
        self.file_path = file_path
        self.sp = self.load_tokenizer()
        self.train_data, self.val_data = self.load_data()

    # 加载tokenizer
    def load_tokenizer(self):
        sp = spm.SentencePieceProcessor()
        sp.Load(self.model_path)
        return sp

    # 加载数据
    def load_data(self, split_rate=0.8):
        with open(self.file_path, "r", encoding="utf-8") as f:
            text = f.read()
        train_data = text[:int(len(text) * split_rate)]
        val_data = text[int(len(text) * split_rate):]
        sp = self.load_tokenizer()
        train_data = sp.Encode(train_data, out_type=int)
        val_data = sp.Encode(val_data, out_type=int)
        return train_data, val_data

    # 生成数据迭代器
    def seq_data(self, data="train_data", win_len=128, batch_size=10):
        data = self.train_data if data == "train_data" else self.val_data
        data = data[random.randint(0, win_len-1):]
        num_subseqs = (len(data)-1)//win_len
        num_indexs = list(range(0, num_subseqs*win_len, win_len))
        random.shuffle(num_indexs)
        #生成迭代器
        num_batch = len(num_indexs)//batch_size
        for i in range(0, num_batch*batch_size, batch_size):
            x = [data[j:j+win_len] for j in num_indexs[i:i+batch_size]]
            y = [data[j+1:j+win_len+1] for j in num_indexs[i:i+batch_size]]
            yield x, y  #[batch_size, seq_len]


def main():
    liu_gpt = GPTDataset("my_bpe_model.model", "big_liu.txt")
    n = 0
    for x, y in liu_gpt.seq_data(data="train_data", win_len=10, batch_size=3):
        x1 = torch.tensor(x)
        x = liu_gpt.sp.Decode(x, out_type=str)
        y = liu_gpt.sp.Decode(y, out_type=str)
        print(x1.shape)
        print(x, "\n", y, "\n")
        n += 1
        if n > 5:
            break

if __name__ == "__main__":
    main()

