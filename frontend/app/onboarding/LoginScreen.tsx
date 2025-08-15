
import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Image, Platform, Animated, Easing } from 'react-native';
import { MaterialIcons, FontAwesome, MaterialCommunityIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
export default function LoginScreen({ onSendOtp, onGoogleSignIn, onSkip }: { onSendOtp?: (phone: string) => void, onGoogleSignIn?: () => void, onSkip?: () => void }) {
  const [phone, setPhone] = useState('');
  const [showAlert, setShowAlert] = useState(false);
  const [googleAnim] = useState(new Animated.Value(0));

  // Shimmer animation for Google button
  React.useEffect(() => {
    Animated.loop(
      Animated.timing(googleAnim, {
        toValue: 1,
        duration: 1800,
        easing: Easing.linear,
        useNativeDriver: true,
      })
    ).start();
  }, []);

  return (
    <LinearGradient
      colors={["#e0f7fa", "#f9fbe7", "#fff"]}
      style={styles.bg}
      start={{ x: 0, y: 0 }}
      end={{ x: 1, y: 1 }}
    >
      <View style={styles.container}>
        {/* Header with back and voice icons would go here */}
        <Text style={styles.title}>Enter Your Mobile Number</Text>
        <View style={styles.inputRow}>
          <View style={styles.iconBox}>
            <MaterialIcons name="phone" size={24} color="#388e3c" style={styles.phoneIcon} />
          </View>
          <Text style={styles.countryCode}>+91</Text>
          <TextInput
            style={styles.input}
            placeholder="Mobile Number"
            placeholderTextColor="#bdbdbd"
            keyboardType="number-pad"
            maxLength={10}
            value={phone}
            onChangeText={text => {
              const cleaned = text.replace(/[^0-9]/g, '');
              setPhone(cleaned);
              if (showAlert && cleaned.length === 10) setShowAlert(false);
            }}
          />
        </View>
        {showAlert && (
          <Text style={styles.alertText}>Please enter a valid 10-digit mobile number</Text>
        )}
        <TouchableOpacity
          activeOpacity={0.85}
          style={styles.shadowWrap}
          onPress={() => {
            if (phone.length !== 10) {
              setShowAlert(true);
            } else {
              setShowAlert(false);
              onSendOtp && onSendOtp(phone);
            }
          }}
          disabled={phone.length !== 10}
        >
          <LinearGradient
            colors={["#43e97b", "#38f9d7"]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={[styles.primaryBtn, phone.length !== 10 && { opacity: 0.5 }]}
          >
            <Text style={styles.primaryBtnText}>Send OTP</Text>
          </LinearGradient>
        </TouchableOpacity>
        <View style={{ height: 18 }} />
        <TouchableOpacity
          style={styles.googleBtn}
          onPress={onGoogleSignIn}
          activeOpacity={0.85}
        >
          <Image source={require('../../assets/images/google-logo.png')} style={[styles.googleLogo, { width: 28, height: 28 }]} />
          <Text style={styles.googleBtnText}>Sign in with Google</Text>
          <Animated.View
            style={[
              styles.shimmer,
              {
                transform: [
                  {
                    translateX: googleAnim.interpolate({
                      inputRange: [0, 1],
                      outputRange: [-60, 260],
                    }),
                  },
                ],
              },
            ]}
          >
            <LinearGradient
              colors={["#fff", "#e0e0e0", "#fff"]}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
              style={styles.shimmerGradient}
            />
          </Animated.View>
        </TouchableOpacity>
        <TouchableOpacity style={styles.outlineBtn} onPress={onSkip} activeOpacity={0.8}>
          <Text style={styles.outlineBtnText}>Skip & Use Offline Mode</Text>
        </TouchableOpacity>
        <View style={{ flex: 1 }} />
        <Image source={require('../../assets/images/adaptive-icon.png')} style={styles.illustration} />
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  bg: {
    flex: 1,
    width: '100%',
    minHeight: '100%',
    justifyContent: 'center',
    alignItems: 'center',
  },
  container: {
    flex: 1,
    width: '100%',
    maxWidth: 400,
    paddingHorizontal: 24,
    paddingTop: 48,
    paddingBottom: 24,
    alignItems: 'center',
    justifyContent: 'center',
    alignSelf: 'center',
  },
  title: {
    fontSize: 26,
    fontWeight: '700',
    color: '#222',
    marginBottom: 32,
    fontFamily: Platform.OS === 'web' ? 'Inter, Arial, sans-serif' : undefined,
    textAlign: 'center',
  },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    borderRadius: 24,
    paddingHorizontal: 12,
    paddingVertical: 4,
    marginBottom: 10,
    width: '100%',
    maxWidth: 320,
    shadowColor: '#000',
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 2,
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  iconBox: {
    width: 32,
    height: 32,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 4,
    backgroundColor: 'transparent',
  },
  phoneIcon: {
    // No background, just icon
  },
  countryCode: {
    fontSize: 18,
    color: '#388e3c',
    fontWeight: 'bold',
    marginRight: 4,
  },
  input: {
    flex: 1,
    borderWidth: 0,
    fontSize: 18,
    paddingVertical: 10,
    paddingHorizontal: 8,
    backgroundColor: 'transparent',
    borderRadius: 20,
    color: '#222',
    fontFamily: Platform.OS === 'web' ? 'Inter, Arial, sans-serif' : undefined,
    letterSpacing: 1,
  },
  shadowWrap: {
    width: '100%',
    maxWidth: 320,
    borderRadius: 30,
    marginTop: 18,
    marginBottom: 8,
    shadowColor: '#43e97b',
    shadowOpacity: 0.18,
    shadowRadius: 12,
    elevation: 4,
  },
  primaryBtn: {
    borderRadius: 30,
    paddingVertical: 16,
    paddingHorizontal: 32,
    width: '100%',
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#43e97b',
    shadowOpacity: 0.18,
    shadowRadius: 12,
    elevation: 4,
    // Animation for tap/hover can be handled by TouchableOpacity's activeOpacity
  },
  primaryBtnText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    letterSpacing: 1,
    fontFamily: Platform.OS === 'web' ? 'Inter, Arial, sans-serif' : undefined,
  },
  googleBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#388e3c',
    borderRadius: 30,
    paddingVertical: 14,
    paddingHorizontal: 32,
    width: '100%',
    maxWidth: 320,
    marginBottom: 16,
    overflow: 'hidden',
    position: 'relative',
  },
  googleLogo: {
    marginRight: 12,
  },
  googleBtnText: {
    color: '#388e3c',
    fontSize: 18,
    fontWeight: 'bold',
    fontFamily: Platform.OS === 'web' ? 'Inter, Arial, sans-serif' : undefined,
    zIndex: 2,
  },
  shimmer: {
    position: 'absolute',
    left: 0,
    top: 0,
    bottom: 0,
    width: 60,
    height: '100%',
    zIndex: 1,
    opacity: 0.35,
  },
  shimmerGradient: {
    flex: 1,
    borderRadius: 30,
  },
  outlineBtn: {
    borderWidth: 1,
    borderColor: '#795548',
    borderRadius: 30,
    paddingVertical: 14,
    paddingHorizontal: 32,
    width: '100%',
    maxWidth: 320,
    marginTop: 8,
    marginBottom: 16,
    backgroundColor: 'rgba(255,255,255,0.7)',
    alignItems: 'center',
  },
  outlineBtnText: {
    color: '#795548',
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
    fontFamily: Platform.OS === 'web' ? 'Inter, Arial, sans-serif' : undefined,
  },
  illustration: {
    width: 120,
    height: 120,
    marginTop: 32,
    resizeMode: 'contain',
    alignSelf: 'center',
  },
  alertText: {
    color: 'red',
    fontSize: 14,
    marginBottom: 2,
    textAlign: 'center',
    width: '100%',
    fontFamily: Platform.OS === 'web' ? 'Inter, Arial, sans-serif' : undefined,
  },
});
