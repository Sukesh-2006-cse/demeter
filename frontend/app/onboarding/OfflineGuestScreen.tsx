import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import SplashScreen from './SplashScreen';

export default function App() {
  return <SplashScreen />;
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff' },
  message: { fontSize: 18, color: '#795548', textAlign: 'center', marginBottom: 32, fontWeight: 'bold' },
  primaryBtn: { backgroundColor: '#388e3c', borderRadius: 30, paddingVertical: 14, paddingHorizontal: 32, marginBottom: 12, width: 260 },
  primaryBtnText: { color: '#fff', fontSize: 18, fontWeight: 'bold', textAlign: 'center' },
});
