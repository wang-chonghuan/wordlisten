import React, { useState } from 'react';
import { List, Typography, Checkbox, Button, message } from 'antd';

interface WordsListProps {
  words: any[];
  onSelectionChange: (selectedWords: any[]) => void;
}

const WordsList: React.FC<WordsListProps> = ({ words, onSelectionChange }) => {
  const [selectedWordIds, setSelectedWordIds] = useState<number[]>([]);

  const handleCheckboxChange = (wordId: number) => {
    setSelectedWordIds((prevSelectedWordIds) => {
      if (prevSelectedWordIds.includes(wordId)) {
        return prevSelectedWordIds.filter((id) => id !== wordId);
      } else {
        return [...prevSelectedWordIds, wordId];
      }
    });
  };

  const handleConfirm = () => {
    const selectedWords = words.filter((word) => selectedWordIds.includes(word.id));
    onSelectionChange(selectedWords);
    message.success('Selected words have been submitted.');
  };

  return (
    <div>
      {words.length > 0 ? (
        <>
          <Button type="primary" onClick={handleConfirm} style={{ marginBottom: '10px' }}>
            Confirm Selection
          </Button>
          <List
            bordered
            dataSource={words}
            renderItem={(word) => (
              <List.Item key={word.id}>
                <Checkbox
                  checked={selectedWordIds.includes(word.id)}
                  onChange={() => handleCheckboxChange(word.id)}
                >
                  <Typography.Text>{word.id}: {word.word} - {word.translation}</Typography.Text>
                </Checkbox>
              </List.Item>
            )}
            style={{ maxHeight: '1000px', overflowY: 'auto' }}
          />
        </>
      ) : (
        <p>No words available</p>
      )}
    </div>
  );
};

export default WordsList;
