import React from 'react'
import "./Header.css";
import mars from "../images/mars.jpg"

// Displays the header of the website
function Header(props) {
    return (
        <div className="mars" id="header">
            <img src={mars} alt=""></img>
            MARS
        </div>
    )
}

export default Header;