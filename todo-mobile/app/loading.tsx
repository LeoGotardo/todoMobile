import { View, ActivityIndicator, Text } from 'react-native';

export default function Loading() {
  return (
    <View>
      <ActivityIndicator size="large" color="#0000ff" />
      <Text>Loading...</Text>
    </View>
  );
}