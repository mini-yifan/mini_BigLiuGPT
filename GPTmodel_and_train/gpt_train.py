from my_gpt_model import GPTconfig, GPTmodel
from GPTDataset import GPTDataset
import torch
import torch.nn as nn
import torch.optim as optim
import csv
#from torch.utils.tensorboard import SummaryWriter

#writter = SummaryWriter(log_dir='./tf-logs')#tensorboard启动命令：在所在文件目录下 tensorboard --logdir tf-logs

def training_loop(model, liu_gpt, optimizer, device, epochs, win_len, batch_size):
    loss_list = []
    loss_list_val = []
    for epoch in range(1, epochs + 1):
        i_num = 0  # 记录循环次数
        loss_sum = 0
        loss_sum_val = 0
        # 训练
        model.train()
        for train_x, train_y in liu_gpt.seq_data(data="train_data", win_len=win_len, batch_size=batch_size):
            train_x = torch.tensor(train_x).to(device=device)
            train_y = torch.tensor(train_y).to(device=device)
            _, loss = model(train_x, train_y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            loss_sum += loss.item()
            i_num += 1
            print(loss_sum)
        loss_mean = loss_sum / i_num
        if epoch % 20 == 0:
            print("epoch:", epoch, "loss:", loss_mean, "-----------train")
            loss_list.append(loss_mean)
        model.eval()
        with torch.no_grad():
            i_num_val = 0
            for test_x, test_y in liu_gpt.seq_data(data="val_data", win_len=win_len, batch_size=batch_size):
                test_x = torch.tensor(test_x).to(device=device)
                test_y = torch.tensor(test_y).to(device=device)
                _, loss_val = model(test_x, test_y)
                loss_sum_val += loss_val.item()
                i_num_val += 1
            loss_mean_val = loss_sum_val / i_num_val
            if epoch % 20 == 0:
                print("epoch:", epoch, "val loss:", loss_mean_val, "------val")
                loss_list_val.append(loss_mean_val)
        #writter.add_scalars("train_val_loss", {"train_loss": loss_mean, "val_loss": loss_mean_val}, epoch)
    return loss_list, loss_list_val

def main():
    device = (torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu'))  # GPU设备
    config = GPTconfig()
    model = GPTmodel(config).to(device=device)
    liu_gpt = GPTDataset("my_bpe_model.model", "big_liu.txt")

    epochs = 2
    optimizer = optim.AdamW(model.parameters(), lr=1e-3)
    win_len = config.seq_len
    batch_size = 80
    loss_list, loss_list_val = training_loop(model, liu_gpt, optimizer, device, epochs, win_len, batch_size)

    model.cpu()
    torch.save(model.state_dict(), "my_gpt_model.pt")
    torch.save(model, "my_gpt_model_net.pth")

    with open("loss_list.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        for i in range(len(loss_list)):
            writer.writerow([loss_list[i], loss_list_val[i]])
    print("数据写入:loss_list")

if __name__ == "__main__":
    main()