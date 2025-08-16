import React from "react";
import { View, Text, Image, TouchableOpacity, ScrollView, StyleSheet } from "react-native";
import { MaterialCommunityIcons, MaterialIcons, Feather } from '@expo/vector-icons';

import Footer from '../../components/Footer';

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

export default function HomeScreen() {
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

      {/* Shared Footer */}
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
});
