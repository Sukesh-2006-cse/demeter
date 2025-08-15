import React from 'react';
import { Image } from 'react-native';

export function AppLogoIcon({ size = 28, style }: { size?: number; style?: any }) {
  return (
    <Image
      source={require('../../assets/images/icon.png')}
      style={[{ width: size, height: size, resizeMode: 'contain' }, style]}
    />
  );
}
