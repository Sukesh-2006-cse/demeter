<<<<<<< HEAD
import React from "react";
import { View, Text, Image, TouchableOpacity, ScrollView, StyleSheet } from "react-native";
import { MaterialCommunityIcons, MaterialIcons, Feather } from '@expo/vector-icons';

=======
// HomeScreen.tsx
import React, { useEffect, useState } from 'react';
import { MaterialCommunityIcons, MaterialIcons } from '@expo/vector-icons';
import { ScrollView, StyleSheet, Text, View, ActivityIndicator } from 'react-native';
>>>>>>> 1c536cb9a4e326c74a9552013ff83afab7e1f0c2
import Footer from '../../components/Footer';
import WeatherSection from '../../components/weatherSection';

<<<<<<< HEAD
const heroImg = require("../../assets/images/hi.png");

const news = [
  {
    title: "Monsoon Arrives Early in South India",
    summary: "Farmers prepare for an early sowing season as the monsoon hits Kerala ahead of schedule.",
    img: "https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=80&q=80",
  },
  {
    title: "New Subsidy Scheme Announced",
    summary: "Government introduces new credit subsidies for smallholder farmers.",
    img: "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?auto=format&fit=crop&w=80&q=80",
  },
  {
    title: "Pest Alert: Armyworm Spotted",
    summary: "Agricultural department issues pest alert for maize crops in central India.",
    img: "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=80&q=80",
  },
];
=======
interface WeatherValues {
  temperature: number;
  humidity: number;
  windSpeed: number;
  precipitationIntensity: number;
}
>>>>>>> 1c536cb9a4e326c74a9552013ff83afab7e1f0c2

export default function HomeScreen() {
  const [weather, setWeather] = useState<WeatherValues | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchWeather = async () => {
      try {
        const response = await fetch(
          'https://api.tomorrow.io/v4/timelines?location=40.7128,-74.0060&fields=temperature,humidity,windSpeed,precipitationIntensity&timesteps=1h&units=metric&apikey=KwkYiyncBsyJrB5Q1iCQyilihYH2FD6A'

        );
        const data = await response.json();
        const latest = data.data.timelines[0].intervals[0].values;

        setWeather({
          temperature: latest.temperature,
          humidity: latest.humidity,
          windSpeed: latest.windSpeed,
          precipitationIntensity: latest.precipitationIntensity ?? 0,
        });
      } catch (error) {
        console.error('Error fetching weather:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchWeather();
  }, []);

  return (
    <View style={{ flex: 1, backgroundColor: "#f9fafb" }}>
      <ScrollView contentContainerStyle={{ paddingBottom: 100 }}>
        {/* Header */}
        <View style={styles.headerCard}>
          <View style={{ flexDirection: "row", alignItems: "center" }}>
            <View style={{ marginRight: 10 }}>
              <View accessible accessibilityLabel="Demeter logo">
                <View style={{ width: 36, height: 36, marginRight: 4 }}>
                  <View style={{ width: 36, height: 36, borderRadius: 18, backgroundColor: "#22c55e", justifyContent: "center", alignItems: "center" }}>
                    <MaterialCommunityIcons name="leaf" size={20} color="#fff" />
                  </View>
                </View>
              </View>
            </View>
            <View>
              <Text style={styles.headerTitle}>Demeter</Text>
              <Text style={styles.headerSubtitle}>Agricultural AI Companion</Text>
            </View>
          </View>
          <TouchableOpacity
            accessibilityLabel="News"
            style={styles.newsBtn}
            onPress={() => {}}
          >
            <MaterialCommunityIcons name="newspaper-variant-outline" size={24} color="#22c55e" />
          </TouchableOpacity>
        </View>

<<<<<<< HEAD
        {/* Hero */}
        <View style={styles.heroCard}>
          <Image
            source={heroImg}
            style={styles.heroImg}
            accessible
            accessibilityLabel="Demeter hero"
          />
          <TouchableOpacity style={styles.getStartedBtn} accessibilityLabel="Get Started">
            <Text style={styles.getStartedText}>Get Started</Text>
          </TouchableOpacity>
        </View>

        {/* Weather */}
        <View style={styles.weatherCard}>
          <View style={{ flexDirection: "row", alignItems: "center", marginBottom: 10 }}>
            <Feather name="sun" size={18} color="#fbbf24" style={{ marginRight: 6 }} accessibilityLabel="Weather sun icon" />
            <Text style={styles.weatherTitle}>Weather (Last Updated: 2h ago)</Text>
          </View>
          <View style={styles.weatherRow}>
            <View style={styles.weatherItem}>
              <MaterialCommunityIcons name="thermometer" size={20} color="#22c55e" accessibilityLabel="Temperature" />
              <Text style={styles.weatherValue}>28°C</Text>
              <Text style={styles.weatherLabel}>Temp</Text>
            </View>
            <View style={styles.weatherItem}>
              <Feather name="droplet" size={20} color="#38bdf8" accessibilityLabel="Humidity" />
              <Text style={styles.weatherValue}>65%</Text>
              <Text style={styles.weatherLabel}>Humidity</Text>
            </View>
            <View style={styles.weatherItem}>
              <Feather name="wind" size={20} color="#a3e635" accessibilityLabel="Wind" />
              <Text style={styles.weatherValue}>12 km/h</Text>
              <Text style={styles.weatherLabel}>Wind</Text>
            </View>
            <View style={styles.weatherItem}>
              <MaterialIcons name="wb-sunny" size={20} color="#fde68a" accessibilityLabel="UV Index" />
              <Text style={styles.weatherValue}>5</Text>
              <Text style={styles.weatherLabel}>UV</Text>
            </View>
          </View>
        </View>
=======
        {/* Crop & Growth Stage */}
        <View style={styles.row}>
          <View style={[styles.card, { backgroundColor: '#e6f9ed' }]}>
            <MaterialCommunityIcons name="sprout" size={28} color="#22c55e" />
            <Text style={styles.cardLabel}>Current Crop</Text>
            <Text style={styles.cardValue}>Wheat</Text>
          </View>
          <View style={[styles.card, { backgroundColor: '#e6f0fa' }]}>
            <MaterialCommunityIcons name="calendar-star" size={28} color="#2563eb" />
            <Text style={styles.cardLabel}>Growth Stage</Text>
            <Text style={styles.cardValue}>Flowering</Text>
          </View>
        </View>

        {/* Weather Section */}
        <WeatherSection weather={weather} loading={loading} />
>>>>>>> 1c536cb9a4e326c74a9552013ff83afab7e1f0c2

        {/* News */}
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
      </ScrollView>

<<<<<<< HEAD
      {/* Shared Footer */}
=======
      {/* Footer */}
>>>>>>> 1c536cb9a4e326c74a9552013ff83afab7e1f0c2
      <Footer />
    </View>
  );
}

const styles = StyleSheet.create({
<<<<<<< HEAD
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
  weatherCard: {
    backgroundColor: "#f0fdf4",
    borderRadius: 18,
    marginHorizontal: 16,
    marginBottom: 16,
    padding: 16,
    shadowColor: "#000",
    shadowOpacity: 0.04,
    shadowRadius: 4,
    elevation: 2,
  },
  weatherTitle: {
    fontWeight: "bold",
    color: "#166534",
    fontSize: 15,
  },
  weatherRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 4,
  },
  weatherItem: {
    alignItems: "center",
    flex: 1,
  },
  weatherIcon: {
    fontSize: 20,
    marginBottom: 2,
  },
  weatherValue: {
    fontWeight: "bold",
    color: "#166534",
    fontSize: 15,
  },
  weatherLabel: {
    fontSize: 12,
    color: "#4ade80",
    marginTop: 2,
  },
  newsSection: {
    backgroundColor: "#fff",
    borderRadius: 18,
    marginHorizontal: 16,
    marginBottom: 16,
    padding: 16,
    shadowColor: "#000",
    shadowOpacity: 0.04,
    shadowRadius: 4,
    elevation: 2,
  },
  newsTitle: {
    fontWeight: "bold",
    color: "#166534",
    fontSize: 15,
  },
  newsCard: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#f0fdf4",
    borderRadius: 12,
    padding: 10,
    marginBottom: 10,
  },
  newsImg: {
    width: 48,
    height: 48,
    borderRadius: 8,
    marginRight: 8,
  },
  newsCardTitle: {
    fontWeight: "bold",
    color: "#166534",
    fontSize: 14,
  },
  newsCardSummary: {
    color: "#4ade80",
    fontSize: 12,
    marginTop: 2,
  },
  footerNav: {
    position: "absolute",
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: "#fff", // Add white background
    borderTopColor: "#e5e7eb",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 24,
    paddingVertical: 10,
    maxWidth: 480,
    alignSelf: "center",
    elevation: 8,
    zIndex: 10,
  },
  footerBtn: {
    alignItems: "center",
    justifyContent: "center",
  },
  footerIcon: {
    fontSize: 22,
    color: "#22c55e",
  },
  footerLabel: {
    fontSize: 11,
    color: "#374151",
    marginTop: 4,
  },
=======
  container: { flex: 1, backgroundColor: '#fff', paddingHorizontal: 16, paddingTop: 32 },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#22223b' },
  subtitle: { fontSize: 14, color: '#64748b' },
  offlineBadge: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#fef3c7', borderRadius: 8, paddingHorizontal: 8 },
  offlineText: { color: '#d97706', fontWeight: 'bold', marginLeft: 4, fontSize: 12 },
  row: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 20 },
  card: { flex: 1, alignItems: 'center', padding: 16, borderRadius: 12, marginHorizontal: 4, elevation: 1 },
  cardLabel: { fontSize: 13, color: '#64748b', marginTop: 8 },
  cardValue: { fontSize: 16, fontWeight: 'bold', color: '#22223b', marginTop: 2 },
  section: { backgroundColor: '#fff', borderRadius: 12, padding: 16, marginBottom: 20, elevation: 1 },
  sectionTitle: { fontSize: 16, fontWeight: 'bold', color: '#22223b', marginBottom: 12 },
  healthRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 10 },
  healthLabel: { fontSize: 14, color: '#22223b', marginLeft: 8, width: 90 },
  progressBarBg: { flex: 1, height: 8, backgroundColor: '#e5e7eb', borderRadius: 4, marginHorizontal: 8, overflow: 'hidden' },
  progressBar: { height: 8, borderRadius: 4 },
  healthStatusGood: { color: '#2563eb', fontWeight: 'bold', fontSize: 13, width: 50 },
  healthStatusExcellent: { color: '#22c55e', fontWeight: 'bold', fontSize: 13, width: 70 },
  healthStatusLow: { color: '#eab308', fontWeight: 'bold', fontSize: 13, width: 40 },
  recentAction: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#f0fdf4', borderRadius: 8, padding: 10, marginTop: 8 },
  recentActionTitle: { fontWeight: 'bold', color: '#22223b', fontSize: 14 },
  recentActionSubtitle: { color: '#64748b', fontSize: 12, marginTop: 2 },
>>>>>>> 1c536cb9a4e326c74a9552013ff83afab7e1f0c2
});
