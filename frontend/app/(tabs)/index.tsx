// HomeScreen.tsx
import React, { useEffect, useState } from 'react';
import { MaterialCommunityIcons, MaterialIcons } from '@expo/vector-icons';
import { ScrollView, StyleSheet, Text, View, ActivityIndicator } from 'react-native';
import Footer from '../../components/Footer';
import WeatherSection from '../../components/weatherSection';

interface WeatherValues {
  temperature: number;
  humidity: number;
  windSpeed: number;
  precipitationIntensity: number;
}

export default function HomeScreen() {
  const [weather, setWeather] = useState<WeatherValues | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchWeather = async () => {
      try {
        const response = await fetch(
          'https://api.tomorrow.io/v4/timelines?location=40.7128,-74.0060&fields=temperature,humidity,windSpeed,precipitationIntensity&timesteps=1h&units=metric&apikey=KwkYiyncBsyJrB5Q1iCQyilihYH2FD6A'

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

  return (
    <View style={{ flex: 1 }}>
      <ScrollView style={styles.container} contentContainerStyle={{ paddingBottom: 100 }}>
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.title}>Demeter</Text>
            <Text style={styles.subtitle}>Agricultural AI Companion</Text>
          </View>
          <View style={styles.offlineBadge}>
            <MaterialIcons name="wifi-off" size={16} color="#d97706" />
            <Text style={styles.offlineText}>Offline Mode</Text>
          </View>
        </View>

        {/* Crop & Growth Stage */}
        <View style={styles.row}>
          <View style={[styles.card, { backgroundColor: '#e6f9ed' }]}>
            <MaterialCommunityIcons name="sprout" size={28} color="#22c55e" />
            <Text style={styles.cardLabel}>Current Crop</Text>
            <Text style={styles.cardValue}>Wheat</Text>
          </View>
          <View style={[styles.card, { backgroundColor: '#e6f0fa' }]}>
            <MaterialCommunityIcons name="calendar-star" size={28} color="#2563eb" />
            <Text style={styles.cardLabel}>Growth Stage</Text>
            <Text style={styles.cardValue}>Flowering</Text>
          </View>
        </View>

        {/* Weather Section */}
        <WeatherSection weather={weather} loading={loading} />

        {/* Farm Health Overview */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Farm Health Overview</Text>
          <View style={styles.healthRow}>
            <MaterialCommunityIcons name="water" size={20} color="#2563eb" />
            <Text style={styles.healthLabel}>Soil Moisture</Text>
            <View style={styles.progressBarBg}>
              <View style={[styles.progressBar, { width: '70%', backgroundColor: '#2563eb' }]} />
            </View>
            <Text style={styles.healthStatusGood}>Good</Text>
          </View>
          <View style={styles.healthRow}>
            <MaterialCommunityIcons name="leaf" size={20} color="#22c55e" />
            <Text style={styles.healthLabel}>Crop Health</Text>
            <View style={styles.progressBarBg}>
              <View style={[styles.progressBar, { width: '100%', backgroundColor: '#22c55e' }]} />
            </View>
            <Text style={styles.healthStatusExcellent}>Excellent</Text>
          </View>
          <View style={styles.healthRow}>
            <MaterialCommunityIcons name="bug" size={20} color="#eab308" />
            <Text style={styles.healthLabel}>Pest Risk</Text>
            <View style={styles.progressBarBg}>
              <View style={[styles.progressBar, { width: '20%', backgroundColor: '#eab308' }]} />
            </View>
            <Text style={styles.healthStatusLow}>Low</Text>
          </View>
        </View>

        {/* Recent Actions */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Recent Actions</Text>
          <View style={styles.recentAction}>
            <MaterialCommunityIcons name="test-tube" size={20} color="#22c55e" />
            <View style={{ marginLeft: 8 }}>
              <Text style={styles.recentActionTitle}>Soil Test Completed</Text>
              <Text style={styles.recentActionSubtitle}>2 hours ago • pH: 6.8, N-P-K: Good</Text>
            </View>
          </View>
        </View>
      </ScrollView>

      {/* Footer */}
      <Footer />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', paddingHorizontal: 16, paddingTop: 32 },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#22223b' },
  subtitle: { fontSize: 14, color: '#64748b' },
  offlineBadge: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#fef3c7', borderRadius: 8, paddingHorizontal: 8 },
  offlineText: { color: '#d97706', fontWeight: 'bold', marginLeft: 4, fontSize: 12 },
  row: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 20 },
  card: { flex: 1, alignItems: 'center', padding: 16, borderRadius: 12, marginHorizontal: 4, elevation: 1 },
  cardLabel: { fontSize: 13, color: '#64748b', marginTop: 8 },
  cardValue: { fontSize: 16, fontWeight: 'bold', color: '#22223b', marginTop: 2 },
  section: { backgroundColor: '#fff', borderRadius: 12, padding: 16, marginBottom: 20, elevation: 1 },
  sectionTitle: { fontSize: 16, fontWeight: 'bold', color: '#22223b', marginBottom: 12 },
  healthRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 10 },
  healthLabel: { fontSize: 14, color: '#22223b', marginLeft: 8, width: 90 },
  progressBarBg: { flex: 1, height: 8, backgroundColor: '#e5e7eb', borderRadius: 4, marginHorizontal: 8, overflow: 'hidden' },
  progressBar: { height: 8, borderRadius: 4 },
  healthStatusGood: { color: '#2563eb', fontWeight: 'bold', fontSize: 13, width: 50 },
  healthStatusExcellent: { color: '#22c55e', fontWeight: 'bold', fontSize: 13, width: 70 },
  healthStatusLow: { color: '#eab308', fontWeight: 'bold', fontSize: 13, width: 40 },
  recentAction: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#f0fdf4', borderRadius: 8, padding: 10, marginTop: 8 },
  recentActionTitle: { fontWeight: 'bold', color: '#22223b', fontSize: 14 },
  recentActionSubtitle: { color: '#64748b', fontSize: 12, marginTop: 2 },
});
