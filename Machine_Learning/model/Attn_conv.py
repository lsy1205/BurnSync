import torch
import torch.nn as nn
import torch.nn.functional as F

class Attn_conv(nn.Module):
    def __init__(self, n_class):
        super(Attn_conv, self).__init__()
        
        # 卷积模块
        self.conv1 = nn.Conv1d(in_channels=6, out_channels=32, kernel_size=3, padding=1)  # 卷积层1
        self.conv2 = nn.Conv1d(in_channels=32, out_channels=64, kernel_size=3, padding=1)  # 卷积层2
        self.batch_norm1 = nn.BatchNorm1d(32)  # 归一化层1
        self.batch_norm2 = nn.BatchNorm1d(64)  # 归一化层2
        
        # 自注意力模块
        self.query = nn.Linear(64, 64)
        self.key = nn.Linear(64, 64)
        self.value = nn.Linear(64, 64)
        self.scale = 64 ** 0.5  # 缩放因子
        
        # 分类头
        self.fc = nn.Linear(64, n_class)  # 最终分类层

    def forward(self, x):
        # 输入形状: (batch_size, 6, 30)
        
        # 卷积模块
        x = self.conv1(x)  # (batch_size, 32, 30)
        x = self.batch_norm1(x)
        x = F.relu(x)
        
        x = self.conv2(x)  # (batch_size, 64, 30)
        x = self.batch_norm2(x)
        x = F.relu(x)
        
        x = x.transpose(1, 2)  # 转换形状以适配 Attention 模块: (batch_size, 30, 64)
        
        # 自注意力模块
        Q = self.query(x)  # (batch_size, 30, 64)
        K = self.key(x)    # (batch_size, 30, 64)
        V = self.value(x)  # (batch_size, 30, 64)
        
        attention_scores = torch.bmm(Q, K.transpose(1, 2)) / self.scale  # (batch_size, 30, 30)
        attention_weights = F.softmax(attention_scores, dim=-1)          # (batch_size, 30, 30)
        attention_output = torch.bmm(attention_weights, V)               # (batch_size, 30, 64)
        
        # 全局平均池化: 聚合时间步信息
        x = attention_output.mean(dim=1)  # (batch_size, 64)
        
        # 分类头
        x = self.fc(x)  # (batch_size, n_class)
        return x