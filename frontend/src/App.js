import './App.css';
import React, { Component } from 'react';
import Header from "./components/Header";
import axios from "axios";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
          userName: "",
          recommended: [],
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

                    Not working yet:
                    genres: Only returns IDs of genres, not genre names, will later be fixed
                */
                var rec = JSON.parse(res.data).anime;
                console.log(rec);
                this.setState({
                  recommended: rec,
                })
                console.log("Recommended shows:");
                for(var i = 0; i < rec.length; i++) {
                    console.log(rec[i].name);
                }
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
                <div className="Recommendations">
                  <ul>
                    {this.state.recommended.map((entry,key)=>{
                      return (
                        <div key={key}>
                          {entry.name}
                        </div>
                      )})}
                  </ul>
                </div>
            </div>
        );
    }
}

export default App;
