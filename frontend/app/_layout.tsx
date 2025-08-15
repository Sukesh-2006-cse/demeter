import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { useFonts } from 'expo-font';
import { Stack } from 'expo-router';
import { useState } from 'react';
import LoginScreen from './onboarding/LoginScreen';
import OtpScreen from './onboarding/OtpScreen';
import { StatusBar } from 'expo-status-bar';
import 'react-native-reanimated';

import { useColorScheme } from '@/hooks/useColorScheme';


export default function RootLayout() {
  const colorScheme = useColorScheme();
  const [loaded] = useFonts({
    SpaceMono: require('../assets/fonts/SpaceMono-Regular.ttf'),
  });
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showOtp, setShowOtp] = useState(false);
  const [phone, setPhone] = useState('');

  if (!loaded) {
    // Async font loading only occurs in development.
    return null;
  }

  if (!isLoggedIn) {
    if (showOtp) {
      return <OtpScreen onVerify={() => setIsLoggedIn(true)} onBack={() => setShowOtp(false)} />;
    }
    return (
      <LoginScreen
        onSendOtp={(phone) => {
          setPhone(phone);
          setShowOtp(true);
        }}
        onGoogleSignIn={() => setIsLoggedIn(true)}
        onSkip={() => setIsLoggedIn(true)}
      />
    );
  }

  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <Stack>
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="+not-found" />
      </Stack>
      <StatusBar style="auto" />
    </ThemeProvider>
  );
}

export function TabLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
