# Training Scripts

This directory contains training scripts for all the AI models used in the agricultural system.

## Scripts Overview

### `train_crop.py`
Trains the crop recommendation model using soil and climate data.

**Features:**
- Random Forest classifier
- Cross-validation evaluation
- Feature importance analysis
- Model persistence

**Usage:**
```bash
python train_crop.py
```

### `train_market_yield.py`
Trains both market price prediction and crop yield prediction models.

**Market Price Model:**
- Time series forecasting
- Random Forest regressor
- Market factors analysis

**Yield Prediction Model:**
- Gradient boosting regressor
- Environmental factors integration
- Yield optimization insights

**Usage:**
```bash
python train_market_yield.py
```

### `train_weather_risk.py`
Trains the weather risk assessment model.

**Features:**
- Multi-class risk categorization (low/medium/high)
- Weather pattern analysis
- Feature scaling and preprocessing
- Risk factor importance ranking

**Usage:**
```bash
python train_weather_risk.py
```

### `train_pest.py`
Creates a pest detection model in ONNX format.

**Features:**
- CNN-based image classification
- ONNX model export
- Multi-pest detection
- Treatment recommendations

**Usage:**
```bash
python train_pest.py
```

## Data Requirements

Each training script expects specific data files in the `../data/` directory:

- `crop_dataset.csv` - Crop recommendation data
- `market_dataset.csv` - Market price historical data  
- `weather_data.csv` - Weather and climate data
- `pest_images/` - Directory with labeled pest images

## Model Outputs

Trained models are saved to `../models/cloud/`:

- `crop_recommendation.pkl`
- `market_price.pkl`
- `yield_model.pkl`
- `weather_risk.pkl`
- `pest_model.onnx`

## Training Pipeline

To train all models:

```bash
# Train crop recommendation
python train_crop.py

# Train market and yield models
python train_market_yield.py

# Train weather risk model
python train_weather_risk.py

# Create pest detection model
python train_pest.py
```

## Model Evaluation

Each script includes:
- Train/validation/test splits
- Cross-validation where appropriate
- Performance metrics
- Feature importance analysis
- Classification/regression reports

## Customization

To adapt for your specific use case:

1. **Data Format**: Modify data loading functions for your CSV format
2. **Features**: Add/remove features in preprocessing steps
3. **Model Architecture**: Adjust hyperparameters and model types
4. **Evaluation**: Add custom metrics for your domain

## Dependencies

Required packages:
- scikit-learn
- pandas
- numpy
- onnx (for pest model)
- opencv-python (for image processing)

Install with:
```bash
pip install -r ../requirements.txt
```

## Production Considerations

For production deployment:

1. **Data Validation**: Add input data validation
2. **Model Versioning**: Implement model version tracking
3. **A/B Testing**: Set up model comparison frameworks
4. **Monitoring**: Add model performance monitoring
5. **Retraining**: Implement automated retraining pipelines

## Troubleshooting

Common issues:

- **Missing Data**: Scripts create dummy data if real datasets are missing
- **Memory Issues**: Reduce dataset size or use batch processing
- **ONNX Errors**: Ensure compatible ONNX version for pest model
- **Feature Mismatch**: Verify column names match expected features