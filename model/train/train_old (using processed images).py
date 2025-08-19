import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import tensorflow as tf
import seaborn as sns
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import Sequence
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator

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
        self.datagen = ImageDataGenerator(
            featurewise_center=False,  # set input mean to 0 over the dataset
            samplewise_center=False,  # set each sample mean to 0
            featurewise_std_normalization=False,  # divide inputs by std of the dataset
            samplewise_std_normalization=False,  # divide each input by its std
            zca_whitening=False,  # apply ZCA whitening
            rotation_range=30,  # randomly rotate images in the range (degrees, 0 to 180)
            zoom_range=0.2,  # Randomly zoom image
            width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
            height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
            horizontal_flip=True,  # randomly flip images
            vertical_flip=True
            # 添加其他您需要的变换
        )

    def __len__(self):
        return int(np.ceil(len(self.files) / self.batch_size))

    def __getitem__(self, idx):
        batch_x = self.files[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_y = self.labels[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_x_processed = np.array([self.load_and_preprocess(file) for file in batch_x])
        batch_x_augmented = np.array([self.datagen.random_transform(img) for img in batch_x_processed])
        return batch_x_augmented, np.array(batch_y)

    def load_and_preprocess(self, file_path):
        image = np.load(file_path)
        if image.ndim == 2:
            image = np.stack((image,) * 3, axis=-1)
        return image


# 加载文件名和标签
def load_filenames_and_labels(paths):
    files = []
    labels = []
    tot = 1200  # float("INF")
    for path, label in paths.items():
        tot = min(tot, len(glob.glob(os.path.join(path, '*.npy'))))
    for path, label in paths.items():
        for i, file in enumerate(glob.glob(os.path.join(path, '*.npy'))):
            files.append(file)
            labels.append(label)
            print(f"({i + 1}/{tot})")
            if i + 1 >= tot:
                break
    return files, labels


# 定义CNN模型
def build_model():
    model = Sequential([
        Conv2D(32, (3, 3), padding="same", activation="relu", input_shape=(256, 256, 3)),
        MaxPooling2D(),
        Conv2D(32, (3, 3), padding="same", activation="relu"),
        MaxPooling2D(),
        Conv2D(64, (3, 3), padding="same", activation="relu"),
        MaxPooling2D(),
        Dropout(0.4),
        Flatten(),
        Dense(128, activation="relu"),
        Dense(2, activation="softmax")
    ])
    return model


# 绘图函数
def plot_training_history(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs_range = range(len(acc))  # 修改这里

    plt.figure(figsize=(15, 15))
    plt.subplot(2, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(2, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()


def main():
    # 加载训练文件名和标签
    training_paths = {
        data_paths['created_with_ai']['processed_training_data_dir']: 1,
        data_paths['not_created_with_ai']['processed_training_data_dir']: 0
    }
    X_train_files, y_train = load_filenames_and_labels(training_paths)

    cnt = []
    for i in y_train:
        if i == 0:
            cnt.append("not created with ai")
        else:
            cnt.append("created with ai")
    sns.set_style('darkgrid')
    sns.countplot(cnt)
    # plt.show()
    # plt.figure(figsize=(5, 5))
    # plt.imshow(X_train_files[0])
    # plt.title(y_train[0])
    # plt.show()

    # 加载测试文件名和标签
    testing_paths = {
        data_paths['created_with_ai']['processed_testing_data_dir']: 1,
        data_paths['not_created_with_ai']['processed_testing_data_dir']: 0
    }
    X_test_files, y_test = load_filenames_and_labels(testing_paths)

    y_train = [int(label) for label in y_train]
    y_test = [int(label) for label in y_test]

    # 创建训练和测试数据生成器
    train_generator = DataGenerator(X_train_files, y_train, batch_size=32)
    test_generator = DataGenerator(X_test_files, y_test, batch_size=32)

    # 构建模型
    model = build_model()

    # 编译模型
    opt = Adam(learning_rate=0.000001)
    model.compile(optimizer=opt, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # 创建模型保存回调
    checkpoint_path = "../src/models/model_epoch_{epoch:02d}.h5"  # 修改路径和文件名格式
    model_checkpoint_callback = ModelCheckpoint(
        filepath=checkpoint_path,
        save_weights_only=False,
        save_freq='epoch'
    )

    # 训练模型，并添加回调
    history = model.fit(
        train_generator,
        epochs=500,
        validation_data=test_generator,
        # callbacks=[model_checkpoint_callback]  # 添加回调
    )

    # 保存模型
    model.save('../src/models/model.h5')

    # 评估模型
    test_loss, test_accuracy = model.evaluate(test_generator)
    print(f"Test Accuracy: {test_accuracy:.4f}")

    # 绘制训练历史图
    plot_training_history(history)


if __name__ == "__main__":
    main()
