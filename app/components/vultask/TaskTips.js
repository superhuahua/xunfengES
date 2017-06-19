import React from 'react';
import { Popover, Button } from 'antd';

class TaskTips extends React.Component{
    render(){
        let content = (
            <div>
                <strong>搜索规则</strong><br />
                主机，host:192.168.1.1<br />
                端口，port:80<br />
                代码语言，codes:php<br />
                服务，server:apache<br />
                CMS，cms:discuz!<br /><br />
                组合查询使用 ";"<br />
                eg:<br />
                host:192.168.1.1;port:80<br />
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