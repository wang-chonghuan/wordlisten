import React, { useState } from 'react';
import { List, Typography, Checkbox, Button, message } from 'antd';

interface WordsListProps {
  words: any[];
  onSelectionChange: (selectedWords: any[]) => void;
}

const WordsList: React.FC<WordsListProps> = ({ words, onSelectionChange }) => {
  const [selectedWordIds, setSelectedWordIds] = useState<number[]>([]);
  const [selectAll, setSelectAll] = useState<boolean>(false);

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

  const handleSelectAllChange = (e: any) => {
    const checked = e.target.checked;
    setSelectAll(checked);
    if (checked) {
      const allWordIds = words.map((word) => word.id);
      setSelectedWordIds(allWordIds);
    } else {
      setSelectedWordIds([]);
    }
  };

  return (
    <div>
      {words.length > 0 ? (
        <>
          <div style={{ marginBottom: '10px' }}>
            <Checkbox checked={selectAll} onChange={handleSelectAllChange}>
              Select All
            </Checkbox>
            <Button type="primary" onClick={handleConfirm} style={{ marginLeft: '10px' }}>
              Confirm Selection
            </Button>
          </div>
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
