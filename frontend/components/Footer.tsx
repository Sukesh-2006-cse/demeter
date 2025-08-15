import { MaterialCommunityIcons, MaterialIcons } from '@expo/vector-icons';
import { Link, usePathname } from 'expo-router';
import React from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';

export default function Footer() {
  const pathname = usePathname();
  return (
    <View style={styles.footer}>
      {/* Home */}
      <Link href="/(tabs)" asChild>
        <TouchableOpacity style={pathname === '/(tabs)' || pathname === '/' ? styles.footerItemActive : styles.footerItem} activeOpacity={0.7} disabled={pathname === '/(tabs)' || pathname === '/'}>
          <MaterialCommunityIcons name="sprout" size={28} color="#22c55e" />
          <Text style={pathname === '/(tabs)' || pathname === '/' ? styles.footerLabelActive : styles.footerLabel}>Home</Text>
        </TouchableOpacity>
      </Link>
      {/* Alerts */}
      <Link href="/(tabs)/alerts" asChild>
        <TouchableOpacity style={pathname === '/(tabs)/alerts' ? styles.footerItemActive : styles.footerItem} activeOpacity={0.7} disabled={pathname === '/(tabs)/alerts'}>
          <MaterialIcons name="notification-important" size={28} color="#ef4444" />
          <Text style={pathname === '/(tabs)/alerts' ? styles.footerLabelActive : styles.footerLabel}>Alerts</Text>
        </TouchableOpacity>
      </Link>
      {/* Voice */}
      <Link href="/(tabs)/voice" asChild>
        <TouchableOpacity style={pathname === '/(tabs)/voice' ? styles.footerItemActive : styles.footerItem} activeOpacity={0.7} disabled={pathname === '/(tabs)/voice'}>
          <MaterialCommunityIcons name="account-voice" size={28} color="#6d28d9" />
          <Text style={pathname === '/(tabs)/voice' ? styles.footerLabelActive : styles.footerLabel}>Voice</Text>
        </TouchableOpacity>
      </Link>
      {/* Community */}
      <Link href="/(tabs)/community" asChild>
        <TouchableOpacity style={pathname === '/(tabs)/community' ? styles.footerItemActive : styles.footerItem} activeOpacity={0.7} disabled={pathname === '/(tabs)/community'}>
          <MaterialCommunityIcons name="account-group" size={28} color="#6d28d9" />
          <Text style={pathname === '/(tabs)/community' ? styles.footerLabelActive : styles.footerLabel}>Community</Text>
        </TouchableOpacity>
      </Link>
      {/* Menu */}
      <Link href="/(tabs)/menu" asChild>
        <TouchableOpacity style={pathname === '/(tabs)/menu' ? styles.footerItemActive : styles.footerItem} activeOpacity={0.7} disabled={pathname === '/(tabs)/menu'}>
          <MaterialIcons name="menu" size={28} color={pathname === '/(tabs)/menu' ? '#22223b' : '#64748b'} />
          <Text style={pathname === '/(tabs)/menu' ? styles.footerLabelActive : styles.footerLabel}>Menu</Text>
        </TouchableOpacity>
      </Link>
    </View>
  );
}

const styles = StyleSheet.create({
  footer: {
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 0,
    height: 72,
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 8,
    zIndex: 10,
  },
  footerItem: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 8,
    borderRadius: 12,
  },
  footerItemActive: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 8,
    borderRadius: 12,
    backgroundColor: '#f4f6f8',
  },
  footerLabel: {
    fontSize: 13,
    color: '#64748b',
    marginTop: 2,
  },
  footerLabelActive: {
    fontSize: 13,
    color: '#22223b',
    fontWeight: 'bold',
    marginTop: 2,
  },
});
