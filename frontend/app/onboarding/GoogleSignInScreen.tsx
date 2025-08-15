import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image } from 'react-native';

export default function GoogleSignInScreen() {
  return (
    <View style={styles.container}>
      {/* Header with back and voice icons would go here */}
      <TouchableOpacity style={styles.googleBtn}>
        <Image source={require('../../assets/images/partial-react-logo.png')} style={styles.googleLogo} />
        <Text style={styles.googleBtnText}>Sign in with Google</Text>
      </TouchableOpacity>
      {/* Optional: show detected name/email after sign-in */}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff' },
  googleBtn: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#fff', borderWidth: 1, borderColor: '#388e3c', borderRadius: 30, paddingVertical: 14, paddingHorizontal: 32 },
  googleLogo: { width: 28, height: 28, marginRight: 12, resizeMode: 'contain' },
  googleBtnText: { color: '#388e3c', fontSize: 18, fontWeight: 'bold' },
});
