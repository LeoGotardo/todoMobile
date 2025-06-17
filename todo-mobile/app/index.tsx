// app/index.tsx
import React, { useEffect, useState } from 'react';
import { onAuthStateChanged, User } from 'firebase/auth';
import { useRouter } from 'expo-router';

import Loading from './loading';
import { auth } from '@/lib/firebaseConfig';

const App: React.FC = () => {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser: User | null) => {
      setUser(currentUser);
      setIsLoading(false);
      
      // Navegar baseado no estado do usuário
      if (currentUser) {
        router.replace('/home');
      } else {
        router.replace('/login');
      }
    });

    return unsubscribe;
  }, []);

  if (isLoading) {
    return <Loading />;
  }

  // Este componente só será mostrado brevemente antes do redirect
  return <Loading />;
};

export default App;