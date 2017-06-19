import React from 'react';
import { Upload, notification, Button, Icon } from 'antd';

class UploadPlugins extends React.Component{
    render(){
        const props = {
            name: 'file',
            action: '/uploadPlugins',
            showUploadList: false,
            onChange(info) {
                if (info.file.status === 'done') {
                    notification.open({
                        message: `${info.file.name} 插件上传成功`,
                        icon: <Icon type="smile-circle" style={{ color: '#108ee9' }} />
                    });
                } else if (info.file.status === 'error') {
                    notification.open({
                        message: `${info.file.name} 插件上传失败`,
                        icon: <Icon type="smile-circle" style={{ color: '#108ee9' }} />
                    });
                }
            }
        };
        return(
            <div>
                <Upload {...props}>
                    <Button type="dashed" ghost>
                        <Icon type="upload" /> 上传插件
                    </Button>
                </Upload>
            </div>
        )
    }
}

export default UploadPlugins;