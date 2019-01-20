import React, { Component } from 'react';
import ReactTable from 'react-table';

class Table extends Component {
    constructor(props) {
        super(props);
        this.state = {
            columns: ["Job Title", "Summary", "Location"],
            jobs: props.jobs,
        }
    }

    render() {
        const data = this.state.jobs;
        console.log(data)
        const columns = [{
            Header: 'Job Title',
            accessor: 'job_title'
        }]
        <ReactTable 
        data = {data} 
        columns= {columns}
        />
    }
}

export default Table;