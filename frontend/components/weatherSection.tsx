import React, { useEffect, useState } from 'react';
import { View, Text, ActivityIndicator, StyleSheet } from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';

interface WeatherValues {
  temperature: number;
  humidity: number;
  windSpeed: number;
  precipitationIntensity: number; // use this for rainfall
}

const WeatherSection: React.FC = () => {
  const [weather, setWeather] = useState<WeatherValues | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchWeather = async () => {
      try {
        const response = await fetch(
          'https://api.tomorrow.io/v4/timelines?location=19.0760,72.8777&fields=temperature,humidity,windSpeed,precipitationIntensity&timesteps=1h&units=metric&apikey=KwkYiyncBsyJrB5Q1iCQyilihYH2FD6A'
        );

        const data = await response.json();

        const latest = data.data.timelines[0].intervals[0].values;

        setWeather({
          temperature: latest.temperature,
          humidity: latest.humidity,
          windSpeed: latest.windSpeed,
           precipitationIntensity: latest.precipitationIntensity ?? 0,
        });
      } catch (error) {
        console.error('Error fetching weather:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchWeather();
  }, []);

  if (loading) {
    return <ActivityIndicator size="large" color="#0000ff" style={{ marginTop: 50 }} />;
  }

  return (
    <View style={styles.section}>
      <View style={styles.sectionHeader}>
        <MaterialCommunityIcons name="weather-partly-cloudy" size={20} color="#22223b" />
        <Text style={styles.sectionTitle}>Weather (Last Updated: 2h ago)</Text>
        <MaterialCommunityIcons name="white-balance-sunny" size={20} color="#fbbf24" style={{ marginLeft: 4 }} />
      </View>

      <View style={styles.weatherRow}>
        <View style={styles.weatherItem}>
          <MaterialCommunityIcons name="thermometer" size={20} color="#ef4444" />
          <Text style={styles.weatherValue}>{weather?.temperature.toFixed(1)}°C</Text>
          <Text style={styles.weatherLabel}>Temp</Text>
        </View>

        <View style={styles.weatherItem}>
          <MaterialCommunityIcons name="water-percent" size={20} color="#2563eb" />
          <Text style={styles.weatherValue}>{weather?.humidity.toFixed(0)}%</Text>
          <Text style={styles.weatherLabel}>Humidity</Text>
        </View>

        <View style={styles.weatherItem}>
          <MaterialCommunityIcons name="weather-windy" size={20} color="#64748b" />
          <Text style={styles.weatherValue}>{weather?.windSpeed.toFixed(1)} km/h</Text>
          <Text style={styles.weatherLabel}>Wind</Text>
        </View>

        <View style={styles.weatherItem}>
          <MaterialCommunityIcons name="weather-sunny-alert" size={20} color="#fbbf24" />
          <Text style={styles.weatherValue}>
  {weather?.precipitationIntensity && weather.precipitationIntensity > 0 ? 'High' : 'Low'}
</Text>

          <Text style={styles.weatherLabel}>Rainfall</Text>
        </View>
      </View>
    </View>
  );
};

export default WeatherSection;

const styles = StyleSheet.create({
  section: {
    marginBottom: 20,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 5,
  },
  weatherRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  weatherItem: {
    alignItems: 'center',
    flex: 1,
  },
  weatherValue: {
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 4,
  },
  weatherLabel: {
    fontSize: 12,
    color: '#555',
  },
});

