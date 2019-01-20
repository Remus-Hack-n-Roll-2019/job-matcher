import React, { Component } from 'react';
// import Table from './Table';
import ReactTable from 'react-table';
import './App.css';

//Modified from https://gist.github.com/radtech/14f084922013df4efa0be20376cab28b#file-fileupload-js

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      jobs: [],
      columns: [
        { Header: "Job Title",
          accessor: "job_title" },
          { Header: "Company",
          accessor: "company" },
          { Header: "Location",
          accessor: "location" },
          // { Header: "Link",
          //   accessor: "link" },
          {
            Header: "Link",
            id: 'hyperlink',
            accessor: 'link',
            Cell: ({value}) => (<a href={value} target="_blank">Go</a>)
          }],
    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  handleUploadImage(ev) {
    ev.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);
    data.append('filename', this.fileName === undefined ? '' : this.fileName.value);

    fetch('http://127.0.0.1:5000/upload', {
      method: 'POST',
      body: data,
    }).then((response) => {
      response.json().then((body) => {
        console.log(body);
        this.setState({ jobs: body['joblist'], keywords: body['keywords'] });
      });
    });
  }

  render() {
    return (
      <div>
        <h2>Upload your resume and check out your best matching jobs!</h2>
        <form onSubmit={this.handleUploadImage}>
          <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
          <div>
            <button> Upload</button>
          </div>
        </form>
        <div>
          <br/>
          {console.log(this.state.jobs)}

          <ReactTable
            data = {this.state.jobs}
            columns= {this.state.columns}
            />
          {/* <Table jobs={this.state.jobs} /> */}
        </div>
      </div>
    );
  }
}

export default App;
