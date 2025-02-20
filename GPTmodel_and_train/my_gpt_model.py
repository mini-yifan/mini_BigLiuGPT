import torch
from torch import nn
from torchinfo import summary
import torch.nn.functional as F
import math
import sentencepiece as spm

class GPTconfig:
    vocab_size: int = 8000  # 词表大小
    seq_len: int = 224  # 序列长度,即模型将接收和处理的每个样本中的单词数量
    embed_dim: int = 224  # 嵌入维度
    n_head: int = 7  # 注意力头数
    n_layer: int = 8  # Transformer层数
    dropout: float = 0.3
    device = (torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu'))

class PositionalEncoding(nn.Module):
    """位置编码"""
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.dropout = nn.Dropout(self.config.dropout)
        self.P = torch.zeros((1, config.seq_len, config.embed_dim)).to(device = self.config.device)
        X = torch.arange(config.seq_len, dtype=torch.float).reshape(-1, 1)/\
            torch.pow(10000, torch.arange(0, config.embed_dim, 2, dtype=torch.float)/config.embed_dim)
        self.P[:, :, 0::2] = torch.sin(X)
        self.P[:, :, 1::2] = torch.cos(X)

    def forward(self, x):
        #x: [batch_size, seq_len, embed_dim]
        x = x + self.P[:, :x.shape[1], :].requires_grad_(False) #位置编码不求梯度
        return self.dropout(x)

class LayerNorm(nn.Module):
    """层归一化"""
    def __init__(self, config):
        super().__init__()
        self.embed_dim = config.embed_dim
        self.LayerNorm = nn.LayerNorm(self.embed_dim)

    def forward(self, x):
        out = self.LayerNorm(x)
        return out


class SelfAttention(nn.Module):
    """自注意力机制"""
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.attn_dropout = nn.Dropout(config.dropout)

    def mask_softmax(self, attn):
        """掩码softmax"""
        seq_len = attn.size(-1)
        mask = torch.tril(torch.ones(seq_len, seq_len))\
            .view(1, seq_len, seq_len).requires_grad_(False)#创建一个下三角矩阵,不更新梯度
        mask = mask.to(device = self.config.device)
        attn = attn.masked_fill(mask[:, :seq_len, :seq_len] == 0, float('-inf'))
        attn = F.softmax(attn, dim=-1)
        return attn

    def forward(self, q, k, v):
        attn = torch.bmm(q, k.transpose(-2, -1))/math.sqrt(self.config.seq_len)#transpose() 函数在 PyTorch 中用于交换张量的两个维度
        attn = self.mask_softmax(attn)
        attn = torch.bmm(self.attn_dropout(attn), v)
        return attn


class MultiHeadAttention(nn.Module):
    """多头自注意力机制"""
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.wk = nn.Linear(config.embed_dim, config.embed_dim)
        self.wq = nn.Linear(config.embed_dim, config.embed_dim)
        self.wv = nn.Linear(config.embed_dim, config.embed_dim)
        self.selfattention = SelfAttention(config)
        self.wo = nn.Linear(config.embed_dim, config.embed_dim)

    def transpose_qkv(self, qkv):
        """将qkv的维度进行转换，分出n_head个头"""
        qkv = qkv.reshape(qkv.shape[0], qkv.shape[1], self.config.n_head, -1) #[batch_size, seq_len, embed_dim]->[batch_size, seq_len, n_head, embed_dim/n_head]
        qkv = qkv.permute(0, 2, 1, 3) #[batch_size, n_head, seq_len, embed_dim/n_head]
        qkv = qkv.reshape(-1, qkv.shape[2], qkv.shape[3]) #[batch_size*n_head, seq_len, embed_dim/n_head]
        return qkv

    def output_cat(self, attn):
        """将transpose_qkv操作反转"""
        attn = attn.reshape(-1, self.config.n_head, attn.shape[1], attn.shape[2]) #[batch_size*n_head, seq_len, embed_dim/n_head]->[batch_size, n_head, seq_len, embed_dim/n_head]
        attn = attn.permute(0, 2, 1, 3) #[batch_size, seq_len, n_head, embed_dim/n_head]
        attn = attn.reshape(attn.shape[0], attn.shape[1], -1) #[batch_size, seq_len, embed_dim]
        return attn

    def forward(self, x):
        k = self.transpose_qkv(self.wk(x))
        q = self.transpose_qkv(self.wq(x))
        v = self.transpose_qkv(self.wv(x))
        attn = self.selfattention(q, k, v) #[batch_size*n_head, seq_len, embed_dim/n_head]
        attn = self.output_cat(attn)
        return self.wo(attn)


class FeedForward(nn.Module):
    """两个全连接层的mlp"""
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.net = nn.Sequential(
            nn.Linear(config.embed_dim, 4 * config.embed_dim),
            nn.GELU(),
            nn.Linear(4 * config.embed_dim, config.embed_dim),
            nn.Dropout(config.dropout),
        )

    def forward(self, x):
        x = self.net(x)
        return x


class Block(nn.Module):
    """Transformer块"""
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.ln1 = LayerNorm(config)
        self.attn = MultiHeadAttention(config)
        self.ln2 = LayerNorm(config)
        self.ffn = FeedForward(config)

    def forward(self, x):
        out = self.attn(self.ln1(x))
        out = x + out
        out2 = self.ffn(self.ln2(out))
        out2 = out + out2
        return out2


class GPTmodel(nn.Module):
    """主模型"""
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.embeding = nn.Embedding(config.vocab_size, config.embed_dim)
        self.position = PositionalEncoding(config)
        self.blocks = nn.Sequential(*[Block(config) for _ in range(config.n_layer)])
        self.ln = LayerNorm(config)
        self.final_linear = nn.Linear(config.embed_dim, config.vocab_size, bias=False)
        self.apply(self._init_weights)

    #初始化参数
    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, features, targets=None):
        x = self.position(self.embeding(features))
        x = self.blocks(x)
        x = self.ln(x)
        x = self.final_linear(x)  # x: [batch_size, seq_len, embed]->[batch_size, seq_len, vocab_size]
        if targets is None:
            loss = None
        else:
            x = x.view(-1, x.shape[-1])#x: [batch_size*seq_len, vocab_size]
            targets = targets.view(-1)#targets: [batch_size*seq_len]
            loss = F.cross_entropy(x, targets)
        return x, loss

    @torch.no_grad()
    def genarate(self, seq, max_new_tokens):
        for _ in range(max_new_tokens):
            x = seq[:, -self.config.seq_len:] #seq: [batch_size, seq_len]
            self.config.seq_len = x.shape[1]
            new_w, _ = self.forward(x) #new_w: [batch_size, seq_len, vocab_size]
            new_w = new_w[:, -1, :]
            new_w = F.softmax(new_w, dim=-1)
            new_token_index = torch.multinomial(new_w, num_samples=1)#从新词概率分布中采样（抽取）一个新词
            seq = torch.cat((seq, new_token_index), dim=1)
        return seq

def main():
    config = GPTconfig()
    model = GPTmodel(config)
    summary(model, input_size=([100, config.seq_len]), dtypes=[torch.long])

    model_path = 'my_bpe_model.model'  # 这里填写你的模型文件路径
    sp = spm.SentencePieceProcessor(model_file=model_path)

    text = ""
    x = torch.tensor([sp.Encode(text)])
    out_tensor = model.genarate(x, max_new_tokens=30)
    out = sp.Decode(out_tensor.tolist()[0])
    print(out)

if __name__ == '__main__':
    main()
    '''
    mask = torch.tril(torch.ones(GPTconfig.seq_len, GPTconfig.seq_len)) \
        .view(1, GPTconfig.seq_len, GPTconfig.seq_len).requires_grad_(False)  # 创建一个下三角矩阵,不更新梯度
    print(mask.shape)
    '''