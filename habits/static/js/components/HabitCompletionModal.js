import React, { Component } from "react";
import { Button, Modal, ModalHeader, ModalBody, ModalFooter, Form, FormGroup, Input, Label } from "reactstrap";

export default class HabitModal extends Component {
	constructor(props) {
		super(props);
		this.state = {
			activeHabit: this.props.activeHabit,
		};
	}

	handleChange = (e) => {
		let { name, value } = e.target;

		if (e.target.type === "checkbox") {
			value = e.target.checked;
		}

		const activeHabit = { ...this.state.activeHabit, [name]: value };

		this.setState({ activeHabit });
	};

	render() {
		const { toggle, onSave } = this.props;

		return (
			<Modal isOpen={true} toggle={toggle}>
				<ModalHeader toggle={toggle}>Habit</ModalHeader>
				<ModalBody>
					<Form>
						<FormGroup>
							<Label for="todo-title">Full Title</Label>
							<Input
								type="text"
								id="todo-title"
								name="name"
								value={this.state.activeHabit.name}
								onChange={this.handleChange}
								placeholder="Enter Habit Title"
							/>
						</FormGroup>
						<FormGroup>
							<Label for="todo-description">One Word Label</Label>
							<Input
								type="text"
								id="todo-description"
								name="one_word_label"
								value={this.state.activeHabit.one_word_label}
								onChange={this.handleChange}
								placeholder="Enter one word habit description"
							/>
						</FormGroup>
					</Form>
				</ModalBody>
				<ModalFooter>
					<Button color="success" onClick={() => onSave(this.state.activeHabit)}>
						Save
					</Button>
				</ModalFooter>
			</Modal>
		);
	}
}
