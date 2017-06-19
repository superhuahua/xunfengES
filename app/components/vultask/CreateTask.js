import React from 'react';
import { Modal, Button, Transfer, Input, Form, Icon, notification } from 'antd';

import axios from 'axios';

const FormItem = Form.Item;

class CreateTask extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            visible: false,
            targetKeys: []
        }
    }

    handleChange = (targetKeys) => {
        this.setState({ targetKeys });
    }

    showModal = () => {
        this.setState({ visible: true });
    }

    handleCancel = () => {
        this.setState({ visible: false });
    }

    setVulScan = (vulTaskName, vulPluginsId, netLoc) => {
        axios.post('/setVulScan',{
            vul_task_netloc: netLoc,
            vul_task_name: vulTaskName,
            vul_task_plugin_id: vulPluginsId
        })
        .then(function(res){
            notification.open({
                message: '扫描任务创建成功',
                icon: <Icon type="smile-circle" style={{ color: '#108ee9' }} />
            });
        })
        .catch(function(err){
            notification.open({
                message: '扫描任务创建失败',
                icon: <Icon type="frown" style={{ color: '#108ee9' }} />
            });
        });
    }

    handleSubmit = (searchResult, e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            let vulTaskName = values.vulTaskName;
            let vulPluginsId = this.state.targetKeys;
            let netLoc = searchResult;
            this.setVulScan(vulTaskName, vulPluginsId, netLoc);
        });
    }

    render() {
        const { getFieldDecorator } = this.props.form;
        const { searchResult, vulPlugins } = this.props;
        const { visible } = this.state;
        const mockData = [];
        vulPlugins.map( (v, key) => {
            const data = {
                key: v._id,
                title: v._source.name,
                description: v._source.info
            }
            mockData.push(data)
        });
        return (
            <div>
                <Button type="primary" onClick={this.showModal} ghost>
                    创建漏扫任务
                </Button>
                <Modal
                    width="700px"
                    visible={visible}
                    title="创建任务"
                    onCancel={this.handleCancel}
                    footer={null}
                >
                    <Form onSubmit={this.handleSubmit.bind(this, searchResult)}>
                        <FormItem 
                            label="任务名"
                        >
                            {getFieldDecorator('vulTaskName')(
                            <Input 
                                prefix={<Icon type="search" />}
                                placeholder="Basic usage" 
                            />
                            )}
                        </FormItem>
                        <FormItem
                            label="选择插件"
                        >
                            <Transfer
                                dataSource={mockData}
                                showSearch
                                listStyle={{
                                    width: 250,
                                    height: 300,
                                }}
                                operations={['to right', 'to left']}
                                onChange={this.handleChange}
                                targetKeys={this.state.targetKeys}
                                render={item => `${item.title}-${item.description}`}
                            />
                        </FormItem>
                        <FormItem>
                            <Button type="primary" htmlType="submit" onClick={this.handleCancel}>创建任务</Button>
                        </FormItem>
                    </Form>
                </Modal>
            </div>
        )
    }
}

CreateTask = Form.create({})(CreateTask);
export default CreateTask;