import React from 'react';
import { Button, message } from 'antd';
import axios from 'axios';

interface GenerateAudioButtonProps {
  fetchWords: () => void;
}

const GenerateAudioButton: React.FC<GenerateAudioButtonProps> = ({ fetchWords }) => {
  const generateAudio = async () => {
    try {
      const response = await axios.post('http://localhost:8000/generate_audio/');
      message.success('Audio generated for records with empty audio fields.');
      console.log(response.data);
      fetchWords();
    } catch (error) {
      console.error('Error generating audio:', error);
      message.error('Failed to generate audio.');
    }
  };

  return <Button onClick={generateAudio}>Generate Audio</Button>;
};

export default GenerateAudioButton;
