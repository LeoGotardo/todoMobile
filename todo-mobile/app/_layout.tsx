// app/_layout.tsx
import React from 'react';
import { Stack } from 'expo-router';

// IMPORTANTE: Importar a configuração do Firebase primeiro
import { auth } from '@/lib/firebaseConfig';

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ headerShown: false }} />
      <Stack.Screen name="login" options={{ title: 'Login' }} />
      <Stack.Screen name="home" options={{ title: 'Home' }} />
      <Stack.Screen name="loading" options={{ headerShown: false }} />
    </Stack>
  );
}