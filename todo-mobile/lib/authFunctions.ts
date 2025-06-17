// authFunctions.ts para Web (usando popup)
import {
  GoogleAuthProvider,
  signInWithPopup,
  signOut,
  UserCredential,
  User,
  AuthCredential
} from "firebase/auth";
import { auth } from './firebaseConfig';

// Tipos para as respostas
interface AuthSuccessResult {
  success: true;
  data: {
    user: User;
    credential: AuthCredential | null;
    token: string | null;
  };
}

interface AuthErrorResult {
  success: false;
  error: {
    errorCode: string;
    errorMessage: string;
    email?: string;
    credential?: AuthCredential | null;
  };
}

interface SignOutSuccessResult {
  success: true;
  message: string;
}

interface SignOutErrorResult {
  success: false;
  error: string;
}

type AuthResult = AuthSuccessResult | AuthErrorResult;
type SignOutResult = SignOutSuccessResult | SignOutErrorResult;

const provider = new GoogleAuthProvider();
provider.addScope('https://www.googleapis.com/auth/contacts.readonly');

// Função para login com Google usando popup
export const signInWithGoogle = async (): Promise<AuthResult> => {
  try {
    const result: UserCredential = await signInWithPopup(auth, provider);
    const credential = GoogleAuthProvider.credentialFromResult(result);
    const token = credential?.accessToken || null;
    const user = result.user;

    return {
      success: true,
      data: { user, credential, token }
    };
    
  } catch (error: any) {
    const errorCode = error.code || 'unknown-error';
    const errorMessage = error.message || 'An unknown error occurred';
    const email = error.customData?.email;
    const credential = GoogleAuthProvider.credentialFromError(error);

    return {
      success: false,
      error: { errorCode, errorMessage, email, credential }
    };
  }
};

// Função para logout
export const signOutUser = async (): Promise<SignOutResult> => {
  try {
    await signOut(auth);
    return {
      success: true,
      message: "Logout realizado com sucesso."
    };
  } catch (error: any) {
    return {
      success: false,
      error: "Erro ao fazer logout: " + (error.message || 'Erro desconhecido')
    };
  }
};