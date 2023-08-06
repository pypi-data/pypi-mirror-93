import inspect
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_datasets as tfds
import pandas as pd
import inspect
from tqdm import tqdm
def models_fgs28(batch_size,train_path,valid_path,num_classes,epochs):

    # List all available models
    model_dictionary = {m[0]:m[1] for m in inspect.getmembers(tf.keras.applications, inspect.isfunction)}
    
    # Use the Image Data Generator to import the images from the dataset
    train_datagen = ImageDataGenerator(rescale = 1./255,
                                       shear_range = 0.2,
                                       zoom_range = 0.2,
                                       horizontal_flip = True)

    val_datagen = ImageDataGenerator(rescale = 1./255)

    # Make sure you provide the same target size as initialied for the image size
    train_processed_224 = train_datagen.flow_from_directory(train_path,
                                                     target_size = (224, 224),
                                                     batch_size = 32,
                                                     class_mode = 'categorical')
    validation_processed_224 = val_datagen.flow_from_directory(valid_path,
                                                target_size = (224, 224),
                                                batch_size = 32,
                                                class_mode = 'categorical')

    # Make sure you provide the same target size as initialied for the image size
    train_processed_331 = train_datagen.flow_from_directory(train_path,
                                                     target_size = (331, 331),
                                                     batch_size = 32,
                                                     class_mode = 'categorical')
    validation_processed_331 = val_datagen.flow_from_directory(valid_path,
                                                target_size = (331, 331),
                                                batch_size = 32,
                                                class_mode = 'categorical')

    # Loop over each model available in Keras
    num_train =train_processed_224.n
    print('NO.of samples for train:',num_train)
    num_iterations = int(num_train/batch_size)
    print('NO.iterations:',num_iterations)

    # Loop over each model available in Keras
    model_benchmarks = {'model_name': [], 'num_model_params': [], 'validation_accuracy': []}
    for model_name, model in tqdm(model_dictionary.items()):
        print('Model name is :',model_name)
        # Special handling for "NASNetLarge" since it requires input images with size (331,331)
        if 'NASNetLarge' in model_name:
            input_shape=(331,331,3)
            train_processed = train_processed_331
            validation_processed = validation_processed_331
        else:
            input_shape=(224,224,3)
            train_processed = train_processed_224
            validation_processed = validation_processed_224
        # load the pre-trained model with global average pooling as the last layer and freeze the model weights
        pre_trained_model = model(include_top=False, pooling='avg', input_shape=input_shape)
        pre_trained_model.trainable = False
        # custom modifications on top of pre-trained model and fit
        clf_model = tf.keras.models.Sequential()
        clf_model.add(pre_trained_model)
        clf_model.add(tf.keras.layers.Dense(num_classes, activation='softmax'))
        clf_model.compile(loss='categorical_crossentropy', metrics=['accuracy'])
        history = clf_model.fit(train_processed, epochs=epochs, validation_data=validation_processed,steps_per_epoch=num_iterations)
        # Calculate all relevant metrics
        clf_model.save(model_name+'.h5')
        model_benchmarks['model_name'].append(model_name)
        model_benchmarks['num_model_params'].append(pre_trained_model.count_params())
        model_benchmarks['validation_accuracy'].append(history.history['val_accuracy'][-1])

    # Convert Results to DataFrame for easy viewing
    benchmark_df = pd.DataFrame(model_benchmarks)
    # sort in ascending order of num_model_params column
    benchmark_df.sort_values('num_model_params', inplace=True)
    # write results to csv file
    benchmark_df.to_csv('benchmark_df.csv', index=False)
    print(benchmark_df)

    # Loop over each row and plot the num_model_params vs validation_accuracy
    markers=[".",",","o","v","^","<",">","1","2","3","4","8","s","p","P","*","h","H","+","x","X","D","d","|","_",4,5,6,7,8,9,10,11]
    plt.figure(figsize=(7,5))
    for row in benchmark_df.itertuples():
        plt.scatter(row.num_model_params, row.validation_accuracy, label=row.model_name, marker=markers[row.Index], s=150, linewidths=2)
    plt.xscale('log')
    plt.xlabel('Number of Parameters in Model')
    plt.ylabel('Validation Accuracy after Epochs')
    plt.title('Accuracy vs Model Size')
    # Move legend out of the plot
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left');