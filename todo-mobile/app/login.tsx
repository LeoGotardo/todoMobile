// app/login.tsx
import { checkRedirectResult, signInWithGoogle } from '@/lib/authFunctions';
import React, { useEffect } from 'react';
import { View, Button, Alert, StyleSheet, Text } from 'react-native';

const Login: React.FC = () => {
  useEffect(() => {
    // Verificar se há resultado de redirect quando o componente monta
    const handleRedirectResult = async () => {
      try {
        const result = await checkRedirectResult();
        if (result.success && result.data) {
          console.log('Login bem-sucedido via redirect:', result.data.user.email);
        } else if (!result.success) {
          console.error('Erro no redirect:', result.error);
          Alert.alert('Erro de Autenticação', result.error.errorMessage);
        }
      } catch (error) {
        console.error('Erro ao verificar redirect:', error);
      }
    };

    handleRedirectResult();
  }, []);

  const handleGoogleSignIn = async (): Promise<void> => {
    try {
      await signInWithGoogle();
      // O redirect acontecerá automaticamente
    } catch (error: any) {
      console.error('Erro no login:', error);
      Alert.alert(
        'Erro', 
        'Falha ao iniciar login com Google. Tente novamente.'
      );
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>ToDo Mobile</Text>
      <Text style={styles.subtitle}>Faça login para continuar</Text>
      
      <View style={styles.buttonContainer}>
        <Button 
          title="Entrar com Google" 
          onPress={handleGoogleSignIn}
          color="#4285F4"
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  subtitle: {
    fontSize: 16,
    marginBottom: 40,
    color: '#666',
    textAlign: 'center',
  },
  buttonContainer: {
    width: '100%',
    maxWidth: 250,
  },
});

export default Login;