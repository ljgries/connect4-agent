import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class Connect4Model(nn.Module):
	def __init__(self, device):
		super().__init__()
		self.device = device
		# define the layers

		# conv
		self.initial_conv = nn.Conv2d(3, 128, kernel_size=3, stride=1, padding=1, bias=True)
		self.initial_bn = nn.BatchNorm2d(128)

		# Res block 1
		self.res1_conv1 = nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1, bias=False)
		self.res1_bn1 = nn.BatchNorm2d(128)
		self.res1_conv2 = nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1, bias=False)
		self.res1_bn2 = nn.BatchNorm2d(128)

		# Res block 2
		self.res2_conv1 = nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1, bias=False)
		self.res2_bn1 = nn.BatchNorm2d(128)
		self.res2_conv2 = nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1, bias=False)
		self.res2_bn2 = nn.BatchNorm2d(128)

		# value head
		self.value_conv = nn.Conv2d(128, 3, kernel_size=1, stride=1, bias=True)
		self.value_bn = nn.BatchNorm2d(3)
		self.value_fc = nn.Linear(3*6*7,32)
		self.value_head = nn.Linear(32,1)

		# policy head
		self.policy_conv = nn.Conv2d(128, 32, kernel_size=1, stride=1, bias=True)
		self.policy_bn = nn.BatchNorm2d(32)
		self.policy_head = nn.Linear(32*6*7,7)
		self.policy_ls = nn.LogSoftmax(dim=1)

		self.to(device)

	def forward(self,x):
		# define connections between the layers
		# x will be shape (3, 6, 7)

		# add dimension for batch size
		x = x.view(-1, 3, 6, 7)
		x = F.relu(self.initial_bn(self.initial_conv(x)))

		# Res Block 1
		res = x
		x = F.relu(self.res1_bn1(self.res1_conv1(x)))
		x = F.relu(self.res1_bn2(self.res1_conv2(x)))
		x = F.relu(x + res)  # Modified line

		# Res Block 2
		res = x
		x = F.relu(self.res2_bn1(self.res2_conv1(x)))
		x = F.relu(self.res2_bn2(self.res2_conv2(x)))
		x = F.relu(x + res)  # Modified line

		# value head
		v = F.relu(self.value_bn(self.value_conv(x)))
		v = v.view(v.size(0), -1)  # Flatten the tensor while keeping the batch dimension
		v = F.relu(self.value_fc(v))
		v = torch.tanh(self.value_head(v))  # Output shape should be [batch_size, 1]

		# policy head
		p = F.relu(self.policy_bn(self.policy_conv(x)))
		p = p.view(-1,32*6*7)
		p = F.relu(self.policy_head(p))
		p = self.policy_ls(p).exp()

		return v, p

if __name__ == "__main__":
	device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
	model = Connect4Model(device) # instantiate model
	print(model)
