import React, { useState } from 'react';
import { View, Text, TextInput, Button, SafeAreaView } from 'react-native';
import axios from 'axios';
import * as Crypto from 'expo-crypto';

const SERVER_URL = 'http://10.0.2.2:3000';

const App = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [seed, setSeed] = useState('');
  const [token, setToken] = useState('');

  const handleEnroll = async () => {
    const res = await axios.post(`${SERVER_URL}/enroll`, { username, password });
    setSeed(res.data);
    console.log(res.data);
  };

  const handleGenerateToken = async () => {
    const time = Math.floor(Date.now() / 30000);
  const digest = await Crypto.digestStringAsync(
    Crypto.CryptoDigestAlgorithm.SHA1,
    seed + time.toString(),
    { encoding: Crypto.CryptoEncoding.HEX }
  );
  setToken(digest.slice(0, 6));
  };

  const handleVerify = async () => {
    const res = await axios.get(`${SERVER_URL}/verify/${username}`, {
      params: { token },
    });
    alert(res.data);
  };

  return (
    <SafeAreaView>
      <Text>Username:</Text>
      <TextInput value={username} onChangeText={setUsername} />
      <Text>Password:</Text>
      <TextInput value={password} onChangeText={setPassword} />
      <Button title="Enroll" onPress={handleEnroll} />
      <Text>Seed: {seed}</Text>
      <Button title="Generate Token" onPress={handleGenerateToken} />
      <Text>Token: {token}</Text>
      <Button title="Verify" onPress={handleVerify} />
    </SafeAreaView>
  );
};

export default App;