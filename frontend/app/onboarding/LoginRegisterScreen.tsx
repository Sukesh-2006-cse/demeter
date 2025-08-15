import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

export default function LoginRegisterScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to Demeter</Text>
      <TouchableOpacity style={styles.primaryBtn} onPress={() => navigation.replace('LoginScreen')}>
        <Text style={styles.primaryBtnText}>Login</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.secondaryBtn} onPress={() => navigation.replace('ProfileSetupScreen')}>
        <Text style={styles.secondaryBtnText}>Register</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff' },
  title: { fontSize: 28, fontWeight: 'bold', color: '#222', marginBottom: 40 },
  primaryBtn: { backgroundColor: '#388e3c', borderRadius: 30, paddingVertical: 16, paddingHorizontal: 32, marginBottom: 16, width: 260 },
  primaryBtnText: { color: '#fff', fontSize: 18, fontWeight: 'bold', textAlign: 'center' },
  secondaryBtn: { backgroundColor: '#fff', borderRadius: 30, paddingVertical: 16, paddingHorizontal: 32, borderWidth: 1, borderColor: '#388e3c', width: 260 },
  secondaryBtnText: { color: '#388e3c', fontSize: 18, fontWeight: 'bold', textAlign: 'center' },
});
