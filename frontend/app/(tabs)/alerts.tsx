import { MaterialCommunityIcons, MaterialIcons } from '@expo/vector-icons';
import React from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import Footer from '../../components/Footer';

export default function AlertsScreen() {
  return (
    <View style={{ flex: 1, backgroundColor: '#fff' }}>
      {/* Header */}
      <View style={styles.header}>
        <View style={{ flexDirection: 'row', alignItems: 'center' }}>
          <MaterialIcons name="notification-important" size={28} color="#ef4444" style={{ marginRight: 8 }} />
          <Text style={styles.headerTitle}>Alerts</Text>
        </View>
        <View style={styles.badge}><Text style={styles.badgeText}>3</Text></View>
      </View>

      {/* Alert Summary */}
      <View style={styles.summaryRow}>
        <View style={[styles.summaryCard, { backgroundColor: '#fdecec', borderColor: '#ef4444' }] }>
          <MaterialIcons name="error-outline" size={28} color="#ef4444" />
          <Text style={styles.summaryTitle}>Critical</Text>
          <Text style={styles.summaryCount}>1 active</Text>
        </View>
        <View style={[styles.summaryCard, { backgroundColor: '#fffbe6', borderColor: '#eab308' }] }>
          <MaterialIcons name="warning-amber" size={28} color="#eab308" />
          <Text style={styles.summaryTitle}>Warning</Text>
          <Text style={styles.summaryCount}>1 active</Text>
        </View>
        <View style={[styles.summaryCard, { backgroundColor: '#eef6ff', borderColor: '#2563eb' }] }>
          <MaterialIcons name="info-outline" size={28} color="#2563eb" />
          <Text style={styles.summaryTitle}>Info</Text>
          <Text style={styles.summaryCount}>1 active</Text>
        </View>
      </View>

  <ScrollView style={{ flex: 1 }} contentContainerStyle={{ paddingBottom: 100 }}>
        {/* Critical Alert */}
        <View style={styles.alertCard}>
          <View style={{ flexDirection: 'row', alignItems: 'center' }}>
            <MaterialIcons name="warning" size={24} color="#eab308" style={{ marginRight: 8 }} />
            <Text style={styles.alertTitle}>Water Stress Detected</Text>
            <View style={[styles.levelBadge, { backgroundColor: '#ef4444' }]}><Text style={styles.levelBadgeText}>High</Text></View>
          </View>
          <Text style={styles.alertDesc}>Soil moisture levels are below optimal range in Section A</Text>
          <Text style={styles.alertTime}>2 hours ago</Text>
        </View>
        {/* Warning Alert */}
        <View style={styles.alertCard}>
          <View style={{ flexDirection: 'row', alignItems: 'center' }}>
            <MaterialCommunityIcons name="weather-rainy" size={24} color="#64748b" style={{ marginRight: 8 }} />
            <Text style={styles.alertTitle}>Rain Forecast</Text>
            <View style={[styles.levelBadge, { backgroundColor: '#eab308' }]}><Text style={styles.levelBadgeText}>Medium</Text></View>
          </View>
          <Text style={styles.alertDesc}>Moderate rainfall expected in next 24 hours</Text>
          <Text style={styles.alertTime}>4 hours ago</Text>
        </View>
        {/* Info Alert */}
        <View style={styles.alertCard}>
          <View style={{ flexDirection: 'row', alignItems: 'center' }}>
            <MaterialIcons name="check-circle" size={24} color="#22c55e" style={{ marginRight: 8 }} />
            <Text style={styles.alertTitle}>Fertilizer Application Complete</Text>
            <View style={[styles.levelBadge, { backgroundColor: '#64748b' }]}><Text style={styles.levelBadgeText}>Low</Text></View>
          </View>
          <Text style={styles.alertDesc}>NPK fertilizer applied successfully to all sections</Text>
          <Text style={styles.alertTime}>1 day ago</Text>
        </View>
      </ScrollView>
  {/* Custom Footer */}
  <Footer />
    </View>
  );
}

const styles = StyleSheet.create({
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingTop: 32,
    paddingBottom: 12,
    backgroundColor: '#fff',
  },
  headerTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#22223b',
  },
  badge: {
    backgroundColor: '#ef4444',
    borderRadius: 12,
    minWidth: 24,
    height: 24,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 6,
  },
  badgeText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 14,
  },
  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 8,
    marginBottom: 12,
  },
  summaryCard: {
    flex: 1,
    alignItems: 'center',
    borderRadius: 12,
    borderWidth: 1,
    marginHorizontal: 4,
    paddingVertical: 10,
    backgroundColor: '#fff',
  },
  summaryTitle: {
    fontWeight: 'bold',
    fontSize: 15,
    marginTop: 4,
    color: '#22223b',
  },
  summaryCount: {
    fontSize: 13,
    color: '#64748b',
    marginTop: 2,
  },
  alertCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    marginHorizontal: 12,
    marginBottom: 16,
    padding: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOpacity: 0.06,
    shadowRadius: 4,
    shadowOffset: { width: 0, height: 2 },
  },
  alertTitle: {
    fontWeight: 'bold',
    fontSize: 16,
    color: '#22223b',
    flex: 1,
  },
  alertDesc: {
    color: '#22223b',
    fontSize: 14,
    marginTop: 8,
  },
  alertTime: {
    color: '#64748b',
    fontSize: 12,
    marginTop: 6,
  },
  levelBadge: {
    borderRadius: 6,
    paddingHorizontal: 8,
    paddingVertical: 2,
    marginLeft: 8,
  },
  levelBadgeText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 13,
  },
});
