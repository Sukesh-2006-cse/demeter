import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

export default function SplashScreen() {
  return (
    <LinearGradient colors={['#388e3c', '#fbc02d']} style={styles.container}>
      <View style={styles.logoContainer}>
        {/* Replace with your leaf + AI brain icon */}
        <Image source={require('../../assets/images/adaptive-icon.png')} style={styles.logo} />
      </View>
      <Text style={styles.tagline}>Your Farming Companion – Works Even Without Internet</Text>
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.primaryBtn}><Text style={styles.primaryBtnText}>Continue with Mobile Number</Text></TouchableOpacity>
        <TouchableOpacity style={styles.secondaryBtn}><Text style={styles.secondaryBtnText}>Continue with Google</Text></TouchableOpacity>
      </View>
      <Text style={styles.terms}>By continuing, you agree to our Terms</Text>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  logoContainer: { marginBottom: 32 },
  logo: { width: 96, height: 96, resizeMode: 'contain' },
  tagline: { fontSize: 20, fontWeight: 'bold', color: '#222', textAlign: 'center', marginBottom: 40 },
  buttonContainer: { width: '100%', alignItems: 'center' },
  primaryBtn: { backgroundColor: '#388e3c', borderRadius: 30, paddingVertical: 16, paddingHorizontal: 32, marginBottom: 16, width: 280 },
  primaryBtnText: { color: '#fff', fontSize: 18, fontWeight: 'bold', textAlign: 'center' },
  secondaryBtn: { backgroundColor: '#fff', borderRadius: 30, paddingVertical: 16, paddingHorizontal: 32, borderWidth: 1, borderColor: '#388e3c', width: 280 },
  secondaryBtnText: { color: '#388e3c', fontSize: 18, fontWeight: 'bold', textAlign: 'center' },
  terms: { fontSize: 12, color: '#555', marginTop: 24, textAlign: 'center' },
});
