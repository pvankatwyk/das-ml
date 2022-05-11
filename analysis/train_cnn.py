from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D


def train_cnn(training_data_directory, test_data_directory):
    photo_size = (256, 256, 3)

    # Initiate data processing tools to automatically
    training_data_processor = ImageDataGenerator(
        rescale=1. / 255,
        horizontal_flip=True,
        zoom_range=0.2,
        rotation_range=10,
        shear_range=0.2,
        height_shift_range=0.1,
        width_shift_range=0.1
    )

    test_data_processor = ImageDataGenerator(rescale=1. / 255)

    # Load data into Python session from local computer
    training_data = training_data_processor.flow_from_directory(
        training_data_directory,
        target_size=(256, 256),
        batch_size=32,
        class_mode='categorical',
        color_mode='rgb'
    )

    testing_data = test_data_processor.flow_from_directory(
        test_data_directory,
        target_size=(256, 256),
        batch_size=32,
        class_mode='categorical',
        shuffle=False,
        color_mode='rgb'
    )

    # choose model parameters
    num_conv_layers = 2
    num_dense_layers = 1
    layer_size = 32
    num_training_epochs = 10

    MODEL_NAME = r"event_model"
    print(MODEL_NAME)

    # Initiate model variable
    model = Sequential()

    # begin adding properties to model variable
    # e.g. add a convolutional layer
    model.add(Conv2D(layer_size, (3, 3), input_shape=(256, 256, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # add additional convolutional layers based on num_conv_layers
    for _ in range(num_conv_layers - 1):
        model.add(Conv2D(layer_size, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

    # reduce dimensionality
    model.add(Flatten())

    # add fully connected "dense" layers if specified
    for _ in range(num_dense_layers):
        model.add(Dense(layer_size))
        model.add(Activation('relu'))

    # add output layer
    model.add(Dense(2))
    model.add(Activation('softmax'))

    # compile the sequential model with all added properties
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'],
                  )

    # use the data already loaded previously to train/tune the model
    model.fit(training_data,
              epochs=num_training_epochs,
              validation_data=testing_data)

    # save the trained model
    model.save(f'{MODEL_NAME}_2.h5')


if __name__ == "__main__":
    training_data_directory = 'F:/Research/DAS/event_detection_dataset/eq_vs_none_augmented/train/'
    test_data_directory = 'F:/Research/DAS/event_detection_dataset/eq_vs_none_augmented/test/'
    train_cnn(training_data_directory, test_data_directory)