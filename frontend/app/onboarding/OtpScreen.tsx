import React, { useState, useRef } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity } from 'react-native';

export default function OtpScreen({ onVerify, onBack }: { onVerify?: () => void; onBack?: () => void }) {
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const inputs = useRef<(TextInput | null)[]>([]);

  const handleChange = (text: string, idx: number) => {
    if (/^\d?$/.test(text)) {
      const newOtp = [...otp];
      newOtp[idx] = text;
      setOtp(newOtp);
      if (text && idx < 5) {
        inputs.current[idx + 1]?.focus();
      }
    }
  };

  const handleKeyPress = (e: any, idx: number) => {
    if (e.nativeEvent.key === 'Backspace' && otp[idx] === '' && idx > 0) {
      inputs.current[idx - 1]?.focus();
    }
  };

  return (
    <View style={styles.container}>
      {/* Header with back and voice icons would go here */}
      <Text style={styles.title}>Verify OTP</Text>
      <View style={styles.otpRow}>
        {otp.map((digit, i) => (
          <TextInput
            key={i}
            ref={ref => { inputs.current[i] = ref; }}
            style={styles.otpInput}
            maxLength={1}
            keyboardType="number-pad"
            value={digit}
            onChangeText={text => handleChange(text, i)}
            onKeyPress={e => handleKeyPress(e, i)}
            returnKeyType={i === 5 ? 'done' : 'next'}
            autoFocus={i === 0}
          />
        ))}
      </View>
      <TouchableOpacity style={styles.primaryBtn} onPress={onVerify}><Text style={styles.primaryBtnText}>Verify</Text></TouchableOpacity>
      <TouchableOpacity><Text style={styles.resend}>Resend OTP</Text></TouchableOpacity>
      {onBack && (
        <TouchableOpacity onPress={onBack} style={{ marginTop: 8 }}><Text style={{ color: '#388e3c' }}>Back</Text></TouchableOpacity>
      )}
      {/* Shield animation placeholder */}
      <View style={styles.shield}><Text>🛡️</Text></View>
    </View>
  );
}
// ...existing code...

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff' },
  title: { fontSize: 24, fontWeight: 'bold', color: '#222', marginBottom: 32 },
  otpRow: { flexDirection: 'row', justifyContent: 'center', marginBottom: 24 },
  otpInput: { width: 44, height: 54, borderWidth: 2, borderColor: '#388e3c', borderRadius: 10, fontSize: 24, textAlign: 'center', marginHorizontal: 6, backgroundColor: '#f9fbe7' },
  primaryBtn: { backgroundColor: '#388e3c', borderRadius: 30, paddingVertical: 14, paddingHorizontal: 32, marginBottom: 12, width: 260 },
  primaryBtnText: { color: '#fff', fontSize: 18, fontWeight: 'bold', textAlign: 'center' },
  resend: { color: '#388e3c', fontWeight: 'bold', marginTop: 8 },
  shield: { marginTop: 32, fontSize: 32 },
});
