import React from 'react';
import { Form, Input, Tag, Button, notification, Icon } from 'antd';
const FormItem = Form.Item;
import axios from 'axios';

class CreateTask extends React.Component{

    setHostScan = (scanIP) => {
        axios.post('/setHostScan',{
            scan_hosts: scanIP
        })
        .then(function(res){
            notification.open({
                message: '任务创建成功',
                icon: <Icon type="smile-circle" style={{ color: '#108ee9' }} />
            });
        })
        .catch(function(err){
            notification.open({
                message: '任务创建失败',
                icon: <Icon type="frown" style={{ color: '#108ee9' }} />
            });
        });
    }

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            this.setHostScan(values.scanAssets);
        });
    }

    render(){
        const { getFieldDecorator } = this.props.form;
        const formItemLayout = {
            labelCol: { span: 0 },
            wrapperCol: { span: 24 },
        };
        return(
            <Form onSubmit={this.handleSubmit}>
                <FormItem
                    label="资产列表"
                    {...formItemLayout}
                >
                    {getFieldDecorator('scanAssets')(
                        <Input type="textarea" rows={4} />
                    )}
                </FormItem>
                <FormItem
                    {...formItemLayout}
                >
                    <Button type="primary" htmlType="submit">Go!</Button>
                </FormItem>
            </Form>
        )
    }
}

CreateTask = Form.create({})(CreateTask);
export default CreateTask;