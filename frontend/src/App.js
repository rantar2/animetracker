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
        axios
            .get("http://localhost:8000/api/")
            .then((res) => console.log(res))
            .catch((err) => console.log(err));
    }

    state = {
      userName: ""
    }
    handleInput = event => {
      this.setState({userName: event.target.value});
    }
    logUserName = event => {
      event.preventDefault();
      //console.log(this.state.userName);
      axios
            .post("http://localhost:8000/api/", {userName: this.state.userName})
            .then((res) => {
                console.log(res.data);
            })
            .catch((err) => console.log(err));
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
