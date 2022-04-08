import './App.css';
import React, { Component } from 'react';
import Header from "./components/Header";
import axios from "axios";
import ReactBasicTable from "react-basic-table";
import { Multiselect } from "multiselect-react-dropdown";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
          userName: "",
          recommended: [],
          all_genres: [],
          selected_genres: [],
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

    setUserName = event => {
      this.setState({userName: event.target.value});
    }
    setGenres = event => {
        console.log("List: " + JSON.stringify(event));
        var list = [];
        for(var i = 0; i < event.length; i++) {
            list.push(event[i].genre_name);
        }
        this.setState({selected_genres: JSON.stringify(list)});
    }

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
    onSelect(selectedList, selectedItem) {
        console.log("Added: " + selectedItem.genre_name)
        this.setState(prevState => ({
            selected_genres: [...prevState.selected_genres, selectedItem]
        }))
    }
    onRemove(selectedList, removedItem) {
        console.log("Removed: " + removedItem.genre_name)
    }
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
