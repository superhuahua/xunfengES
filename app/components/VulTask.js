import React from 'react';
import { Row, Col, Card } from 'antd';

import SearchAssets from './vultask/SearchAssets';
import TaskTips from './vultask/TaskTips';

class VulTask extends React.Component{
    render(){
        return(
            <Row gutter={16}>
                <Col span={8} offset={8}>
                    <Card title="漏洞扫描" extra={<TaskTips />} >
                        <SearchAssets />
                    </Card>
                </Col>
            </Row>
        )
    }
}

export default VulTask;