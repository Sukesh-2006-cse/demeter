import React, { useState } from "react";
import { View, Text, TouchableOpacity, Image, ActivityIndicator, ScrollView, Animated, Easing, Dimensions } from "react-native";
import * as ImagePicker from "expo-image-picker";
import { Feather, MaterialCommunityIcons } from "@expo/vector-icons";
import Footer from "../../components/Footer";

export default function PestDetectionScreen() {
  const [image, setImage] = useState<string | null>(null);
  const [predicting, setPredicting] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [fadeAnim] = useState(new Animated.Value(0));
  const screenWidth = Dimensions.get('window').width;


  const pickImage = async () => {
    setResult(null);
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 0.8,
    });
    if (!result.canceled && result.assets && result.assets[0].uri) {
      setImage(result.assets[0].uri);
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 500,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }).start();
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
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 500,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }).start();
    }
  };

  const removeImage = () => {
    setImage(null);
    setResult(null);
    fadeAnim.setValue(0);
  };

  const predictPest = async () => {
    setPredicting(true);
    setTimeout(() => {
      setResult("Detected: Aphid Infestation"); // Simulate prediction
      setPredicting(false);
    }, 2000);
  };

  return (
    <View style={{ flex: 1, backgroundColor: '#f6f8f3' }}>
      {/* Banner */}
      <View style={{ width: '100%', backgroundColor: '#e6f4ea', paddingVertical: 18, alignItems: 'center', flexDirection: 'row', justifyContent: 'center', borderBottomWidth: 1, borderBottomColor: '#d1fae5', marginBottom: 8, shadowColor: '#000', shadowOpacity: 0.03, shadowRadius: 4, elevation: 1 }}>
        <MaterialCommunityIcons name="bug" size={28} color="#65a30d" style={{ marginRight: 10 }} />
        <Text style={{ fontSize: 22, fontWeight: 'bold', color: '#166534', letterSpacing: 0.5 }}>Pest Detection</Text>
      </View>
      <View style={{ flex: 1 }}>
        <ScrollView contentContainerStyle={{ alignItems: 'center', paddingTop: 24, paddingHorizontal: 16, paddingBottom: 120 }}>
          {/* Image Preview Card */}
          <View style={{ width: Math.min(screenWidth - 32, 340), backgroundColor: '#fff', borderRadius: 28, shadowColor: '#000', shadowOpacity: 0.08, shadowRadius: 12, elevation: 3, padding: 22, alignItems: 'center', marginBottom: 22, borderWidth: 1, borderColor: '#e5e7eb' }}>
            {image ? (
              <Animated.View style={{ width: 220, height: 220, borderRadius: 24, overflow: 'hidden', marginBottom: 12, borderWidth: 2, borderColor: '#a3e635', backgroundColor: '#f7fee7', opacity: fadeAnim }}>
                <Image
                  source={{ uri: image }}
                  style={{ width: '100%', height: '100%', borderRadius: 24, resizeMode: 'cover' }}
                  accessible
                  accessibilityLabel="Selected pest image"
                />
                <TouchableOpacity
                  onPress={removeImage}
                  style={{ position: 'absolute', top: 10, right: 10, backgroundColor: '#fff', borderRadius: 999, padding: 5, elevation: 2, borderWidth: 1, borderColor: '#e5e7eb' }}
                  accessibilityLabel="Remove image"
                >
                  <Feather name="x" size={20} color="#ef4444" />
                </TouchableOpacity>
              </Animated.View>
            ) : (
              <View style={{ width: 220, height: 220, borderRadius: 24, borderWidth: 2, borderColor: '#a3a3a3', borderStyle: 'dashed', backgroundColor: '#f3f4f6', alignItems: 'center', justifyContent: 'center', marginBottom: 12 }}>
                <MaterialCommunityIcons name="image-frame" size={72} color="#a3a3a3" />
                <Text style={{ color: '#a3a3a3', marginTop: 12, fontSize: 16, textAlign: 'center', maxWidth: 180 }}>
                  Upload or capture an image to detect pests.
                </Text>
              </View>
            )}
            {/* Upload Buttons */}
            <View style={{ flexDirection: 'row', justifyContent: 'center', gap: 16, marginTop: 8 }}>
              <TouchableOpacity
                style={{ backgroundColor: '#65a30d', borderRadius: 999, paddingVertical: 14, paddingHorizontal: 28, flexDirection: 'row', alignItems: 'center', marginRight: 8, shadowColor: '#65a30d', shadowOpacity: 0.10, shadowRadius: 4, elevation: 2 }}
                onPress={pickImage}
                accessibilityLabel="Pick from gallery"
              >
                <Feather name="image" size={22} color="#fff" />
                <Text style={{ color: '#fff', fontWeight: 'bold', fontSize: 16, marginLeft: 9 }}>Gallery</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={{ backgroundColor: '#b45309', borderRadius: 999, paddingVertical: 14, paddingHorizontal: 28, flexDirection: 'row', alignItems: 'center', marginLeft: 8, shadowColor: '#b45309', shadowOpacity: 0.10, shadowRadius: 4, elevation: 2 }}
                onPress={takePhoto}
                accessibilityLabel="Open camera"
              >
                <Feather name="camera" size={22} color="#fff" />
                <Text style={{ color: '#fff', fontWeight: 'bold', fontSize: 16, marginLeft: 9 }}>Camera</Text>
              </TouchableOpacity>
            </View>
          </View>
          {/* Predict Button */}
          {image && (
            <TouchableOpacity
              style={{ backgroundColor: '#166534', borderRadius: 999, paddingVertical: 16, paddingHorizontal: 48, marginBottom: 22, marginTop: 2, shadowColor: '#166534', shadowOpacity: 0.12, shadowRadius: 4, elevation: 2 }}
              onPress={predictPest}
              disabled={predicting}
              accessibilityLabel="Detect pest"
            >
              <Text style={{ color: '#fff', fontWeight: 'bold', fontSize: 18, letterSpacing: 0.5 }}>
                {predicting ? "Detecting..." : "Detect Pest"}
              </Text>
            </TouchableOpacity>
          )}
          {/* Progress Indicator */}
          {predicting && (
            <View style={{ marginTop: 10, marginBottom: 10 }}>
              <ActivityIndicator size="large" color="#65a30d" />
              <Text style={{ color: '#64748b', marginTop: 8 }}>Analyzing image...</Text>
            </View>
          )}
          {/* Result Card */}
          {result && (
            <View style={{ marginTop: 16, backgroundColor: '#f0fdf4', borderRadius: 20, padding: 20, alignItems: 'center', borderWidth: 1, borderColor: '#bbf7d0', maxWidth: 340 }}>
              <MaterialCommunityIcons name="bug-check" size={36} color="#65a30d" style={{ marginBottom: 6 }} />
              <Text style={{ color: '#166534', fontWeight: 'bold', fontSize: 18, marginBottom: 4 }}>{result}</Text>
              <Text style={{ color: '#64748b', fontSize: 15, textAlign: 'center' }}>For more help, consult an expert or try another image.</Text>
              <TouchableOpacity
                style={{ marginTop: 12, backgroundColor: '#e5e7eb', borderRadius: 999, paddingVertical: 10, paddingHorizontal: 28 }}
                onPress={removeImage}
                accessibilityLabel="Try another image"
              >
                <Text style={{ color: '#166534', fontWeight: 'bold', fontSize: 16 }}>Try Another</Text>
              </TouchableOpacity>
            </View>
          )}
        </ScrollView>
      </View>
      <Footer />
    </View>
  );
}
