import './App.css';
import React, { Component } from 'react';
import Header from "./components/Header";
import axios from "axios";
import ReactBasicTable from "react-basic-table"

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
          userName: "",
          recommended: [],
          ready: false,
        }
    }
    componentDidMount() {
        document.title = "MARS - My Anime Recommendations"
        axios
            .get("http://localhost:8000/api/")
            .then((res) => console.log(res))
            .catch((err) => console.log(err));
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

    render() {
      if (this.state.ready) {
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
      }}
        return (
            <div className="App">
                <Header />
                <div  className="App-body">
                    <h2>
                        Find Anime Recommendations:
                    </h2>
                    <div className="Search-Bar">
                      <input onChange={this.handleInput} placeholder="Enter MAL Username"/>
                      <button onClick={this.logUserName}> Search </button>
                    </div>
                </div>
                <div className="Recommendations-Container">
                    <div className="Recommendations">
                        {this.state.ready
                            ? <ReactBasicTable columns={cols} rows={rows} pageSize="2"/>
                            : <ul>{"Recommendations will appear here."}</ul>
                        }
                    </div>
                </div>
            </div>
        );
    }
}

export default App;
