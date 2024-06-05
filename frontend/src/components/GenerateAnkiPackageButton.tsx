import React, { useState } from 'react';
import { Button, Input, message } from 'antd';
import axios from 'axios';

interface GenerateAnkiPackageButtonProps {
  fetchWords: () => void;
}

const GenerateAnkiPackageButton: React.FC<GenerateAnkiPackageButtonProps> = ({ fetchWords }) => {
  const [tags, setTags] = useState<string>('');

  const generateAnkiPackage = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/generate_anki?tags=${tags}`);
      message.success('Anki package generated successfully.');
      console.log(response.data);
      fetchWords();
    } catch (error) {
      console.error('Error generating Anki package:', error);
      message.error('Failed to generate Anki package.');
    }
  };

  return (
    <div>
      <Input
        placeholder="Enter tags separated by commas"
        value={tags}
        onChange={(e) => setTags(e.target.value)}
        style={{ width: 300, marginRight: 10 }}
      />
      <Button onClick={generateAnkiPackage}>Generate Anki Package</Button>
    </div>
  );
};

export default GenerateAnkiPackageButton;
