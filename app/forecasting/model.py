from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Input,LSTM,Dense,Dropout
from tensorflow.keras.optimizers import Adam 

from app.forecasting.config import(
    LSTM_UNITS,
    DROPOUT_RATE,
    LEARNING_RATE
)

LSTM_UNITS = 50
DROPOUT_RATE = 0.2
LEARNING_RATE = 0.001

def build_lstm_model(input_shape: tuple) -> Sequential:
    """
    Builds and compile an LSTM model.

    Parameters:
        Shape of the input dat (time_steps,features).

    Returns:
        Sequential: 
            Compiled LSTM model.
    """
    
    model = Sequential()
    
    # Input-Layer
    model.add(Input(shape = input_shape))
    
    # LSTM-Layer
    model.add(LSTM(units = LSTM_UNITS))
    
    # Dropout-Layer
    model.add(Dropout(DROPOUT_RATE))
    
    # Dense-Layer
    model.add(Dense(25))
    
    # Output-Layer
    model.add(Dense(1))
    
    # Compile
    model.compile(optimizer = Adam(learning_rate = LEARNING_RATE),loss = "mean_squared_error", metrics = ["mae"])
    
    return model
