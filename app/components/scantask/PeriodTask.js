import React from 'react';
import { Form, Input, Tag, Button, notification, Icon } from 'antd';
const FormItem = Form.Item;

import axios from 'axios';

class PeriodTask extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            periodAssets:"",
            periodTimes:"",
            periodPorts:""
        };
    }

    setPeriodConfig = (periodAssets, periodTimes, periodPorts) => {
        axios.post('/taskconfig/all',{
            scanHosts:periodAssets,
            scanPeriod:periodTimes,
            scanPorts:periodPorts  
        })
        .then(function(res){
            notification.open({
                message: '更新配置成功',
                icon: <Icon type="smile-circle" style={{ color: '#108ee9' }} />
            });
        })
        .catch(function(err){
            notification.open({
                message: '更新配置失败',
                icon: <Icon type="frown" style={{ color: '#108ee9' }} />
            });
        });
    }

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            let { periodAssets, periodTimes, periodPorts } = values;
            this.setPeriodConfig(periodAssets, periodTimes, periodPorts);
        });
    }

    componentDidMount(){
        let that = this;

        axios.get('/taskconfig/all')
        .then(function(res){
            let hostsList = res.data.scanHosts
            let strhosts = ""
            for(let v in hostsList){
                strhosts += hostsList[v] + '\n';
            }
            that.setState({
                periodAssets:strhosts,
                periodTimes:res.data.scanPeriod,
                periodPorts:res.data.scanPorts  
            });
        })
        .catch(function(err){
            notification.open({
                message: '获取配置失败',
                icon: <Icon type="frown" style={{ color: '#108ee9' }} />
            });
        });
        
    }

    render(){
        let { getFieldDecorator } = this.props.form;

        return(
            <Form onSubmit={this.handleSubmit}>
                <FormItem
                    label="资产列表"
                >
                {getFieldDecorator('periodAssets',{
                    initialValue:this.state.periodAssets
                })(
                    <Input type="textarea" rows={4} />
                )}
                </FormItem>
                <FormItem
                    label="探测周期"
                >
                {getFieldDecorator('periodTimes',{
                    initialValue:this.state.periodTimes
                })(
                    <Input 
                        size="large"
                    />
                )}
                </FormItem>
                <FormItem
                    label="探测端口"
                >
                {getFieldDecorator('periodPorts',{
                    initialValue:this.state.periodPorts
                })(
                    <Input 
                        size="large"
                    />                
                )}
                </FormItem>
                <FormItem>
                    <Button type="primary" htmlType="submit">更新</Button>
                </FormItem>
            </Form>
        )
    }
}

PeriodTask = Form.create({})(PeriodTask);
export default PeriodTask;