from my_gpt_model import GPTconfig, GPTmodel
import torch
import sentencepiece as spm


def main():
    # 加载已经训练好的SentencePiece模型
    model_path = 'my_bpe_model.model'  # 这里填写你的模型文件路径
    sp = spm.SentencePieceProcessor(model_file=model_path)

    while True:
        # 待分词的文本
        text = input("请输入待分词的文本：")
        if text == "exit":
            break
        x = torch.tensor([sp.Encode(text)])
        #print(x)

        config = GPTconfig()
        clone_model = GPTmodel(config)
        clone_model.load_state_dict(torch.load("my_gpt_model.pt"))
        clone_model.eval()
        out_tensor = clone_model.genarate(x, 100)
        out = sp.Decode(out_tensor.tolist()[0])
        print(out)

if __name__ == '__main__':
    main()