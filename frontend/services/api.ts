/**
 * API service for communicating with the Flask backend
 */

const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:5000';

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface CropRecommendationRequest {
  N: number;
  P: number;
  K: number;
  temperature: number;
  humidity: number;
  ph: number;
  rainfall: number;
  language?: string;
}

export interface MarketPredictionRequest {
  crop: string;
  location?: string;
  timeframe?: number;
  language?: string;
}

export interface YieldPredictionRequest {
  crop: string;
  area_hectares: number;
  soil_conditions: {
    N: number;
    P: number;
    K: number;
    ph: number;
  };
  weather_conditions: {
    temperature: number;
    humidity: number;
    rainfall: number;
  };
  language?: string;
}

export interface RiskAssessmentRequest {
  location: string;
  crop?: string;
  weather_data?: {
    temperature: number;
    humidity: number;
    rainfall: number;
    wind_speed: number;
    pressure: number;
  };
  language?: string;
}

export interface PestDetectionRequest {
  image: string; // Base64 encoded image
  crop_type?: string;
  language?: string;
}

class ApiService {
  private async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          error: data.error || `HTTP ${response.status}: ${response.statusText}`,
        };
      }

      return {
        success: true,
        data,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Network error occurred',
      };
    }
  }

  /**
   * Get crop recommendations based on soil and climate conditions
   */
  async getCropRecommendations(
    request: CropRecommendationRequest
  ): Promise<ApiResponse> {
    return this.makeRequest('/crop-recommendation', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Get market price predictions
   */
  async getMarketPredictions(
    request: MarketPredictionRequest
  ): Promise<ApiResponse> {
    return this.makeRequest('/market-prediction', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Get crop yield predictions (uses market prediction endpoint)
   */
  async getYieldPredictions(
    request: YieldPredictionRequest
  ): Promise<ApiResponse> {
    // Convert yield request to market prediction format
    const marketRequest = {
      crop: request.crop,
      location: request.soil_conditions ? 'location' : undefined,
      area_hectares: request.area_hectares,
      soil_conditions: request.soil_conditions,
      weather_conditions: request.weather_conditions,
      language: request.language
    };
    
    return this.makeRequest('/market-prediction', {
      method: 'POST',
      body: JSON.stringify(marketRequest),
    });
  }

  /**
   * Get weather risk assessment
   */
  async getRiskAssessment(
    request: RiskAssessmentRequest
  ): Promise<ApiResponse> {
    return this.makeRequest('/risk-assessment', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Detect pests from image
   */
  async detectPests(request: PestDetectionRequest): Promise<ApiResponse> {
    return this.makeRequest('/pest-detection', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Get general agricultural advice using query endpoint
   */
  async getAdvice(query: string, language?: string): Promise<ApiResponse> {
    return this.makeRequest('/query', {
      method: 'POST',
      body: JSON.stringify({ text: query, context: { language } }),
    });
  }

  /**
   * Get supported languages
   */
  async getSupportedLanguages(): Promise<ApiResponse> {
    return this.makeRequest('/languages');
  }

  /**
   * Health check endpoint
   */
  async healthCheck(): Promise<ApiResponse> {
    return this.makeRequest('/health');
  }

  /**
   * Upload image for pest detection
   */
  async uploadImage(imageUri: string): Promise<ApiResponse> {
    try {
      const formData = new FormData();
      formData.append('image', {
        uri: imageUri,
        type: 'image/jpeg',
        name: 'pest_image.jpg',
      } as any);

      const response = await fetch(`${API_BASE_URL}/upload-image`, {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          error: data.error || `HTTP ${response.status}: ${response.statusText}`,
        };
      }

      return {
        success: true,
        data,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Upload failed',
      };
    }
  }

  /**
   * Get historical data for a specific crop
   */
  async getHistoricalData(
    crop: string,
    dataType: 'price' | 'yield' | 'weather',
    timeRange?: string
  ): Promise<ApiResponse> {
    const params = new URLSearchParams({
      crop,
      type: dataType,
      ...(timeRange && { range: timeRange }),
    });

    return this.makeRequest(`/api/historical-data?${params}`);
  }

  /**
   * Get weather forecast
   */
  async getWeatherForecast(
    location: string,
    days?: number
  ): Promise<ApiResponse> {
    const params = new URLSearchParams({
      location,
      ...(days && { days: days.toString() }),
    });

    return this.makeRequest(`/api/weather-forecast?${params}`);
  }

  /**
   * Save user preferences
   */
  async saveUserPreferences(preferences: {
    language?: string;
    location?: string;
    crops?: string[];
    notifications?: boolean;
  }): Promise<ApiResponse> {
    return this.makeRequest('/api/user-preferences', {
      method: 'POST',
      body: JSON.stringify(preferences),
    });
  }

  /**
   * Get user preferences
   */
  async getUserPreferences(): Promise<ApiResponse> {
    return this.makeRequest('/api/user-preferences');
  }
}

export const apiService = new ApiService();
export default apiService;