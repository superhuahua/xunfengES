import React from 'react';
import { Form, Input, Icon, Button, notification } from 'antd';
const FormItem = Form.Item;

import axios from 'axios';

import ShowResult from './ShowResult';
import CreateTask from './CreateTask';

class SearchAssets extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            searchResult:[],
            vulPlugins:[]
        }
    }

    getSearchReuslt = (q) => {
        let that = this;
        axios.post('/vultask/search',{
            searchValue: q
        })
        .then(function(res){
            notification.open({
                message: '搜索到' + res.data.count + '个结果',
                icon: <Icon type="smile-circle" style={{ color: '#108ee9' }} />
            });
            that.setState({ searchResult:res.data.searchResult});
        })
        .catch(function(err){
            notification.open({
                message: '搜索失败',
                icon: <Icon type="frown" style={{ color: '#108ee9' }} />
            });
        });
    }

    getPlugins = () => {
        let that = this;
        axios.get('/vultask/getplugins')
        .then(function(res){
            notification.open({
                message: '成功获取插件信息',
                icon: <Icon type="smile-circle" style={{ color: '#108ee9' }} />
            });
            that.setState({ vulPlugins:res.data.vulPlugins });
        })
        .catch(function(err){
            notification.open({
                message: '获取插件信息失败',
                icon: <Icon type="frown" style={{ color: '#108ee9' }} />
            });
        });        
    }

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            this.getSearchReuslt(values.searchAssets);
        });
    }

    componentDidMount(){
        this.getPlugins();
    }

    render(){
        const { getFieldDecorator } = this.props.form;
        const formItemLayout = {
            labelCol: { span: 0 },
            wrapperCol: { span: 24 },
        };
        const { searchResult, vulPlugins } = this.state;

        return(
            <div>
            <Form onSubmit={this.handleSubmit}>
                <FormItem
                    label="搜索资产"
                    {...formItemLayout}
                >
                    {getFieldDecorator('searchAssets')(
                        <Input
                            prefix={<Icon type="search" />}
                            placeholder="input search text"
                        />
                    )}
                </FormItem>
                <FormItem
                    {...formItemLayout}
                >
                    <Button type="primary" htmlType="submit" >搜索</Button>
                </FormItem>
            </Form>
            <div style={{ margin:"10px 0px" }} >
                <ShowResult searchResult={searchResult}/>
            </div>
            <div style={{ margin:"10px 0px" }} >
                <CreateTask searchResult={searchResult} vulPlugins={vulPlugins} />
            </div>
            </div>
        )
    }
}

SearchAssets = Form.create({})(SearchAssets);
export default SearchAssets;