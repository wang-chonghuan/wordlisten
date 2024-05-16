import React, { useState } from 'react';
import { Input, Button, message } from 'antd';
import axios from 'axios';

interface SearchWordInputProps {
  setWordDetails: React.Dispatch<React.SetStateAction<any | null>>;
}

const SearchWordInput: React.FC<SearchWordInputProps> = ({ setWordDetails }) => {
  const [searchId, setSearchId] = useState('');

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchId(event.target.value);
  };

  const handleSearch = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/word/${searchId}`);
      setWordDetails(response.data);
      console.log(response.data);
    } catch (error) {
      console.error('Error fetching word details:', error);
      message.error('Failed to fetch word details.');
    }
  };

  return (
    <div>
      <Input
        type="text"
        value={searchId}
        onChange={handleSearchChange}
        placeholder="Enter Word ID"
        style={{ width: '200px', marginRight: '8px' }}
      />
      <Button onClick={handleSearch}>Search Word</Button>
    </div>
  );
};

export default SearchWordInput;
