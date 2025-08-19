import React, { useState, useRef, useEffect } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, FlatList, KeyboardAvoidingView, Platform, Modal, Animated, Easing } from 'react-native';
import { useNavigation, NavigationProp } from '@react-navigation/native';
import { useLocalSearchParams } from 'expo-router';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';

// Reusable ExpandableMessage component
const ExpandableMessage = ({ text, limit = 200 }: { text: string; limit?: number }) => {
	const [expanded, setExpanded] = useState(false);
	const isLong = text.length > limit;
	const displayText = !expanded && isLong ? text.slice(0, limit) + '...' : text;
	return (
		<View style={{ paddingVertical: 2 }}>
			<View style={{ flexDirection: 'row', flexWrap: 'wrap', alignItems: 'flex-start' }}>
				<Text style={{ fontSize: 16, flexShrink: 1 }}>{displayText}</Text>
			</View>
			{isLong && (
				<TouchableOpacity onPress={() => setExpanded(e => !e)}>
					<Text style={{ color: '#2563eb', marginTop: 2, fontSize: 13, fontWeight: '500' }}>{expanded ? 'Show less' : 'Show more'}</Text>
				</TouchableOpacity>
			)}
		</View>
	);
};

type Message = { id: string; sender: 'bot' | 'user'; text: string };

type RootStackParamList = {
	ChatBotScreen: undefined;
	VoiceScreen: undefined;
	// add other screens here if needed
};

export default function ChatBotScreen() {
    const navigation = useNavigation<NavigationProp<RootStackParamList>>();
    const params = useLocalSearchParams();
    const shouldBlinkMic = params.blinkMic === '1';
    const [messages, setMessages] = useState<Message[]>([
		{ id: '1', sender: 'bot', text: 'Hello! I am your AI assistant. How can I help you today?' }
	]);
	const [input, setInput] = useState('');
	const [listening, setListening] = useState(false);
	const voiceAnim = useRef(new Animated.Value(1)).current;
	const flatListRef = useRef<FlatList<any>>(null);

    useEffect(() => {
        if (flatListRef.current) {
            flatListRef.current.scrollToEnd({ animated: true });
        }
    }, [messages]);

	useEffect(() => {
		if (listening) {
			Animated.loop(
				Animated.sequence([
					Animated.timing(voiceAnim, { toValue: 1.2, duration: 400, useNativeDriver: true, easing: Easing.inOut(Easing.ease) }),
					Animated.timing(voiceAnim, { toValue: 1, duration: 400, useNativeDriver: true, easing: Easing.inOut(Easing.ease) })
				])
			).start();
		} else {
			voiceAnim.setValue(1);
		}
	}, [listening]);

    const handleSend = () => {
        if (!input.trim()) return;
        setMessages(prev => [...prev, { id: Date.now().toString(), sender: 'user', text: input }]);
        setInput('');
        setTimeout(() => {
            setMessages(prev => [...prev, { id: (Date.now() + 1).toString(), sender: 'bot', text: 'This is a sample AI response. (Integrate your backend here!)' }]);
        }, 900);
    };
    

    const handleImage = async () => {
        let result = await ImagePicker.launchImageLibraryAsync({ mediaTypes: ImagePicker.MediaTypeOptions.Images, allowsEditing: true, quality: 0.7 });
        if (!result.canceled && result.assets && result.assets[0]) {
            setMessages(prev => [...prev, { id: Date.now().toString(), sender: 'user', text: '[Image sent]' }]);
        }
    };

	const handleVoice = () => {
		setListening(true); // immediately start listening
		// Simulate listening for 3 seconds, then close
		setTimeout(() => setListening(false), 3000);
	};

    const renderItem = ({ item }: { item: Message }) => (
        <View style={[styles.messageRow, item.sender === 'user' ? styles.userRow : styles.botRow]}>
            {item.sender === 'bot' && <MaterialCommunityIcons name="robot" size={24} color="#6d28d9" style={{ marginRight: 8 }} />}
            <View style={[styles.bubble, item.sender === 'user' ? styles.userBubble : styles.botBubble]}>
                <ExpandableMessage text={item.text} />
            </View>
            {item.sender === 'user' && <MaterialCommunityIcons name="account" size={24} color="#388e3c" style={{ marginLeft: 8 }} />}
        </View>
    );

    return (
        <KeyboardAvoidingView style={{ flex: 1, backgroundColor: '#f8fafc' }} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
			<View style={styles.header}>
				<MaterialCommunityIcons name="robot" size={28} color="#6d28d9" style={{ marginRight: 8 }} />
				<Text style={styles.headerTitle}>AI ChatBot</Text>
				{/* Voice icon moves here when listening */}
				{listening && (
					<TouchableOpacity onPress={handleVoice} activeOpacity={0.7} style={{ marginLeft: 12 }}>
						<Animated.View style={{ transform: [{ scale: voiceAnim }] }}>
							<MaterialCommunityIcons name="microphone" size={28} color="#e53935" />
						</Animated.View>
					</TouchableOpacity>
				)}
			</View>
			<FlatList
				ref={flatListRef}
				data={messages}
				renderItem={renderItem}
				keyExtractor={item => item.id}
				contentContainerStyle={{ padding: 16, paddingBottom: 80 }}
				style={{ flex: 1 }}
			/>
			<View style={styles.inputBar}>
				<TouchableOpacity style={styles.iconBtn} onPress={handleImage} accessibilityLabel="Upload or take image">
					<MaterialCommunityIcons name="plus" size={22} color="#64748b" />
				</TouchableOpacity>
				<View style={{ flex: 1, flexDirection: 'row', alignItems: 'center', backgroundColor: '#e5e7eb', borderRadius: 16, paddingHorizontal: 12, minHeight: 44 }}>
					<TextInput
						style={styles.input}
						placeholder="Ask anything"
						value={input}
						onChangeText={setInput}
						onSubmitEditing={handleSend}
						returnKeyType="send"
						placeholderTextColor="#64748b"
						multiline={false}
						numberOfLines={1}
						textAlignVertical="center"
						autoCorrect
						autoCapitalize="sentences"
					/>
					{/* Voice icon only shown here if not listening */}
					<TouchableOpacity style={[styles.iconBtn, { marginLeft: 8, marginRight: 8 }]} accessibilityLabel="Voice input" onPress={handleVoice}>
						<MaterialCommunityIcons name="microphone" size={22} color="#64748b" />
					</TouchableOpacity>
				</View>
				<TouchableOpacity style={[styles.sendBtn, { marginLeft: 10 }]} onPress={handleSend} accessibilityLabel="Send message">
					<MaterialCommunityIcons name="send" size={22} color="#fff" />
				</TouchableOpacity>
			</View>
			{/* Google Voice style pop-up modal */}
			<Modal visible={listening} transparent animationType="fade">
				<View style={styles.voiceModalOverlay}>
					<View style={styles.voiceModalBox}>
						<TouchableOpacity onPress={handleVoice} activeOpacity={0.7}>
							<Animated.View style={{ alignItems: 'center', justifyContent: 'center', marginBottom: 18, transform: [{ scale: voiceAnim }] }}>
								<MaterialCommunityIcons name="microphone" size={60} color="#e53935" />
								<View style={styles.voiceWaves}>
									<View style={[styles.wave, { backgroundColor: '#e57373', opacity: 0.5 }]} />
									<View style={[styles.wave, { backgroundColor: '#e53935', opacity: 0.7 }]} />
									<View style={[styles.wave, { backgroundColor: '#b71c1c', opacity: 0.9 }]} />
								</View>
							</Animated.View>
						</TouchableOpacity>
						<Text style={{ fontSize: 18, fontWeight: 'bold', color: '#222', marginBottom: 8 }}>Listening...</Text>
						<Text style={{ fontSize: 14, color: '#666', marginBottom: 18 }}>Speak now</Text>
						<TouchableOpacity style={styles.voiceStopBtn} onPress={() => setListening(false)}>
							<Text style={{ color: '#fff', fontWeight: 'bold', fontSize: 16 }}>Stop</Text>
						</TouchableOpacity>
					</View>
				</View>
			</Modal>
		</KeyboardAvoidingView>
	);
}

const styles = StyleSheet.create({
	header: { flexDirection: 'row', alignItems: 'center', padding: 16, backgroundColor: '#fff', borderBottomWidth: 1, borderBottomColor: '#ececec' },
	headerTitle: { fontSize: 20, fontWeight: 'bold', color: '#22223b' },
	messageRow: { flexDirection: 'row', alignItems: 'flex-end', marginBottom: 12 },
	userRow: { justifyContent: 'flex-end' },
	botRow: { justifyContent: 'flex-start' },
	bubble: { maxWidth: '75%', padding: 12, borderRadius: 18 },
	userBubble: { backgroundColor: '#388e3c', borderBottomRightRadius: 4 },
	botBubble: { backgroundColor: '#e9e9fc', borderBottomLeftRadius: 4 },
	inputBar: { flexDirection: 'row', alignItems: 'center', padding: 8, backgroundColor: '#fff', borderTopWidth: 1, borderTopColor: '#ececec', position: 'absolute', bottom: 0, left: 0, right: 0, gap: 8 },
	iconBtn: { backgroundColor: '#e5e7eb', borderRadius: 20, width: 36, height: 36, justifyContent: 'center', alignItems: 'center' },
	input: { flex: 1, fontSize: 17, backgroundColor: 'transparent', paddingHorizontal: 0, paddingVertical: 10, color: '#222', fontWeight: 'bold', minWidth: 60, maxWidth: 400 },
	sendBtn: { backgroundColor: '#6d28d9', borderRadius: 18, padding: 10, justifyContent: 'center', alignItems: 'center' },
	voiceModalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.25)', justifyContent: 'center', alignItems: 'center' },
	voiceModalBox: { backgroundColor: '#fff', borderRadius: 24, padding: 32, alignItems: 'center', width: 300, elevation: 8, shadowColor: '#000', shadowOpacity: 0.15, shadowRadius: 16, shadowOffset: { width: 0, height: 4 } },
	voiceWaves: { flexDirection: 'row', justifyContent: 'center', alignItems: 'center', marginTop: 10, marginBottom: 10 },
	wave: { width: 12, height: 24, borderRadius: 6, marginHorizontal: 3 },
	voiceStopBtn: { backgroundColor: '#e53935', borderRadius: 16, paddingVertical: 8, paddingHorizontal: 32, marginTop: 8 },
});
