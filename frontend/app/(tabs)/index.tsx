

import { MaterialCommunityIcons, MaterialIcons } from '@expo/vector-icons';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import Footer from '../../components/Footer';


export default function HomeScreen() {
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

        {/* Weather */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <MaterialCommunityIcons name="weather-partly-cloudy" size={20} color="#22223b" />
            <Text style={styles.sectionTitle}>Weather (Last Updated: 2h ago)</Text>
            <MaterialCommunityIcons name="white-balance-sunny" size={20} color="#fbbf24" style={{ marginLeft: 4 }} />
          </View>
          <View style={styles.weatherRow}>
            <View style={styles.weatherItem}>
              <MaterialCommunityIcons name="thermometer" size={20} color="#ef4444" />
              <Text style={styles.weatherValue}>28°C</Text>
              <Text style={styles.weatherLabel}>Temp</Text>
            </View>
            <View style={styles.weatherItem}>
              <MaterialCommunityIcons name="water-percent" size={20} color="#2563eb" />
              <Text style={styles.weatherValue}>65%</Text>
              <Text style={styles.weatherLabel}>Humidity</Text>
            </View>
            <View style={styles.weatherItem}>
              <MaterialCommunityIcons name="weather-windy" size={20} color="#64748b" />
              <Text style={styles.weatherValue}>12 km/h</Text>
              <Text style={styles.weatherLabel}>Wind</Text>
            </View>
            <View style={styles.weatherItem}>
              <MaterialCommunityIcons name="weather-sunny-alert" size={20} color="#fbbf24" />
              <Text style={styles.weatherValue}>High</Text>
              <Text style={styles.weatherLabel}>UV</Text>
            </View>
          </View>
        </View>

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
  {/* Custom Footer */}
  <Footer />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    paddingHorizontal: 16,
    paddingTop: 32,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#22223b',
  },
  subtitle: {
    fontSize: 14,
    color: '#64748b',
  },
  offlineBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fef3c7',
    borderRadius: 8,
    paddingHorizontal: 8,
  },
  offlineText: {
    color: '#d97706',
    fontWeight: 'bold',
    marginLeft: 4,
    fontSize: 12,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  card: {
    flex: 1,
    alignItems: 'center',
    padding: 16,
    borderRadius: 12,
    marginHorizontal: 4,
    elevation: 1,
  },
  cardLabel: {
    fontSize: 13,
    color: '#64748b',
    marginTop: 8,
  },
  cardValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#22223b',
    marginTop: 2,
  },
  section: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
    elevation: 1,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#22223b',
    marginLeft: 6,
  },
  weatherRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 8,
  },
  weatherItem: {
    alignItems: 'center',
    flex: 1,
  },
  weatherValue: {
    fontSize: 15,
    fontWeight: 'bold',
    color: '#22223b',
    marginTop: 2,
  },
  weatherLabel: {
    fontSize: 12,
    color: '#64748b',
  },
  healthRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  healthLabel: {
    fontSize: 14,
    color: '#22223b',
    marginLeft: 8,
    width: 90,
  },
  progressBarBg: {
    flex: 1,
    height: 8,
    backgroundColor: '#e5e7eb',
    borderRadius: 4,
    marginHorizontal: 8,
    overflow: 'hidden',
  },
  progressBar: {
    height: 8,
    borderRadius: 4,
  },
  healthStatusGood: {
    color: '#2563eb',
    fontWeight: 'bold',
    fontSize: 13,
    width: 50,
  },
  healthStatusExcellent: {
    color: '#22c55e',
    fontWeight: 'bold',
    fontSize: 13,
    width: 70,
  },
  healthStatusLow: {
    color: '#eab308',
    fontWeight: 'bold',
    fontSize: 13,
    width: 40,
  },
  recentAction: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f0fdf4',
    borderRadius: 8,
    padding: 10,
    marginTop: 8,
  },
  recentActionTitle: {
    fontWeight: 'bold',
    color: '#22223b',
    fontSize: 14,
  },
  recentActionSubtitle: {
    color: '#64748b',
    fontSize: 12,
    marginTop: 2,
  },
});
