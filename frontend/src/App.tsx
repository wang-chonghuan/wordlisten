import React from 'react';
import { Breadcrumb, ConfigProvider, Layout, Menu, theme } from 'antd';
import Dashboard from './pages/Dashboard';
import HomeLayout from './pages/HomeLayout';



const App: React.FC = () => {


  return (
    <ConfigProvider
      theme={{
        components: {
          Layout: {
            headerBg: '#001529',
            headerColor: '#ffffff',
            headerHeight: 64,
            headerPadding: '0 50px',
            footerBg: '#f5f5f5',
            footerPadding: '24px 50px',
          },
        },
      }}
    >
      <HomeLayout />
    </ConfigProvider>
  );
};

export default App;
