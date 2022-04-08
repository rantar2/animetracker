import './App.css';
import React, { Component } from 'react';
import Header from "./components/Header";
import axios from "axios";
import { Multiselect } from "multiselect-react-dropdown";
import Recommendations from './components/Recommendations';

// Base website manager, responsible for displaying the website and transmitting data to the backend
class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            userName: "",
            recommended: [],
            all_genres: [],
            selected_genres: "[]",
            ready: false,
        }
    }

    componentDidMount() {
        document.title = "MARS - My Anime Recommendations"
        axios
            .get("http://localhost:8000/api/")
            .then((res) => {
                console.log(res)

                var genreList = JSON.parse(res.data).genre_list
                this.setState({
                  all_genres: genreList,
                })
                console.log(this.state.all_genres)
            })
            .catch((err) => console.log(err));
    }

    // Updates username that will be sent to backend
    setUserName = event => {
        this.setState({userName: event.target.value});
    }
    // Updates selected genres list that will be sent to backend
    setGenres = event => {
        console.log("List: " + JSON.stringify(event));
        var list = [];
        for(var i = 0; i < event.length; i++) {
            list.push(event[i].genre_name);
        }
        if(list.length === 0)
            this.setState({selected_genres: "[]"});
        else
            this.setState({selected_genres: JSON.stringify(list)});
    }
    
    // Sends all relevent information from this.state to the backend
    executeSearch = event => {
        event.preventDefault();
        //console.log(this.state.userName);
        axios
            .post("http://localhost:8000/api/", {userName: this.state.userName, selected_genres: this.state.selected_genres})
            .then((res) => {
                /* Array of shows with the corresponding data:
                    name: Anime title
                    main_picture: Main picture for this specific anime, contains url to image
                    synopsis: Anime synopsis
                    animeID: ID of anime on MAL
                    rank: Rank of anime in terms of popularity
                    genres: Returns each genre the show contains in a string
                */
                var rec = JSON.parse(res.data).anime;
                console.log(rec);
                this.setState({
                  recommended: rec,  // Update state variable with results
                  ready: true,
                })
                console.log("Recommended shows:");
                for(var i = 0; i < rec.length; i++) {
                    console.log(rec[i].name);
                }
            })
            .catch((err) => console.log(err));
    };

    // Uses the React Basic Table package to generate a table of recommended shows, returns the rows and columns of the table
    generateTable() {
        var cols = ["Relevance"]
        var rows = []
        for(var p in this.state.recommended[0]) {
            cols.push(p.replace(/^\w/, (c) => c.toUpperCase()).replace("_"," "))
        }
        for(var i=0; i< this.state.recommended.length;i++) {
            var entry = [
                <span data-reactbasictable-value={"Entry" + i+1}> {i+1} </span>
            ]
            for(var key in this.state.recommended[i]) {
                if (key=="main_picture") {
                    entry.push(<a href={"https://myanimelist.net/anime/"+this.state.recommended[i]["MAL_ID"]}>
                    <img className="thumbnail" src={this.state.recommended[i][key]}>
                    </img></a>)
                } else {
                    entry.push(<span data-reactbasictable-value={key.toString()}> {this.state.recommended[i][key]} </span>)
                }
            }
            rows.push(entry)
        }
        return {cols: cols, rows: rows};
    }

    // Renders the page by returning HTML and React components
    render() {
        var cols = ["Relevance"]
        var rows = []
        if (this.state.ready) {
            var tableData = this.generateTable();
            cols = tableData.cols;
            rows = tableData.rows;
        }
        return (
            <div className="App">
                <Header />
                <div  className="App-body">
                    <div className="Top-Box">
                        <h2>
                            Find Anime Recommendations:
                        </h2>
                    </div>
                    <div className="Middle-Box">
                        <div className="Search-Bar">
                            <input onChange={this.setUserName} placeholder="Enter MAL Username"/>
                            <button onClick={this.executeSearch}> Search </button>
                        </div>
                        <div className="Genre-Dropdown">
                            <Multiselect options={this.state.all_genres} onSelect={this.setGenres} onRemove={this.setGenres} displayValue="genre_name"/>
                        </div>
                    </div>
                    <div className="Bottom-Box">
                    </div>
                </div>
                <Recommendations ready={this.state.ready} rows={rows} cols={cols}/>
            </div>
        );
    }
}
export default App;
