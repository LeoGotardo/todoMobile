import React, { useState } from 'react';
import {
  SafeAreaView,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { SocketClient } from '../services/SocketClient';
import { styles } from '../styles/styles';

interface RegisterScreenProps {
  onRegisterSuccess: () => void;
}

const RegisterScreen: React.FC<RegisterScreenProps> = ({ onRegisterSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleRegister = async () => {
    if (!username || !password) {
      Alert.alert('Erro', 'Por favor, preencha todos os campos');
      return;
    }

    setLoading(true);
    const client = new SocketClient();
    const response = await client.sendAndReceive({
      type: 'createUser',
      username,
      password,
    });
    setLoading(false);

    if (response.success) {
      Alert.alert('Sucesso', 'Usuário registrado com sucesso!', [
        { text: 'OK', onPress: onRegisterSuccess },
      ]);
    } else {
      Alert.alert('Erro', response.error || 'Falha no registro');
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.loginContainer}>
        <Text style={styles.title}>Criar Conta</Text>
        
        <TextInput
          style={styles.input}
          placeholder="Email"
          value={username}
          onChangeText={setUsername}
          autoCapitalize="none"
          keyboardType="email-address"
        />
        
        <TextInput
          style={styles.input}
          placeholder="Senha"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />
        
        <TouchableOpacity
          style={[styles.button, styles.primaryButton]}
          onPress={handleRegister}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Registrar</Text>
          )}
        </TouchableOpacity>
        
        <TouchableOpacity
          style={[styles.button, styles.secondaryButton]}
          onPress={onRegisterSuccess}
        >
          <Text style={styles.secondaryButtonText}>Voltar ao Login</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

export default RegisterScreen;