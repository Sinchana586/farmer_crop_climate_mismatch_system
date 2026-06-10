# ============================================================
# KERAS NEURAL NETWORK
# ============================================================

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical
import tensorflow as tf
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load Dataset
df = pd.read_csv(
    "/workspaces/farmer_crop_climate_mismatch_system/datasets/Crop_recommendation.csv"
)

# Features and Target
X = df.drop("label", axis=1).values
y_raw = df["label"].values

# Encode Labels
le = LabelEncoder()
y = le.fit_transform(y_raw)

num_classes = len(le.classes_)

# Scale Features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train Test Split
X_train_k, X_test_k, y_train_k, y_test_k = train_test_split(
    X_scaled,
    y,
    test_size=0.35,
    random_state=42
)

print("Training Shape:", X_train_k.shape)
print("Testing Shape :", X_test_k.shape)
print("Classes:", num_classes)
print("\n--- Training Keras Neural Network ---")

# Convert labels to one-hot encoding
y_train_cat = to_categorical(
    y_train_k,
    num_classes=num_classes
)

y_test_cat = to_categorical(
    y_test_k,
    num_classes=num_classes
)

# Build Model
keras_model = Sequential([

    Input(shape=(X_train_k.shape[1],)),

    Dense(
        128,
        activation="relu"
    ),

    Dropout(0.20),

    Dense(
        64,
        activation="relu"
    ),

    Dropout(0.15),

    Dense(
        32,
        activation="relu"
    ),

    Dense(
        num_classes,
        activation="softmax"
    )

])

# Compile Model
keras_model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Early Stopping
early_stop = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

# Train Model
history = keras_model.fit(
    X_train_k,
    y_train_cat,
    epochs=50,
    batch_size=32,
    validation_split=0.15,
    callbacks=[early_stop],
    verbose=1
)

# Evaluate Model
loss, keras_acc_raw = keras_model.evaluate(
    X_test_k,
    y_test_cat,
    verbose=0
)

keras_acc = keras_acc_raw * 100

print(
    f"\nKeras Neural Network Accuracy: {keras_acc:.2f}%"
)
import joblib

keras_model.save(
    "/workspaces/farmer_crop_climate_mismatch_system/models/neural_network_model.h5"
)

joblib.dump(
    scaler,
    "/workspaces/farmer_crop_climate_mismatch_system/models/neural_network_scaler.pkl"
)

joblib.dump(
    le,
    "/workspaces/farmer_crop_climate_mismatch_system/models/neural_network_label_encoder.pkl"
)

print("✅ Model files saved successfully")