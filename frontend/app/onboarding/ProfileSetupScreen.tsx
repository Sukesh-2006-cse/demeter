import React from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Image } from 'react-native';

export default function ProfileSetupScreen() {
  return (
    <View style={styles.container}>
      {/* Header with back and voice icons would go here */}
      <Text style={styles.title}>Set Up Your Profile</Text>
      <TextInput style={styles.input} placeholder="Name" />
      {/* Replace Picker with a dropdown/selector with flag icons in production */}
      <View style={styles.languageRow}>
        <Text style={styles.label}>Preferred Language:</Text>
        <TextInput style={styles.input} placeholder="Select Language" />
        <TouchableOpacity style={styles.voiceBtn}><Text style={styles.voiceBtnText}>🔊</Text></TouchableOpacity>
      </View>
      <Text style={styles.progress}>Step 2 of 2</Text>
      <TouchableOpacity style={styles.primaryBtn}><Text style={styles.primaryBtnText}>Save & Continue</Text></TouchableOpacity>
      <Image source={require('../../assets/images/adaptive-icon.png')} style={styles.illustration} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff' },
  title: { fontSize: 24, fontWeight: 'bold', color: '#222', marginBottom: 24 },
  input: { borderBottomWidth: 2, borderColor: '#388e3c', fontSize: 18, width: 220, padding: 8, marginBottom: 16 },
  languageRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 16 },
  label: { fontSize: 16, color: '#222', marginRight: 8 },
  voiceBtn: { marginLeft: 8, backgroundColor: '#fbc02d', borderRadius: 20, padding: 8 },
  voiceBtnText: { fontSize: 18 },
  progress: { fontSize: 14, color: '#795548', marginBottom: 16 },
  primaryBtn: { backgroundColor: '#388e3c', borderRadius: 30, paddingVertical: 14, paddingHorizontal: 32, marginBottom: 12, width: 260 },
  primaryBtnText: { color: '#fff', fontSize: 18, fontWeight: 'bold', textAlign: 'center' },
  illustration: { width: 120, height: 120, marginTop: 32, resizeMode: 'contain' },
});
