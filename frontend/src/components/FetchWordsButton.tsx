import React from 'react';
import { Button, message } from 'antd';
import axios from 'axios';

interface FetchWordsButtonProps {
  setWords: React.Dispatch<React.SetStateAction<any[]>>;
}

const FetchWordsButton: React.FC<FetchWordsButtonProps> = ({ setWords }) => {
  const fetchWords = async () => {
    try {
      const response = await axios.get('http://localhost:8000/words/');
      setWords(response.data);
      console.log(response.data);
    } catch (error) {
      console.error('Error fetching words:', error);
      message.error('Failed to fetch words.');
    }
  };

  return <Button onClick={fetchWords}>Fetch Words</Button>;
};

export default FetchWordsButton;
