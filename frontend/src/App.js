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

    render() {
        return (
            <div className="App">
                <Header />
                <div className="App-body">
                    <p>
                        We will add stuff here
                    </p>
                </div>
            </div>
        );
    }
}

export default App;
