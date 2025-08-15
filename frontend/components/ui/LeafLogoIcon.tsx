import React from 'react';
import { Image } from 'react-native';

export function LeafLogoIcon({ size = 24, style }: { size?: number; style?: any }) {
  return (
    <Image
      source={require('../../assets/images/leaf-logo.png')}
      style={[{ width: size, height: size, resizeMode: 'contain' }, style]}
    />
  );
}
