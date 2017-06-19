import React from 'react';
import { Row, Col, Card } from 'antd';

import CreateTask from './scantask/CreateTask';
import PeriodTask from './scantask/PeriodTask';
import TaskTips from './scantask/TaskTips';

class AssetsTask extends React.Component{
    render(){
        return(
            <Row gutter={16}>
                <Col span={8} offset={4}>
                    <Card title="资产发现" extra={<TaskTips />} style={{ height:"473px" }}>
                        <CreateTask />
                    </Card>
                </Col>
                <Col span={8} >
                    <Card title="周期发现配置">
                        <PeriodTask />
                    </Card>
                </Col>
            </Row>
        )
    }
}

export default AssetsTask;