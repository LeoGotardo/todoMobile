import React, { useState, useEffect } from 'react';
import { SafeAreaView, StyleSheet } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import LoginScreen from './src/screens/loginScreen';
import RegisterScreen from './src/screens/registerScreen';
import TodoScreen from './src/screens/todoScreen';

const App: React.FC = () => {
  const [screen, setScreen] = useState<'login' | 'register' | 'todos'>('login');
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    checkAutoLogin();
  }, []);

  const checkAutoLogin = async () => {
    const savedUserId = await AsyncStorage.getItem('userId');
    if (savedUserId) {
      setUserId(savedUserId);
      setScreen('todos');
    }
  };

  const handleLoginSuccess = (id: string) => {
    setUserId(id);
    setScreen('todos');
  };

  const handleLogout = async () => {
    await AsyncStorage.removeItem('userId');
    setUserId(null);
    setScreen('login');
  };

  switch (screen) {
    case 'login':
      return (
        <LoginScreen
          onLoginSuccess={handleLoginSuccess}
          onRegister={() => setScreen('register')}
        />
      );
    case 'register':
      return (
        <RegisterScreen onRegisterSuccess={() => setScreen('login')} />
      );
    case 'todos':
      return userId ? (
        <TodoScreen userId={userId} onLogout={handleLogout} />
      ) : null;
  }
};

export default App;