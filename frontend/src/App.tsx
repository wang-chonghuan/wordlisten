import React from 'react';
import { Breadcrumb, ConfigProvider, Layout, Menu, theme } from 'antd';
import Dashboard from './pages/Dashboard';

const { Header, Content, Footer } = Layout;

const items = [{
  key: '1',
  label: 'Home',
}, {
  key: '2',
  label: 'Words',
}, {
  key: '3',
  label: 'Listen',
}, {
  key: '4',
  label: 'Chat',
}];

const App: React.FC = () => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

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
      <Layout>
        <Header
          style={{
            position: 'sticky',
            top: 0,
            zIndex: 1,
            width: '100%',
            display: 'flex',
            alignItems: 'center',
            backgroundColor: '#001529', // 确保背景颜色与主题一致
            padding: '0 50px', // 确保内边距与主题一致
            color: '#ffffff', // 确保文字颜色与主题一致
          }}
        >
          <div className="demo-logo" style={{ color: '#ffffff', fontSize: '24px', marginRight: '30px' }}>
            WordListen
          </div>
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['1']}
            items={items}
            style={{ flex: 1, minWidth: 0 }}
          />
        </Header>
        <Content style={{ padding: '0 48px' }}>
          <Breadcrumb style={{ margin: '16px 0' }}>
            <Breadcrumb.Item>App</Breadcrumb.Item>
            <Breadcrumb.Item>Home</Breadcrumb.Item>
          </Breadcrumb>
          <div
            style={{
              padding: 24,
              minHeight: 380,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            <Dashboard />
          </div>
        </Content>
        <Footer style={{ textAlign: 'center', backgroundColor: '#f5f5f5', padding: '24px 50px' }}>
          Ant Design ©{new Date().getFullYear()} Created by Ant UED
        </Footer>
      </Layout>
    </ConfigProvider>
  );
};

export default App;
