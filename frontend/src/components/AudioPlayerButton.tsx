import React from 'react';
import { Button } from 'antd';

interface AudioPlayerButtonProps {
  audioData: string;
}

const AudioPlayerButton: React.FC<AudioPlayerButtonProps> = ({ audioData }) => {
  const playAudio = () => {
    const binaryString = atob(audioData);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    const audioBlob = new Blob([bytes], { type: 'audio/mp3' });
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    audio.play();
  };

  return <Button onClick={playAudio}>Play Audio</Button>;
};

export default AudioPlayerButton;
