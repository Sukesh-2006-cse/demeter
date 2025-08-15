import React from 'react';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import Footer from '../../components/Footer';

export default function CommunityScreen() {
  return (
    <View style={{ flex: 1, backgroundColor: '#fff' }}>
      {/* Header */}
      <View style={styles.header}>
        <View style={{ flexDirection: 'row', alignItems: 'center' }}>
          <MaterialCommunityIcons name="account-group" size={28} color="#6d28d9" style={{ marginRight: 8 }} />
          <Text style={styles.headerTitle}>Community</Text>
        </View>
      </View>
      <ScrollView style={{ flex: 1 }} contentContainerStyle={{ paddingBottom: 100 }}>
        <Text style={styles.infoText}>Welcome to the Community page!</Text>
      </ScrollView>
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
  infoText: {
    fontSize: 16,
    color: '#64748b',
    margin: 24,
    textAlign: 'center',
  },
});
