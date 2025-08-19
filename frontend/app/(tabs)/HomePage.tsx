import React from "react";
import { View, Text, Image, ScrollView, TouchableOpacity } from "react-native";
import Footer from "../../components/Footer";
import { Feather, MaterialCommunityIcons } from '@expo/vector-icons';

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

export default function HomePage() {
  return (
    <View className="flex-1 bg-gray-50">
      <ScrollView contentContainerStyle={{ paddingBottom: 100 }}>
        {/* Header */}
        <View className="flex-row justify-between items-center bg-green-50 rounded-2xl px-4 py-4 mt-6 mx-4 mb-4 shadow-sm">
          <View className="flex-row items-center">
            <View className="mr-2.5">
              <View accessible accessibilityLabel="Demeter logo">
                <View className="w-9 h-9 mr-1">
                  <View className="w-9 h-9 rounded-full bg-green-500 justify-center items-center">
                    <MaterialCommunityIcons name="leaf" size={20} color="#fff" />
                  </View>
                </View>
              </View>
            </View>
            <View>
              <Text className="text-lg font-bold text-green-800">Demeter</Text>
              <Text className="text-xs text-green-900 mt-0.5">Agricultural AI Companion</Text>
            </View>
          </View>
          <TouchableOpacity
            accessibilityLabel="News"
            className="bg-green-100 rounded-full p-2"
            onPress={() => {}}
          >
            <MaterialCommunityIcons name="newspaper-variant-outline" size={24} color="#22c55e" />
          </TouchableOpacity>
        </View>

        {/* Hero */}
        <View className="bg-gray-200 rounded-2xl mx-4 mb-4 overflow-hidden aspect-square relative shadow-sm w-full max-w-[400px] self-center">
          <Image
            source={heroImg}
            className="w-full h-full rounded-2xl"
            style={{ resizeMode: "contain" }}
            accessible
            accessibilityLabel="Demeter hero"
          />
          <TouchableOpacity className="absolute left-4 bottom-4 bg-green-500 rounded-full py-2 px-7 shadow" accessibilityLabel="Get Started">
            <Text className="text-white font-semibold text-base">Get Started</Text>
          </TouchableOpacity>
        </View>

        {/* Weather */}
        <View className="bg-green-50 rounded-2xl mx-4 mb-4 p-4 shadow-sm">
          <View className="flex-row items-center mb-2.5">
            <Feather name="sun" size={20} color="#fbbf24" style={{ marginRight: 8 }} accessibilityLabel="Weather sun icon" />
            <Text className="font-semibold text-green-900 text-base">Weather (Last Updated: 2h ago)</Text>
          </View>
          <View className="flex-row justify-between mt-1 space-x-2">
            <View className="flex-1 items-center bg-white rounded-xl py-3 mx-0.5 border border-gray-200 shadow-sm">
              <MaterialCommunityIcons name="thermometer" size={18} color="#22c55e" accessibilityLabel="Temperature" />
              <Text className="font-bold text-green-900 text-base mt-1">28°C</Text>
              <Text className="text-xs text-green-600 mt-0.5">Temp</Text>
            </View>
            <View className="flex-1 items-center bg-white rounded-xl py-3 mx-0.5 border border-gray-200 shadow-sm">
              <Feather name="droplet" size={18} color="#38bdf8" accessibilityLabel="Humidity" />
              <Text className="font-bold text-green-900 text-base mt-1">65%</Text>
              <Text className="text-xs text-green-600 mt-0.5">Humidity</Text>
            </View>
            <View className="flex-1 items-center bg-white rounded-xl py-3 mx-0.5 border border-gray-200 shadow-sm">
              <Feather name="wind" size={18} color="#a3e635" accessibilityLabel="Wind" />
              <Text className="font-bold text-green-900 text-base mt-1">12 km/h</Text>
              <Text className="text-xs text-green-600 mt-0.5">Wind</Text>
            </View>
            <View className="flex-1 items-center bg-white rounded-xl py-3 mx-0.5 border border-gray-200 shadow-sm">
              <Feather name="cloud-rain" size={18} color="#60a5fa" accessibilityLabel="Rainfall" />
              <Text className="font-bold text-green-900 text-base mt-1">4 mm</Text>
              <Text className="text-xs text-green-600 mt-0.5">Rainfall</Text>
            </View>
          </View>
        </View>

        {/* News */}
        <View className="bg-white rounded-2xl mx-4 mb-4 p-4 shadow-sm">
          <View className="flex-row items-center mb-2.5">
            <MaterialCommunityIcons name="newspaper-variant-outline" size={18} color="#22c55e" style={{ marginRight: 6 }} accessibilityLabel="News icon" />
            <Text className="font-bold text-green-900 text-base">Agriculture News</Text>
          </View>
          {news.map((item, idx) => (
            <TouchableOpacity
              key={idx}
              className="flex-row items-center bg-green-50 rounded-xl p-2.5 mb-2.5"
              accessibilityLabel={item.title}
            >
              <Image
                source={{ uri: item.img }}
                className="w-12 h-12 rounded-lg mr-2"
                style={{ resizeMode: "cover" }}
                accessible
                accessibilityLabel={item.title}
              />
              <View className="flex-1 ml-2.5">
                <Text className="font-bold text-green-900 text-sm" numberOfLines={1}>{item.title}</Text>
                <Text className="text-green-600 text-xs mt-0.5" numberOfLines={1}>{item.summary}</Text>
              </View>
              <MaterialCommunityIcons name="chevron-right" size={20} color="#22c55e" accessibilityLabel="Read more" style={{ marginLeft: 8 }} />
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>

      {/* Footer */}
  <Footer />
    </View>
  );
}

