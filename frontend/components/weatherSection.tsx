// WeatherSection.tsx
import React from 'react';
import { View, Text, ActivityIndicator, StyleSheet } from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';

interface WeatherValues {
  temperature: number;
  humidity: number;
  windSpeed: number;
  precipitationIntensity: number;
}

interface Props {
  weather: WeatherValues | null;
  loading: boolean;
}

const WeatherSection: React.FC<Props> = ({ weather, loading }) => {
  if (loading) {
    return <ActivityIndicator size="large" color="#2563eb" style={{ marginTop: 16 }} />;
  }

  return (
    <View style={styles.section}>
      <View style={styles.sectionHeader}>
        <MaterialCommunityIcons name="weather-partly-cloudy" size={20} color="#22223b" />
        <Text style={styles.sectionTitle}>Weather (Last Updated)</Text>
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
          <MaterialCommunityIcons name="weather-rainy" size={20} color="#fbbf24" />
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
  section: { backgroundColor: '#fff', borderRadius: 12, padding: 16, marginBottom: 20, elevation: 1 },
  sectionHeader: { flexDirection: 'row', alignItems: 'center', marginBottom: 12 },
  sectionTitle: { fontSize: 16, fontWeight: 'bold', color: '#22223b', marginLeft: 6 },
  weatherRow: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 8 },
  weatherItem: { alignItems: 'center', flex: 1 },
  weatherValue: { fontSize: 15, fontWeight: 'bold', color: '#22223b', marginTop: 2 },
  weatherLabel: { fontSize: 12, color: '#64748b' },
});
