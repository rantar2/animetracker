import './App.css';
import React, { Component } from 'react';
import Header from "./components/Header";
import axios from "axios";

class App extends Component {
    constructor(props) {
        super(props);
    }
    componentDidMount() {
        document.title = "MARS - My Anime Recommendations"
    }

    state = {
      userName: ""
    }
    handleInput = event => {
      this.setState({userName: event.target.value});
    }
    logUserName = () => {
      console.log(this.state.userName);
      axios
            .post("http://localhost:8000/api/", {userName: this.state.userName})
            .then((res) => {
                this.setState({userName: "",});
            })
            .catch((err) => {});
    };

    render() {
        return (
            <div className="App">
                <Header />
                <div  className="App-body">
                    <h2>
                        Find Anime Recommendations
                    </h2>
                    <div className="Search-Bar">
                      <input onChange={this.handleInput} placeholder="Enter MAL Username"/>
                      <button onClick={this.logUserName}> Search </button>
                    </div>
                </div>
            </div>
        );
    }
}

export default App;
