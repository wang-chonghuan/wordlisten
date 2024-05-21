import React, { useState } from 'react';
import { Button, Input, message, List, Card } from 'antd';
import axios from 'axios';

interface WordDetail {
  id: number;
  word: string;
  translation: string;
  tags: string | null;
  datetime: string;
  remark: Record<string, any> | null;
  audio: string | null;
}

interface FetchWordsButtonProps {
  setWords: React.Dispatch<React.SetStateAction<WordDetail[]>>;
}

const FetchWordsButton: React.FC<FetchWordsButtonProps> = ({ setWords }) => {
  const [tags, setTags] = useState<string>('');
  const [words, setWordsState] = useState<WordDetail[]>([]);

  const fetchWords = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/words?tags=${tags}`);
      setWords(response.data);
      setWordsState(response.data);
      console.log(response.data);
    } catch (error) {
      console.error('Error fetching words:', error);
      message.error('Failed to fetch words.');
    }
  };

  return (
    <div>
      <Input
        placeholder="Tags"
        value={tags}
        onChange={(e) => setTags(e.target.value)}
        style={{ marginBottom: '10px' }}
      />
      <Button onClick={fetchWords}>Fetch Words</Button>
      
      <List
        grid={{ gutter: 16, column: 1 }}
        dataSource={words}
        renderItem={item => (
          <List.Item>
            <Card title={item.word}>
              <p><strong>Translation:</strong> {item.translation}</p>
              <p><strong>Tags:</strong> {item.tags}</p>
              <p><strong>Date:</strong> {item.datetime}</p>
              <p><strong>Remark:</strong> {JSON.stringify(item.remark)}</p>
              {item.audio && (
                <audio key={item.id} controls>
                  <source src={`data:audio/wav;base64,${item.audio}`} type="audio/wav" />
                  Your browser does not support the audio element.
                </audio>
              )}
            </Card>
          </List.Item>
        )}
      />
    </div>
  );
};

export default FetchWordsButton;
