import { MaterialCommunityIcons } from '@expo/vector-icons';
import { AppLogoIcon } from '../../components/ui/AppLogoIcon';
import React, { useState, useRef, useEffect } from 'react';
import { Animated, Easing, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import Footer from '../../components/Footer';
import { useRouter } from 'expo-router';

// FeatureCard component for modern UI
type FeatureCardProps = {
	icon: React.ReactNode;
	title: string;
	subtitle: string;
	color: string;
	onPress: () => void;
};

function FeatureCard({ icon, title, subtitle, color, onPress }: FeatureCardProps) {
	return (
		<TouchableOpacity
			style={{
				flexDirection: 'row',
				alignItems: 'center',
				backgroundColor: '#fff',
				borderRadius: 14,
				borderWidth: 1,
				borderColor: '#e5e7eb',
				padding: 16,
				shadowColor: color,
				shadowOpacity: 0.08,
				shadowRadius: 6,
				shadowOffset: { width: 0, height: 2 },
				elevation: 2,
				marginBottom: 2,
				gap: 12,
				borderLeftWidth: 5,
				borderLeftColor: color,
			}}
			activeOpacity={0.85}
			onPress={onPress}
		>
			{icon}
			<View>
				<Text style={{ fontWeight: 'bold', fontSize: 16, color: '#22223b' }}>{title}</Text>
				<Text style={{ color: '#64748b', fontSize: 13, marginTop: 2 }}>{subtitle}</Text>
			</View>
		</TouchableOpacity>
	);
}

export default function VoiceScreen() {
	const router = useRouter();
	const [modal, setModal] = useState<null | 'crop' | 'market' | 'yield' | 'pest'>(null);
	const [input, setInput] = useState('');
	const [result, setResult] = useState<string | null>(null);
	const [isChatActive, setIsChatActive] = useState(false);

	// Animated voice icon and ring
	const scaleAnim = useRef(new Animated.Value(1)).current;
	const ringAnim = useRef(new Animated.Value(1)).current;
	useEffect(() => {
		Animated.loop(
			Animated.parallel([
				Animated.sequence([
					Animated.timing(scaleAnim, { toValue: 1.18, duration: 1400, useNativeDriver: true, easing: Easing.inOut(Easing.ease) }),
					Animated.timing(scaleAnim, { toValue: 1, duration: 1400, useNativeDriver: true, easing: Easing.inOut(Easing.ease) }),
				]),
				Animated.sequence([
					Animated.timing(ringAnim, { toValue: 1.35, duration: 1400, useNativeDriver: true, easing: Easing.inOut(Easing.ease) }),
					Animated.timing(ringAnim, { toValue: 1, duration: 1400, useNativeDriver: true, easing: Easing.inOut(Easing.ease) }),
				]),
			])
		).start();
	}, [scaleAnim, ringAnim]);

	const handleAction = (type: 'crop' | 'market' | 'yield' | 'pest') => {
		setModal(type);
		setInput('');
		setResult(null);
	};

	const handleSubmit = () => {
		if (modal === 'crop') setResult('Recommended Crop: Wheat\nReason: Best suited for your soil and season.');
		if (modal === 'market') setResult('Predicted Price: ₹2,500/qtl for Wheat\n₹2,100/qtl for Rice');
		if (modal === 'yield') setResult('Estimated Yield: 3.2 tons/ha\nTip: Use balanced fertilizer for better results.');
		if (modal === 'pest') setResult('Pest Risk: High\nAdvice: Use Neem Oil. Monitor weekly.');
	};

	const closeModal = () => {
		setModal(null);
		setInput('');
		setResult(null);
	};

	return (
		<View style={{ flex: 1, backgroundColor: '#fff' }}>
			{/* Header */}
			<View style={styles.header}>
				<View style={{ flexDirection: 'row', alignItems: 'center' }}>
					{/* Changed logo to microphone icon */}
					<MaterialCommunityIcons name="microphone" size={28} color="#6d28d9" style={{ marginRight: 8 }} />
					<Text style={styles.headerTitle}>Your Companion</Text>
				</View>
				<View style={styles.langBadge}><Text style={styles.langBadgeText}>Hindi + English</Text></View>
			</View>
			{/* Animated Voice Icon below header */}
			<View style={{ alignItems: 'center', marginTop: 18, marginBottom: 8 }}>
				<Animated.View style={{
					justifyContent: 'center',
					alignItems: 'center',
					width: 90,
					height: 90,
					borderRadius: 45,
					backgroundColor: '#f3f4f6',
					marginBottom: 0,
					transform: [{ scale: ringAnim }],
					borderWidth: 3,
					borderColor: '#bda6f7',
				}}>
					<Animated.View style={{ transform: [{ scale: scaleAnim }] }}>
						<TouchableOpacity activeOpacity={0.7} onPress={() => router.push({ pathname: '/onboarding/ChatBotScreen', params: { blinkMic: '1' } })} accessibilityLabel="Tap to speak">
							<MaterialCommunityIcons name="microphone" size={56} color="#6d28d9" />
						</TouchableOpacity>
					</Animated.View>
				</Animated.View>
				<Text style={{ color: '#6d28d9', fontWeight: 'bold', marginTop: 18, fontSize: 16 }}>Tap to Speak</Text>
			</View>
			<ScrollView style={{ flex: 1 }} contentContainerStyle={{ paddingBottom: 100 }}>
				 {/* Voice Card */}
				 <View style={styles.voiceCard}>
					 {/* Removed man speaking icon, replaced by animated voice icon above */}
					 <Text style={styles.readyText}>Ready to Help</Text>
					 <Text style={styles.subText}>Try our new AI Smart Tools below</Text>


					 {/* Chatbox UI - Interactive */}
					<TouchableOpacity
						activeOpacity={0.85}
						onPress={() => router.push('/onboarding/ChatBotScreen')}
						style={{
							flexDirection: 'row',
							alignItems: 'center',
							backgroundColor: '#e5e7eb',
							borderRadius: 18,
							paddingHorizontal: 24,
							paddingVertical: 14,
							marginTop: 22,
							marginLeft: 0,
							marginRight: 0,
							width: '100%',
							alignSelf: 'center',
							shadowColor: '#b0b0b0',
							shadowOpacity: 0.5,
							shadowRadius: 16,
							shadowOffset: { width: 0, height: 0 },
							elevation: 8,
							borderWidth: 2,
							borderColor: '#b0b0b0',
						}}
					>
						<MaterialCommunityIcons name="plus" size={24} color="#64748b" style={{ marginRight: 10 }} />
						<Text style={{ color: '#22223b', fontSize: 18, fontWeight: 'bold', letterSpacing: 0.2, flex: 1 }}>
							Ask anything
						</Text>
						<MaterialCommunityIcons name="microphone" size={24} color="#64748b" />
					</TouchableOpacity>
				 </View>
				 <Text style={styles.quickTitle}>AI Smart Tools</Text>
				 <View style={{ gap: 12, marginHorizontal: 8, marginTop: 4 }}>
					 <FeatureCard
						 icon={<MaterialCommunityIcons name="leaf" size={28} color="#22c55e" style={{ marginRight: 12 }} />}
						 title="Crop Recommendation"
						 subtitle="Get the best crop for your field"
						 color="#22c55e"
						 onPress={() => handleAction('crop')}
					 />
					 <FeatureCard
						 icon={<MaterialCommunityIcons name="currency-inr" size={28} color="#eab308" style={{ marginRight: 12 }} />}
						 title="Market Price Prediction"
						 subtitle="Predict market rates for your crops"
						 color="#eab308"
						 onPress={() => handleAction('market')}
					 />
					 <FeatureCard
						 icon={<MaterialCommunityIcons name="chart-line" size={28} color="#2563eb" style={{ marginRight: 12 }} />}
						 title="Yield Prediction"
						 subtitle="Estimate your crop yield"
						 color="#2563eb"
						 onPress={() => handleAction('yield')}
					 />
					 <FeatureCard
						 icon={<MaterialCommunityIcons name="bug" size={28} color="#ef4444" style={{ marginRight: 12 }} />}
						 title="Pest Risk Prediction"
						 subtitle="Assess pest risk for your crop"
						 color="#ef4444"
						 onPress={() => handleAction('pest')}
					 />
				 </View>

				 {/* Modal for AI features */}
				 {modal && (
					 <View style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: '#0008', justifyContent: 'center', alignItems: 'center', zIndex: 10 }}>
						 <View style={{ backgroundColor: '#fff', borderRadius: 18, padding: 24, width: '85%', maxWidth: 350, alignItems: 'center', elevation: 5 }}>
							 <Text style={{ fontWeight: 'bold', fontSize: 18, marginBottom: 8 }}>
								 {modal === 'crop' && 'Crop Recommendation'}
								 {modal === 'market' && 'Market Price Prediction'}
								 {modal === 'yield' && 'Yield Prediction'}
								 {modal === 'pest' && 'Pest Risk Prediction'}
							 </Text>
							 <Text style={{ color: '#64748b', marginBottom: 12, textAlign: 'center' }}>
								 {modal === 'crop' && 'Enter your soil and season details:'}
								 {modal === 'market' && 'Enter crop or market name:'}
								 {modal === 'yield' && 'Enter crop and field details:'}
								 {modal === 'pest' && 'Enter crop and pest details:'}
							 </Text>
							 <View style={{ width: '100%', marginBottom: 12 }}>
								 <View style={{ borderWidth: 1, borderColor: '#e5e7eb', borderRadius: 8, paddingHorizontal: 10, paddingVertical: 6 }}>
									 <input
										 style={{ width: '100%', fontSize: 15, outline: 'none', border: 'none', background: 'transparent' }}
										 placeholder={modal === 'crop' ? 'e.g. Loamy, Kharif' : modal === 'market' ? 'e.g. Wheat, Delhi' : modal === 'yield' ? 'e.g. Rice, 2 acres' : 'e.g. Wheat, Aphid'}
										 value={input}
										 onChange={e => setInput(e.target.value)}
										 autoFocus
									 />
								 </View>
							 </View>
							 <TouchableOpacity style={{ backgroundColor: '#6d28d9', borderRadius: 8, paddingHorizontal: 24, paddingVertical: 10, marginBottom: 8 }} onPress={handleSubmit}>
								 <Text style={{ color: '#fff', fontWeight: 'bold', fontSize: 16 }}>Get Result</Text>
							 </TouchableOpacity>
							 {result && <Text style={{ marginTop: 10, color: '#22c55e', fontWeight: 'bold', textAlign: 'center' }}>{result}</Text>}
							 <TouchableOpacity style={{ marginTop: 16 }} onPress={closeModal}>
								 <Text style={{ color: '#64748b', fontWeight: 'bold' }}>Close</Text>
							 </TouchableOpacity>
						 </View>
					 </View>
				 )}




				{/* Remove everything from here down (duplicate FeatureCard type and function) */}
				{/* FeatureCard component for modern UI
				type FeatureCardProps = {
					icon: React.ReactNode;
					title: string;
					subtitle: string;
					color: string;
					onPress: () => void;
				};

				function FeatureCard({ icon, title, subtitle, color, onPress }: FeatureCardProps) {
					return (
						<TouchableOpacity
							style={{
								flexDirection: 'row',
								alignItems: 'center',
								backgroundColor: '#fff',
								borderRadius: 14,
								borderWidth: 1,
								borderColor: '#e5e7eb',
								padding: 16,
								shadowColor: color,
								shadowOpacity: 0.08,
								shadowRadius: 6,
								shadowOffset: { width: 0, height: 2 },
								elevation: 2,
								marginBottom: 2,
								gap: 12,
								borderLeftWidth: 5,
								borderLeftColor: color,
							}}
							activeOpacity={0.85}
							onPress={onPress}
						>
							{icon}
							<View>
								<Text style={{ fontWeight: 'bold', fontSize: 16, color: '#22223b' }}>{title}</Text>
								<Text style={{ color: '#64748b', fontSize: 13, marginTop: 2 }}>{subtitle}</Text>
							</View>
						</TouchableOpacity>
					);
				} */}
			</ScrollView>
			{/* Custom Footer */}
			<Footer />
		</View>
	);
}

const styles = StyleSheet.create({
	header: {
		flexDirection: 'row',
		alignItems: 'center',
		justifyContent: 'space-between',
		paddingHorizontal: 16,
		paddingTop: 32,
		paddingBottom: 12,
		backgroundColor: '#fff',
	},
	headerTitle: {
		fontSize: 22,
		fontWeight: 'bold',
		color: '#22223b',
	},
	langBadge: {
		backgroundColor: '#f4f6f8',
		borderRadius: 8,
		paddingHorizontal: 10,
		paddingVertical: 4,
	},
	langBadgeText: {
		color: '#64748b',
		fontWeight: 'bold',
		fontSize: 13,
	},
	voiceCard: {
		backgroundColor: '#fff',
		borderRadius: 16,
		margin: 16,
		alignItems: 'center',
		padding: 24,
		elevation: 2,
		shadowColor: '#000',
		shadowOpacity: 0.06,
		shadowRadius: 4,
		shadowOffset: { width: 0, height: 2 },
	},
	micCircle: {
		width: 80,
		height: 80,
		borderRadius: 40,
		backgroundColor: '#f4f6f8',
		alignItems: 'center',
		justifyContent: 'center',
		marginBottom: 16,
	},
	readyText: {
		fontWeight: 'bold',
		fontSize: 18,
		color: '#22223b',
		marginBottom: 4,
	},
	subText: {
		color: '#64748b',
		fontSize: 14,
		marginBottom: 16,
	},
	speakBtn: {
		flexDirection: 'row',
		alignItems: 'center',
		backgroundColor: '#22223b',
		borderRadius: 24,
		paddingHorizontal: 24,
		paddingVertical: 10,
		marginTop: 8,
	},
	speakBtnText: {
		color: '#fff',
		fontWeight: 'bold',
		fontSize: 16,
		marginLeft: 8,
	},
	quickTitle: {
		fontWeight: 'bold',
		fontSize: 16,
		color: '#22223b',
		marginLeft: 16,
		marginTop: 8,
		marginBottom: 8,
	},
	quickCard: {
		backgroundColor: '#fff',
		borderRadius: 12,
		marginHorizontal: 12,
		marginBottom: 12,
		padding: 12,
		borderWidth: 1,
		borderColor: '#e5e7eb',
	},
	quickRow: {
		flexDirection: 'row',
		alignItems: 'center',
	},
	quickMain: {
		fontWeight: 'bold',
		fontSize: 15,
		color: '#22223b',
	},
	quickEn: {
		color: '#64748b',
		fontSize: 13,
		fontWeight: 'normal',
	},
	quickSub: {
		color: '#64748b',
		fontSize: 13,
		marginTop: 2,
	},
	chatBotBtn: {
		flexDirection: 'row',
		alignItems: 'center',
		backgroundColor: '#e0f2fe',
		borderRadius: 16,
		paddingHorizontal: 20,
		paddingVertical: 12,
		marginTop: 16,
		shadowColor: '#000',
		shadowOpacity: 0.1,
		shadowRadius: 8,
		shadowOffset: { width: 0, height: 4 },
		elevation: 4,
	},
	chatBotBtnText: {
		color: '#0d9488',
		fontWeight: 'bold',
		fontSize: 16,
	},
});
