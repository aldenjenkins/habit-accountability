import React, { Component } from "react";
import HabitCompletionModal from "./components/HabitCompletionModal.js";
import axios from "axios";

var today = new Date();
var dd = String(today.getDate()).padStart(2, "0");
var mm = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
var yyyy = today.getFullYear();

today = yyyy + "-" + mm + "-" + dd;

class HabitCompletionApp extends Component {
	constructor(props) {
		super(props);
		this.state = {
			viewCompleted: false,
			habitCompletionList: [],
			modal: null,
			activeItem: {
				id: 0,
				name: "",
				did_complete: false,
			},
		};
	}

	componentDidMount() {
		this.refreshList();
	}

	refreshList = () => {
		axios
			.get("/habits/api/habit_completion/")
			.then((res) => this.setState({ habitCompletionList: res.data }))
			.catch((err) => console.log(err));
	};

	toggle = () => {
		this.setState({ modal: !this.state.modal });
	};

	handleSubmit = (item) => {
		this.toggle();

		if (item.id) {
			axios.put(`/habits/api/habit_completion/${item.id}/`, item).then((res) => this.refreshList());
			return;
		}
		axios.post("/habits/api/habit_completion/", item).then((res) => this.refreshList());
	};

	handleDelete = (item) => {
		axios.delete(`/habits/api/habit_completion/${item.id}/`).then((res) => this.refreshList());
	};

	createItem = () => {
		const item = { name: "", one_word_label: "" };

		this.setState({ activeItem: item, modal: !this.state.modal });
	};

	editItem = (item) => {
		this.setState({ activeItem: item, modal: !this.state.modal });
	};

	displayCompleted = (status) => {
		if (status) {
			return this.setState({ viewCompleted: true });
		}

		return this.setState({ viewCompleted: false });
	};

	renderTabList = () => {
		return (
			<div className="nav nav-tabs">
				<span
					onClick={() => this.displayCompleted(true)}
					className={this.state.viewCompleted ? "nav-link active" : "nav-link"}
				>
					Complete
				</span>
				<span
					onClick={() => this.displayCompleted(false)}
					className={this.state.viewCompleted ? "nav-link" : "nav-link active"}
				>
					Incomplete
				</span>
			</div>
		);
	};

	renderItems = () => {
		const { viewCompleted } = this.state;
		const newItems = this.state.habitCompletionList.filter((item) => item.did_complete === viewCompleted);

		return newItems.map((item) => (
			<li key={item.id} className="list-group-item d-flex justify-content-between align-items-center">
				<span className={`todo-title mr-2 ${this.state.viewCompleted ? "completed-todo" : ""}`} title={item.name}>
					{item.name}
				</span>
				<span>
					<button className="btn btn-secondary mr-2" onClick={() => this.editItem(item)}>
						Edit
					</button>
					<button className="btn btn-danger" onClick={() => this.handleDelete(item)}>
						Delete
					</button>
				</span>
			</li>
		));
	};

	render() {
		return (
			<main className="container">
				<div className="row">
					<div className="col-md-6 col-sm-10 mx-auto p-0">
						<div className="card p-3">
							<div className="mb-4">
								<button className="btn btn-primary" onClick={this.createItem}>
									Add task
								</button>
							</div>
							{this.renderTabList()}
							<ul className="list-group list-group-flush border-top-0">{this.renderItems()}</ul>
						</div>
					</div>
				</div>
				{this.state.modal ? (
					<HabitCompletionModal activeItem={this.state.activeItem} toggle={this.toggle} onSave={this.handleSubmit} />
				) : null}
			</main>
		);
	}
}

export default HabitCompletionApp;
