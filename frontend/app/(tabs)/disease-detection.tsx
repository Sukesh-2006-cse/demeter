import React, { useState } from "react";
import { View, Text, TouchableOpacity, Image, ActivityIndicator, ScrollView } from "react-native";
import * as ImagePicker from "expo-image-picker";
import { Feather, MaterialCommunityIcons } from "@expo/vector-icons";
import Footer from "../../components/Footer";

export default function DiseaseDetectionScreen() {
  const [image, setImage] = useState<string | null>(null);
  const [predicting, setPredicting] = useState(false);
  const [result, setResult] = useState<string | null>(null);

  const pickImage = async () => {
    setResult(null);
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 0.8,
    });
    if (!result.canceled && result.assets && result.assets[0].uri) {
      setImage(result.assets[0].uri);
    }
  };

  const takePhoto = async () => {
    setResult(null);
    let result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      quality: 0.8,
    });
    if (!result.canceled && result.assets && result.assets[0].uri) {
      setImage(result.assets[0].uri);
    }
  };

  const removeImage = () => {
    setImage(null);
    setResult(null);
  };

  const predictDisease = async () => {
    setPredicting(true);
    setTimeout(() => {
      setResult("Detected: Powdery Mildew"); // Simulate prediction
      setPredicting(false);
    }, 2000);
  };

  return (
    <View style={{ flex: 1, backgroundColor: '#f9fafb' }}>
      <View style={{ flex: 1 }}>
        <ScrollView contentContainerStyle={{ alignItems: 'center', paddingTop: 16, paddingHorizontal: 16, paddingBottom: 120 }}>
          {/* Header moved to top left with logo */}
          <View
  style={{
    flexDirection: 'row',
    alignItems: 'center',
    width: '100%',
    backgroundColor: '#e6f4ea',
    paddingTop: 18,
    paddingBottom: 18,
    paddingLeft: 18,
    borderBottomWidth: 1,
    borderBottomColor: '#d1fae5',
    marginBottom: 8,
  }}
>
  <MaterialCommunityIcons name="bug" size={28} color="#65a30d" style={{ marginRight: 10 }} />
  <Text style={{ fontSize: 22, fontWeight: 'bold', color: '#166534', letterSpacing: 0.5 }}>
    Pest Detection
  </Text>
</View>
          <Text style={{ fontSize: 26, fontWeight: 'bold', color: '#166534', marginBottom: 4 }}>Disease Detection</Text>
          <Text style={{ color: '#64748b', fontSize: 15, marginBottom: 18, textAlign: 'center', maxWidth: 320 }}>
            Upload or capture a clear image of the plant leaf to detect possible diseases. Supported formats: JPG, PNG.
          </Text>
          <View style={{ width: 260, backgroundColor: '#fff', borderRadius: 20, shadowColor: '#000', shadowOpacity: 0.06, shadowRadius: 8, elevation: 2, padding: 18, alignItems: 'center', marginBottom: 18, borderWidth: 1, borderColor: '#e5e7eb' }}>
            {image ? (
              <View style={{ width: 180, height: 180, borderRadius: 16, overflow: 'hidden', marginBottom: 10, position: 'relative', borderWidth: 2, borderColor: '#bbf7d0' }}>
                <Image
                  source={{ uri: image }}
                  style={{ width: '100%', height: '100%', borderRadius: 16, resizeMode: 'cover' }}
                  accessible
                  accessibilityLabel="Selected leaf image"
                />
                <TouchableOpacity
                  onPress={removeImage}
                  style={{ position: 'absolute', top: 8, right: 8, backgroundColor: '#fff', borderRadius: 999, padding: 4, elevation: 2, borderWidth: 1, borderColor: '#e5e7eb' }}
                  accessibilityLabel="Remove image"
                >
                  <Feather name="x" size={18} color="#ef4444" />
                </TouchableOpacity>
              </View>
            ) : (
              <View style={{ width: 180, height: 180, borderRadius: 16, borderWidth: 2, borderColor: '#a3a3a3', borderStyle: 'dashed', backgroundColor: '#f3f4f6', alignItems: 'center', justifyContent: 'center', marginBottom: 10 }}>
                <MaterialCommunityIcons name="image-frame" size={64} color="#a3a3a3" />
                <Text style={{ color: '#a3a3a3', marginTop: 8, fontSize: 15 }}>No Image Selected</Text>
              </View>
            )}
            <View style={{ flexDirection: 'row', justifyContent: 'center', gap: 16, marginTop: 12 }}>
              <TouchableOpacity
                style={{
                  backgroundColor: '#4caf50',
                  borderRadius: 999,
                  paddingVertical: 14,
                  paddingHorizontal: 28,
                  flexDirection: 'row',
                  alignItems: 'center',
                  marginRight: 8,
                  elevation: 2,
                }}
                onPress={pickImage}
                accessibilityLabel="Pick from gallery"
              >
                <Feather name="image" size={22} color="#fff" style={{ marginRight: 8 }} />
                <Text style={{ color: '#fff', fontWeight: 'bold', fontSize: 17 }}>Gallery</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={{
                  backgroundColor: '#a0521d',
                  borderRadius: 999,
                  paddingVertical: 14,
                  paddingHorizontal: 28,
                  flexDirection: 'row',
                  alignItems: 'center',
                  marginLeft: 8,
                  elevation: 2,
                }}
                onPress={takePhoto}
                accessibilityLabel="Open camera"
              >
                <Feather name="camera" size={22} color="#fff" style={{ marginRight: 8 }} />
                <Text style={{ color: '#fff', fontWeight: 'bold', fontSize: 17 }}>Camera</Text>
              </TouchableOpacity>
            </View>
          </View>
          {image && (
            <TouchableOpacity
              style={{ backgroundColor: '#166534', borderRadius: 999, paddingVertical: 14, paddingHorizontal: 40, marginBottom: 18, marginTop: 2, shadowColor: '#166534', shadowOpacity: 0.10, shadowRadius: 4, elevation: 2 }}
              onPress={predictDisease}
              disabled={predicting}
              accessibilityLabel="Detect disease"
            >
              <Text style={{ color: '#fff', fontWeight: 'bold', fontSize: 17, letterSpacing: 0.5 }}>
                {predicting ? "Detecting..." : "Detect Disease"}
              </Text>
            </TouchableOpacity>
          )}
          {predicting && (
            <View style={{ marginTop: 8, marginBottom: 8 }}>
              <ActivityIndicator size="large" color="#22c55e" />
              <Text style={{ color: '#64748b', marginTop: 6 }}>Analyzing image...</Text>
            </View>
          )}
          {result && (
            <View style={{ marginTop: 12, backgroundColor: '#f0fdf4', borderRadius: 16, padding: 16, alignItems: 'center', borderWidth: 1, borderColor: '#bbf7d0', maxWidth: 320 }}>
              <MaterialCommunityIcons name="alert-circle-check" size={32} color="#22c55e" style={{ marginBottom: 4 }} />
              <Text style={{ color: '#166534', fontWeight: 'bold', fontSize: 17, marginBottom: 2 }}>{result}</Text>
              <Text style={{ color: '#64748b', fontSize: 14, textAlign: 'center' }}>If you need more help, consult an expert or try another image.</Text>
              <TouchableOpacity
                style={{ marginTop: 10, backgroundColor: '#e5e7eb', borderRadius: 999, paddingVertical: 8, paddingHorizontal: 22 }}
                onPress={removeImage}
                accessibilityLabel="Try another image"
              >
                <Text style={{ color: '#166534', fontWeight: 'bold', fontSize: 15 }}>Try Another</Text>
              </TouchableOpacity>
            </View>
          )}
        </ScrollView>
      </View>
      {/* Floating camera button added back */}
      
      <Footer />
    </View>
  );
}
