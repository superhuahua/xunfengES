import React from 'react';
import { Popover, Button } from 'antd';

class TaskTips extends React.Component{
    render(){

        let content = (
            <div>
                <strong>资产发现</strong><br />
                单次扫描<br />
                192.168.1.1-192.168.1.255<br />
                使用master队列扫描（默认）<br />
                192.168.1.1-192.168.1.255|celery<br />
                使用celery队列扫描 <br /><br />

                <strong>配置项：</strong><br />
                周期验证配置：周期扫描IP<br />
                验证周期：天|小时，如5|16，即每5天16点进行扫描。<br /><br />
            </div>
        );

        return(
            <Popover placement="rightTop" content={content} title="Title">
                <Button type="dashed">帮助</Button>
            </Popover>   
        )
    }
}

export default TaskTips;