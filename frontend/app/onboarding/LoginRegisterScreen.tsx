import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, TextInput, KeyboardAvoidingView, Platform, ActivityIndicator } from 'react-native';
import { MaterialIcons, Feather, FontAwesome } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

export default function LoginRegisterScreen() {
  const router = useRouter();
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [pin, setPin] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState<'login' | 'register'>('login');

  // Only allow 10 digits for phone
  const handlePhoneChange = (text: string) => {
    const cleaned = text.replace(/[^0-9]/g, '').slice(0, 10);
    setPhone(cleaned);
  };

  const handleConfirm = async () => {
    if ((phone.length !== 10 && !email) || pin.length !== 4) {
      setError('Please enter a valid 10-digit phone OR an email, and a 4-digit PIN.');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const endpoint = mode === 'register' ? 'register' : 'login';
      const res = await fetch('http://localhost:8000/' + endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone: phone || undefined, email: email || undefined, pin }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || 'Something went wrong.');
      } else {
        setError('');
        router.replace('/(tabs)');
      }
    } catch (err) {
      setError('Network error.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView style={styles.container} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      {/* Header without icon */}
      <View style={{ alignItems: 'center', marginBottom: 12 }}>
        <Text style={styles.title}>{mode === 'login' ? 'Login' : 'Register'}</Text>
      </View>
      {/* Input with icon */}
      <View style={styles.inputRow}>
        <Feather name="phone" size={22} color="#388e3c" style={styles.inputIcon} />
        <TextInput
          style={[styles.input, { backgroundColor: 'transparent' }]}
          placeholder="Phone Number"
          keyboardType="number-pad"
          value={phone}
          onChangeText={handlePhoneChange}
          maxLength={10}
          placeholderTextColor="#888"
          returnKeyType="next"
        />
      </View>
      <View style={styles.inputRow}>
        <MaterialIcons name="email" size={22} color="#388e3c" style={styles.inputIcon} />
        <TextInput
          style={[styles.input, { backgroundColor: 'transparent' }]}
          placeholder="Email ID"
          keyboardType="email-address"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          placeholderTextColor="#888"
          returnKeyType="next"
        />
      </View>
      <View style={styles.inputRow}>
        <FontAwesome name="lock" size={22} color="#388e3c" style={styles.inputIcon} />
        <TextInput
          style={[styles.input, { backgroundColor: 'transparent' }]}
          placeholder="4-digit PIN Password"
          keyboardType="number-pad"
          value={pin}
          onChangeText={setPin}
          maxLength={4}
          secureTextEntry
          placeholderTextColor="#888"
          returnKeyType="done"
        />
      </View>
      {error ? <Text style={styles.error}>{error}</Text> : null}
      {loading ? <ActivityIndicator size="large" color="#388e3c" style={{ marginBottom: 12 }} /> : null}
      <TouchableOpacity style={styles.primaryBtn} onPress={handleConfirm} disabled={loading}>
        <Text style={styles.primaryBtnText}>{mode === 'login' ? 'Login' : 'Register'}</Text>
        <MaterialIcons name="arrow-forward-ios" size={18} color="#fff" style={{ marginLeft: 8 }} />
      </TouchableOpacity>
      <TouchableOpacity onPress={() => setMode(mode === 'login' ? 'register' : 'login')} style={{ marginTop: 18 }}>
        <Text style={{ color: '#388e3c', fontWeight: 'bold', fontSize: 15 }}>
          {mode === 'login' ? "Don't have an account? Register" : 'Already have an account? Login'}
        </Text>
      </TouchableOpacity>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff', paddingHorizontal: 16 },
  title: { fontSize: 28, fontWeight: 'bold', color: '#222', marginBottom: 8, textAlign: 'center' },
  inputRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 18, backgroundColor: 'transparent', borderRadius: 18, paddingHorizontal: 12, paddingVertical: 2, width: 270 },
  inputIcon: { marginRight: 8 },
  input: { flex: 1, borderBottomWidth: 0, fontSize: 18, paddingVertical: 10, color: '#222', backgroundColor: 'transparent' },
  error: { color: '#d32f2f', marginBottom: 12, fontSize: 15, textAlign: 'center' },
  primaryBtn: { backgroundColor: '#388e3c', borderRadius: 30, paddingVertical: 16, paddingHorizontal: 32, marginTop: 8, width: 260, flexDirection: 'row', alignItems: 'center', justifyContent: 'center' },
  primaryBtnText: { color: '#fff', fontSize: 18, fontWeight: 'bold', textAlign: 'center', marginRight: 6 },
});
