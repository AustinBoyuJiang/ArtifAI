import numpy as np
import os
import glob
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import Sequence
from sklearn.model_selection import train_test_split

# 文件夹路径
data_paths = {
    "created_with_ai": {
        "processed_training_data_dir": "..\\data\\data\\processed\\training\\created_with_ai",
        "processed_testing_data_dir": "..\\data\\data\\processed\\testing\\created_with_ai"
    },
    "not_created_with_ai": {
        "processed_training_data_dir": "..\\data\\data\\processed\\training\\not_created_with_ai",
        "processed_testing_data_dir": "..\\data\\data\\processed\\testing\\not_created_with_ai"
    }
}


# 数据生成器
class DataGenerator(Sequence):
    def __init__(self, files, labels, batch_size):
        self.files = files
        self.labels = labels
        self.batch_size = batch_size

    def __len__(self):
        return int(np.ceil(len(self.files) / self.batch_size))

    def __getitem__(self, idx):
        batch_x = self.files[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_y = self.labels[idx * self.batch_size:(idx + 1) * self.batch_size]

        return np.array([self.load_and_preprocess(file) for file in batch_x]), np.array(batch_y)

    def load_and_preprocess(self, file_path):
        image = np.load(file_path)
        # 如果图像是灰度的，将其转换为三通道
        if image.ndim == 2:
            image = np.stack((image,) * 3, axis=-1)
        return image


# 加载文件名和标签
def load_filenames_and_labels(paths):
    files = []
    labels = []
    for path, label in paths.items():
        tot = len(glob.glob(os.path.join(path, '*.npy')))
        for i, file in enumerate(glob.glob(os.path.join(path, '*.npy'))):
            files.append(file)
            labels.append(label)
            print(f"({i+1}/{tot})")
    return files, labels


# 构建模型
def build_model(input_shape):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model


# 主函数
def main():
    # 加载训练文件名和标签
    training_paths = {
        data_paths['created_with_ai']['processed_testing_data_dir']: 1,
        data_paths['not_created_with_ai']['processed_testing_data_dir']: 0
    }
    X_train_files, y_train = load_filenames_and_labels(training_paths)

    # 加载测试文件名和标签
    testing_paths = {
        data_paths['created_with_ai']['processed_training_data_dir']: 1,
        data_paths['not_created_with_ai']['processed_training_data_dir']: 0
    }
    X_test_files, y_test = load_filenames_and_labels(testing_paths)

    # 定义训练和测试生成器
    train_generator = DataGenerator(X_train_files, y_train, batch_size=32)
    test_generator = DataGenerator(X_test_files, y_test, batch_size=32)

    # 构建模型
    model = build_model((256, 256, 3))  # 确保这里的尺寸与您的图像数据相匹配

    # 训练模型
    model.fit(train_generator, epochs=10, validation_data=test_generator)

    # 保存模型到本地目录
    model.save('**/src/models/model.h5')  # 指定模型保存的路径

    # 使用测试数据评估模型
    test_loss, test_accuracy = model.evaluate(test_generator)
    print(f"Test Accuracy: {test_accuracy:.4f}")

if __name__ == "__main__":
    main()