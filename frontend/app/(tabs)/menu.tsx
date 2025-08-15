import { MaterialCommunityIcons, MaterialIcons } from '@expo/vector-icons';
import React from 'react';
import { ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import Footer from '../../components/Footer';

export default function MenuScreen() {
  return (
    <View style={{ flex: 1, backgroundColor: '#fff' }}>
      {/* Header */}
      <View style={styles.header}>
        <MaterialIcons name="menu" size={28} color="#22223b" style={{ marginRight: 8 }} />
        <Text style={styles.headerTitle}>Menu</Text>
      </View>
      <ScrollView style={{ flex: 1 }} contentContainerStyle={{ paddingBottom: 100 }}>
        {/* Profile Card */}
        <View style={styles.profileCard}>
          <View style={styles.profileRow}>
            <View style={styles.avatarCircle}>
              <MaterialCommunityIcons name="account" size={40} color="#6d28d9" />
            </View>
            <View>
              <Text style={styles.profileName}>राम प्रसाद शर्मा</Text>
              <Text style={styles.profileMeta}>Farmer ID: DEM001234</Text>
              <Text style={styles.profileMeta}>Village: खेतपुर, UP</Text>
            </View>
          </View>
        </View>
        {/* App Status Card */}
        <View style={styles.statusCard}>
          <Text style={styles.statusTitle}>App Status</Text>
          <View style={styles.statusRow}>
            <Text style={styles.statusLabel}>Version</Text>
            <Text style={styles.statusValue}>2.1.4</Text>
          </View>
          <View style={styles.statusRow}>
            <Text style={styles.statusLabel}>Data Sync</Text>
            <View style={styles.statusBadge}><Text style={styles.statusBadgeText}>3 pending</Text></View>
          </View>
          <View style={styles.statusRow}>
            <Text style={styles.statusLabel}>Storage Used</Text>
            <Text style={styles.statusValue}>2.3 GB / 5 GB</Text>
          </View>
        </View>
        {/* Menu Options */}
        <View style={styles.menuCard}>
          <MenuOption icon={<MaterialIcons name="person-outline" size={24} color="#64748b" />} label="Profile" />
          <MenuOption icon={<MaterialIcons name="settings" size={24} color="#64748b" />} label="Settings" />
          <MenuOption icon={<MaterialCommunityIcons name="book-open-variant" size={24} color="#64748b" />} label="Crop Library" badgeType="new" />
          <MenuOption icon={<MaterialIcons name="cloud-download" size={24} color="#64748b" />} label="Offline Data" badgeType="pending" />
          <MenuOption icon={<MaterialIcons name="share" size={24} color="#64748b" />} label="Share App" />
          <MenuOption icon={<MaterialIcons name="help-outline" size={24} color="#64748b" />} label="Help & Support" />
        </View>
      </ScrollView>
      <Footer />
    </View>
  );
}

type MenuOptionProps = {
  icon: React.ReactNode;
  label: string;
  badgeType?: 'new' | 'pending';
};

function MenuOption({ icon, label, badgeType }: MenuOptionProps) {
  let badge = null;
  if (badgeType === 'new') {
    badge = (
      <View style={styles.newBadge}>
        <Text style={styles.newBadgeText}>New</Text>
      </View>
    );
  } else if (badgeType === 'pending') {
    badge = (
      <View style={styles.pendingBadge}>
        <Text style={styles.pendingBadgeText}>3 pending</Text>
      </View>
    );
  }
  return (
    <TouchableOpacity style={styles.menuOption} activeOpacity={0.7}>
      <View style={styles.menuIcon}>{icon}</View>
      <Text style={styles.menuLabel}>{label}</Text>
      {badge && <View style={styles.menuBadge}>{badge}</View>}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'flex-start',
    paddingHorizontal: 16,
    paddingTop: 32,
    paddingBottom: 12,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#f1f1f1',
  },
  headerTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#22223b',
  },
  avatarCircle: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: '#f4f6f8',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
  },
  profileCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    marginHorizontal: 16,
    marginTop: 16,
    marginBottom: 16,
    padding: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOpacity: 0.06,
    shadowRadius: 4,
    shadowOffset: { width: 0, height: 2 },
  },
  profileRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  profileName: {
    fontWeight: 'bold',
    fontSize: 18,
    color: '#22223b',
    marginBottom: 2,
  },
  profileMeta: {
    color: '#64748b',
    fontSize: 13,
  },
  statusCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    marginHorizontal: 16,
    marginBottom: 16,
    padding: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOpacity: 0.06,
    shadowRadius: 4,
    shadowOffset: { width: 0, height: 2 },
  },
  statusTitle: {
    fontWeight: 'bold',
    fontSize: 16,
    color: '#22223b',
    marginBottom: 8,
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 4,
  },
  statusLabel: {
    color: '#64748b',
    fontSize: 14,
  },
  statusValue: {
    fontWeight: 'bold',
    fontSize: 15,
    color: '#22223b',
  },
  statusBadge: {
    backgroundColor: '#fffbe6',
    borderColor: '#eab308',
    borderWidth: 1,
    borderRadius: 6,
    paddingHorizontal: 8,
    paddingVertical: 2,
    marginLeft: 8,
  },
  statusBadgeText: {
    color: '#eab308',
    fontWeight: 'bold',
    fontSize: 13,
  },
  menuCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    marginHorizontal: 16,
    marginBottom: 16,
    paddingVertical: 4,
    elevation: 2,
    shadowColor: '#000',
    shadowOpacity: 0.06,
    shadowRadius: 4,
    shadowOffset: { width: 0, height: 2 },
  },
  menuOption: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 14,
    paddingHorizontal: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f1f1f1',
    backgroundColor: '#fff',
  },
  menuIcon: {
    marginRight: 16,
  },
  menuLabel: {
    fontSize: 15,
    color: '#22223b',
    flex: 1,
  },
  menuBadge: {
    marginLeft: 8,
  },
  newBadge: {
    backgroundColor: '#22223b',
    borderRadius: 6,
    paddingHorizontal: 8,
    paddingVertical: 2,
  },
  newBadgeText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 12,
  },
  pendingBadge: {
    backgroundColor: '#f4f6f8',
    borderRadius: 6,
    paddingHorizontal: 8,
    paddingVertical: 2,
  },
  pendingBadgeText: {
    color: '#64748b',
    fontWeight: 'bold',
    fontSize: 12,
  },
});
