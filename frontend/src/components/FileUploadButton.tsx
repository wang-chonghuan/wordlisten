import React from 'react';
import { Upload, Button, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import axios from 'axios';

const FileUploadButton: React.FC = () => {
  const handleUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/import_json/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      message.success('File uploaded successfully.');
      console.log(response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
      message.error('Failed to upload file.');
    }
  };

  const uploadProps = {
    beforeUpload: (file: File) => {
      handleUpload(file);
      return false;
    },
  };

  return (
    <Upload {...uploadProps} showUploadList={false}>
      <Button icon={<UploadOutlined />}>Upload JSON</Button>
    </Upload>
  );
};

export default FileUploadButton;
