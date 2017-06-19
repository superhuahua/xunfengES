import React from 'react';
import { Layout, Menu, Icon, notification } from 'antd';
const { Content, Header, Footer } = Layout;
import { Link } from 'react-router';
import axios from 'axios';

import UploadPlugins from './components/UploadPlugins';

class App extends React.Component{

    handleClick = (e) => {
        if(e.key == 5){
            axios.post('/loginOut')
            .then(function(res){
                notification.open({
                    message: '注销成功',
                    icon: <Icon type="smile-circle" style={{ color: '#108ee9' }} />
                });
            })
            .catch(function(err){
                notification.open({
                    message: '注销失败',
                    icon: <Icon type="frown" style={{ color: '#108ee9' }} />
                });
            });
        }
    }

    render() {
        return (
            <Layout style={{ height: '100vh' , backgroundImage: 'url(/static/images/wind.jpeg)', backgroundSize: '100%' }}>
                <Header style={{ position: 'fixed', width: '100%', opacity:0.8  }}>
                    <Menu
                        theme="dark"
                        mode="horizontal"
                        defaultSelectedKeys={['1']}
                        style={{ lineHeight: '64px', fontSize: '15px' }}
                        onClick={this.handleClick}
                    >
                        <Menu.Item key="1">
                            <Link to={'/'}><Icon type="search" /><span className="nav-text">资产发现</span></Link>
                        </Menu.Item>
                        <Menu.Item key="2">
                            <Link to={'/vul'}><Icon type="code" /><span className="nav-text">漏洞扫描</span></Link>
                        </Menu.Item>
                        <Menu.Item key="3">
                            <Link href="http://localhost:5555" target="_blank"><Icon type="eye-o" /><span className="nav-text">Flower</span></Link>
                        </Menu.Item>
                        <Menu.Item key="4">
                            <Link href="http://localhost:5601" target="_blank"><Icon type="star-o" /><span className="nav-text">Kibana</span></Link>
                        </Menu.Item>
                        <Menu.Item key="5" style={{ float:"right" }} >
                            <Icon type="poweroff" />注销
                        </Menu.Item>
                        <Menu.Item key="6" style={{ float:"right" }}>
                            <UploadPlugins />
                        </Menu.Item>
                    </Menu>
                </Header>
                <Content style={{ padding: '0 50px', marginTop: 84, opacity:0.8  }}>
                    {this.props.children}
                </Content>
                <Footer style={{ textAlign: 'center' }}>
                    Superhua Design ©2017
                </Footer>
            </Layout>
        );
    }
}

export default App;