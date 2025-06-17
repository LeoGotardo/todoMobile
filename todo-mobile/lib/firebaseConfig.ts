// firebaseConfig.ts
import { initializeApp, FirebaseApp } from 'firebase/app';
import { initializeAuth, getReactNativePersistence } from 'firebase/auth';
import ReactNativeAsyncStorage from '@react-native-async-storage/async-storage';

// Configuração do Firebase
const firebaseConfig = {
  apiKey: "AIzaSyA0AkZ1klZUm6URVI5mTzpLfG3PeAIGJ0M",
  authDomain: "todo-mobile-654e1.firebaseapp.com",
  projectId: "todo-mobile-654e1",
  storageBucket: "todo-mobile-654e1.firebasestorage.app",
  messagingSenderId: "831912942572",
  appId: "1:831912942572:web:77b84027635733d3cd3ec9"
};

// Inicializar Firebase
const app: FirebaseApp = initializeApp(firebaseConfig);

// Inicializar Auth (versão simplificada)
const auth: initializeAuth = initializeAuth(app, { persistence: getReactNativePersistence(ReactNativeAsyncStorage) });

// Configurar idioma
auth.languageCode = 'pt';

// Exportar as instâncias
export { auth };
export default app;