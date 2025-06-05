import { initializeApp, getAuth } from 'firebase/app';
import { GoogleAuthProvider, signInWithPopup, getRedirectResult, signOut } from "firebase/auth";


export default function firebase() {
  // Initialize Firebase
  const firebaseConfig = {
    apiKey: "AIzaSyA0AkZ1klZUm6URVI5mTzpLfG3PeAIGJ0M",
    authDomain: "todo-mobile-654e1.firebaseapp.com",
    projectId: "todo-mobile-654e1",
    storageBucket: "todo-mobile-654e1.firebasestorage.app",
    messagingSenderId: "831912942572",
    appId: "1:831912942572:web:77b84027635733d3cd3ec9"
  };


  const provider = new GoogleAuthProvider();
  provider.addScope('https://www.googleapis.com/auth/contacts.readonly');

  const app = initializeApp(firebaseConfig);
  const auth = getAuth(app);
  auth.languageCode = 'it';


  signInWithPopup(auth, provider)
    .then((result) => {
      // This gives you a Google Access Token. You can use it to access the Google API.
      const credential = GoogleAuthProvider.credentialFromResult(result);
      const token = credential.accessToken;
      // The signed-in user info.
      const user = result.user;
      // IdP data available using getAdditionalUserInfo(result)
      const userInfo = {'user': user, 'credential': credential, 'token': token};
      
      return (true, userInfo);
    }).catch((error) => {
      // Handle Errors here.
      const errorCode = error.code;
      const errorMessage = error.message;
      // The email of the user's account used.
      const email = error.customData.email;
      // The AuthCredential type that was used.
      const credential = GoogleAuthProvider.credentialFromError(error);
    
      const errorInfo = {'errorCode': errorCode, 'errorMessage': errorMessage, 'email': email, 'credential': credential};
      return (false, errorInfo);
    });


  getRedirectResult(auth)
    .then((result) => {
      // This gives you a Google Access Token. You can use it to access Google APIs.
      const credential = GoogleAuthProvider.credentialFromResult(result);
      const token = credential.accessToken;

      // The signed-in user info.
      const user = result.user;
      // IdP data available using getAdditionalUserInfo(result)
      return (user, credential, token);
    }).catch((error) => {
      // Handle Errors here.
      const errorCode = error.code;
      const errorMessage = error.message;
      // The email of the user's account used.
      const email = error.customData.email;
      // The AuthCredential type that was used.
      const credential = GoogleAuthProvider.credentialFromError(error);
      
      return (errorCode, errorMessage, email, credential);
    });


  signOut(auth).then(() => {
    return "Sign-out successful.";
  }).catch((error) => {
    return "An error happened: " + error;
  });
}