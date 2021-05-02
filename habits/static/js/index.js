import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import "bootstrap/dist/css/bootstrap.min.css";
import HabitApp from "./HabitApp";
import HabitCompletionApp from "./HabitCompletionApp";

var today = new Date();
var dd = String(today.getDate()).padStart(2, "0");
var mm = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
var yyyy = today.getFullYear();
today = "Habits: " + yyyy + "-" + mm + "-" + dd;

document.getElementById("heading").innerHTML = today;
ReactDOM.render(<HabitApp />, document.getElementById("habits"));
//import reportWebVitals from "./reportWebVitals";

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
