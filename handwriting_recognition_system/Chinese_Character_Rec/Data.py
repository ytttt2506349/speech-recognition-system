
from torchvision import transforms
from PIL import Image
from torch.utils.data import Dataset


class MyDataset(Dataset):
    def __init__(self, txt_path, num_class, transforms=None):
        super(MyDataset, self).__init__()
        images = []
        labels = []
        with open(txt_path, 'r') as f:
            for line in f:
                if int(line.split('\\')[1]) >= num_class:
                    break
                line = line.strip('\n')
                images.append(line)
                labels.append(int(line.split('\\')[1]))
        self.images = images
        self.labels = labels
        self.transforms = transforms

    def __getitem__(self, index):
        image = Image.open(self.images[index]).convert('RGB')
        label = self.labels[index]
        if self.transforms is not None:
            image = self.transforms(image)
        return image, label

    def __len__(self):
        return len(self.labels)
# 测试集/推理用的图像预处理（transform_test）
transform_test = transforms.Compose([
    transforms.Resize((64, 64)),  # 图像缩放到64x64（可根据你的模型调整尺寸）
    transforms.Grayscale(num_output_channels=1),  # 转为灰度图
    transforms.ToTensor(),  # 转为Tensor
    transforms.Normalize(mean=[0.5], std=[0.5])  # 归一化
])