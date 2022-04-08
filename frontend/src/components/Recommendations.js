import React from 'react'
import "./Recommendations.css";
import ReactBasicTable from "react-basic-table";

// Displays the table of recommendations
class Recommendations extends React.Component {
    constructor(props) {
        super(props);
        this.ready = false;
        this.cols = ["Relevance"];
        this.rows = [];
    }
    
    render() {
        this.ready = this.props.ready;
        this.cols = this.props.cols;
        this.rows = this.props.rows;
        return (
            <div className="Recommendations-Container">
                <div className="Recommendations">
                    {this.ready
                        ? <ReactBasicTable columns={this.cols} rows={this.rows} pageSize="2"/>
                        : <ul>{"Recommendations will appear here."}</ul>
                    }
                </div>
            </div>
        )
    }
}

export default Recommendations;