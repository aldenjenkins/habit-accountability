import React, { Component } from "react";
import HabitModal from "./components/HabitCompletionModal.js";
import DatePicker from "react-date-picker";
import { Button, Modal, ModalHeader, ModalBody, ModalFooter, Form, FormGroup, Input, Label } from "reactstrap";
import axios from "axios";
import jquery from "jquery";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		var cookies = document.cookie.split(";");
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jquery.trim(cookies[i]);
			if (cookie.substring(0, name.length + 1) === name + "=") {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

var csrftoken = getCookie("csrftoken");

class HabitApp extends Component {
	constructor(props) {
		super(props);
		this.state = {
			viewCompleted: false,
			requestedDate: new Date(),
			habitList: [],
			habitCompletionList: [],
			modal: null,
			activeCompletion: {
				id: 0,
				habit: 0,
				name: "",
				did_complete: false,
			},
			activeHabit: {
				id: 0,
				name: "",
				one_word_label: "",
			},
		};
	}

	componentDidMount() {
		this.refreshList();
	}

	refreshList = () => {
		const requestedDate = this.state.requestedDate.toLocaleString().slice(0, 9).replaceAll("/", "-");
		axios
			.get(`/habits/api/habit/?date=${requestedDate}`)
			.then((res) => this.setState({ habitList: res.data }))
			.catch((err) => console.log(err));
		axios
			.get(`/habits/api/habit_completion/?date=${requestedDate}`)
			.then((res) => this.setState({ habitCompletionList: res.data }))
			.catch((err) => console.log(err));
	};

	toggleModal = () => {
		this.setState({ modal: !this.state.modal });
	};

	handleHabitSubmit = (habit) => {
		const requestedDate = this.state.requestedDate.toLocaleString().slice(0, 9).replaceAll("/", "-");
		this.toggleModal();

		if (habit.id) {
			axios.patch(`/habits/api/habit/${habit.id}/?date=${requestedDate}`, habit).then((res) => this.refreshList());
			return;
		}
		axios.post("/habits/api/habit/", habit).then((res) => this.refreshList());
	};

	handleCompletionSubmit = (completion) => {
		const requestedDate = this.state.requestedDate.toLocaleString().slice(0, 9).replaceAll("/", "-");
		axios
			.patch(`/habits/api/habit_completion/${completion.id}/?date=${requestedDate}`, completion)
			.then((res) => this.refreshList());
	};

	handleHabitDelete = (habit) => {
		axios.delete(`/habits/api/habit/${habit.id}/`).then((res) => this.refreshList());
	};

	createItem = () => {
		const item = { name: "", one_word_label: "" };

		this.setState({ activeHabit: item, modal: !this.state.modal });
	};

	editItem = (item) => {
		this.setState({ activeHabit: item, modal: !this.state.modal });
	};

	renderHabits = () => {
		const newItems = this.state.habitList;

		return newItems.map((habit) => (
			<li key={habit.id} className="list-group-item d-flex justify-content-between align-items-center">
				<span className="todo-title mr-2" title={habit.name}>
					{habit.name}
				</span>
				<span style={{ minWidth: 140 + "px" }}>
					<button className="btn btn-secondary mr-2" onClick={() => this.editItem(habit)}>
						Edit
					</button>
					<button className="btn btn-danger" onClick={() => this.handleHabitDelete(habit)}>
						Delete
					</button>
				</span>
			</li>
		));
	};

	renderCompletions = () => {
		const newItems = this.state.habitCompletionList;

		return newItems.map((completion) => (
			<li key={completion.id} className="list-group-item d-flex justify-content-between align-items-center">
				<span
					className={`todo-title mr-2 ${this.state.viewCompleted ? "completed-todo" : ""}`}
					title={completion.name}
				>
					{completion.name}
				</span>
				<span>
					<FormGroup check>
						<input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
						<Label check>
							<Input
								id={completion.id}
								type="checkbox"
								name="did_complete"
								checked={completion.did_complete}
								onChange={(e) => this.handleCompletion(completion, e)}
							/>
							Completed
						</Label>
					</FormGroup>
					{/*	
					<button className="btn btn-secondary mr-1" onClick={() => this.handleCompletion(completion)}>
						Complete
					</button>
					*/}
				</span>
			</li>
		));
	};

	handleRequestedDateChange = (date) => {
		this.setState({ requestedDate: date }, () => {
			this.refreshList();
		});
	};
	handleCompletion = (completion, e) => {
		let { name, value } = e.target;

		if (e.target.type === "checkbox") {
			value = e.target.checked;
		}

		const activeCompletion = { ...completion, [name]: value };

		this.setState({ activeCompletion });
		this.handleCompletionSubmit(activeCompletion);
	};

	render() {
		return (
			<main className="container">
				<div className="row" style={{ margin: "0 0 0 0" }}>
					<div className="datePicker">
						<DatePicker onChange={(e) => this.handleRequestedDateChange(e)} value={this.state.requestedDate} />
					</div>
					<div className="column">
						<div className="mx-auto p-0">
							<div className="card p-3">
								<div className="mb-4">
									<button className="btn btn-primary" onClick={this.createItem}>
										Add Habit
									</button>
								</div>
								<ul className="list-group list-group-flush border-top-0">{this.renderHabits()}</ul>
							</div>
						</div>
					</div>
					<div className="column">
						<div className="mx-auto p-0">
							<div className="card p-3">
								<div className="mb-4">
									<ul className="list-group list-group-flush border-top-0">{this.renderCompletions()}</ul>
								</div>
							</div>
						</div>
					</div>
				</div>
				{this.state.modal ? (
					<HabitModal activeHabit={this.state.activeHabit} toggle={this.toggleModal} onSave={this.handleHabitSubmit} />
				) : null}
			</main>
		);
	}
}

export default HabitApp;
