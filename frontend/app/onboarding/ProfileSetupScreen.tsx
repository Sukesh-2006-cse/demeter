import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Image } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { MaterialIcons, Feather } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

const LANGUAGES = [
  { label: 'English', value: 'en', flag: '🇬🇧' },
  { label: 'Hindi', value: 'hi', flag: '🇮🇳' },
  { label: 'Tamil', value: 'ta', flag: '🇮🇳' },
  { label: 'Telugu', value: 'te', flag: '🇮🇳' },
  { label: 'Kannada', value: 'kn', flag: '🇮🇳' },
  { label: 'Marathi', value: 'mr', flag: '🇮🇳' },
];

export default function ProfileSetupScreen() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [language, setLanguage] = useState('');
  const [showLangs, setShowLangs] = useState(false);
  const [image, setImage] = useState<string | null>(null);
  const [error, setError] = useState('');

  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 0.7,
    });
    if (!result.canceled && result.assets && result.assets[0].uri) {
      setImage(result.assets[0].uri);
    }
  };

  const handleSave = () => {
    if (!name || !language) {
      setError('Please fill all fields and select a language.');
      return;
    }
    setError('');
    // Save logic here (API or local storage)
    // Navigate to menu page
    router.replace('/(tabs)/menu');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Set Up Your Profile</Text>
      {/* Profile Picture */}
      <TouchableOpacity style={styles.avatarCircle} onPress={pickImage} accessibilityLabel="Upload profile picture">
        {image ? (
          <Image source={{ uri: image }} style={styles.avatarImg} />
        ) : (
          <MaterialIcons name="person" size={48} color="#bdbdbd" />
        )}
        <View style={styles.cameraIcon}><Feather name="camera" size={18} color="#fff" /></View>
      </TouchableOpacity>
      {/* Name */}
      <View style={styles.inputRow}>
        <MaterialIcons name="person" size={22} color="#388e3c" style={styles.inputIcon} />
        <TextInput style={styles.input} placeholder="Name" value={name} onChangeText={setName} placeholderTextColor="#888" />
      </View>
      {/* Change PIN Option Only */}
      <TouchableOpacity style={styles.changeOptionBtn} onPress={() => router.push('/onboarding/ChangePasswordScreen')} accessibilityLabel="Change PIN">
        <Text style={styles.changeOptionText}>Change PIN</Text>
        <MaterialIcons name="arrow-forward-ios" size={18} color="#388e3c" style={{ marginLeft: 8 }} />
      </TouchableOpacity>
      {/* Language Picker */}
      <TouchableOpacity style={styles.inputRow} onPress={() => setShowLangs(!showLangs)}>
        <MaterialIcons name="language" size={22} color="#388e3c" style={styles.inputIcon} />
        <Text style={[styles.input, { color: language ? '#222' : '#888' }]}>{language ? LANGUAGES.find(l => l.value === language)?.flag + ' ' + LANGUAGES.find(l => l.value === language)?.label : 'Select Language'}</Text>
        <MaterialIcons name={showLangs ? 'expand-less' : 'expand-more'} size={22} color="#888" />
      </TouchableOpacity>
      {showLangs && (
        <View style={styles.langDropdown}>
          {LANGUAGES.map(l => (
            <TouchableOpacity key={l.value} style={styles.langOption} onPress={() => { setLanguage(l.value); setShowLangs(false); }}>
              <Text style={{ fontSize: 18 }}>{l.flag} {l.label}</Text>
            </TouchableOpacity>
          ))}
        </View>
      )}
      {error ? <Text style={styles.error}>{error}</Text> : null}
      <TouchableOpacity style={styles.primaryBtn} onPress={handleSave}>
        <Text style={styles.primaryBtnText}>Save & Continue</Text>
        <MaterialIcons name="arrow-forward-ios" size={18} color="#fff" style={{ marginLeft: 8 }} />
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff' },
  title: { fontSize: 24, fontWeight: 'bold', color: '#222', marginBottom: 18 },
  avatarCircle: { width: 80, height: 80, borderRadius: 40, backgroundColor: '#f3f4f6', alignItems: 'center', justifyContent: 'center', marginBottom: 18, position: 'relative' },
  avatarImg: { width: 80, height: 80, borderRadius: 40 },
  cameraIcon: { position: 'absolute', bottom: 4, right: 4, backgroundColor: '#388e3c', borderRadius: 12, padding: 3, borderWidth: 2, borderColor: '#fff' },
  inputRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 14, backgroundColor: '#f3f4f6', borderRadius: 18, paddingHorizontal: 12, paddingVertical: 2, width: 270 },
  inputIcon: { marginRight: 8 },
  input: { flex: 1, borderBottomWidth: 0, fontSize: 18, paddingVertical: 10, color: '#222', backgroundColor: 'transparent' },
  changeOptionBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', backgroundColor: '#f3f4f6', borderRadius: 18, paddingHorizontal: 12, paddingVertical: 14, marginBottom: 14, width: 270 },
  changeOptionText: { fontSize: 16, color: '#388e3c', fontWeight: '500' },
  langDropdown: { backgroundColor: '#fff', borderRadius: 10, elevation: 3, marginBottom: 10, width: 270, alignSelf: 'center', paddingVertical: 4 },
  langOption: { paddingVertical: 10, paddingHorizontal: 18 },
  error: { color: '#d32f2f', marginBottom: 12, fontSize: 15, textAlign: 'center' },
  primaryBtn: { backgroundColor: '#388e3c', borderRadius: 30, paddingVertical: 14, paddingHorizontal: 32, marginBottom: 12, width: 260, flexDirection: 'row', alignItems: 'center', justifyContent: 'center' },
  primaryBtnText: { color: '#fff', fontSize: 18, fontWeight: 'bold', textAlign: 'center', marginRight: 6 },
});
