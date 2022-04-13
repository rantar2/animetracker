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
            allGenres: [],
            selectedGenres: "[]",
            ready: false,
            maxResults: 20,
            showingOptions: false,
            tv: true,
            movies: false,
            specials: false,
            ovas: false,
            onas: false
        }
    }

    componentDidMount() {
        document.title = "MARS - My Anime Recommendations"
        axios
            .get("http://localhost:8000/api/")
            .then((res) => {
                console.log(res)

                var genreList = JSON.parse(res.data).genre_list
                genreList.sort(function(a,b) {
                  return (a.genre_name < b.genre_name) ? -1 :
                   (a.genre_name > b.genre_name) ? 1 : 0;
                });
                genreList.splice(35, 1);
                genreList.splice(24, 1);
                genreList.splice(17, 1);
                this.setState({allGenres: genreList});
                console.log(this.state.allGenres)

            })
            .catch((err) => console.log(err));
    }

    // Updates username that will be sent to backend
    setUserName = event => {
        this.setState({userName: event.target.value});
    }
    // Updates selected genres list that will be sent to backend
    setGenres = event => {
        console.log("Selected Genre List: " + JSON.stringify(event));
        var list = [];
        for(var i = 0; i < event.length; i++) {
            list.push(event[i].genre_name);
        }
        if(list.length === 0)
            this.setState({selectedGenres: "[]"});
        else
            this.setState({selectedGenres: JSON.stringify(list)});
    }

    setTV = event => {
        this.setState({tv: event.target.checked});
    }
    setMovie = event => {
        this.setState({movies: event.target.checked});
    }
    setSpecials = event => {
        this.setState({specials: event.target.checked});
    }
    setOVAs = event => {
        this.setState({ovas: event.target.checked});
    }
    setONAs = event => {
        this.setState({onas: event.target.checked});
    }

    // Updates user preference for maximum results generated
    setMaxGenres = event => {
      var n = event.target.value.replace(/\D/g, '')
      if (n == "")
        n="0";
      n = parseInt(n)
      this.setState({maxResults:n});
    }

    // Sends all relevent information from this.state to the backend
    executeSearch = event => {
        event.preventDefault();
        //console.log(this.state.userName);
        axios
            .post("http://localhost:8000/api/", {
              userName: this.state.userName,
              selected_genres: this.state.selectedGenres,
              max_results: Math.max(0,this.state.maxResults),
              tv: this.state.tv,
              movies: this.state.movies,
              specials: this.state.specials,
              ovas: this.state.ovas,
              onas: this.state.onas
            })
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
                document.getElementById("topBox").style.display = "none";
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

    showAdvancedOptions = event => {
        event.preventDefault();
        if(this.state.showingOptions) {
            document.getElementById("advancedOptions").style.pointerEvents = "none";
            document.getElementById("advancedOptions").style.opacity = 0;
            document.getElementById("advancedOptionsText").innerText = "Click to show advanced options";
            document.getElementById("advancedOptionsWrapper").style.backgroundColor = "#ff6666";
            this.setState({showingOptions: false});
        } else {
            document.getElementById("advancedOptions").style.pointerEvents = "auto";
            document.getElementById("advancedOptions").style.opacity = 1;
            document.getElementById("advancedOptionsText").innerText = "Click to hide advanced options";
            document.getElementById("advancedOptionsWrapper").style.backgroundColor = "#222";
            this.setState({showingOptions: true});
        }
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
                
                <div  className="App-body">
                    <Header />
                    <div className="Top-Box" id="topBox">
                        <h2>
                            Find Anime Recommendations:
                        </h2>
                    </div>
                    <div className="Middle-Box">
                        <div className="Search-Bar">
                            <input onChange={this.setUserName}
                              placeholder="MAL Username (optional)"
                            />
                            <button onClick={this.executeSearch}>
                              Search
                            </button>
                        </div>
                        <div id="advancedOptionsWrapper" className="Advanced-Options-Wrapper">
                            <button id="advancedOptionsText" className="Advanced-Options-Text" onClick={this.showAdvancedOptions}>
                                Click to show advanced options
                            </button>
                            <div id="advancedOptions" className="Advanced-Options">
                                <div className="Genre-Dropdown">
                                    <Multiselect
                                    options={this.state.allGenres}
                                    onSelect={this.setGenres}
                                    onRemove={this.setGenres}
                                    displayValue="genre_name"
                                    placeholder="Select Genres (optional)"
                                    hidePlaceholder={true}
                                    />
                                </div>
                                <div className="Media-Options">
                                    <div>Show </div>
                                    <div>TV: </div>
                                    <input type="checkbox" defaultChecked="true" onChange={this.setTV}></input>
                                    <div>Movies: </div>
                                    <input type="checkbox" onChange={this.setMovie}></input>
                                    <div>Specials: </div>
                                    <input type="checkbox" onChange={this.setSpecials}></input>
                                    <div>OVAs: </div>
                                    <input type="checkbox" onChange={this.setOVAs}></input>
                                    <div>ONAs: </div>
                                    <input type="checkbox" onChange={this.setONAs}></input>
                                </div>
                                <input className="Max-Results"
                                    type="text"
                                    placeholder="Max Results (Default 20)"
                                    onChange={this.setMaxGenres}
                                />
                            </div>
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
