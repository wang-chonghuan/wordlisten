import React, { useState } from 'react';
import { Layout, Card, Space, message } from 'antd';
import axios from 'axios';
import FileUploadButton from '../components/FileUploadButton';
import FetchWordsButton from '../components/FetchWordsButton';
import GenerateAudioButton from '../components/GenerateAudioButton';
import SearchWordInput from '../components/SearchWordInput';
import AudioPlayerButton from '../components/AudioPlayerButton';
import WordsList from '../components/WordsList';

const Dashboard: React.FC = () => {
  const [words, setWords] = useState<any[]>([]);
  const [wordDetails, setWordDetails] = useState<any | null>(null);
  const [selectedWords, setSelectedWords] = useState<any[]>([]);

  const handleSelectionChange = async (selectedWords: any[]) => {
    setSelectedWords(selectedWords);
    console.log("Selected words:", selectedWords);

    // 提取选中单词的 ID 列表
    const selectedWordIds = selectedWords.map(word => word.id);

    try {
      // 向后端发送 POST 请求，生成音频文件
      const response = await axios.post('http://localhost:8000/generate_custom_audio', {
        word_ids: selectedWordIds
      });

      // 显示成功消息
      message.success(`Audio file generated: ${response.data.detail}`);
    } catch (error) {
      // 显示错误消息
      console.error("Error generating audio file:", error);
      message.error("Failed to generate audio file.");
    }
  };

  return (
    <Space direction="vertical" size="middle" style={{ display: 'flex' }}>
      <Card title="File Upload">
        <FileUploadButton />
      </Card>
      <Card title="Fetch Words">
        <FetchWordsButton setWords={setWords} />
      </Card>
      <Card title="Generate Audio">
        <GenerateAudioButton fetchWords={() => setWords} />
      </Card>
      <Card title="Search Word">
        <SearchWordInput setWordDetails={setWordDetails} />
      </Card>
      <Card title="Word Details">
        {wordDetails ? (
          <div>
            <p>ID: {wordDetails.id}</p>
            <p>Word: {wordDetails.word}</p>
            <p>Translation: {wordDetails.translation}</p>
            <p>Flag: {wordDetails.flag}</p>
            <p>DateTime: {wordDetails.datetime}</p>
            <p>Remark: {wordDetails.remark ? JSON.stringify(wordDetails.remark) : 'None'}</p>
            {wordDetails.audio && <AudioPlayerButton audioData={wordDetails.audio} />}
          </div>
        ) : (
          <p>No word details available</p>
        )}
      </Card>
      <Card title="Words List">
        <WordsList words={words} onSelectionChange={handleSelectionChange} />
      </Card>
    </Space>
  );
};

export default Dashboard;
