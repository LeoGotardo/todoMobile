import React, { useEffect, useState } from 'react';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { NavigationContainer } from '@react-navigation/native'; // Container para navegação
import { createStackNavigator } from '@react-navigation/stack'; // Para navegação do tipo Stack
import Login from './login';
import Home from './home';
import Loading from './loading';
import firebase from '../firebaseConfig';


const Stack = createStackNavigator();

export default function App() {
  const user = true
  const home = user ? "Home" : "Login"

  return (
      <Stack.Navigator initialRouteName={home}> {/* Tela inicial será Login */}
        <Stack.Screen name="Login" component={Login} />
        <Stack.Screen name="Home" component={Home} />
        <Stack.Screen name="Home" component={Loading} />
      </Stack.Navigator>
  )
}
