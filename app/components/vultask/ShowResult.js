import React from 'react';
import { Modal, Button, Table } from 'antd';

const columns = [{
  title: 'Host',
  dataIndex: 'host',
  width: 150,
}, {
  title: 'Port',
  dataIndex: 'port',
  width: 150,
}, {
  title: 'Server',
  dataIndex: 'server',
}];

class ShowResult extends React.Component{
    constructor(props){
        super(props);

        this.state = {
            visible: false
        }
    }

    showModal = () => {
        this.setState({ visible: true });
    }

    handleCancel = () => {
        this.setState({ visible: false });
    }

    render() {
        const { visible } = this.state;
        const { searchResult } = this.props;
        const data = [];
        searchResult.map( (v, index) => {
            data.push({
                key: index,
                host: v.host,
                port: v.port,
                server: v.server
            });
        });

        return (
            <div>
                <Button type="primary" onClick={this.showModal} ghost>
                    搜索结果
                </Button>
                <Modal
                    width="700px"
                    visible={visible}
                    title="搜索结果"
                    onCancel={this.handleCancel}
                    footer={null}
                >
                <Table 
                    columns={columns} 
                    dataSource={data} 
                    pagination={{ pageSize: 20 }} 
                    scroll={{ y: 240 }} 
                />
                </Modal>
            </div>
        )
    }
}

export default ShowResult;