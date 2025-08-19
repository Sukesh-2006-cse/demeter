import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity } from 'react-native';
import { MaterialIcons, FontAwesome } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

export default function ChangePasswordScreen() {
  const router = useRouter();
  const [oldPin, setOldPin] = useState('');
  const [newPin, setNewPin] = useState('');
  const [confirmPin, setConfirmPin] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = () => {
    if (newPin.length !== 4 || newPin !== confirmPin) {
      setError('PINs must match and be 4 digits.');
      setSuccess('');
      return;
    }
    setError('');
    setSuccess('Password changed successfully!');
    setTimeout(() => router.back(), 1200);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Change Password</Text>
      <View style={styles.inputRow}>
        <FontAwesome name="lock" size={22} color="#388e3c" style={styles.inputIcon} />
        <TextInput style={styles.input} placeholder="Old PIN" keyboardType="number-pad" value={oldPin} onChangeText={setOldPin} maxLength={4} secureTextEntry placeholderTextColor="#888" />
      </View>
      <View style={styles.inputRow}>
        <MaterialIcons name="lock-outline" size={22} color="#388e3c" style={styles.inputIcon} />
        <TextInput style={styles.input} placeholder="New PIN" keyboardType="number-pad" value={newPin} onChangeText={setNewPin} maxLength={4} secureTextEntry placeholderTextColor="#888" />
      </View>
      <View style={styles.inputRow}>
        <MaterialIcons name="lock-outline" size={22} color="#388e3c" style={styles.inputIcon} />
        <TextInput style={styles.input} placeholder="Confirm New PIN" keyboardType="number-pad" value={confirmPin} onChangeText={setConfirmPin} maxLength={4} secureTextEntry placeholderTextColor="#888" />
      </View>
      {error ? <Text style={styles.error}>{error}</Text> : null}
      {success ? <Text style={styles.success}>{success}</Text> : null}
      <TouchableOpacity style={styles.primaryBtn} onPress={handleChange}>
        <Text style={styles.primaryBtnText}>Change Password</Text>
        <MaterialIcons name="arrow-forward-ios" size={18} color="#fff" style={{ marginLeft: 8 }} />
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff', paddingHorizontal: 16 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#222', marginBottom: 18 },
  inputRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 14, backgroundColor: '#f3f4f6', borderRadius: 18, paddingHorizontal: 12, paddingVertical: 2, width: 270 },
  inputIcon: { marginRight: 8 },
  input: { flex: 1, borderBottomWidth: 0, fontSize: 18, paddingVertical: 10, color: '#222', backgroundColor: 'transparent' },
  error: { color: '#d32f2f', marginBottom: 12, fontSize: 15, textAlign: 'center' },
  success: { color: '#388e3c', marginBottom: 12, fontSize: 15, textAlign: 'center' },
  primaryBtn: { backgroundColor: '#388e3c', borderRadius: 30, paddingVertical: 14, paddingHorizontal: 32, marginBottom: 12, width: 260, flexDirection: 'row', alignItems: 'center', justifyContent: 'center' },
  primaryBtnText: { color: '#fff', fontSize: 18, fontWeight: 'bold', textAlign: 'center', marginRight: 6 },
});
