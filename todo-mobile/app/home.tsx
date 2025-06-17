// app/home.tsx
import { signOutUser } from '@/lib/authFunctions';
import { auth } from '@/lib/firebaseConfig';
import React from 'react';
import { View, Button, Text, Alert, StyleSheet } from 'react-native';


const Home: React.FC = () => {
  const currentUser = auth.currentUser;

  const handleSignOut = async (): Promise<void> => {
    try {
      const result = await signOutUser();
      
      if (result.success) {
        console.log(result.message);
        // O redirecionamento será feito automaticamente pelo onAuthStateChanged
      } else {
        console.error('Erro no logout:', result.error);
        Alert.alert('Erro', result.error);
      }
    } catch (error) {
      console.error('Erro inesperado no logout:', error);
      Alert.alert('Erro', 'Ocorreu um erro ao fazer logout.');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.welcomeText}>
        Bem-vindo ao ToDo Mobile!
      </Text>
      
      <Text style={styles.userText}>
        {currentUser?.displayName || currentUser?.email || 'Usuário'}
      </Text>
      
      <View style={styles.content}>
        <Text style={styles.placeholderText}>
          Aqui você pode adicionar suas funcionalidades do ToDo
        </Text>
      </View>
      
      <View style={styles.buttonContainer}>
        <Button 
          title="Sair" 
          onPress={handleSignOut}
          color="#dc3545"
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  welcomeText: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
    color: '#333',
  },
  userText: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 30,
    color: '#666',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  placeholderText: {
    fontSize: 16,
    color: '#999',
    textAlign: 'center',
    fontStyle: 'italic',
  },
  buttonContainer: {
    width: '100%',
    maxWidth: 200,
    alignSelf: 'center',
  },
});

export default Home;