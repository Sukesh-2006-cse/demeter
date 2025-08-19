
import React, { useEffect, useState } from 'react';
import { useRouter } from 'expo-router';
import { View, Text, Image, TouchableOpacity, ScrollView, StyleSheet, ActivityIndicator, Platform, Animated } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { MaterialCommunityIcons, MaterialIcons, Feather } from '@expo/vector-icons';
const heroImg = require('../../assets/images/react-logo.png');
// If news.json is missing, comment out the import and the news section below, or provide a fallback.
// import news from '../../data/news.json';
import Footer from '../../components/Footer';
import WeatherSection from '../../components/weatherSection';

interface WeatherValues {
  temperature: number;
  humidity: number;
  windSpeed: number;
  precipitationIntensity: number;
}

export default function HomeScreen() {
  // ...existing code...
  const scaleAnim = React.useRef(new Animated.Value(1)).current;

  const handlePressIn = () => {
    Animated.spring(scaleAnim, {
      toValue: 0.93,
      useNativeDriver: true,
      speed: 30,
      bounciness: 8,
    }).start();
  };
  const handlePressOut = () => {
    Animated.spring(scaleAnim, {
      toValue: 1,
      useNativeDriver: true,
      speed: 30,
      bounciness: 8,
    }).start();
  };
  const router = useRouter();
  const [weather, setWeather] = useState<WeatherValues | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedState, setSelectedState] = useState('Andhra Pradesh');
  const [news, setNews] = useState<any[]>([]);
  const [newsLoading, setNewsLoading] = useState(false);
  const states = [
    'Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Goa','Gujarat','Haryana','Himachal Pradesh','Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal','Delhi','Jammu and Kashmir','Ladakh','Puducherry','Chandigarh','Andaman and Nicobar Islands','Dadra and Nagar Haveli and Daman and Diu','Lakshadweep'
  ];
  const [showStatePicker, setShowStatePicker] = useState(false);

  useEffect(() => {
    const fetchWeather = async () => {
      setLoading(true);
      try {
        // Use selectedState as location, fallback to 'Andhra Pradesh' if empty
        const location = selectedState || 'Andhra Pradesh';
        const res = await import('../../services/api');
        const apiService = res.apiService;
        const result = await apiService.getWeatherForecast(location, 1);
        if (result.success && result.data) {
          // Expecting result.data to have temperature, humidity, windSpeed, precipitationIntensity
          setWeather({
            temperature: result.data.temperature ?? 0,
            humidity: result.data.humidity ?? 0,
            windSpeed: result.data.windSpeed ?? 0,
            precipitationIntensity: result.data.precipitationIntensity ?? 0,
          });
        } else {
          setWeather(null);
          console.error('Weather API error:', result.error || result.message);
        }
      } catch (error) {
        setWeather(null);
        console.error('Error fetching weather:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchWeather();
  }, [selectedState]);

  useEffect(() => {
    async function fetchNews() {
      setNewsLoading(true);
      try {
        // newsdata.io endpoint for India, English, agriculture, and state
        const url = `https://newsdata.io/api/1/news?apikey=pub_9f317139e83b4424855bc2e212cbc476&country=in&language=en&q=agriculture farmer ${encodeURIComponent(selectedState)}`;
        const res = await fetch(url);
        const data = await res.json();
        console.log('newsdata.io response:', data);
        if (data.status === 'error' || !Array.isArray(data.results)) {
          setNews([]);
          if (data.message) {
            setNews([{ title: 'API Error', description: data.message }]);
          }
        } else {
          setNews(data.results);
        }
      } catch (e) {
        setNews([{ title: 'Network Error', description: String(e) }]);
      } finally {
        setNewsLoading(false);
      }
    }
    fetchNews();
  }, [selectedState]);

  return (
    <View style={{ flex: 1, backgroundColor: "#f9fafb" }}>
      <ScrollView contentContainerStyle={{ paddingBottom: 100 }}>
        {/* Header */}
        <View style={styles.headerCard}>
          <View style={{ flexDirection: "row", alignItems: "center", flex: 1 }}>
            <View style={{ marginRight: 10 }}>
              <View accessible accessibilityLabel="Demeter logo">
                <View style={{ width: 36, height: 36, marginRight: 4 }}>
                  <View style={{ width: 36, height: 36, borderRadius: 18, backgroundColor: "#22c55e", justifyContent: "center", alignItems: "center" }}>
                    <MaterialCommunityIcons name="leaf" size={20} color="#fff" />
                  </View>
                </View>
              </View>
            </View>
            <View style={{ flex: 1 }}>
              <Text style={styles.headerTitle}>Demeter</Text>
              <Text style={styles.headerSubtitle}>Agricultural AI Companion</Text>
            </View>
          </View>
          {/* Advanced UI State Selector */}
          <View style={styles.advancedStateBox}>
            <Picker
              selectedValue={selectedState}
              onValueChange={value => setSelectedState(value)}
              style={styles.advancedPicker}
              dropdownIconColor="#2563eb"
              accessibilityLabel="Select State for News"
            >
              <Picker.Item label="Select State" value="" color="#2563eb" />
              {states.map(state => <Picker.Item key={state} label={state} value={state} />)}
            </Picker>
          </View>
        </View>
  {/* State Picker Modal removed, now in header */}

        {/* Hero */}
        <View style={styles.heroCard}>
          <Image
            source={require('../../assets/images/hi.png')}
            style={styles.heroImg}
            accessible
            accessibilityLabel="Demeter hero"
          />
          <Animated.View style={{
            transform: [{ scale: scaleAnim }],
            shadowColor: '#22c55e',
            shadowOffset: { width: 0, height: 8 },
            shadowOpacity: 0.35,
            shadowRadius: 16,
            elevation: 8,
          }}>
            <TouchableOpacity
              style={styles.getStartedBtn}
              accessibilityLabel="Get Started"
              onPress={() => router.push('/onboarding/ChatBotScreen')}
              onPressIn={handlePressIn}
              onPressOut={handlePressOut}
              activeOpacity={0.85}
            >
              <Text style={styles.getStartedText}>Get Started</Text>
            </TouchableOpacity>
          </Animated.View>
        </View>

  {/* Crop & Growth Stage removed as requested */}


        {/* Weather Section */}
        <WeatherSection weather={weather} loading={loading} />

  {/* State Selector removed from below weather, now in header */}

        {/* News Section */}
        <View style={{ marginTop: 8, marginBottom: 16, paddingHorizontal: 12 }}>
          <View style={{ backgroundColor: '#e8f5e9', borderRadius: 16, padding: 0, shadowColor: '#388e3c', shadowOpacity: 0.08, shadowRadius: 6, elevation: 2 }}>
            <View style={{ flexDirection: 'row', alignItems: 'center', backgroundColor: '#22c55e', borderTopLeftRadius: 16, borderTopRightRadius: 16, paddingVertical: 10, paddingHorizontal: 14 }}>
              <MaterialCommunityIcons name="newspaper-variant-outline" size={22} color="#fff" style={{ marginRight: 8 }} />
              <Text style={{ fontWeight: 'bold', fontSize: 18, color: '#fff', flex: 1 }}>Agri & Farmer News ({selectedState})</Text>
            </View>
            <View style={{ padding: 14 }}>
              {newsLoading ? (
                <ActivityIndicator size="large" color="#388e3c" style={{ marginVertical: 16 }} />
              ) : news.length === 0 ? (
                <Text style={{ color: '#888', fontSize: 15, textAlign: 'center', marginVertical: 16 }}>No news found.</Text>
              ) : (
                news.slice(0, 5).map((item, idx) => (
                  <View key={idx} style={{
                    backgroundColor: item.title === 'API Error' || item.title === 'Network Error' ? '#fee2e2' : '#fff',
                    borderRadius: 12,
                    marginBottom: 12,
                    padding: 12,
                    elevation: 1,
                    borderWidth: item.title === 'API Error' || item.title === 'Network Error' ? 1 : 0,
                    borderColor: item.title === 'API Error' || item.title === 'Network Error' ? '#ef4444' : 'transparent',
                    flexDirection: 'row',
                    alignItems: 'flex-start',
                  }}>
                    <MaterialCommunityIcons name={item.title === 'API Error' || item.title === 'Network Error' ? 'alert-circle-outline' : 'leaf'} size={22} color={item.title === 'API Error' || item.title === 'Network Error' ? '#ef4444' : '#22c55e'} style={{ marginRight: 10, marginTop: 2 }} />
                    <View style={{ flex: 1 }}>
                      <Text style={{ fontWeight: 'bold', fontSize: 15, color: item.title === 'API Error' || item.title === 'Network Error' ? '#ef4444' : '#222', marginBottom: 2 }}>{item.title}</Text>
                      {item.source && <Text style={{ color: '#2563eb', fontSize: 13 }}>{item.source.name}</Text>}
                      <Text style={{ color: '#555', fontSize: 13, marginTop: 2 }}>{item.description}</Text>
                      {item.url && <Text style={{ color: '#388e3c', fontSize: 13, marginTop: 2 }} numberOfLines={1}>{item.url}</Text>}
                    </View>
                  </View>
                ))
              )}
            </View>
          </View>
        </View>

        {/* News */}
        {/*
        <View style={styles.newsSection}>
          <View style={{ flexDirection: "row", alignItems: "center", marginBottom: 10 }}>
            <MaterialCommunityIcons name="newspaper-variant-outline" size={18} color="#22c55e" style={{ marginRight: 6 }} accessibilityLabel="News icon" />
            <Text style={styles.newsTitle}>Agriculture News</Text>
          </View>
          {news.map((item, idx) => (
            <TouchableOpacity
              key={idx}
              style={styles.newsCard}
              accessibilityLabel={item.title}
            >
              <Image
                source={{ uri: item.img }}
                style={styles.newsImg}
                resizeMode="cover"
                accessible
                accessibilityLabel={item.title}
              />
              <View style={{ flex: 1, marginLeft: 10 }}>
                <Text style={styles.newsCardTitle} numberOfLines={1}>{item.title}</Text>
                <Text style={styles.newsCardSummary} numberOfLines={1}>{item.summary}</Text>
              </View>
              <Feather name="chevron-right" size={20} color="#22c55e" accessibilityLabel="Read more" style={{ marginLeft: 8 }} />
            </TouchableOpacity>
          ))}
        </View>
        */}
      </ScrollView>
      <Footer />
    </View>
  );
}

const styles = StyleSheet.create({
  headerCard: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#f0fdf4",
    borderRadius: 18,
    padding: 16,
    marginTop: 24,
    marginHorizontal: 16,
    marginBottom: 16,
    shadowColor: "#000",
    shadowOpacity: 0.04,
    shadowRadius: 4,
    elevation: 2,
  },
  advancedStateBox: {
    borderWidth: 2,
    borderColor: '#166534', // dark green
    borderRadius: 16,
    backgroundColor: '#f0fdf4',
    paddingHorizontal: 10,
    paddingVertical: 0,
    marginLeft: 8,
    minWidth: 140,
    maxWidth: 170,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#22c55e', // lighter green for shine
    shadowOpacity: 0.18,
    shadowRadius: 6,
    elevation: 4,
    height: 40,
    flexDirection: 'row',
    overflow: 'hidden',
  },
  advancedStateLabel: {
    color: '#2563eb',
    fontWeight: 'bold',
    fontSize: 15,
    marginBottom: 2,
    textAlign: 'center',
  },
  advancedPicker: {
    width: 140,
    height: 40,
    color: '#222',
    fontSize: 15,
    backgroundColor: 'transparent',
    borderRadius: 16,
    borderWidth: 0,
    marginTop: 0,
    paddingLeft: 8,
    paddingRight: 8,
    paddingVertical: 0,
    textAlignVertical: 'center',
    borderColor: 'transparent', // force no black border
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#15803d",
  },
  headerSubtitle: {
    fontSize: 12,
    color: "#166534",
    marginTop: 2,
  },
  newsBtn: {
    backgroundColor: "#bbf7d0",
    borderRadius: 999,
    padding: 8,
  },
  heroCard: {
    backgroundColor: "#e5e7eb",
    borderRadius: 18,
    marginHorizontal: 16,
    marginBottom: 16,
    overflow: "hidden",
    aspectRatio: 1, // Square shape
    position: "relative",
    shadowColor: "#000",
    shadowOpacity: 0.04,
    shadowRadius: 4,
    elevation: 2,
    width: "100%",
    maxWidth: 400,
    alignSelf: "center",
  },
  heroImg: {
    width: "100%",
    height: "100%",
    borderRadius: 18,
    resizeMode: "contain",
  },
  getStartedBtn: {
    position: "absolute",
    left: 16,
    bottom: 16,
    backgroundColor: "#22c55e",
    borderRadius: 999,
    paddingVertical: 10,
    paddingHorizontal: 28,
    shadowColor: "#000",
    shadowOpacity: 0.12,
    shadowRadius: 4,
    elevation: 2,
  },
  getStartedText: {
    color: "#fff",
    fontWeight: "600",
    fontSize: 16,
  },
  row: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 20 },
  card: { flex: 1, alignItems: 'center', padding: 16, borderRadius: 12, marginHorizontal: 4, elevation: 1 },
  cardLabel: { fontSize: 13, color: '#64748b', marginTop: 8 },
  cardValue: { fontSize: 16, fontWeight: 'bold', color: '#22223b', marginTop: 2 },
});

