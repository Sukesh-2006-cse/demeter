"""
Data preprocessing utilities
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.impute import SimpleImputer
import cv2
from typing import Dict, Any, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class DataPreprocessor:
    """General data preprocessing utilities"""
    
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.imputers = {}
    
    def preprocess_tabular_data(self, df: pd.DataFrame, target_column: str = None) -> Tuple[pd.DataFrame, Dict]:
        """
        Preprocess tabular data for ML models
        
        Args:
            df: Input dataframe
            target_column: Name of target column (if any)
            
        Returns:
            Preprocessed dataframe and preprocessing metadata
        """
        df_processed = df.copy()
        metadata = {
            'numeric_columns': [],
            'categorical_columns': [],
            'preprocessing_steps': []
        }
        
        # Identify column types
        numeric_columns = df_processed.select_dtypes(include=[np.number]).columns.tolist()
        categorical_columns = df_processed.select_dtypes(include=['object']).columns.tolist()
        
        if target_column and target_column in categorical_columns:
            categorical_columns.remove(target_column)
        
        metadata['numeric_columns'] = numeric_columns
        metadata['categorical_columns'] = categorical_columns
        
        # Handle missing values
        if numeric_columns:
            imputer_numeric = SimpleImputer(strategy='median')
            df_processed[numeric_columns] = imputer_numeric.fit_transform(df_processed[numeric_columns])
            self.imputers['numeric'] = imputer_numeric
            metadata['preprocessing_steps'].append('numeric_imputation')
        
        if categorical_columns:
            imputer_categorical = SimpleImputer(strategy='most_frequent')
            df_processed[categorical_columns] = imputer_categorical.fit_transform(df_processed[categorical_columns])
            self.imputers['categorical'] = imputer_categorical
            metadata['preprocessing_steps'].append('categorical_imputation')
        
        # Encode categorical variables
        for col in categorical_columns:
            encoder = LabelEncoder()
            df_processed[col] = encoder.fit_transform(df_processed[col].astype(str))
            self.encoders[col] = encoder
            metadata['preprocessing_steps'].append(f'label_encoding_{col}')
        
        # Scale numeric features
        if numeric_columns:
            scaler = StandardScaler()
            df_processed[numeric_columns] = scaler.fit_transform(df_processed[numeric_columns])
            self.scalers['standard'] = scaler
            metadata['preprocessing_steps'].append('standard_scaling')
        
        return df_processed, metadata
    
    def preprocess_crop_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Specific preprocessing for crop recommendation data"""
        df_processed = df.copy()
        
        # Handle soil pH ranges
        if 'ph' in df_processed.columns:
            df_processed['ph_category'] = pd.cut(df_processed['ph'], 
                                               bins=[0, 6.0, 7.5, 14], 
                                               labels=['acidic', 'neutral', 'alkaline'])
        
        # Create nutrient ratios
        if all(col in df_processed.columns for col in ['N', 'P', 'K']):
            df_processed['NPK_ratio'] = df_processed['N'] / (df_processed['P'] + df_processed['K'] + 1e-6)
            df_processed['total_nutrients'] = df_processed['N'] + df_processed['P'] + df_processed['K']
        
        # Temperature and humidity interactions
        if all(col in df_processed.columns for col in ['temperature', 'humidity']):
            df_processed['temp_humidity_interaction'] = df_processed['temperature'] * df_processed['humidity']
        
        return df_processed
    
    def preprocess_market_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Specific preprocessing for market price data"""
        df_processed = df.copy()
        
        # Convert date columns
        date_columns = ['date', 'timestamp', 'market_date']
        for col in date_columns:
            if col in df_processed.columns:
                df_processed[col] = pd.to_datetime(df_processed[col])
                df_processed[f'{col}_year'] = df_processed[col].dt.year
                df_processed[f'{col}_month'] = df_processed[col].dt.month
                df_processed[f'{col}_day'] = df_processed[col].dt.day
                df_processed[f'{col}_weekday'] = df_processed[col].dt.weekday
        
        # Create price change features
        if 'price' in df_processed.columns:
            df_processed['price_change'] = df_processed['price'].pct_change()
            df_processed['price_volatility'] = df_processed['price'].rolling(window=7).std()
        
        # Seasonal features
        if 'month' in df_processed.columns or any('month' in col for col in df_processed.columns):
            month_col = 'month' if 'month' in df_processed.columns else [col for col in df_processed.columns if 'month' in col][0]
            df_processed['season'] = df_processed[month_col].map({
                12: 'winter', 1: 'winter', 2: 'winter',
                3: 'spring', 4: 'spring', 5: 'spring',
                6: 'summer', 7: 'summer', 8: 'summer',
                9: 'autumn', 10: 'autumn', 11: 'autumn'
            })
        
        return df_processed

class ImagePreprocessor:
    """Image preprocessing utilities for pest detection"""
    
    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        self.target_size = target_size
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess image for model input
        
        Args:
            image_path: Path to image file
            
        Returns:
            Preprocessed image array
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize
            image = cv2.resize(image, self.target_size)
            
            # Normalize
            image = image.astype(np.float32) / 255.0
            
            # Add batch dimension
            image = np.expand_dims(image, axis=0)
            
            return image
            
        except Exception as e:
            logger.error(f"Error preprocessing image {image_path}: {e}")
            raise
    
    def preprocess_image_batch(self, image_paths: List[str]) -> np.ndarray:
        """Preprocess batch of images"""
        images = []
        for path in image_paths:
            try:
                img = self.preprocess_image(path)
                images.append(img[0])  # Remove batch dimension
            except Exception as e:
                logger.warning(f"Skipping image {path}: {e}")
                continue
        
        if not images:
            raise ValueError("No valid images found in batch")
        
        return np.array(images)
    
    def augment_image(self, image: np.ndarray) -> List[np.ndarray]:
        """Apply data augmentation to image"""
        augmented = [image]
        
        # Horizontal flip
        augmented.append(cv2.flip(image, 1))
        
        # Rotation
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        
        for angle in [15, -15, 30, -30]:
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(image, rotation_matrix, (width, height))
            augmented.append(rotated)
        
        # Brightness adjustment
        for factor in [0.8, 1.2]:
            bright = cv2.convertScaleAbs(image, alpha=factor, beta=0)
            augmented.append(bright)
        
        return augmented

class WeatherDataPreprocessor:
    """Weather data preprocessing utilities"""
    
    def preprocess_weather_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess weather data for risk assessment"""
        df_processed = df.copy()
        
        # Convert temperature units if needed
        if 'temperature_f' in df_processed.columns:
            df_processed['temperature_c'] = (df_processed['temperature_f'] - 32) * 5/9
        
        # Create weather indices
        if all(col in df_processed.columns for col in ['temperature_c', 'humidity', 'rainfall']):
            # Heat index
            df_processed['heat_index'] = self._calculate_heat_index(
                df_processed['temperature_c'], 
                df_processed['humidity']
            )
            
            # Drought index
            df_processed['drought_risk'] = self._calculate_drought_risk(
                df_processed['rainfall'], 
                df_processed['temperature_c']
            )
        
        # Wind chill
        if all(col in df_processed.columns for col in ['temperature_c', 'wind_speed']):
            df_processed['wind_chill'] = self._calculate_wind_chill(
                df_processed['temperature_c'], 
                df_processed['wind_speed']
            )
        
        return df_processed
    
    def _calculate_heat_index(self, temp_c: pd.Series, humidity: pd.Series) -> pd.Series:
        """Calculate heat index"""
        temp_f = temp_c * 9/5 + 32
        hi = 0.5 * (temp_f + 61.0 + ((temp_f - 68.0) * 1.2) + (humidity * 0.094))
        return (hi - 32) * 5/9  # Convert back to Celsius
    
    def _calculate_drought_risk(self, rainfall: pd.Series, temperature: pd.Series) -> pd.Series:
        """Calculate drought risk index"""
        # Simple drought index based on rainfall and temperature
        return (temperature / (rainfall + 1)) * 10
    
    def _calculate_wind_chill(self, temp_c: pd.Series, wind_speed: pd.Series) -> pd.Series:
        """Calculate wind chill index"""
        temp_f = temp_c * 9/5 + 32
        wind_mph = wind_speed * 2.237  # Convert m/s to mph
        
        wc = 35.74 + (0.6215 * temp_f) - (35.75 * (wind_mph ** 0.16)) + (0.4275 * temp_f * (wind_mph ** 0.16))
        return (wc - 32) * 5/9  # Convert back to Celsius